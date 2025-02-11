import pandas as pd
import numpy as np
import plotly.express as px
import os
import streamlit as st

st.sidebar.header("Filter Options")

def main(df):
    # Define a helper function: if the user selects nothing then use all unique values.
    def get_filter_values(label, series, default_all=True):
        all_vals = sorted(series.dropna().unique())  # sorting for easier UX
        selection = st.sidebar.multiselect(label, options=all_vals, 
                                           default=all_vals if default_all else [])
        # If empty, use the full set.
        return selection if selection else all_vals

    # Required filters (filtering on Service, Person_ID, County, Disability_Complexity)
    service_filter = get_filter_values("Service", df['Service'])
    # Although Person_ID is mentioned for filtering (to ensure unique people later),
    # typically we do not filter on Person_ID. For completeness, if you wish to include it:

    county_filter = get_filter_values("County", df['County'])
    Complexity_filter = get_filter_values("Disability Complexity", df['Disability_Complexity'])

    # Optional filter for Service Provider. (If nothing is selected, do not filter on it.)
    provider_filter = st.sidebar.multiselect("Service Provider (Optional)", 
                                             options=sorted(df['Service_Provider'].dropna().unique()))
    # Additional Boxplot filters (also on the sidebar)
    cost_type_filter = get_filter_values("Cost Type for Boxplot", df['Cost_Type'])
    cost_description_filter = get_filter_values("Cost Description for Boxplot", df['Cost_Description'])

    # Filter the dataframe ------------------------------------------------------
    # First filter by the four main fields:
    filtered_df = df[
        df['Service'].isin(service_filter) &
        df['County'].isin(county_filter) &
        df['Disability_Complexity'].isin(Complexity_filter)
    ]

    # Now, if a Service Provider selection has been made, further filter.
    if provider_filter:
        filtered_df = filtered_df[filtered_df['Service_Provider'].isin(provider_filter)]

    # Display message if no records after filtering.
    if filtered_df.empty:
        st.write("No data matches the selected filters.")
    else:
        # Aggregations are computed only after filtering -----------------------
        # If the Service Provider filter was used, include that in the grouping.
        # Otherwise, group by only Service, County, and Disability Complexity.
        grouping_columns = ['Service', 'County', 'Disability_Complexity']
        if provider_filter:
            grouping_columns.append('Service_Provider')
        
        grouped_df = filtered_df.groupby(grouping_columns).agg(
            Total_Cost=('Cost_Value', 'sum'),
            Number_of_People=('Person_ID', 'nunique')
        ).reset_index()

        # Calculate Average Cost
        grouped_df['Average_Cost'] = round(grouped_df['Total_Cost'] / grouped_df['Number_of_People'],0)

        # Compute overall 75th and 25th quantiles based on individual costs
        individual_costs = filtered_df.groupby('Person_ID')['Cost_Value'].sum()
        q75 = individual_costs.quantile(0.75)
        q25 = individual_costs.quantile(0.25)
        grouped_df['Cost_75th_Percentile'] = round(q75,0)
        grouped_df['Cost_25th_Percentile'] = round(q25,0)

        st.subheader("Aggregated Data")
        st.dataframe(grouped_df)

        # Download button for aggregated data
        csv = grouped_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Aggregated Data as CSV",
            data=csv,
            file_name='aggregated_data.csv',
            mime='text/csv'
        )

        # Comparative Bar Chart -----------------------------------------------
        if provider_filter:
            # When Service Provider is part of the grouping/color breakdown.
            fig_bar = px.bar(grouped_df, x="Service", y="Total_Cost", 
                     color="County", barmode="group",
                     title="Total Cost by Service and County")
        else:
            fig_bar = px.bar(grouped_df, x="Service", y="Total_Cost",
                     color="County", barmode="group",
                     title="Total Cost by Service and County")

        st.plotly_chart(fig_bar)
        
        # Comparative Bar Chart average -----------------------------------------------
        if provider_filter:
            # When Service Provider is part of the grouping/color breakdown.
            fig_bar = px.bar(grouped_df, x="Service", y="Average_Cost", 
                     color="County", barmode="group",
                     title="Average_Cost by Service and County")
        else:
            fig_bar = px.bar(grouped_df, x="Service", y="Average_Cost",
                     color="County", barmode="group",
                     title="Average_Cost Service and County")

        st.plotly_chart(fig_bar)

        # Boxplot of Cost Distribution -----------------------------------------
        # Further filter filtered_df using cost type and cost description criteria
        boxplot_df = filtered_df[
            filtered_df['Cost_Type'].isin(cost_type_filter) &
            filtered_df['Cost_Description'].isin(cost_description_filter)
        ]

        # It is possible that after this filtering there are no records
        if boxplot_df.empty:
            st.write("No data available for the selected Cost Type and Cost Description filters.")
        else:
            fig_box = px.box(boxplot_df, x="Cost_Type", y="Cost_Value", 
                             color="Cost_Description",
                             title="Cost Distribution by Type and Description")
            st.plotly_chart(fig_box)

