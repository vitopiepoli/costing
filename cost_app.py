import pandas as pd
import streamlit as st
from cost import template_cost, simulate_service_costs
from cost_viz import main
from analysis import run_analysis
import numpy as np

# Streamlit app
st.title("Disability Care Cost Data - POC")

# Create tabs
tabs = ["Description", "Residential Care Costs", "Database", "Visualisation", "Analysis"]
selected_tab = st.tabs(tabs)

# Content for the first tab ("App Description")
with selected_tab[0]:
    st.write("""
    ## Welcome to the Residential Care Cost Data App

    This application provides detailed information and analysis on the costs associated with residential care. 
    You can navigate through the tabs to explore different aspects of the data.

    - **Residential Care Costs**: displays a template for capturing cost information, including details like service type, person ID, county, disability severity, cost type, description, and value.
    - **Database**: will aggregate the data entered using the template.
    - **Visualisation**: will provide visual representations of the collected data, such as charts and graphs
    - **Analysis**: tools and insights for analyzing the cost data, potentially including trend analysis or comparisons between different cost categories.
    """)

# Content for the second tab ("Residential Care Costs")
with selected_tab[1]:  # Use the second tab object
    template_df = template_cost()
    st.dataframe(template_df.style.format({"Cost_Value": "{:.2f}"})) # Format Cost_Value
    # Alternatively, display as a table with formatting
    # st.write(template_df.to_html(index=False, formatters={"Cost_Value": "{:.2f}".format}), unsafe_allow_html=True)

# Content for the third tab ("Database")
with selected_tab[2]:
    st.write("Database")
    collated_df = simulate_service_costs()
    # instantiate collated_df within session state
    st.session_state.collated_df = collated_df
    st.dataframe(st.session_state.collated_df.head(100).style.format({"Cost_Value": "{:.2f}"})) # Format Cost_Value

# Content for the fourth tab ("Visualisation")
with selected_tab[3]:
    st.write("Data visualisation")     
    main(st.session_state.collated_df)

# Content for the fifth tab ("Analysis")
with selected_tab[4]:
    st.write("Analysis")
    if st.button("Run Analysis"):
        model_glm = run_analysis(st.session_state.collated_df)
    # GLM Results (Streamlit)
        if model_glm:
            st.subheader("GLM Results")
            st.write("GLM Summary:")
            st.write(model_glm.summary()) 

            st.write("Exponentiated Coefficients:")
            exponentiated_coeffs = np.exp(model_glm.params)
            st.write(exponentiated_coeffs) 