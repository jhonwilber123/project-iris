# Sprint 3 Report: "The Visualization" (Dashboard MVP)

*   **Project:** IRIS (Sprint 3)
*   **Sprint Objective:** To build and deploy a functional, interactive web application (MVP) using Streamlit to visualize the results of the IRIS Index.

---

### Executive Summary

This sprint marked the project's transition from data analysis to tangible data product development. A functional web application was successfully developed using Streamlit and PyDeck, presenting the Project IRIS results in an intuitive and interactive manner.

The development process faced and overcame a series of complex technical challenges, including library dependency issues, map rendering bugs, and the need for advanced debugging logic. The final result is a polished, multilingual dashboard featuring an interactive risk map, dynamic filters, and a detailed "District Profile" for in-depth analysis.

Finally, the application was **successfully deployed to Streamlit Cloud**, meeting and exceeding all sprint objectives.

### Milestones and Features Implemented

1.  **Environment Setup & App Structure:**
    *   Required dependencies (`streamlit`, `pydeck`, `shapely`) were installed and managed via `requirements.txt`.
    *   The `app/app.py` file structure was created to house the application code.

2.  **Interactive Risk Map:**
    *   **Challenge:** The initial library choice (`plotly.express.choropleth_mapbox`) failed to render the data despite correct data join keys.
    *   **Solution:** Pivoted to a more robust solution using **PyDeck**, Streamlit's native geospatial visualization library. A scatterplot map was implemented where the color of each point represents the district's risk score.

3.  **Interactivity and User Controls:**
    *   **Language Selector:** A sidebar menu was implemented to dynamically switch the entire UI language between Spanish and English.
    *   **Dynamic Filters:** Sidebar filters were added, allowing users to narrow down the data displayed on the map by Department and `iris_score` range.

4.  **"District Profile" for In-Depth Analysis:**
    *   A detailed analysis section with a selector for specific districts was added.
    *   Information is presented in a clean **tabbed layout** (`st.tabs`) for a better user experience, featuring:
        *   A **gauge chart** for an instant view of the risk level.
        *   A **radar chart** breaking down the individual sub-factors.
        *   A **comparison view** to benchmark a district against the national average or another district.

5.  **Cloud Deployment:**
    *   **Challenge:** The app initially failed on Streamlit Cloud due to missing OS-level dependencies for the `shapely` library.
    *   **Solution:** A `packages.txt` file was created to instruct Streamlit Cloud to install the `libgeos-dev` dependency, resolving the `ModuleNotFoundError`.
    *   **Result:** The application was successfully deployed and is now publicly accessible.

### Sprint Conclusion

Sprint 3 has been successfully completed, resulting in an MVP that is not only functional but also polished and feature-rich. The project has evolved from a set of analyses into an interactive and demonstrable data product.