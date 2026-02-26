import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Load Data
df = pd.read_csv("Impact_of_Remote_Work_on_Mental_Health.csv")

st.title("📊 Remote Work: CEO Storytelling Dashboard")

# ==================================================
# MAIN ACT DROPDOWN
# ==================================================

act_selection = st.selectbox(
    "📖 Select Act",
    [
        "Act I: The New Geography of Work",
        "Act II: The Cost of Connection",
        "Act III: The Support ROI",
        "Systemic Links",
        "Employee Persona Spotlight"
    ]
)

# ==================================================
# ACT I
# ==================================================

if act_selection == "Act I: The New Geography of Work":

    st.header("🗺️ Act I: The New Geography of Work")

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # 1️⃣ Work Mode Distribution (Pie)
    with col1:
        st.subheader("1. Overall Work Mode Distribution")

        work_dist = df["Work_Location"].value_counts().reset_index()
        work_dist.columns = ["Work_Location", "Count"]
        work_dist["Percentage"] = (work_dist["Count"] / work_dist["Count"].sum()) * 100

        fig1 = px.pie(
            work_dist,
            names="Work_Location",
            values="Count",
            hole=0.3
        )

        fig1.update_traces(
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}"
        )

        st.plotly_chart(fig1, use_container_width=True)

    # 2️⃣ Work Mode by Industry
    with col2:
        st.subheader("2. Work Mode by Industry")

        industry_mode = (
            df.groupby(["Industry", "Work_Location"])
            .size()
            .reset_index(name="Count")
        )

        fig2 = px.bar(
            industry_mode,
            x="Industry",
            y="Count",
            color="Work_Location",
            barmode="group"
        )

        fig2.update_traces(
            hovertemplate="Industry: %{x}<br>Count: %{y}<br>Work Mode: %{legendgroup}"
        )

        st.plotly_chart(fig2, use_container_width=True)

    # 3️⃣ Work Mode by Region
    with col3:
        st.subheader("3. Work Mode by Region")

        region_mode = (
            df.groupby(["Region", "Work_Location"])
            .size()
            .reset_index(name="Count")
        )

        fig3 = px.bar(
            region_mode,
            x="Region",
            y="Count",
            color="Work_Location",
            barmode="group"
        )

        fig3.update_traces(
            hovertemplate="Region: %{x}<br>Count: %{y}<br>Work Mode: %{legendgroup}"
        )

        st.plotly_chart(fig3, use_container_width=True)

    # 4️⃣ Experience vs Work Mode
    with col4:
        st.subheader("4. Experience vs Work Mode")

        fig4 = px.box(
            df,
            x="Work_Location",
            y="Years_of_Experience",
            color="Work_Location"
        )

        fig4.update_traces(
            hovertemplate="Work Mode: %{x}<br>Years of Experience: %{y}"
        )

        fig4.update_layout(showlegend=False)

        st.plotly_chart(fig4, use_container_width=True)

    st.success("""
    **Act I Conclusion:**  
    Work mode is not randomly distributed.
    Industry, region, and experience appear to shape how flexibility is allocated.
    This structural pattern sets the foundation for deeper behavioral analysis in Act II.
    """)

# ==================================================
# PLACEHOLDERS FOR OTHER ACTS
# ==================================================

elif act_selection == "Act II: The Cost of Connection":
    st.header("💻 Act II: The Cost of Connection")
    st.info("Act II visuals will be added here.")

elif act_selection == "Act III: The Support ROI":
    st.header("🏢 Act III: The Support ROI")
    st.info("Act III visuals will be added here.")

elif act_selection == "Systemic Links":
    st.header("⚖️ Systemic Links")
    st.info("Systemic link analysis will be added here.")

elif act_selection == "Employee Persona Spotlight":
    st.header("👤 Employee Persona Spotlight")
    st.info("Employee personas will be added here.")
