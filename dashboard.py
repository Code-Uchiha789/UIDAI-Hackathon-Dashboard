from streamlit_pdf_viewer import pdf_viewer
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Aadhaar Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------
# CUSTOM CSS
# --------------------------

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

div[data-testid="metric-container"]{
    background-color:#1e293b;
    border:1px solid #334155;
    padding:15px;
    border-radius:15px;
}

h1,h2,h3 {
    color:white;
}

</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():

    enroll = pd.read_csv(
        "downloaded_Enrollment_Combined_data.csv"
    )

    demo = pd.read_csv(
        "downloaded_Demo_Combined_data.csv"
    )

    bio = pd.read_csv(
        "downloaded_Biometric_Combined_data.csv"
    )

    return enroll, demo, bio


enroll_df, demo_df, bio_df = load_data()

st.sidebar.title("🏛 Aadhaar Analytics")

category = st.sidebar.selectbox(
    "Select Category",
    [
        "Enrollment",
        "Demographic Update",
        "Biometric Update"
    ]
)

if category == "Enrollment":

    df = enroll_df
    value_col = "total_enrollement"

elif category == "Demographic Update":

    df = demo_df
    value_col = "total_demo"

else:

    df = bio_df
    value_col = "total_biometric"



dashboard_tab, report_tab = st.tabs(
    ["📊 Dashboard", "📄 Project Report"]
)


with dashboard_tab:

    st.title(
        "📊 Aadhaar Enrollment & Update Dashboard"
    )

    st.subheader("🗺 India Heatmap")
    
    if category == "Enrollment":
        st.image(
            "heatmap_enrollment.svg",
            use_container_width=True
        )
    
    elif category == "Demographic Update":
        st.image(
            "heatmap_demo.svg",
            use_container_width=True
        )
    
    else:
        st.image(
            "heatmap_biometric.svg",
            use_container_width=True
        )
    
    st.markdown("---")
    
    if category == "Enrollment":
        df = enroll_df
        value_col = "total_enrollement"
    
    elif category == "Demographic Update":
        df = demo_df
        value_col = "total_demo"
    
    else:
        df = bio_df
        value_col = "total_biometric"
    
    st.subheader(
        f"Average {category} Across States"
    )
    
    state_analysis = (
        df.groupby("state")[value_col]
        .mean()
        .reset_index()
    )
    
    state_analysis = state_analysis.sort_values(
        value_col,
        ascending=False
    )
    
    fig = px.bar(
        state_analysis,
        x="state",
        y=value_col,
        color=value_col,
        template="plotly_dark",
        title=f"Average {category} per State"
    )
    
    fig.update_layout(
        xaxis_title="State",
        yaxis_title=f"Average {category}",
        height=600,
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(
        fig,
        use_container_width=True
    )
    
    st.markdown("---")
    st.subheader("👥 Age-wise Analysis")
    
    if category == "Enrollment":
    
        col1, col2, col3 = st.columns(3)
    
        # Age 0-5
        age_0_5 = (
            df.groupby("state")["age_0_5"]
            .agg(["sum", "count"])
        )
    
        age_0_5["avg"] = age_0_5["sum"] / age_0_5["count"]
    
        age_0_5 = (
            age_0_5["avg"]
            .sort_values(ascending=False)
            .reset_index()
        )
    
        # Age 5-17
        age_5_17 = (
            df.groupby("state")["age_5_17"]
            .agg(["sum", "count"])
        )
    
        age_5_17["avg"] = age_5_17["sum"] / age_5_17["count"]
    
        age_5_17 = (
            age_5_17["avg"]
            .sort_values(ascending=False)
            .reset_index()
        )
    
        # Age 18+
        age_18 = (
            df.groupby("state")["age_18_greater"]
            .agg(["sum", "count"])
        )
    
        age_18["avg"] = age_18["sum"] / age_18["count"]
    
        age_18 = (
            age_18["avg"]
            .sort_values(ascending=False)
            .reset_index()
        )
    
        with col1:
    
            fig1 = px.bar(
                age_0_5,
                x="state",
                y="avg",
                color="avg",
                title="Average People (Age 0-5)",
                template="plotly_dark"
            )
    
            fig1.update_layout(
                height=500,
                xaxis_tickangle=-60,
                yaxis_title="Average People"
            )
    
            st.plotly_chart(
                fig1,
                use_container_width=True
            )
    
        with col2:
    
            fig2 = px.bar(
                age_5_17,
                x="state",
                y="avg",
                color="avg",
                title="Average People (Age 5-17)",
                template="plotly_dark"
            )
    
            fig2.update_layout(
                height=500,
                xaxis_tickangle=-60,
                yaxis_title="Average People"
            )
    
            st.plotly_chart(
                fig2,
                use_container_width=True
            )
    
        with col3:
    
            fig3 = px.bar(
                age_18,
                x="state",
                y="avg",
                color="avg",
                title="Average People (Age 18+)",
                template="plotly_dark"
            )
    
            fig3.update_layout(
                height=500,
                xaxis_tickangle=-60,
                yaxis_title="Average People"
            )
    
            st.plotly_chart(
                fig3,
                use_container_width=True
            )
            
    elif category == "Demographic Update":
    
        col1, col2 = st.columns(2)
    
        demo_5_17 = (
            df.groupby("state")["demo_age_5_17"]
            .agg(["sum","count"])
        )
    
        demo_5_17["avg"] = (
            demo_5_17["sum"] /
            demo_5_17["count"]
        )
    
        demo_5_17 = (
            demo_5_17["avg"]
            .sort_values(ascending=False)
            .reset_index()
        )
    
        demo_18 = (
            df.groupby("state")["demo_age_17_"]
            .agg(["sum","count"])
        )
    
        demo_18["avg"] = (
            demo_18["sum"] /
            demo_18["count"]
        )
    
        demo_18 = (
            demo_18["avg"]
            .sort_values(ascending=False)
            .reset_index()
        )
    
        with col1:
    
            fig1 = px.bar(
                demo_5_17,
                x="state",
                y="avg",
                color="avg",
                title="Average Demographic Updates (Age 5-17)",
                template="plotly_dark"
            )
    
            st.plotly_chart(fig1, use_container_width=True)
    
        with col2:
    
            fig2 = px.bar(
                demo_18,
                x="state",
                y="avg",
                color="avg",
                title="Average Demographic Updates (Age 18+)",
                template="plotly_dark"
            )
    
            st.plotly_chart(fig2, use_container_width=True)
    
    else:
    
        col1, col2 = st.columns(2)
    
        bio_5_17 = (
            df.groupby("state")["bio_age_5_17"]
            .agg(["sum","count"])
        )
    
        bio_5_17["avg"] = (
            bio_5_17["sum"] /
            bio_5_17["count"]
        )
    
        bio_5_17 = (
            bio_5_17["avg"]
            .sort_values(ascending=False)
            .reset_index()
        )
    
        bio_18 = (
            df.groupby("state")["bio_age_17_"]
            .agg(["sum","count"])
        )
    
        bio_18["avg"] = (
            bio_18["sum"] /
            bio_18["count"]
        )
    
        bio_18 = (
            bio_18["avg"]
            .sort_values(ascending=False)
            .reset_index()
        )
    
        with col1:
    
            fig1 = px.bar(
                bio_5_17,
                x="state",
                y="avg",
                color="avg",
                title="Average Biometric Updates (Age 5-17)",
                template="plotly_dark"
            )
    
            st.plotly_chart(fig1, use_container_width=True)
    
        with col2:
    
            fig2 = px.bar(
                bio_18,
                x="state",
                y="avg",
                color="avg",
                title="Average Biometric Updates (Age 18+)",
                template="plotly_dark"
            )
    
            st.plotly_chart(fig2, use_container_width=True)
            
    st.markdown("---")
    
    state_name = st.selectbox(
        "Select State",
        sorted(df["state"].dropna().unique())
    )
    
    state_df = df[
        df["state"] == state_name
    ]
    
    tab1,tab2 = st.tabs([
        "District Analysis",
        "Top Districts",
    ])
    
    with tab1:
    
        col1,col2 = st.columns(2)
    
        district_df = (
            state_df.groupby("district")[value_col]
            .mean()
            .reset_index()
            .sort_values(
                value_col,
                ascending=False
            )
        )
    
        # Rename column for cleaner labels
        district_df.rename(
            columns={
                value_col: "Average Value"
            },
            inplace=True
        )
    
    
        with col1:
    
            fig = px.bar(
                district_df,
                x="district",
                y="Average Value",
                color="Average Value",
                template="plotly_dark",
                title=f"Average {category} per District in {state_name}"
            )
    
            fig.update_layout(
                height=700,
                xaxis_title="District",
                yaxis_title=f"Average {category}",
                xaxis_tickangle=-60,
                coloraxis_showscale=False
            )
    
            st.plotly_chart(
                fig,
                use_container_width=True
            )
    
        with col2:
    
            fig2 = px.pie(
                district_df.head(10),
                names="district",
                values="Average Value",
                hole=0.5,
                title=f"Top 10 District Share (Average {category})"
            )
    
            st.plotly_chart(
                fig2,
                use_container_width=True
            )
            
    with tab2:
    
        st.subheader(
            f"Top Districts by Average {category} in {state_name}"
        )
    
        st.dataframe(
            district_df.head(15),
            use_container_width=True
        )
    
with report_tab:

    st.header("📄 UIDAI Hackathon Project Report")

    st.markdown("""
    ### Analysis of Aadhaar Enrolment and Updates

    This report presents:
    - Enrollment analysis
    - Demographic update analysis
    - Biometric update analysis
    - State-wise trends
    - District-level insights
    - Age-wise analysis
    """)

    pdf_viewer(
        "UIDAI Hackathon Report.pdf",
        width=900
    )

    with open("UIDAI Hackathon Report.pdf", "rb") as file:

        st.download_button(
            "📥 Download Report",
            file,
            "UIDAI Hackathon Report.pdf",
            "application/pdf"
        )