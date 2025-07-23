# Exploratory Data Analysis (EDA) Report - INFOBRAS Dataset

*   **Project:** IRIS (Sprint 1, Day 1)
*   **Date:** Monday
*   **Lead Engineer:** Jhon Wilber Ajata Ascarrunz
*   **Objective:** To load and perform an initial exploratory analysis of the Public Works (INFOBRAS) dataset to identify and document issues related to data quality, structure, and data types.

---

### 1. Executive Summary

A comprehensive exploratory analysis was conducted on the raw INFOBRAS dataset, comprising 178,257 records and 113 columns. The analysis revealed that while the dataset is information-rich, it suffers from significant and systemic issues that render it unsuitable for direct analysis or modeling. Four critical problem areas were identified: **structural defects, data type contamination, a high prevalence of null values, and inconsistent column naming conventions.** This report details each of these findings and establishes a clear foundation for the data cleaning phase scheduled for Day 2.

---

### 2. Analysis Process & Methodology

The analysis was carried out within a Jupyter Notebook (`01_Data_Cleaning_INFOBRAS.ipynb`), following a systematic process to ensure complete coverage of the dataset's condition.

**2.1. Environment Setup and Data Ingestion:**
*   A professional working environment was established, including a Git repository and a Python virtual environment (`iris_env`), to ensure project reproducibility.
*   The raw `infobras.csv` file was loaded into a Pandas DataFrame named `df_raw`. During this step, initial technical hurdles such as `FileNotFoundError` and `SyntaxError` were overcome by implementing best practices like relative pathing (`../data/`).
*   The successful data load triggered a `DtypeWarning`, which served as the first piece of evidence for mixed data types in several columns, validating the need for a deep-dive investigation.

**2.2. Systematic Diagnostics:**
A sequence of three fundamental Pandas commands was applied to gain a holistic view of the data:

*   **`df_raw.info(verbose=True, show_counts=True)`:** Used to obtain a technical summary of the DataFrame's structure.
*   **`df_raw.describe(include='all')`:** Employed to get descriptive statistics for both numerical and categorical columns.
*   **`df_raw.isna().sum().sort_values(ascending=False)`:** Used to quantify and prioritize the missing data issues across all columns.

---

### 3. Key Findings (Diagnosis)

The analysis revealed the following critical issues requiring resolution:

**3.1. Severe Structural Defects:**
*   **Duplicated Columns:** The dataset contains duplicated sets of columns. For instance, both `RUC` and `RUC.1`, as well as `Monto del contrato en soles` and `Monto del contrato en soles.1`, exist. This duplication likely distinguishes between the project contractor and the supervisor, but the current naming convention is ambiguous and structurally flawed.

**3.2. Widespread Data Type Contamination:**
*   **Dates as Text (`object`):** 16 columns representing dates (e.g., `Fecha de inicio de obra`, `Fecha de finalizacion real`) are stored as strings, preventing any duration calculations or time-series analysis.
*   **Financial Values as Text (`object`):** 18 columns representing monetary values or percentages (e.g., `Costo de la obra en soles`, `Avance Físico Real Acumulado (%)`) are stored as strings due to the presence of non-numeric characters like "S/.", ",", and "%".

**3.3. High Incidence of Missing Data (Nulls):**
*   **Unusable Columns:** Several columns were found to be completely empty (e.g., `Fecha de aprobación` with 0 non-null values) or over 99.9% empty (e.g., `Tipo de certificado de inversión pública`), rendering them useless for analysis.
*   **Implicitly Meaningful Nulls:** In binary-like columns such as `¿Corresponde a un saldo de Obra?`, it was observed that the absence of a value (`NaN`) likely represents the 'No' category—a data recording practice that must be explicitly corrected.

**3.4. Inconsistent Column Naming Conventions:**
*   Column names exhibit a mix of upper and lower case, spaces, accents, and special characters (e.g., `¿`, `°`, `/`), hindering programmatic manipulation and violating standard style conventions.

---

### 4. Conclusion & Next Steps

The exploratory analysis was successful, providing a detailed and precise map of all issues plaguing the INFOBRAS dataset. The day's objective of diagnosing the data's condition has been met.

Based on these findings, the plan for Day 2 is clear: proceed with the construction of a data cleaning pipeline in Python. This pipeline must, at a minimum:
1.  Standardize all column names.
2.  Rename duplicated columns to resolve structural ambiguity.
3.  Remove useless columns.
4.  Convert date and numeric columns to their correct data types.
5.  Implement a strategy to handle null values, including the conversion of implicit nulls to explicit values.

**Day's Deliverable (COMPLETED):**
*   This report and the corresponding section of the `01_Data_Cleaning_INFOBRAS.ipynb` notebook, containing the code and outputs of the analysis.