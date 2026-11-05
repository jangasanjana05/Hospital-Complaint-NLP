
import streamlit as st
import pandas as pd
from datetime import datetime
import backend

st.set_page_config(
    page_title="Hospital Complaint Management",
    page_icon="🏥",
    layout="wide"
)

# Professional styling
st.markdown("""
<style>
.stApp {
    background-color: #f5f8fc;
}
[data-testid="stSidebar"] {
    background-color: #e8eef7;
}
.main-title {
    color: #17365d;
    font-size: 34px;
    font-weight: bold;
}
.subtitle {
    color: #52657a;
    font-size: 17px;
}
div.stButton > button {
    border-radius: 8px;
    font-weight: bold;
    min-height: 42px;
}
</style>
""", unsafe_allow_html=True)

# Session history
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar
st.sidebar.title("🏥 Complaint System")
st.sidebar.caption("NLP-Based Complaint Management")

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

    st.markdown(
        '<div class="main-title">🏥 Hospital Complaint Management</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">Complaint Category and Priority Prediction Using NLP</div>',
        unsafe_allow_html=True
    )

    st.write("")
    st.info(
        "Welcome! This application uses Natural Language Processing "
        "to identify complaint categories and predict their priority."
    )

    data = backend.get_dashboard_data()

    col1, col2, col3 = st.columns(3)

    col1.metric("Dataset Records", len(data))
    col2.metric("Complaint Categories", data["category"].nunique())
    col3.metric("Priority Levels", data["priority"].nunique())

    st.subheader("Application Features")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### 📝 Complaint Prediction")
        st.write("Predict complaint category and priority.")

        st.markdown("### 📋 Complaint History")
        st.write("View complaints submitted during this session.")

    with c2:
        st.markdown("### 📊 Dashboard")
        st.write("View category and priority statistics.")

        st.markdown("### ℹ️ About Project")
        st.write("Learn about the project and technologies.")

# COMPLAINT PREDICTION
elif page == "Complaint Prediction":

    st.title("📝 Complaint Prediction")
    st.caption(
        "Enter a complaint below to predict its category and priority."
    )

    # Clear input before creating the text area
    if st.button("🧹 Clear Complaint"):
        st.session_state.complaint_input = ""
        st.rerun()

    complaint = st.text_area(
        "Enter Hospital Complaint",
        placeholder="Example: I waited for two hours but the doctor did not attend me.",
        height=150,
        key="complaint_input"
    )

    if st.button("🔍 Predict Complaint", type="primary"):

        if complaint.strip():

            try:
                category, priority = backend.predict_complaint(
                    complaint
                )

                st.success("Prediction completed successfully!")

                st.subheader("Prediction Results")

                col1, col2 = st.columns(2)

                with col1:
                    with st.container(border=True):
                        st.markdown("### 🏷️ Complaint Category")
                        st.subheader(category)

                with col2:
                    with st.container(border=True):
                        st.markdown("### 🚦 Predicted Priority")

                        if priority == "High":
                            st.error("🔴 HIGH PRIORITY")
                        elif priority == "Medium":
                            st.warning("🟠 MEDIUM PRIORITY")
                        else:
                            st.success("🟢 LOW PRIORITY")

                st.session_state.history.append({
                    "Complaint": complaint,
                    "Category": category,
                    "Priority": priority,
                    "Date and Time": datetime.now().strftime(
                        "%d-%m-%Y %H:%M:%S"
                    )
                })

                st.info(
                    "Please review this prediction before taking action."
                )

            except Exception as e:
                st.error(f"Prediction error: {e}")

        else:
            st.warning("Please enter a complaint first.")

    st.divider()
    st.caption(
        "Disclaimer: Predictions are AI-generated suggestions. "
        "They are not a substitute for professional judgment "
        "or emergency medical assessment."
    )

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
            "⬇️ Download Complaint History",
            data=csv,
            file_name="complaint_history.csv",
            mime="text/csv"
        )

        if st.button("🗑️ Clear History"):
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
        st.bar_chart(backend.get_category_counts())

    with col2:
        st.subheader("Complaints by Priority")
        st.bar_chart(backend.get_priority_counts())

    st.subheader("Dataset Overview")
    st.dataframe(
        data.head(20),
        use_container_width=True,
        hide_index=True
    )

# ABOUT PROJECT
elif page == "About Project":

    st.title("ℹ️ About Project")

    st.subheader(
        "Hospital Complaint Classification and Priority Prediction Using NLP"
    )

    st.write("""
    **Objective**

    To classify hospital complaints into different categories
    and predict their priority using Natural Language Processing.

    **Technologies Used**
    - Python
    - Streamlit
    - Pandas
    - Scikit-learn
    - TF-IDF
    - Multinomial Naive Bayes

    **Machine Learning Tasks**
    1. Complaint Category Classification
    2. Complaint Priority Prediction

    **Complaint Categories**
    - Billing
    - Doctor Service
    - Hospital Management
    - Nursing Service
    - Pharmacy
    - Waiting Time

    **Priority Levels**
    - High
    - Medium
    - Low
    """)

    st.warning(
        "The predictions are model-generated suggestions. "
        "Hospital staff should review them before taking action."
    )
