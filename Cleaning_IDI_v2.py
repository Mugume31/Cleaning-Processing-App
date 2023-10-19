#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
st.set_option('deprecation.showPyplotGlobalUse', False)

# File upload widget
uploaded_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx", "xls"])

# Check if a file is uploaded
if uploaded_file is not None:
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(uploaded_file, sheet_name="Listing")
        selected_district = st.selectbox('Select District', ['All'] + list(df['District'].unique()))

        # Check if a district is selected
        if selected_district == 'All':
            filtered_df = df  # No specific district selected, use the entire DataFrame
            title_suffix = 'All Districts'
        else:
            # Filter the DataFrame based on the selected district
            filtered_df = df[df['District'] == selected_district]
            title_suffix = selected_district

        # Calculate the percentage of missing values for each column compared to total rows for the selected district
        missing_values_percentage_rows_filtered = (filtered_df.isna().mean() * 100).round(2)

        # Create a DataFrame to store the information for the selected district
        missing_values_df_filtered = pd.DataFrame({
            'Column': missing_values_percentage_rows_filtered.index,
            f'Missing Values Percentage (of total rows) - {title_suffix}': missing_values_percentage_rows_filtered.values,
        })

        # Display the DataFrames
        st.subheader(f'Percentage of Missing Values for Each Column ({title_suffix})')
        st.dataframe(missing_values_df_filtered)

        # Check if a district is selected
        selected_district_1 = st.selectbox('Select District', ['All'] + list(df['District'].unique()))
        if selected_district_1 == 'All':
            filtered_df = df  # No specific district selected, use the entire DataFrame
            title_suffix = 'All Districts'
        else:
            # Filter the DataFrame based on the selected district
            filtered_df = df[df['District'] == selected_district_1]
            title_suffix = selected_district_1

        # Calculate the percentage of total columns with missing values for the selected district
        percentage_columns_with_missing_filtered = (filtered_df.isna().any().sum() / len(filtered_df.columns)) * 100

        # Display the results in Streamlit
        st.subheader(f'Overall Percentage of Columns with Missing Values ({title_suffix})')
        st.markdown(f"**Percentage of Columns with Missing Values:** {percentage_columns_with_missing_filtered:.2f%}")

        st.subheader("Duplicate IDs")

        # Get the counts of each unique value in the "Beneficiary ID" column
        id_counts = df["Beneficiary ID"].value_counts()

        # Filter for IDs with count more than 1
        ids_with_more_than_one_count = id_counts[id_counts > 1].index.tolist()

        # Display the result
        st.write(ids_with_more_than_one_count)

        # Add a tip/explanation
        st.info("Checking for Beneficiary IDs with more than one count helps identify potential duplicate entries.")

        selected_district_2 = st.selectbox('Select District', ['All'] + list(df['District'].unique()), key='district_2')

        # Check if a district is selected
        selected_district_2 = st.selectbox('Select District', ['All'] + list(df['District'].unique()))
        if selected_district_2 == 'All':
            filtered_df = df  # No specific district selected, use the entire DataFrame
        else:
            # Filter the DataFrame based on the selected district
            filtered_df = df[df['District'] == selected_district_2]

        # Filter columns by data type for the filtered DataFrame
        object_columns = filtered_df.select_dtypes(include='object')
        int_columns = filtered_df.select_dtypes(include='int64')

        # Display value counts for object columns in the filtered DataFrame
        for col in object_columns.columns:
            st.subheader(f"Frequency Count for {col} in {selected_district_2}")
            st.write(object_columns[col].value_counts())
            st.write("\n")

        # Display value counts for int64 columns in the filtered DataFrame
        for col in int_columns.columns:
            st.subheader(f"Frequency count for {col} in {selected_district_2}")
            st.write(int_columns[col].value_counts())
            st.write("\n")

        # Add a tip/explanation
        st.info("This analysis helps identify inconsistencies in labels for different columns, such as the same label being repeated twice but with different spellings. Use the filter to select a specific district.")

        selected_district_3 = st.selectbox('Select District', ['All'] + list(df['District'].unique()), key='district_3')

        # Check if a district is selected
        if selected_district_3 == 'All':
            filtered_df = df  # No specific district selected, use the entire DataFrame
            title_suffix = 'All Districts'
        else:
            # Filter the DataFrame based on the selected district
            filtered_df = df[df['District'] == selected_district_3]
            title_suffix = selected_district_3

        # Filter columns by data type for float columns
        float_columns = filtered_df.select_dtypes(include='float64')

        # Create a list to store the figures
        fig_list = []

        # Create a violin plot for each float column
        for col in float_columns.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.violinplot(x=filtered_df[col], ax=ax)
            plt.title(f'Violin Plot for {col} in {title_suffix}')
            plt.xlabel('Value')
            plt.ylabel('Density')
            fig_list.append(fig)  # Append the figure to the list

        # Display the violin plots in Streamlit
        for fig in fig_list:
            st.pyplot(fig)

        # Add a tip/explanation
        st.info("Use the filter to select a specific district and observe how the violin plots change. Violin plots are useful for visualizing the distribution and identifying outliers in the data.")

        filtered_df = df[(df['Age'] >= 0) & (df['Age'] <= 19)]

        df["Antiretroviral Therapy (ART) Initiation"].value_counts()

        filtered_df = df[(df['Age'] >= 0) & (df['Age'] <= 17) & (df["OVC_SERV(1 Yes, 0 No)"] == 1)]

        pivot_1 = filtered_df.pivot_table(index="District", values="Instance", columns="OVC_SERV(1 Yes, 0 No)", aggfunc="count")

        filtered_df_2 = df[(df['Age'] >= 18) & (df["OVC_SERV(1 Yes, 0 No)"] == 1)]

        pivot_2 = filtered_df_2.pivot_table(index="District", values="Instance", columns="OVC_SERV(1 Yes, 0 No)", aggfunc="count")

        filtered_df_3 = df[df['Age'].between(0, 19) & (df["OVC_SERV(1 Yes, 0 No)"] == 1) & (df["Currently Enrolled in School (Y/N)"] == "Yes")]

        pivot_3 = filtered_df_3.pivot_table(
            index="District",
            values="Instance",
            columns="Currently Enrolled in School (Y/N)",
            aggfunc="count"
        )

        merged_pivot = pd.merge(pivot_1, pd.merge(pivot_2, pivot_3, on="District", how="outer", suffixes=('_Below_17', '_Above18')), on="District", how="outer")

        merged_pivot.reset_index(inplace=True)

        merged_pivot = merged_pivot.rename(columns={
            "1_x": 'Below_17',
            '1_y': 'Above_18',
            'Yes': 'Child_Care_Giver'})

        merged_pivot["Total"] = merged_pivot["Below_17"] + merged_pivot["Above_18"]
        mapping_dict = {
            "Arua District": 4497,
            "Madi-Okollo District": 877,
            "Nebbi District": 2367,
            "Pakwach District": 1440,
            "Hoima District": 5369,
            "Kikuube District": 3233,
            "Kiryandongo District": 2369,
            "Kagadi District": 4795,
            "Masindi District": 4893,
            "Kibaale District": 2014,
            "Wakiso District": 27258
        }
        merged_pivot["Target"] = merged_pivot["District"].map(mapping_dict)
        merged_pivot["Achieved"] = merged_pivot["Total"] / merged_pivot["Target"] * 100
        merged_pivot["CGVOR"] = merged_pivot["Child_Care_Giver"] / merged_pivot["Total"] * 100
        totals_row = merged_pivot[['Below_17', 'Above_18', 'Child_Care_Giver', 'Target', 'Total']].sum()
        totals_row["Achieved"] = totals_row['Total'] / totals_row['Target'] * 100
        totals_row['CGVOR'] = totals_row['Child_Care_Giver'] / totals_row['Total'] * 100
        merged_pivot = merged_pivot.append(totals_row, ignore_index=True)

        merged_pivot.at[11, "District"] = "Total"
        merged_pivot_rounded = merged_pivot.round(0)

        merged_pivot_rounded.rename(columns={'Achieved': 'Achieved %', 'CGVOR': 'CGVOR %'})

        def color_format(val):
            if val < 60:
                return 'background-color: red'
            elif val < 90:
                return 'background-color: yellow'
            else:
                return 'background-color: green'

        # Identify numeric columns
        numeric_columns = merged_pivot.select_dtypes(include='number').columns

        # Define columns to apply coloring
        columns_to_color = ["Achieved", "CGVOR"]

        # Combine styling for color and no decimal formatting
        styled_df_combined = (
            merged_pivot.style
            .applymap(color_format, subset=columns_to_color)
            .format({col: "{:.0f}" for col in numeric_columns})
        )

        st.title("OVC Serve Comprehensive")
        st.dataframe(styled_df_combined)

        pivot_table_df = df.pivot_table(index="District", columns=["Exited With Graduation"], values="Instance", aggfunc="count", fill_value=0)
        st.title("Exited With Graduation")
        st.dataframe(pivot_table_df)

        result_df = df.groupby("Risk Factor")["Exited With Graduation"].count().reset_index(name="Total")

        st.title("Risk Factor")
        st.dataframe(result_df)

        pivot5 = pd.merge(pivot_2, pivot_1, on="District", how="outer", suffixes=('_Below_17', '_Above18'))

        filtered_df_Hiv = df[(df['Age'] >= 0) & (df['Age'] <= 17) & (df["OVC_HIV STAT (1 Yes, 0 No, )"] == 1)]

        Pivot6 = filtered_df_Hiv.pivot_table(index="District", values="Instance", columns="OVC_HIV STAT (1 Yes, 0 No, )", aggfunc="count")

        Pivot7 = df[df["Risk Factor"] == "CLHIV"].groupby("District")["Risk Factor"].count()

        Pivot8 = df[df["Risk Factor"] == "CLHIV"].groupby(["District", "On_ART_HVAT (1 Yes, 0 No)"]).size().unstack().reset_index().fillna(0)

        df_infants = df[(df["Risk Factor"] == "HEI") & (df["PCR Test"] == 4)]

        Pivot9 = df_infants.groupby("District")["Risk Factor"].value_counts().unstack().reset_index().fillna(0)

        Pivot10 = df_infants.groupby("District")["PCR Test"].value_counts().unstack().reset_index().fillna(0)

        # Merge pivot_2 and pivot_1
        merged_df1 = pd.merge(pivot_2, pivot_1, on="District", how="outer", suffixes=('_Below_17', '_Above18'))

        # Merge with pivot5
        merged_df2 = pd.merge(merged_df1, pivot5, on="District", how="outer")

        # Merge with Pivot6
        merged_df3 = pd.merge(merged_df2, Pivot6, on="District", how="outer", suffixes=('', '_Pivot6'))

        # Merge with Pivot7
        merged_df4 = pd.merge(merged_df3, Pivot7, on="District", how="outer", suffixes=('', '_Pivot7'))

        # Merge with Pivot8
        merged_df5 = pd.merge(merged_df4, Pivot8, on="District", how="outer", suffixes=('', '_Pivot8'))

        # Merge with Pivot9
        merged_df6 = pd.merge(merged_df5, Pivot9, on="District", how="outer", suffixes=('', '_Pivot9'))

        # Merge with Pivot10
        final_merged_df = pd.merge(merged_df6, Pivot10, on="District", how="outer", suffixes=('', '_Pivot10'))

        Cascade_Ending_Epidemic = final_merged_df

        columns_to_exclude = ['1_Below_17_x', '1_Above18_x']

        Cascade_Ending_Epidemic = Cascade_Ending_Epidemic.drop(columns=columns_to_exclude)

        Cascade_Ending_Epidemic.rename(columns={
            '1_Below_17_y': 'Ovc_Serv_17',
            '1_Above18_y': 'Ovc_Serv_18+',
            1: 'Hiv_Stat',
            'Risk Factor': 'CLHIV',
            'No': 'Currently_Not_Receving_Art',
            'Yes': 'Currently_Receving_Art',
            'HEI': 'Number_of_exposed_infants(0-24)',
            4.0: 'Number_of_exposed_infants(0-24)_with_Test'}, inplace=True)
        Cascade_Ending_Epidemic = Cascade_Ending_Epidemic.fillna(0)

        st.title("OVC Program Cascade to Ending the Epidemic (0-17 years)")
        st.dataframe(Cascade_Ending_Epidemic)

        df["Exited With Graduation"].unique()

        df['Enrollment Date'] = pd.to_datetime(df['Enrollment Date'], errors='coerce')

        # Extract the year from "Enrollment Date"
        df['Enrollment Year'] = df['Enrollment Date'].dt.year

        enrolement_year_comp = df.pivot_table(index="Enrollment Year", values="Instance", columns="Exited With Graduation", aggfunc="count", fill_value=0)

        st.subheader('Exited With Graduation Over Enrollment Years')
        enrolement_year_comp.plot(kind='bar', stacked=False, figsize=(20, 15))
        plt.title('Exited With Graduation Over Enrollment Years')
        plt.xlabel('Enrollment Year')
        plt.ylabel('Count')
        plt.legend(title='Exited With Graduation', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()
        st.pyplot()

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.sidebar.info("Please upload an Excel file.")
