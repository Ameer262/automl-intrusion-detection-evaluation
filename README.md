# Critical Evaluation of AutoML-Based Intrusion Detection

## Project Overview

This repository contains the final project for the **Data Science in Cyber** course at the University of Haifa.

The project reproduces and critically evaluates the intrusion-detection workflow presented in the paper:

**“Enabling AutoML for Zero-Touch Network Security: Use-Case Driven Analysis”**

The objective was not only to reproduce the reported results, but also to examine whether the original experimental methodology provides reliable evidence. A corrected evaluation pipeline was developed to reduce data leakage, separate model development from final evaluation, and provide a more rigorous analysis of false positives and false negatives.

---

## Selected Source

### Paper

**Enabling AutoML for Zero-Touch Network Security: Use-Case Driven Analysis**

Paper link:

https://doi.org/10.1109/TNSM.2024.3376631

### Original GitHub Repository

https://github.com/Western-OC2-Lab/AutoML-and-Adversarial-Attack-Defense-for-Zero-Touch-Network-Security

---

## Dataset

The project uses a prepared sample derived from the **CICIDS2017 intrusion-detection dataset**.

Official dataset source:

https://www.unb.ca/cic/datasets/ids-2017.html

The dataset is not included in this repository because of its size. It must be downloaded separately and placed in the location expected by the notebook.

---

## Repository Contents

- `intrusion_detection_project.ipynb`  
  Complete notebook containing the source reproduction, exploratory data analysis, corrected modeling, evaluation, and error analysis.

- `final_project_report.pdf`  
  Final written report summarizing the methodology, results, critical evaluation, and conclusions.

- `requirements.txt`  
  Main Python dependencies required to run the notebook.

- `README.md`  
  Project description, dataset information, and execution instructions.

---

## Main Project Stages

The notebook includes:

1. reproduction of the original clean intrusion-detection experiment;
2. data loading and inspection;
3. missing-value and data-quality analysis;
4. duplicate-profile and leakage analysis;
5. exploratory data analysis;
6. class-prevalence and outlier analysis;
7. Pearson, Spearman, and Kendall correlation analysis;
8. feature-engineering experiments;
9. corrected group-aware training, validation, and test splitting;
10. comparison of multiple machine-learning models;
11. cross-validation and validation-based model selection;
12. validation-based threshold selection;
13. one-time evaluation on an untouched final test set;
14. false-positive and false-negative analysis;
15. cybersecurity impact and threshold trade-off analysis;
16. critical evaluation of the original source’s claims.

---

## Models Evaluated

The corrected workflow compared several model families, including:

- Logistic Regression;
- Random Forest;
- Histogram Gradient Boosting;
- LightGBM.

The final selected model was **LightGBM**.

---

## Corrected Evaluation Methodology

The corrected pipeline introduced several methodological safeguards:

- identical predictor profiles were prevented from crossing dataset splits;
- preprocessing decisions were based only on development data;
- model comparison used cross-validation and independent validation data;
- the classification threshold was selected before final testing;
- the final test set was evaluated exactly once;
- final predictions, probabilities, and results were stored and reused;
- integrity checks verified that the protected final test set remained unchanged.

The final selected classification threshold was:

```text
0.546
```

---

## Final Results

The final LightGBM model used 19 numerical flow-level predictors.

On the untouched corrected final test set, the confusion matrix was:

| Result | Count |
|---|---:|
| True Negatives | 4,496 |
| False Positives | 9 |
| False Negatives | 5 |
| True Positives | 1,157 |

The primary final metrics were approximately:

| Metric | Result |
|---|---:|
| Accuracy | 99.75% |
| Precision | 99.23% |
| Recall | 99.57% |
| Specificity | 99.80% |
| F1 Score | 99.40% |
| Balanced Accuracy | 99.69% |
| MCC | 99.24% |
| ROC-AUC | 99.99% |

The model correctly classified **5,653 of the 5,667 final-test observations**.

---

## Main Findings

The original clean-data results were successfully reproduced and were very close to the values reported by the source.

The corrected evaluation also achieved extremely strong performance. This shows that the source’s central predictive claim is supported on the supplied dataset.

However, the original workflow contained several methodological weaknesses, including:

- possible preprocessing leakage;
- possible feature-selection leakage;
- identical predictor profiles crossing random dataset splits;
- insufficient separation between model development and final testing;
- limited discussion of real-world class prevalence;
- no external or temporal validation.

The corrected experiment therefore supports the narrow conclusion that LightGBM performs very well on this dataset. It does not prove that the same performance will generalize to other organizations, future attacks, or production network environments.

---

## Error Analysis

The final model produced only 14 errors:

- 9 false positives;
- 5 false negatives.

Most errors were not located close to the classification threshold. Several incorrect predictions were made with high confidence, suggesting that minor threshold changes alone would not solve the majority of failures.

Repeated misleading characteristics included:

- forward packet-length statistics;
- segment-size features;
- header-length features;
- flow duration;
- inter-arrival timing values.

Three false positives shared exactly the same values across all 19 predictors and received the same model score. This indicates a repeated systematic failure pattern rather than three unrelated mistakes.

The threshold analysis also demonstrated the expected cybersecurity trade-off:

- lowering the threshold reduced missed attacks but could create more false alerts;
- raising the threshold reduced few false alerts while causing more attacks to remain undetected.

The alternative thresholds were analyzed only descriptively. The official threshold remained frozen at `0.546`.

---

## Execution Instructions

### Option 1: Google Colab

Google Colab is the recommended environment.

1. Open `intrusion_detection_project.ipynb` in Google Colab.
2. Upload or mount the required dataset.
3. Update the dataset path in the notebook when necessary.
4. Install the required packages when prompted.
5. Run the notebook cells in order from top to bottom.

### Option 2: Local Jupyter Environment

Clone the repository:

```bash
git clone https://github.com/Ameer262/automl-intrusion-detection-evaluation.git
```

Enter the repository directory:

```bash
cd automl-intrusion-detection-evaluation
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

Activate the environment on Linux or macOS:

```bash
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Start Jupyter Notebook:

```bash
jupyter notebook
```

Open:

```text
intrusion_detection_project.ipynb
```

Run all notebook cells in order.

---

## Important Reproducibility Notes

- The dataset is not included in this repository.
- Fixed random seeds are used where appropriate.
- Some numerical results may vary slightly because of package versions, operating systems, hardware, and internal library behavior.
- The original source used older versions of several Python libraries.
- Compatibility changes were required for deprecated functions and interfaces.
- The final test set must not be used for additional model or threshold tuning.
- The descriptive threshold analysis does not replace the frozen threshold of `0.546`.

---

## Scope and Limitations

The project successfully reproduced and critically evaluated the clean intrusion-detection branch of the original work.

The complete adversarial attack-and-defense pipeline was not independently reproduced in full under the corrected experimental protocol. Conclusions concerning adversarial robustness should therefore be interpreted separately from the supported clean-data findings.

The final results apply to the evaluated CICIDS2017 sample and should not be interpreted as proof of production readiness.

A real deployment would require:

- external validation;
- later-period testing;
- concept-drift monitoring;
- richer protocol and host context;
- confidence calibration;
- integration with additional security controls;
- analyst review.

---

## Final Conclusion

The original approach is recommended as a strong research baseline for flow-based intrusion detection.

Its central clean-data performance claim is supported by both the reproduction and the corrected evaluation. However, the model should not be used as a standalone production security system without additional validation, contextual enrichment, monitoring, and layered defensive controls.

The project demonstrates that trustworthy cybersecurity machine learning requires more than high accuracy. It also requires careful data separation, leakage prevention, appropriate security metrics, protected final evaluation, detailed error analysis, and cautious interpretation of the experimental evidence.

---

## Author

**Name:** Ameer Rohana
**Student ID:** 215631375
**Course:** Data Science in Cyber  
**Institution:** University of Haifa  
**Year:** 2026
