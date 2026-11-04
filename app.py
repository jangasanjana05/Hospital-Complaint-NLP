
import streamlit as st
import pandas as pd
from datetime import datetime
import backend

st.set_page_config(
    page_title="Hospital Complaint Management",
    page_icon="🏥",
    layout="wide"
)

# Session history
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar navigation
st.sidebar.title("🏥 Complaint System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Complaint Prediction",
        "Complaint History",
        "Dashboard",
        "About Project"
    ]
)

# HOME PAGE
if page == "Home":

    st.title("🏥 Hospital Complaint Classification")
    st.subheader(
        "Complaint Category and Priority Prediction Using NLP"
    )

    st.write(
        "This application uses Natural Language Processing "
        "to classify hospital complaints and predict their priority."
    )

    st.info(
        "Submit a complaint to identify its category and priority."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Dataset Records", len(backend.get_dashboard_data()))

    with col2:
        st.metric(
            "Complaint Categories",
            backend.get_dashboard_data()["category"].nunique()
        )

    with col3:
        st.metric(
            "Priority Levels",
            backend.get_dashboard_data()["priority"].nunique()
        )

# COMPLAINT PREDICTION
elif page == "Complaint Prediction":

    st.title("📝 Complaint Prediction")

    complaint = st.text_area(
        "Enter Hospital Complaint",
        placeholder="Type your complaint here...",
        height=150
    )

    if st.button("Predict Complaint", type="primary"):

        if complaint.strip():

            try:
                category, priority = backend.predict_complaint(
                    complaint
                )

                st.success("Prediction Completed!")

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Complaint Category")
                    st.info(category)

                with col2:
                    st.subheader("Predicted Priority")
                    if priority == "High":
                        st.error(priority)
                    elif priority == "Medium":
                        st.warning(priority)
                    else:
                        st.success(priority)

                st.session_state.history.append({
                    "Complaint": complaint,
                    "Category": category,
                    "Priority": priority,
                    "Date and Time": datetime.now().strftime(
                        "%d-%m-%Y %H:%M:%S"
                    )
                })

            except Exception as e:
                st.error(f"Prediction error: {e}")

        else:
            st.warning("Please enter a complaint.")

# COMPLAINT HISTORY
elif page == "Complaint History":

    st.title("📋 Complaint History")

    if st.session_state.history:

        history_df = pd.DataFrame(st.session_state.history)

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        csv = history_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Complaint History",
            data=csv,
            file_name="complaint_history.csv",
            mime="text/csv"
        )

        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()

    else:
        st.info("No complaints submitted in this session yet.")

# DASHBOARD
elif page == "Dashboard":

    st.title("📊 Complaint Dashboard")

    data = backend.get_dashboard_data()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Complaints by Category")
        category_counts = backend.get_category_counts()
        st.bar_chart(category_counts)

    with col2:
        st.subheader("Complaints by Priority")
        priority_counts = backend.get_priority_counts()
        st.bar_chart(priority_counts)

    st.subheader("Dataset Overview")
    st.dataframe(data.head(20), use_container_width=True)

# ABOUT PROJECT
elif page == "About Project":

    st.title("ℹ️ About Project")

    st.write("""
    **Project Title:**
    Hospital Complaint Classification and Priority Prediction Using NLP

    **Objective:**
    To automatically classify hospital complaints and predict
    their priority using Natural Language Processing.

    **Technologies Used:**
    - Python
    - Streamlit
    - Pandas
    - Scikit-learn
    - TF-IDF
    - Multinomial Naive Bayes

    **Machine Learning Tasks:**
    1. Complaint Category Classification
    2. Complaint Priority Prediction

    **Priority Levels:**
    - High
    - Medium
    - Low
    """)

    st.warning(
        "Predictions are model-generated suggestions and should "
        "be reviewed by hospital staff. They are not a substitute "
        "for emergency assessment or professional judgment."
    )
