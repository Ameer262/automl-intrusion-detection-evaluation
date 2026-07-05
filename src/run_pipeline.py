"""
Run a compact reproducible version of the corrected IDS pipeline.

This script is intentionally shorter than the notebook. It is meant to
make the main experiment runnable outside Colab:

1. load the prepared CICIDS2017 sample;
2. create group-aware train / validation / test splits;
3. train the final LightGBM model;
4. apply the frozen threshold;
5. print and save the final metrics.

For the full analysis, figures, and detailed error analysis, see the
notebook.
"""

import sys

import numpy as np
import pandas as pd

from lightgbm import LGBMClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    balanced_accuracy_score,
    matthews_corrcoef,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
)

from sklearn.model_selection import GroupShuffleSplit

from config import (
    PREPARED_DATA_PATH,
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    RANDOM_SEED,
    TEST_SIZE,
    VALIDATION_SIZE_FROM_DEVELOPMENT,
    FINAL_THRESHOLD,
    LIGHTGBM_PARAMS,
    FINAL_METRICS_PATH,
    FINAL_CONFUSION_MATRIX_PATH,
    ensure_project_directories,
)


def load_prepared_dataset() -> pd.DataFrame:
    """Load the prepared project dataset."""
    if not PREPARED_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Prepared dataset was not found at:\n{PREPARED_DATA_PATH}\n\n"
            "Run this first:\npython src/prepare_dataset.py"
        )

    df = pd.read_csv(PREPARED_DATA_PATH)

    missing_columns = [
        col for col in FEATURE_COLUMNS + [TARGET_COLUMN]
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Prepared dataset is missing required columns:\n"
            + "\n".join(missing_columns)
        )

    return df


def make_duplicate_profile_groups(df: pd.DataFrame) -> pd.Series:
    """
    Create a group id for each exact predictor profile.

    Rows with identical values across all predictor columns receive the
    same group id and therefore cannot cross split boundaries.
    """
    return (
        df[FEATURE_COLUMNS]
        .astype(str)
        .agg("||".join, axis=1)
        .factorize()[0]
    )


def group_split(df: pd.DataFrame):
    """Create group-aware train, validation, and test splits."""
    groups = make_duplicate_profile_groups(df)

    first_split = GroupShuffleSplit(
        n_splits=1,
        test_size=TEST_SIZE,
        random_state=RANDOM_SEED,
    )

    development_idx, test_idx = next(
        first_split.split(
            df,
            df[TARGET_COLUMN],
            groups,
        )
    )

    development_df = df.iloc[development_idx].reset_index(drop=True)
    test_df = df.iloc[test_idx].reset_index(drop=True)

    development_groups = make_duplicate_profile_groups(development_df)

    second_split = GroupShuffleSplit(
        n_splits=1,
        test_size=VALIDATION_SIZE_FROM_DEVELOPMENT,
        random_state=RANDOM_SEED,
    )

    train_idx, validation_idx = next(
        second_split.split(
            development_df,
            development_df[TARGET_COLUMN],
            development_groups,
        )
    )

    train_df = development_df.iloc[train_idx].reset_index(drop=True)
    validation_df = development_df.iloc[validation_idx].reset_index(drop=True)

    return train_df, validation_df, test_df


def evaluate_predictions(y_true, y_probability, threshold):
    """Evaluate binary predictions at the frozen threshold."""
    y_pred = (y_probability >= threshold).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1],
    ).ravel()

    metrics = {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, zero_division=0),
        "Recall": recall_score(y_true, y_pred, zero_division=0),
        "Specificity": tn / (tn + fp) if (tn + fp) else np.nan,
        "F1 Score": f1_score(y_true, y_pred, zero_division=0),
        "Balanced Accuracy": balanced_accuracy_score(y_true, y_pred),
        "MCC": matthews_corrcoef(y_true, y_pred),
        "ROC-AUC": roc_auc_score(y_true, y_probability),
        "Average Precision": average_precision_score(y_true, y_probability),
        "True Negatives": int(tn),
        "False Positives": int(fp),
        "False Negatives": int(fn),
        "True Positives": int(tp),
        "Total Errors": int(fp + fn),
        "Threshold": threshold,
    }

    confusion_df = pd.DataFrame(
        [
            {"Actual": "Benign", "Predicted Benign": int(tn), "Predicted Attack": int(fp)},
            {"Actual": "Attack", "Predicted Benign": int(fn), "Predicted Attack": int(tp)},
        ]
    )

    return metrics, confusion_df


def print_metrics(metrics: dict) -> None:
    """Print a readable metric summary."""
    print("\nFinal test metrics")
    print("------------------")

    percentage_metrics = [
        "Accuracy",
        "Precision",
        "Recall",
        "Specificity",
        "F1 Score",
        "Balanced Accuracy",
        "MCC",
        "ROC-AUC",
        "Average Precision",
    ]

    for name in percentage_metrics:
        print(f"{name}: {100 * metrics[name]:.4f}%")

    print("\nConfusion counts")
    print("----------------")
    print(f"True Negatives: {metrics['True Negatives']:,}")
    print(f"False Positives: {metrics['False Positives']:,}")
    print(f"False Negatives: {metrics['False Negatives']:,}")
    print(f"True Positives: {metrics['True Positives']:,}")
    print(f"Total Errors: {metrics['Total Errors']:,}")
    print(f"Frozen Threshold: {metrics['Threshold']}")


def main() -> int:
    """Run the compact corrected pipeline."""
    ensure_project_directories()

    df = load_prepared_dataset()

    train_df, validation_df, test_df = group_split(df)

    print("Dataset split sizes")
    print("-------------------")
    print(f"Training rows: {len(train_df):,}")
    print(f"Validation rows: {len(validation_df):,}")
    print(f"Final test rows: {len(test_df):,}")

    X_train = train_df[FEATURE_COLUMNS]
    y_train = train_df[TARGET_COLUMN].astype(int)

    X_test = test_df[FEATURE_COLUMNS]
    y_test = test_df[TARGET_COLUMN].astype(int)

    model = LGBMClassifier(**LIGHTGBM_PARAMS)

    model.fit(X_train, y_train)

    test_probability = model.predict_proba(X_test)[:, 1]

    metrics, confusion_df = evaluate_predictions(
        y_true=y_test,
        y_probability=test_probability,
        threshold=FINAL_THRESHOLD,
    )

    print_metrics(metrics)

    metrics_df = pd.DataFrame(
        [{"Metric": key, "Value": value} for key, value in metrics.items()]
    )

    metrics_df.to_csv(FINAL_METRICS_PATH, index=False)
    confusion_df.to_csv(FINAL_CONFUSION_MATRIX_PATH, index=False)

    print("\nSaved outputs")
    print("-------------")
    print(f"Metrics: {FINAL_METRICS_PATH}")
    print(f"Confusion matrix: {FINAL_CONFUSION_MATRIX_PATH}")

    print("\nPipeline completed successfully.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
