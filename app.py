import streamlit as st
from backend import predict_complaint

st.set_page_config(
    page_title="Hospital Complaint Prediction",
    page_icon="🏥"
)

st.title("🏥 Hospital Complaint Classification")
st.write("SRI CHAKRA SUPER SPECIALITY HOSPITAL")
st.subheader("Complaint Category and Priority Prediction Using NLP")

complaint = st.text_area(
    "Enter Hospital Complaint",
    placeholder="Type your hospital complaint here..."
)

if st.button("Predict Complaint"):
    if complaint.strip():
        category, priority = predict_complaint(complaint)

        st.success("Prediction Completed!")

        st.write("### Complaint Category")
        st.info(category)

        st.write("### Complaint Priority")
        st.warning(priority)
    else:
        st.error("Please enter a complaint.")
