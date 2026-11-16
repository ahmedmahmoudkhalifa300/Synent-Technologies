# 🏦 Loan Approval Prediction using Machine Learning

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter&logoColor=white)](./Loan_Approval_Prediction.ipynb)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Video Demo](https://img.shields.io/badge/Video%20Demo-Google%20Drive-4285F4?logo=googledrive&logoColor=white)](https://drive.google.com/file/d/1sjrKCAFlbjbxe1NvlWDLahJbnQALmWn2/view?usp=sharing)
[![GitHub](https://img.shields.io/badge/Author-Ahmed%20Mahmoud%20Khalifa-181717?logo=github)](https://github.com/ahmedmahmoudkhalifa300)

An end-to-end **Data Science & Machine Learning** project that automates the evaluation of bank loan applications and predicts whether a loan will be **Approved (`Y`)** or **Rejected (`N`)** based on applicant demographics, income, loan parameters, property area, and credit history.

🎥 **Project Video Demo:** [Watch on Google Drive](https://drive.google.com/file/d/1sjrKCAFlbjbxe1NvlWDLahJbnQALmWn2/view?usp=sharing) | [`video_demo.md`](./video_demo.md)

---

## 📌 Table of Contents
1. [Problem Statement](#-1-problem-statement)
2. [Dataset Details](#-2-dataset-details)
3. [Methodology & Approach](#-3-methodology--approach)
4. [Experimental Results & Key Findings](#-4-experimental-results--key-findings)
5. [Project Structure](#-5-project-structure)
6. [How to Run the Project](#-6-how-to-run-the-project)
7. [Author](#-7-author)

---

## 🎯 1. Problem Statement

Financial institutions receive hundreds of loan applications daily. Evaluating each application manually is time-consuming, costly, and susceptible to inconsistent human judgment. 

The objective of this project is to build a reliable, leak-free **Supervised Machine Learning pipeline** that predicts the binary target variable **`Loan_Status`**:
- **`Y` (`1`) — Loan Approved:** The applicant meets creditworthiness and financial criteria.
- **`N` (`0`) — Loan Not Approved:** The application poses a high default risk.

> **Technical Note on Problem Formulation:**  
> Because `Loan_Status` is a binary categorical outcome (`Approved` vs. `Not Approved`), this task is a **Binary Classification** problem. In accordance with the project specifications, we implement **Linear Regression** (converting its continuous predictions $\hat{y}$ into binary classes `{0, 1}` using a decision threshold of `0.5`) alongside **Decision Tree Classifier**, **Random Forest Classifier**, and **Logistic Regression** (included as an additional probabilistic classification benchmark).

---

## 📊 2. Dataset Details

- **Dataset Name:** Loan Prediction Problem Dataset
- **Source:** [Kaggle — Loan Prediction Problem Dataset](https://www.kaggle.com/datasets/altruistdelhite04/loan-prediction-problem-dataset)
- **Training File Used:** `train_u6lujuX_CVtuZ9i.csv`
- **Dimensions:** `614` rows (loan applications) × `13` columns (`1` identifier, `11` predictive features, `1` target variable)
- **Target Distribution (`Loan_Status`):**
  - **Approved (`Y` / `1`):** `422` applications (**68.73%**)
  - **Rejected (`N` / `0`):** `192` applications (**31.27%**)

### Feature Dictionary & Missing Value Profile

| # | Column Name | Data Type | Role | Missing Count (%) | Description |
| :-: | :--- | :--- | :--- | :---: | :--- |
| 1 | `Loan_ID` | Categorical (`string`) | Identifier | `0` (0.00%) | Unique loan application ID (dropped before modeling) |
| 2 | `Gender` | Categorical (`string`) | Feature | `13` (2.12%) | Applicant gender (`Male` / `Female`) |
| 3 | `Married` | Categorical (`string`) | Feature | `3` (0.49%) | Applicant marital status (`Yes` / `No`) |
| 4 | `Dependents` | Ordinal (`string`) | Feature | `15` (2.44%) | Number of dependents (`0`, `1`, `2`, `3+`) |
| 5 | `Education` | Categorical (`string`) | Feature | `0` (0.00%) | Education qualification (`Graduate` / `Not Graduate`) |
| 6 | `Self_Employed` | Categorical (`string`) | Feature | `32` (5.21%) | Self-employment status (`Yes` / `No`) |
| 7 | `ApplicantIncome` | Numerical (`int64`) | Feature | `0` (0.00%) | Monthly income of the primary applicant |
| 8 | `CoapplicantIncome` | Numerical (`float64`) | Feature | `0` (0.00%) | Monthly income of the co-applicant |
| 9 | `LoanAmount` | Numerical (`float64`) | Feature | `22` (3.58%) | Loan amount requested (in thousands) |
| 10 | `Loan_Amount_Term` | Numerical (`float64`) | Feature | `14` (2.28%) | Loan repayment period (in months, e.g., `360` = 30 years) |
| 11 | `Credit_History` | Binary (`float64`) | Feature | `50` (8.14%) | Credit history meets guidelines (`1.0` = Good, `0.0` = Bad) |
| 12 | `Property_Area` | Categorical (`string`) | Feature | `0` (0.00%) | Property location (`Urban`, `Semiurban`, `Rural`) |
| 13 | **`Loan_Status`** | **Binary (`string`)** | **Target ($y$)** | `0` (0.00%) | Loan approval status (`Y` = Approved, `N` = Rejected) |

---

## 🛠️ 3. Methodology & Approach

The project follows a rigorous, step-by-step **Machine Learning workflow** inside [`Loan_Approval_Prediction.ipynb`](./Loan_Approval_Prediction.ipynb):

### Step 1: Data Exploration & Understanding
- Inspected schema, data types (`info()`), statistical summaries (`describe(include="all").T`), unique cardinalities, and missing value distributions.

### Step 2: Exploratory Data Analysis (EDA)
Built 10 visual diagnostic plots to uncover relationships in the data:
1. **Univariate Target Plot:** Count plot of `Loan_Status` (`68.7%` Approved vs. `31.3%` Rejected).
2. **Bivariate Categorical Plots:** Count plots of `Education`, `Credit_History`, `Property_Area`, and `Married` vs. `Loan_Status`.
   - *Key EDA Insight:* **`Credit_History`** is the strongest predictor—**79.58%** of applicants with `Credit_History = 1.0` were approved, whereas **92.13%** of applicants with `Credit_History = 0.0` were rejected.
   - *Property Area Insight:* **Semiurban** properties achieved the highest approval rate (**76.82%**), compared to **Urban** (**65.84%**) and **Rural** (**61.45%**).
3. **Numerical Distributions & Skewness:** Histograms with KDE curves for `ApplicantIncome` (skewness = `6.54`) and `LoanAmount` (skewness = `2.68`).
4. **Outlier & Quartile Analysis:** Boxplots of `ApplicantIncome` and `LoanAmount` grouped by `Loan_Status`.
5. **Multivariate Correlation Analysis:** Pearson Correlation Heatmap across all numerical features and the binary target (`Credit_History` correlates at $r = +0.56$ with `Loan_Status`, and `ApplicantIncome` correlates at $r = +0.57$ with `LoanAmount`).

### Step 3: Data Cleaning & Leak-Free Imputation
1. **Dropped Identifier:** Removed `Loan_ID` as it carries no predictive signal.
2. **Target Encoding:** Mapped `Loan_Status` from `{'Y': 1, 'N': 0}`.
3. **Ordinal Feature Cleaning:** Cleaned `Dependents` by replacing `'3+'` with `3` and converting the column to numeric type.
4. **Data Integrity Checks:** Verified zero duplicate rows (`0` duplicates) and zero illogical/negative values.
5. **Outlier Retention Justification:** Retained high-income and large-loan outliers because they represent legitimate high-value applicants rather than data entry errors; using **Median Imputation** and tree-based models naturally mitigates skewness.
6. **Zero Data Leakage Imputation:**
   - **Numerical Features (`LoanAmount`, `Loan_Amount_Term`, `Dependents`):** Imputed using **Median Imputation** (`SimpleImputer(strategy="median")`).
   - **Categorical Features (`Gender`, `Married`, `Education`, `Self_Employed`, `Property_Area`, `Credit_History`):** Imputed using **Mode / Most Frequent Imputation** (`SimpleImputer(strategy="most_frequent")`).
   - All imputation statistics (medians and modes) were learned **strictly from the 80% training split (`491` rows)** and never from the test split.

### Step 4: Feature Encoding & Scaling
- **Train-Test Split:** Stratified 80/20 split (`491` training samples, `123` test samples, `random_state=42`, `stratify=y`) preserving the exact `68.7% / 31.3%` class ratio.
- **One-Hot Encoding:** Converted categorical features into binary indicator columns (`drop_first=True` to prevent multicollinearity in linear models).
- **Standardization:** Applied `StandardScaler` fitted **only on `X_train`** and transformed `X_test`.

### Step 5: Model Training & Evaluation
Trained and evaluated four models:
1. **Linear Regression (with `threshold = 0.5`)** — *[Required]*
2. **Decision Tree Classifier (`max_depth=3, min_samples_leaf=5`)** — *[Required]*
3. **Random Forest Classifier (`n_estimators=100, max_depth=5`)** — *[Required]*
4. **Logistic Regression** — *[Additional Classification Benchmark]*

---

## 🏆 4. Experimental Results & Key Findings

### Model Performance Comparison (on Unseen Test Set — `123` Samples)

| Model | Train Accuracy | Test Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Linear Regression (`Threshold = 0.5`)** *(Required)* | 80.04% | **86.18%** | 84.00% | 98.82% | **90.81%** | 0.8474 |
| **2. Decision Tree Classifier** *(Required)* | 79.84% | **85.37%** | 83.17% | 98.82% | **90.32%** | 0.7729 |
| **3. Random Forest Classifier** *(Required)* | 80.04% | **85.37%** | 83.17% | 98.82% | **90.32%** | 0.8146 |
| **4. Logistic Regression** *(Additional Benchmark)* | 80.04% | **86.18%** | 84.00% | 98.82% | **90.81%** | **0.8486** |

### Key Takeaways
1. **Dominance of `Credit_History`:** Feature importance from Random Forest (Gini importance) and standardized coefficients from Logistic Regression confirm that **`Credit_History`** is by far the most influential determinant of loan approval, followed by **`Property_Area_Semiurban`**, **`LoanAmount`**, and **`CoapplicantIncome`**.
2. **Overfitting Prevention in Decision Trees:** An unpruned Decision Tree (`max_depth=None`) memorized the training set (`100.0%` train accuracy) and dropped to `71.54%` test accuracy. Constraining tree depth (`max_depth=3`) boosted test accuracy from `71.54%` to **`85.37%`** (`90.32%` F1-Score).
3. **Why Classification Models Are Preferred Over Linear Regression:** Although Linear Regression with a `0.5` threshold achieved `86.18%` test accuracy on this dataset (due to the strong binary split of `Credit_History`), **Logistic Regression** (`ROC-AUC = 0.8486`) and **Random Forest** (`ROC-AUC = 0.8146`) are theoretically and practically superior for production deployment because they produce calibrated probabilities bounded in $[0, 1]$ and are robust against extreme income outliers.

---

## 📂 5. Project Structure

```text
├── data/
│   ├── train_u6lujuX_CVtuZ9i.csv        # Official Kaggle training dataset (614 rows × 13 columns)
│   └── test_Y3wMUE5_7gLdaTN.csv         # Official Kaggle unlabeled test dataset
├── train_u6lujuX_CVtuZ9i.csv            # Root copy of training dataset for direct loading
├── Loan_Approval_Prediction.ipynb       # Complete, executed Jupyter Notebook (all steps, plots & metrics)
└── README.md                            # Project documentation
```

---

## 🚀 6. How to Run the Project

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ahmedmahmoudkhalifa300/Synent-Technologies.git
   cd Synent-Technologies/Loan_Approval_Prediction
   ```

2. **Install required Python packages:**
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn jupyter
   ```

3. **Launch Jupyter Notebook:**
   ```bash
   jupyter notebook Loan_Approval_Prediction.ipynb
   ```

---

## 👤 7. Author

**Ahmed Mahmoud Khalifa**  
- 🔗 **GitHub Profile:** [https://github.com/ahmedmahmoudkhalifa300](https://github.com/ahmedmahmoudkhalifa300)
