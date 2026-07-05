"""
Prepare or validate the CICIDS2017 sample used by the project.

This script supports two reproducibility modes:

1. If data/raw/cic_0.01km.csv exists:
   it is treated as the prepared source sample and is standardized.

2. Otherwise, if raw CICIDS2017 CSV files exist under data/raw/cicids2017/:
   they are combined and a fixed-seed binary sample is created.

The output is saved to:
data/processed/cicids2017_prepared_sample.csv
"""

from pathlib import Path
import sys

import numpy as np
import pandas as pd

from config import (
    RAW_CICIDS2017_DIR,
    SOURCE_SAMPLE_PATH,
    PREPARED_DATA_PATH,
    FEATURE_COLUMNS,
    REQUIRED_COLUMNS,
    TARGET_COLUMN,
    EXPECTED_BENIGN_ROWS,
    EXPECTED_ATTACK_ROWS,
    RANDOM_SEED,
    ensure_project_directories,
)


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace from column names."""
    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]
    return df


def standardize_label_column(df: pd.DataFrame) -> pd.DataFrame:
    """Convert the target column to binary: benign=0, attack=1."""
    df = df.copy()

    if TARGET_COLUMN not in df.columns:
        possible_label_columns = [
            col for col in df.columns
            if col.strip().lower() == "label"
        ]

        if not possible_label_columns:
            raise ValueError(
                f"Could not find target column '{TARGET_COLUMN}'."
            )

        df = df.rename(
            columns={possible_label_columns[0]: TARGET_COLUMN}
        )

    if df[TARGET_COLUMN].dtype == object:
        labels = (
            df[TARGET_COLUMN]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        df[TARGET_COLUMN] = np.where(
            labels == "BENIGN",
            0,
            1,
        ).astype(int)

    else:
        df[TARGET_COLUMN] = df[TARGET_COLUMN].astype(int)

    return df


def keep_required_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only the 19 final predictors and binary target."""
    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "The dataset is missing required columns:\n"
            + "\n".join(missing_columns)
        )

    prepared = df[REQUIRED_COLUMNS].copy()

    for col in FEATURE_COLUMNS:
        prepared[col] = pd.to_numeric(
            prepared[col],
            errors="coerce",
        )

    prepared[TARGET_COLUMN] = pd.to_numeric(
        prepared[TARGET_COLUMN],
        errors="coerce",
    )

    prepared = prepared.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    prepared = prepared.dropna(
        subset=REQUIRED_COLUMNS,
    )

    prepared[TARGET_COLUMN] = prepared[TARGET_COLUMN].astype(int)

    return prepared


def load_source_sample() -> pd.DataFrame | None:
    """Load the prepared source sample if it exists."""
    if not SOURCE_SAMPLE_PATH.exists():
        return None

    print(f"Using prepared source sample: {SOURCE_SAMPLE_PATH}")

    return pd.read_csv(SOURCE_SAMPLE_PATH)


def load_raw_cicids2017_files() -> pd.DataFrame:
    """Load and concatenate raw CICIDS2017 CSV files."""
    csv_files = sorted(
        RAW_CICIDS2017_DIR.glob("*.csv")
    )

    if not csv_files:
        raise FileNotFoundError(
            "No dataset was found.\n\n"
            "Expected one of the following:\n"
            f"1. Prepared source sample: {SOURCE_SAMPLE_PATH}\n"
            f"2. Raw CICIDS2017 CSV files under: {RAW_CICIDS2017_DIR}\n\n"
            "See data/README.md for setup instructions."
        )

    print("Loading raw CICIDS2017 files:")

    frames = []

    for path in csv_files:
        print(f"  - {path.name}")
        frames.append(pd.read_csv(path))

    return pd.concat(
        frames,
        ignore_index=True,
    )


def fixed_seed_sample(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a fixed-size binary sample.

    If enough examples exist, this produces:
    - 22,662 benign observations
    - 5,641 attack observations

    If fewer rows are available, it uses all available rows and reports
    the resulting counts.
    """
    benign = df[df[TARGET_COLUMN] == 0]
    attack = df[df[TARGET_COLUMN] == 1]

    benign_n = min(
        EXPECTED_BENIGN_ROWS,
        len(benign),
    )

    attack_n = min(
        EXPECTED_ATTACK_ROWS,
        len(attack),
    )

    if benign_n < EXPECTED_BENIGN_ROWS:
        print(
            "Warning: fewer benign rows than expected. "
            f"Using {benign_n} benign rows."
        )

    if attack_n < EXPECTED_ATTACK_ROWS:
        print(
            "Warning: fewer attack rows than expected. "
            f"Using {attack_n} attack rows."
        )

    sampled = pd.concat(
        [
            benign.sample(
                n=benign_n,
                random_state=RANDOM_SEED,
            ),
            attack.sample(
                n=attack_n,
                random_state=RANDOM_SEED,
            ),
        ],
        ignore_index=True,
    )

    sampled = sampled.sample(
        frac=1.0,
        random_state=RANDOM_SEED,
    ).reset_index(drop=True)

    return sampled


def summarize_dataset(df: pd.DataFrame) -> None:
    """Print a compact dataset summary."""
    class_counts = df[TARGET_COLUMN].value_counts().sort_index()

    benign_count = int(class_counts.get(0, 0))
    attack_count = int(class_counts.get(1, 0))
    total_count = len(df)

    attack_prevalence = (
        attack_count / total_count
        if total_count
        else float("nan")
    )

    print("\nPrepared dataset summary")
    print("------------------------")
    print(f"Rows: {total_count:,}")
    print(f"Predictors: {len(FEATURE_COLUMNS)}")
    print(f"Benign rows: {benign_count:,}")
    print(f"Attack rows: {attack_count:,}")
    print(f"Attack prevalence: {attack_prevalence:.4%}")
    print(f"Output path: {PREPARED_DATA_PATH}")


def main() -> int:
    """Prepare the dataset and save it to the processed folder."""
    ensure_project_directories()

    source_df = load_source_sample()

    if source_df is None:
        raw_df = load_raw_cicids2017_files()
        raw_df = clean_column_names(raw_df)
        raw_df = standardize_label_column(raw_df)
        raw_df = keep_required_columns(raw_df)
        prepared_df = fixed_seed_sample(raw_df)

    else:
        source_df = clean_column_names(source_df)
        source_df = standardize_label_column(source_df)
        prepared_df = keep_required_columns(source_df)

    PREPARED_DATA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    prepared_df.to_csv(
        PREPARED_DATA_PATH,
        index=False,
    )

    summarize_dataset(prepared_df)

    print("\nDataset preparation completed successfully.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
