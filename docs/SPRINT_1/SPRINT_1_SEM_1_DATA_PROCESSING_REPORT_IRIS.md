# Final Data Preprocessing Report for Project IRIS

*   **Project:** IRIS (Sprint 1: "The Dirty Truth")
*   **Primary Data Source:** `DataSet-Obras-Publicas-23-07-2025.xlsx`
*   **Final Certified Asset:** `infobras_certified_v1.csv`
*   **Lead Data Engineer:** Jhon Wilber Ajata Ascarrunz

---

### 1. Executive Summary

A comprehensive data engineering process has been successfully completed to transform the raw INFOBRAS dataset into a high-quality data asset, ready for the predictive modeling phase of Project IRIS. Starting with 180,941 initial records, a robust cleaning, auditing, and curation pipeline was designed and implemented in Python. This pipeline systematically addressed structural issues, data type inconsistencies, logical incoherence, and business plausibility.

The process resulted in the strategic removal of **48,804 low-quality records**, culminating in a final certified dataset of **132,137 rows and 108 columns**. This dataset is structurally sound, logically coherent, free of critical errors, and has been curated to mitigate the impact of extreme outliers. The developed pipeline is robust and reproducible, ensuring a reliable foundation for the upcoming feature engineering phase and the subsequent fusion with external data (SINADEF).

---

### 2. Initial Data State & Challenges

The dataset in its original state was entirely unsuitable for modeling, presenting multiple critical challenges:

*   **Data Contamination:** Crucial date, monetary, and percentage values were stored as text (`object`), making them unusable for calculations.
*   **Structural Defects:** Inconsistent and ambiguous duplicated column names (e.g., `RUC` and `RUC.1`) prevented clear analysis.
*   **Hidden Inconsistencies:** The presence of leading/trailing whitespaces in categorical values caused silent but critical failures in data filtering operations.
*   **Implausible Data:** Existence of logically impossible records, such as projects with end dates preceding their start dates, and execution timelines of zero days or several decades.

### 3. Methodology: The "Baby Steps" Cleaning, Auditing, and Curation Pipeline (v3.0)

A comprehensive Python function (`clean_infobras_data`) was developed to process the data systematically and reproducibly. Each "pasito" (baby step) represents a specific, verifiable transformation.

**3.1. Structural Cleaning Phase (Steps 1-4)**
*   **Shielding:** `.str.strip()` was applied to all 85 text columns to eliminate hidden whitespaces. **This was the most critical action to ensure data integrity.**
*   **Standardization:** All column names were normalized to `snake_case` format.
*   **Repair:** Duplicated columns were renamed to descriptive and unique names (e.g., `ruc_supervisor`).
*   **Pruning:** 6 columns with over 99.9% missing data were dropped.

**3.2. Data Transformation & Auditing Phase (Steps 5-6)**
*   **Dates:** 16 columns were converted to `datetime` format, handling format errors.
*   **Temporal Audit (Step 5.5):** An integrated quality check **detected and removed 898 records** with incoherent dates (end date before start date).
*   **Numerics:** 18 numeric columns were "decontaminated" by stripping symbols ("S/.", "%") and commas, then converted to `float`.

**3.3. Imputation & Curation Phase (Steps 7-8)**
*   **Strategic Imputation:** Null values were filled based on context (e.g., `NaN` in `causal_de_paralizacion` became `'No Paralizada'`).
*   **Data Curation:** Business logic filters were applied to enhance the quality of the final dataset:
    *   **47,887 records** with non-positive execution timelines (zero or negative) were removed.
    *   **19 records** with extreme and implausible timelines (over 10 years) were removed to prevent distortion from anomalous outliers.

---

### 4. Final Product Description: `infobras_certified_v1.csv`

The data engineering process resulted in a final dataset with the following certified characteristics:

*   **Dimensions:** 132,137 rows x 108 columns.
*   **Data Quality:**
    *   **Free of Critical Nulls:** Zero null values in all numeric and text columns. The only remaining nulls are `NaT` (Not a Time) in datetime columns, which represent valid data absences.
    *   **Logical Coherence:** Guaranteed temporal consistency and the absence of negative values in key fields.
    *   **Plausibility:** Cleansed of illogical records and extreme outliers that could skew future analysis.
*   **Structure:** The dataset has a clean structure with standardized column names and correct, consistent data types, making it ready for immediate use without surprises.

---

### 5. Conclusion & Implications for Project IRIS

Sprint 1 has successfully concluded with the creation of a high-fidelity data asset. The process has not only cleaned the data but has fundamentally improved its intrinsic quality through integrated auditing and curation.

This certified dataset (`infobras_certified_v1.csv`) mitigates the risk of "Garbage In, Garbage Out" and provides a solid, reliable foundation upon which Sprint 2 ("The Factor Factory") can be built. The subsequent feature engineering and data fusion with the SINADEF dataset can now proceed with the confidence that they are being built upon a robust source of truth.