# Dataset Preparation Instructions

This folder documents how to prepare the dataset required for the project.

The project uses a prepared sample derived from the **CICIDS2017 intrusion-detection dataset**.  
The dataset itself is not included in this repository because of file size and licensing considerations.

## 1. Official Dataset Source

Download CICIDS2017 from the Canadian Institute for Cybersecurity:

https://www.unb.ca/cic/datasets/ids-2017.html

The relevant files are usually provided under the `MachineLearningCSV` / `MachineLearningCVE` version of the dataset.

## 2. Expected Repository Data Structure

After downloading the dataset, organize the local files as follows:

```text
data/
├── README.md
├── raw/
│   └── cicids2017/
│       ├── Monday-WorkingHours.pcap_ISCX.csv
│       ├── Tuesday-WorkingHours.pcap_ISCX.csv
│       ├── Wednesday-workingHours.pcap_ISCX.csv
│       ├── Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv
│       ├── Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv
│       ├── Friday-WorkingHours-Morning.pcap_ISCX.csv
│       ├── Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv
│       └── Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv
│
└── processed/
    └── cicids2017_prepared_sample.csv
```

The notebook expects the processed dataset to be available at:

```text
data/processed/cicids2017_prepared_sample.csv
```

If the notebook is executed in Google Colab, the path may need to be adjusted to the mounted Google Drive location.

## 3. Prepared Sample Used in This Project

The final project was developed using a prepared CICIDS2017 sample with the following properties:

| Property | Value |
|---|---:|
| Total observations | 28,303 |
| Benign observations | 22,662 |
| Attack observations | 5,641 |
| Attack prevalence | approximately 19.93% |
| Number of retained numerical predictors | 19 |
| Target column | `Label` |

The corrected final evaluation split contained:

| Split | Observations |
|---|---:|
| Training set | 16,851 |
| Validation set | 5,785 |
| Final test set | 5,667 |

The corrected final test set contained:

| Class | Count |
|---|---:|
| Benign | 4,505 |
| Attack | 1,162 |

These values are useful for checking that the prepared data matches the project setup.

## 4. Required Target Format

The target column should be named:

```text
Label
```

The project treats the target as binary:

| Original label meaning | Binary value |
|---|---:|
| Benign traffic | 0 |
| Attack traffic | 1 |

All non-benign labels are treated as attacks.

## 5. Required Predictor Format

The final corrected model uses 19 numerical flow-level predictors.

The dataset-preparation script checks that the required predictors exist, removes unsupported columns, standardizes column names, converts the target to binary format, and saves the prepared file to:

```text
data/processed/cicids2017_prepared_sample.csv
```

## 6. Preparing the Dataset

After placing the raw CICIDS2017 CSV files under:

```text
data/raw/cicids2017/
```

run:

```bash
python src/prepare_dataset.py
```

The script will:

1. read the raw CICIDS2017 CSV files;
2. clean column names;
3. convert labels to binary values;
4. keep the required numerical predictors;
5. remove invalid or unsupported rows;
6. construct the prepared project sample using fixed random seeds;
7. save the prepared dataset to:

```text
data/processed/cicids2017_prepared_sample.csv
```

## 7. Running the Main Pipeline

After the prepared dataset exists, the main corrected pipeline can be executed outside the notebook using:

```bash
python src/run_pipeline.py
```

This script runs a compact version of the corrected experiment:

1. loads the prepared dataset;
2. applies the corrected group-aware split;
3. trains the final LightGBM model;
4. applies the frozen threshold;
5. prints the final evaluation metrics.

## 8. Important Notes

- The raw CICIDS2017 dataset is not committed to this repository.
- The processed sample is also not committed by default because it may be large.
- The notebook can still be run in Google Colab if the dataset path is updated.
- Fixed random seeds are used where applicable.
- Small numerical differences may occur because of library versions, operating systems, or hardware.
- The final test set must not be used for model selection, feature selection, or threshold tuning.

## 9. Troubleshooting

If the notebook or script cannot find the dataset, check that this file exists:

```text
data/processed/cicids2017_prepared_sample.csv
```

If it does not exist, run:

```bash
python src/prepare_dataset.py
```

If the raw files are stored somewhere else, edit the dataset path in:

```text
src/config.py
```

or update the path directly inside the notebook.

## 10. Reproducibility Goal

The purpose of these instructions is to make the dataset-preparation process explicit and reproducible.

The original submitted notebook contained the full analysis, but the added `data/` and `src/` structure makes it clearer how another user can recreate the prepared dataset and rerun the main pipeline outside the notebook.
