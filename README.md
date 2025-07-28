# Project IRIS: Investment Risk Index for Sub-sovereign Assets

## 1. Executive Summary

Project IRIS is a proprietary risk scoring model designed to assess the viability of public infrastructure investments at the municipal level in Peru. By innovatively fusing public works execution data with public health statistics (used as a proxy for social and institutional stability), IRIS provides a deeper, more predictive view of risk than traditional financial models.

**Tech Stack:** Python, Pandas, Scikit-learn, Plotly, Streamlit, Google Cloud Platform (for deployment).

**Keywords:** `FinTech`, `Quantitative Analysis`, `Risk Modeling`, `Data Science`, `Machine Learning`, `Alternative Data`.

---

## 2. Project Goal

The objective is to develop and validate a data product that can provide investors, insurance companies, and development banks with an objective, data-driven score to quantify non-financial investment risk, ultimately leading to more efficient capital allocation and greater social impact.

---

## 3. Project Roadmap & Status

This project is in active development. The planned sprints are as follows:

-   **[Sprint 1: Data Wrangling]**: Consolidating and cleaning public works and public health datasets. **(Completed ✅)**
-   **[Sprint 2: Feature Engineering]**: Developing the G-Factor (Governmental Inefficiency) and S-Factor (Social Vulnerability). **(In Progress ⏳)**
-   **[Sprint 3: Index Construction & Dashboard MVP]**: Building the final IRIS score and deploying an interactive dashboard with Streamlit.
-   **[Sprint 4: Backtesting & Validation]**: Rigorously testing the predictive power of the index against historical project outcomes.

---

## 4. Data Pipeline & Sources

The core of this project is the fusion of two disparate public datasets to generate unique risk signals. The entire process of data ingestion, cleaning, auditing, curation, and fusion is documented in the following notebooks:

-   `notebooks/01_iris_infobras_cleaning.ipynb`
-   `notebooks/02_SINADEF_Processing.ipynb`
-   `notebooks/03_Data_Fusion.ipynb`

### Data Sources

1.  **INFOBRAS - Public Works (`infobras_certified_v1.csv`):**
    *   **Source:** National Open Data Portal of Peru, managed by the Comptroller General's Office.
    *   **Description:** Contains detailed records of over 180,000 public infrastructure projects nationwide.
    *   **Process:** A rigorous 8-step pipeline was implemented, which included column standardization, text cleaning, type conversion, and an auditing/curation phase that removed over 48,000 records with illogical or inconsistent data (e.g., inverted dates, zero-day timelines). The result is a certified dataset at the individual project level.

2.  **SINADEF - National Death Registry (`sinadef_certified_v1.csv`):**
    *   **Source:** National Open Data Portal of Peru, managed by the Ministry of Health (MINSA).
    *   **Description:** Contains records of over 1 million deaths nationwide, including demographic and location data.
    *   **Process:** A pipeline was developed to clean, standardize, and, most critically, **aggregate** the data to the district level (`ubigeo`). Plausibility filters (e.g., removing ages > 110) were applied to ensure the quality of the resulting health indicators.

### Fusion

The final output of Sprint 1 is `iris_master_dataset_v1.csv`, a master dataset that joins the INFOBRAS data (aggregated to the district level to create the **G-Factors**) with the SINADEF data (which form the **S-Factors**). This fusion was performed using a `left merge` on the `ubigeo` key, prioritizing districts with public works activity.

---

## 5. How to Use

*(This section will be updated with instructions on how to run the application and notebooks once Sprint 3 is complete).*