import streamlit as st
import pandas as pd
from io import BytesIO

# Load the Excel data
@st.cache_data
def load_data():
    return pd.read_excel("V6Master.xlsx")

df = load_data()

st.title("Trait Feedback Generator")

# Let user select state for each trait
selections = {}
states = ["Active", "Balanced", "Inactive"]

st.header("Select Trait States")
for trait in df["Name"]:
    selections[trait] = st.selectbox(f"{trait}", states, key=trait)

# Generate result based on selection
results = []
for trait, state in selections.items():
    row = df[df["Name"] == trait].iloc[0]
    feedback = row[state]
    risk = row[f"{state} Risk"] if f"{state} Risk" in row else ""
    results.append({
        "Trait": trait,
        "State": state,
        "Feedback": feedback,
        "Risk": risk
    })

result_df = pd.DataFrame(results)

st.subheader("Generated Feedback")
st.dataframe(result_df)

# Download button
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    return processed_data

excel_data = to_excel(result_df)
st.download_button(label="📥 Download Feedback as Excel", data=excel_data,
                   file_name="trait_feedback_output.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
