import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import streamlit as st

def run_analysis(df):
    # Load data
    df = df.copy()
    # Category conversions
    df['Disability_Complexity'] = df['Disability_Complexity'].astype('category')
    df['Service_Provider'] = df['Service_Provider'].astype('category')
    df['Service'] = df['Service'].astype('category')
    df['County'] = df['County'].astype('category')
    df['Cost_Type'] = df['Cost_Type'].astype('category')
    df['Cost_Description'] = df['Cost_Description'].astype('category')

    df['Disability_Complexity'] = df['Disability_Complexity'].cat.reorder_categories(['high','medium','low'], ordered=True)

    st.subheader("Data Exploration Plots")  # Add a subheader in Streamlit

    st.write("County vs. Cost_Value by Service:")  # Add text descriptions
    fig_catplot = sns.catplot(data=df, x="County", y="Cost_Value", hue="Service", kind="point", ci=None, height=6, aspect=2).fig # Get the figure
    plt.xticks(rotation=45)
    st.pyplot(fig_catplot)  # Use st.pyplot to display the plot

    st.write("Mean Cost_Value by Service and Disability_Complexity:")
    pivot_table = df.pivot_table(index="Service", columns="Disability_Complexity", values="Cost_Value", aggfunc="mean")
    fig, ax = plt.subplots()
    sns.heatmap(pivot_table, annot=True, cmap="YlGnBu", cbar=False, ax=ax)
    st.pyplot(fig)

    # Complexity mapping
    Complexity_mapping = {'Low':1, 'Medium':2, 'High':3}
    df['Disability_Complexity'] = df['Disability_Complexity'].map(Complexity_mapping).fillna(0)
    df.drop(columns=['Person_ID','Cost_Type'], axis=1, inplace=True)

    # One-hot encoding
    categorical_cols = ['Service','County','Cost_Description','Service_Provider']
    df = pd.get_dummies(df, columns=categorical_cols, dummy_na=False)

    # Clean cost
    df['Cost_Value'] = df['Cost_Value'].astype(str).str.replace(',','').astype(float)
    df = df.apply(pd.to_numeric, errors='coerce')

    df.columns = df.columns.str.replace(' ','_')
    df.columns = df.columns.str.replace('-','_')

    target = 'Cost_Value'
    features = [col for col in df.columns if col != target]
    X = df[features]
    y = df[target]

    # Random Forest for feature importance
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
    model_rf = RandomForestRegressor(n_estimators=200,random_state=42,oob_score=True)
    model_rf.fit(X_train,y_train)
    fi = pd.Series(model_rf.feature_importances_, index=X.columns).sort_values(ascending=True)

    # Plot top feature importances (Streamlit)
    st.subheader("Feature Importance")
    st.write("Top 20 Feature Importances (Random Forest):")
    fig_fi = plt.figure(figsize=(10,6))
    fi[:20].plot(kind='barh')
    plt.title('Random Forest Feature Importance')
    st.pyplot(fig_fi)

    # Select top features
    n_top = 20
    selected_features = fi.head(n_top).index.tolist()
    df_selected = df[selected_features + [target]]

    # GLM with top features
    if (df_selected[target] == 0).any():
        df_selected[target] = df_selected[target].replace(0, 0.0001)
    glm_formula = f"{target} ~ {'+'.join(selected_features)}"
    model_glm_selected = smf.glm(
        formula=glm_formula,
        data=df_selected,
        family=sm.families.Gamma(link=sm.families.links.log())
    ).fit()

    
    
    return model_glm_selected
