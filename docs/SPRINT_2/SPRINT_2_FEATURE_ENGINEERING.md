# Sprint 2 Report: "The Factor Factory" (Feature Engineering)

*   **Project:** IRIS (Sprint 2)
*   **Sprint Objective:** To transform the certified master dataset into an analytical dataset by engineering all features corresponding to the **G-Factors (Governmental/Governance)** and **S-Factors (Social/Health)**, and to ultimately construct the first version of the composite IRIS Index.

---

### Executive Summary

This sprint marked the transition from data cleaning to insight generation. Leveraging the high-quality, fused dataset from Sprint 1, a comprehensive feature engineering pipeline was executed. This process translated raw metrics from the INFOBRAS and SINADEF datasets into normalized, risk-oriented factors.

Key G-Factors, such as project paralysis rates and cost/time overrun ratios, were calculated to quantify governmental management efficiency. Concurrently, S-Factors, including the average age of death, were engineered to serve as a proxy for social stability. All individual factors were then normalized to a common scale, had their risk directionality aligned, and were combined through a weighted formula to create the final `iris_score`. The sprint successfully concluded with the production of the `iris_scores_v1.csv` file, the core analytical asset for the project.

### G-Factor (Governance) Engineering

The G-Factors were engineered by aggregating the certified INFOBRAS data at the district (`ubigeo`) level. The primary indicators of governmental inefficiency calculated were:

1.  **`g_factor_tasa_paralizacion` (Paralysis Rate):** The percentage of public works projects in a district that have been officially paralyzed at any point. A direct measure of operational failure.
2.  **`g_factor_ratio_sobretiempo_promedio` (Average Time Overrun Ratio):** A normalized measure of project delays, calculated as `(Actual Duration - Planned Duration) / Planned Duration`. This provides a fair comparison of timeline efficiency across projects of different scales.
3.  **`g_factor_ratio_sobrecosto_promedio` (Average Cost Overrun Ratio):** A normalized measure of budget deviations, calculated as `(Final Cost - Approved Budget) / Approved Budget`. This quantifies financial discipline.

### S-Factor (Social) Engineering

The S-Factors were engineered by aggregating the certified SINADEF death registry data at the district (`ubigeo`) level. The key indicators of social vulnerability were:

1.  **`s_factor_total_muertes` (Total Deaths):** The total number of registered deaths in a district. This serves as a proxy for demographic pressure and scale.
2.  **`s_factor_edad_prom_muerte` (Average Age of Death):** The average age of death in a district. This is a powerful proxy for overall public health, quality of life, and institutional stability.
3.  **`s_factor_tasa_prevenibles` (Preventable Deaths Rate):** This factor was planned but could not be calculated due to the absence of reliable CIE-10 cause-of-death codes in the available raw data. This was noted as a key data limitation.

### IRIS Index Construction

The final step involved synthesizing these factors into a single, comprehensive risk score:

1.  **Imputation:** Missing factor values (primarily for districts with no corresponding SINADEF data) were imputed using the median value to ensure a complete dataset.
2.  **Normalization (Scaling):** All G-Factor and S-Factor columns were scaled to a common `[0, 1]` range using Scikit-learn's `MinMaxScaler`.
3.  **Risk Directionality Adjustment:** The `s_factor_edad_prom_muerte` was inverted (`1 - scaled_value`) to ensure that for every factor, a **higher value corresponds to higher risk**.
4.  **Final Score Calculation:** The normalized factors were grouped into a **G-Score** (average of G-Factors) and an **S-Score** (average of S-Factors). The final `iris_score` was then calculated as a weighted average of these two macro-scores (initially with a 50/50 weighting).

### Sprint Conclusion

Sprint 2 was successfully completed, resulting in the `iris_scores_v1.csv` file. This dataset contains the fully engineered features and the final IRIS score for over 2,000 districts, providing the core engine for the visualization and validation phases to come.