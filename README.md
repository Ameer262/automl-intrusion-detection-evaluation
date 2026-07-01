# Critical Evaluation of AutoML-Based Intrusion Detection

## Project Description

This repository contains the final project for the Data Science in Cyber course.

The project reproduces and critically evaluates an AutoML-based network intrusion detection workflow. The study examines whether the original reported results are reproducible and whether the evaluation methodology provides reliable evidence.

A corrected experimental protocol was also developed to prevent duplicate-profile leakage, separate model development from final evaluation, and evaluate the frozen model on an untouched final test set.

## Selected Source

**Paper:**  
Enabling AutoML for Zero-Touch Network Security: Use-Case Driven Analysis

**Article / Paper Link:**  
[Insert the official paper link here]

**Original GitHub Repository:**  
[Insert the original repository link here]

## Dataset

The project uses a prepared sample derived from the CICIDS2017 intrusion detection dataset.

**Dataset Source:**  
https://www.unb.ca/cic/datasets/ids-2017.html

The dataset itself is not included in this repository. Follow the notebook instructions to place the required data files in the correct directory.

## Repository Contents

- `intrusion_detection_project.ipynb` — complete analysis and experimental notebook.
- `final_project_report.pdf` — final written project report.
- `requirements.txt` — main Python dependencies.
- `README.md` — project description and execution instructions.

## Main Methodology

The project includes:

- reproduction of the original clean intrusion detection experiment;
- data inspection and exploratory analysis;
- missing-value, duplicate, outlier, class-imbalance, and correlation analysis;
- corrected group-aware training, validation, and test splitting;
- comparison of multiple machine-learning models;
- feature-engineering experiments;
- validation-based model and threshold selection;
- one-time final-test evaluation;
- detailed false-positive and false-negative analysis;
- critical evaluation of the source's claims.

## Final Result

The selected LightGBM pipeline used 19 numerical flow-level predictors and a frozen classification threshold of `0.546`.

On the untouched corrected final test set, it produced:

- 4,496 true negatives;
- 9 false positives;
- 5 false negatives;
- 1,157 true positives;
- approximately 99.75% accuracy;
- approximately 99.23% precision;
- approximately 99.57% recall;
- approximately 99.40% F1 score.

## Execution Instructions

1. Clone or download this repository.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
