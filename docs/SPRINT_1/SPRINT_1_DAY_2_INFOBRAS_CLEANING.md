# Data Cleaning Implementation Report - INFOBRAS Dataset

*   **Project:** IRIS (Sprint 1, Day 2)
*   **Date:** Tuesday
*   **Lead Engineer:** Jhon Wilber Ajata Ascarrunz
*   **Objective:** To design and build a Python data cleaning function that takes the raw INFOBRAS CSV as input and returns a clean DataFrame, resolving all issues identified in the Day 1 analysis.

---

### 1. Executive Summary

Following the diagnosis from Day 1, the data cleaning implementation phase was initiated. A robust cleaning pipeline, encapsulated in the function `clean_infobras_data`, was successfully developed. This function executes a logical sequence of steps to standardize, repair, transform, and validate the data, converting the raw, unusable dataset into a structured and reliable data asset.

During the process, technical challenges were overcome, and crucial insights into the data's semantics were discovered. This led to a refined cleaning strategy and the proactive creation of a specific dataset for modeling (`infobras_modeling_v1.csv`). The day's deliverable—a reproducible cleaning function and a clean dataset—has been fully completed.

---

### 2. Cleaning Pipeline Design & Architecture

To ensure reproducibility and professional standards, all cleaning logic was encapsulated within a single function, `clean_infobras_data(df_raw)`. This function follows a sequential and well-documented workflow, transforming the DataFrame step-by-step.

**Design Principles:**
*   **Immutability:** The function operates on a copy of the original DataFrame (`df_raw.copy()`) to prevent unexpected side effects.
*   **Modularity:** Each cleaning step is logically separated and commented within the function, facilitating easy maintenance and debugging.
*   **Robustness:** `errors='coerce'` was used during type conversions to handle unexpected data without interrupting the process, converting invalid values into nulls (`NaN`/`NaT`) for subsequent handling.
*   **Best Practices:** Future-proof syntax was adopted (avoiding `inplace=True`) to ensure compatibility with upcoming versions of the Pandas library, thereby addressing `FutureWarning` messages encountered during development.

---

### 3. Pipeline Implementation Steps

The `clean_infobras_data` function performs the following operations in order:

**3.1. Column Name Standardization:**
*   **Action:** String transformations were applied to convert all 113 column names to `snake_case` format (lowercase, with underscores instead of spaces, and no special characters).
*   **Result:** Consistent and easily manipulated column names (e.g., `df.costo_de_la_obra_en_soles`).

**3.2. Structural Repair (Renaming Duplicates):**
*   **Action:** A renaming dictionary was used to assign descriptive and unique names to duplicated columns (e.g., `ruc.1` became `ruc_supervisor`).
*   **Result:** Structural ambiguity was eliminated, clarifying the distinction between contractor, supervisor, and resident engineer data.

**3.3. Removal of Non-Informative Columns:**
*   **Action:** 6 columns identified as useless due to having over 99.9% null values (e.g., `Fecha de aprobación`, `Otra Marca`) were dropped.
*   **Result:** Reduced noise and dimensionality, focusing the dataset on relevant information.

**3.4. Data Type Transformation ("Decontamination"):**
*   **Action:**
    *   16 date columns were successfully converted from `object` to `datetime64[ns]`, specifying `dayfirst=True` to correctly handle the `DD/MM/YYYY` format.
    *   18 numeric columns were converted from `object` to `float64` after programmatically stripping non-numeric characters ("S/.", ",", "%").
*   **Result:** The data now has the correct types, enabling mathematical and time-series operations essential for the feature engineering phase.

**3.5. Strategic Handling of Null Values:**
*   **Action:**
    *   Logical imputation was applied, such as filling `NaN` in `causal_de_paralizacion` with the string 'No Paralizada'.
    *   Nulls in key categorical geographic columns were filled with 'Desconocido'.
    *   Nulls in key financial amount columns were filled with `0`.
*   **Result:** The most critical data gaps were addressed, preparing the dataset for more comprehensive analysis.

---

### 4. Key Discovery and Creation of Modeling Dataset

During the validation of the cleaning process, an attempt to create a subset for analysis led to a **critical insight**: the initial assumption that finished projects had the status `'Concluida'` was incorrect. "Data detective work" proved that the correct status was `'Finalizado'`.

*   **Action:** The strategy was pivoted to create a `modeling_df` by filtering for `estado_de_ejecucion == 'Finalizado'` and `costo_de_la_obra_en_soles > 0`.
*   **Result:** A high-value secondary dataset, `infobras_modeling_v1.csv`, was generated. It contains 6,336 high-quality, reliable observations and was further enriched with initial feature engineering (calculating cost overrun and time delay ratios). This outcome effectively fast-tracked part of the work planned for Sprint 2.

---

### 5. Conclusion & Deliverables

The Day 2 mission has been successfully completed. A raw, problematic dataset has been transformed into a clean, structured data asset. The developed cleaning pipeline is robust, reusable, and represents the primary engineering artifact of this project phase.

**Day's Deliverables (COMPLETED):**
1.  **A function within the main notebook (`clean_infobras_data`)** that takes the raw works CSV and returns a clean DataFrame.
2.  **The file `infobras_clean_v1.csv`**, representing the general-purpose clean dataset.
3.  **The file `infobras_modeling_v1.csv`**, a high-value byproduct that will serve as the basis for modeling in subsequent sprints.