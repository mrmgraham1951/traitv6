import streamlit as st
import pandas as pd

# Load the Excel file
df = pd.read_excel("V6Master.xlsx")

st.title("Trait Feedback Tool v6")

# Initialize session state for selections
if "selections" not in st.session_state:
    st.session_state.selections = {}

# Create form for user selections
with st.form("trait_form"):
    st.subheader("Select State for Each Trait")
    for trait in df['Name']:
        selection = st.radio(
            label=f"{trait}",
            options=["Active", "Balanced", "Inactive"],
            key=trait
        )
        st.session_state.selections[trait] = selection
    submitted = st.form_submit_button("Generate Feedback")

# Display results if form was submitted
if submitted:
    st.subheader("Feedback Summary")
    results = []
    for trait in df['Name']:
        state = st.session_state.selections[trait]
        row = df[df['Name'] == trait].iloc[0]
        description = row[state]
        risk = row.get(f"{state} Risk", "")
        results.append({
            "Trait": trait,
            "State": state,
            "Feedback": description,
            "Risk": risk if pd.notna(risk) else ""
        })

    result_df = pd.DataFrame(results)
    st.dataframe(result_df)

    # Download option
    st.download_button(
        label="Download Feedback as Excel",
        data=result_df.to_excel(index=False, engine="openpyxl"),
        file_name="trait_feedback_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
