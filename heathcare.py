import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Load Data
df = pd.read_csv("Impact_of_Remote_Work_on_Mental_Health.csv")

st.title("📊 Impact of Remote Work")

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
    Work mode adoption appears structurally balanced across industries, regions, and experience levels, indicating a globally diversified and policy-driven shift toward flexible work models.
    """)

# ==================================================
# PLACEHOLDERS FOR OTHER ACTS
# ==================================================

elif act_selection == "Act II: The Cost of Connection":
    st.header("💻 Act II: The Cost of Connection")

        # --- Ensure Stress Level is usable ---
    # If Stress_Level is categorical (e.g., Low/Medium/High), encode safely
    if df["Stress_Level"].dtype == "object":
        df["Stress_Level"] = pd.Categorical(df["Stress_Level"]).codes + 1
    else:
        df["Stress_Level"] = pd.to_numeric(df["Stress_Level"], errors="coerce")

    # Other numeric columns
    df["Social_Isolation_Rating"] = pd.to_numeric(df["Social_Isolation_Rating"], errors="coerce")
    df["Work_Life_Balance_Rating"] = pd.to_numeric(df["Work_Life_Balance_Rating"], errors="coerce")
    df["Number_of_Virtual_Meetings"] = pd.to_numeric(df["Number_of_Virtual_Meetings"], errors="coerce")
    df["Hours_Worked_Per_Week"] = pd.to_numeric(df["Hours_Worked_Per_Week"], errors="coerce")

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # 1️⃣ Avg Social Isolation by Work Mode
    with col1:
        st.subheader("1. Avg Social Isolation by Work Mode")

        isolation_avg = df.groupby("Work_Location")["Social_Isolation_Rating"].mean().reset_index()

        fig1 = px.bar(
            isolation_avg,
            x="Work_Location",
            y="Social_Isolation_Rating",
            text_auto=True
        )

        min_val = isolation_avg["Social_Isolation_Rating"].min()
        max_val = isolation_avg["Social_Isolation_Rating"].max()

        fig1.update_layout(
            yaxis=dict(
                range=[min_val - 0.02, max_val + 0.02],
                tickformat=".3f",
                dtick=0.01
            )
        )

        fig1.update_traces(
            hovertemplate="Work Mode: %{x}<br>Avg Isolation: %{y:.3f}"
        )

        st.plotly_chart(fig1, use_container_width=True)

                    # 2️⃣ Stress Level Count by Work Mode
    with col2:
        st.subheader("2. Stress Level Count by Work Mode")

        stress_dist = (
            df.groupby(["Work_Location", "Stress_Level"])
            .size()
            .reset_index(name="Count")
        )

        fig2 = px.bar(
            stress_dist,
            x="Work_Location",
            y="Count",
            color="Stress_Level",
            barmode="group"
        )

        fig2.update_traces(
            hovertemplate="Work Mode: %{x}<br>Stress Level: %{legendgroup}<br>Count: %{y}"
        )

        st.plotly_chart(fig2, use_container_width=True)

    # 3️⃣ Avg Virtual Meetings by Work Mode
    with col3:
        st.subheader("3. Number of Virtual Meetings by Work Mode")

        meeting_avg = df.groupby("Work_Location")["Number_of_Virtual_Meetings"].count().reset_index()

        fig3 = px.bar(
            meeting_avg,
            x="Work_Location",
            y="Number_of_Virtual_Meetings",
            text_auto=True
        )

        fig3.update_traces(
            hovertemplate="Work Mode: %{x}<br>Avg Meetings: %{y:.2f}"
        )

        st.plotly_chart(fig3, use_container_width=True)

    # 4️⃣ Avg Work-Life Balance by Work Mode
    with col4:
        st.subheader("4. Avg Work-Life Balance by Work Mode")

        wlb_avg = df.groupby("Work_Location")["Work_Life_Balance_Rating"].mean().reset_index()

        fig4 = px.bar(
            wlb_avg,
            x="Work_Location",
            y="Work_Life_Balance_Rating",
            text_auto=True
        )

        fig4.update_traces(
            hovertemplate="Work Mode: %{x}<br>Avg Work-Life Balance: %{y:.2f}"
        )

        st.plotly_chart(fig4, use_container_width=True)

    st.success("""
    **Act II Conclusion:**  
    Hybrid work appears to strike the optimal balance between productivity demands and employee well-being, while fully remote work increases digital interaction without proportionate well-being gains.
    """)

elif act_selection == "Act III: The Support ROI":
    st.header("🏢 Act III: The Support ROI")

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # 1️⃣ Productivity Change by Company Support
    with col1:
        st.subheader("1. Productivity Change by Company Support")

        prod_support = (
            df.groupby(["Company_Support_for_Remote_Work", "Productivity_Change"])
            .size()
            .reset_index(name="Count")
        )

        fig1 = px.bar(
            prod_support,
            x="Company_Support_for_Remote_Work",
            y="Count",
            color="Productivity_Change",
            barmode="group"
        )

        fig1.update_traces(
            hovertemplate="Support: %{x}<br>Productivity: %{legendgroup}<br>Count: %{y}"
        )

        st.plotly_chart(fig1, use_container_width=True)

    # 2️⃣ Productivity Change by Access to Mental Health Resources
    with col2:
        st.subheader("2. Productivity Change by Mental Health Access")

        prod_access = (
            df.groupby(["Access_to_Mental_Health_Resources", "Productivity_Change"])
            .size()
            .reset_index(name="Count")
        )

        fig2 = px.bar(
            prod_access,
            x="Access_to_Mental_Health_Resources",
            y="Count",
            color="Productivity_Change",
            barmode="group"
        )

        fig2.update_traces(
            hovertemplate="Access: %{x}<br>Productivity: %{legendgroup}<br>Count: %{y}"
        )

        st.plotly_chart(fig2, use_container_width=True)

    # 3️⃣ Productivity vs Mental Health Condition
    with col3:
        st.subheader("3. Productivity Change by Mental Health Condition")

        prod_mental = (
            df.groupby(["Mental_Health_Condition", "Productivity_Change"])
            .size()
            .reset_index(name="Count")
        )

        fig3 = px.bar(
            prod_mental,
            x="Mental_Health_Condition",
            y="Count",
            color="Productivity_Change",
            barmode="group"
        )

        fig3.update_traces(
            hovertemplate="Condition: %{x}<br>Productivity: %{legendgroup}<br>Count: %{y}"
        )

        st.plotly_chart(fig3, use_container_width=True)

        # 4️⃣ Productivity Distribution by Support Level (Stacked % Bar)
    with col4:
        st.subheader("4. Productivity Distribution by Support Level")

        prod_dist = (
            df.groupby(["Company_Support_for_Remote_Work", "Productivity_Change"])
            .size()
            .reset_index(name="Count")
        )

        # Convert to percentage
        prod_dist["Percentage"] = prod_dist.groupby("Company_Support_for_Remote_Work")["Count"].transform(lambda x: x / x.sum() * 100)

        fig4 = px.bar(
            prod_dist,
            x="Company_Support_for_Remote_Work",
            y="Percentage",
            color="Productivity_Change",
            barmode="stack"
        )

        fig4.update_traces(
            hovertemplate="Support: %{x}<br>Productivity: %{legendgroup}<br>Percentage: %{y:.1f}%"
        )

        st.plotly_chart(fig4, use_container_width=True)

    st.success("""
    **Act III Conclusion:**  
    Mental health condition has a stronger observable association with productivity change than company support or access to resources.
    Company support and access to resources show only mild variation, not strong directional impact.
    Productivity decline appears influenced more by underlying mental health conditions than organizational support measures alone.
    """)

elif act_selection == "Systemic Links":
    st.header("⚖️ Systemic Links")

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # 1️⃣ Productivity–Wellness Paradox
    with col1:
        st.subheader("1. Productivity vs Stress Level")

        prod_stress = (
            df.groupby(["Productivity_Change", "Stress_Level"])
            .size()
            .reset_index(name="Count")
        )

        fig1 = px.bar(
            prod_stress,
            x="Productivity_Change",
            y="Count",
            color="Stress_Level",
            barmode="group"
        )

        fig1.update_traces(
            hovertemplate="Productivity: %{x}<br>Stress Level: %{legendgroup}<br>Count: %{y}"
        )

        st.plotly_chart(fig1, use_container_width=True)

    # 2️⃣ Productivity vs Sleep Quality
    with col2:
        st.subheader("2. Productivity vs Sleep Quality")

        sleep_prod = (
            df.groupby(["Productivity_Change", "Sleep_Quality"])
            .size()
            .reset_index(name="Count")
        )

        fig2 = px.bar(
            sleep_prod,
            x="Productivity_Change",
            y="Count",
            color="Sleep_Quality",
            barmode="group"
        )

        fig2.update_traces(
            hovertemplate="Productivity: %{x}<br>Sleep Quality: %{legendgroup}<br>Count: %{y}"
        )

        st.plotly_chart(fig2, use_container_width=True)

    # 3️⃣ Resource Gap: Work-Life Balance vs Mental Health Access
    with col3:
        st.subheader("3. Work-Life Balance by Mental Health Access")

        wlb_access = (
            df.groupby(["Access_to_Mental_Health_Resources", "Work_Life_Balance_Rating"])
            .size()
            .reset_index(name="Count")
        )

        fig3 = px.bar(
            wlb_access,
            x="Access_to_Mental_Health_Resources",
            y="Count",
            color="Work_Life_Balance_Rating",
            barmode="group"
        )

        fig3.update_traces(
            hovertemplate="Access: %{x}<br>Work-Life Balance: %{legendgroup}<br>Count: %{y}"
        )

        st.plotly_chart(fig3, use_container_width=True)

    # 4️⃣ Hybrid Middle Ground: Satisfaction by Work Mode
    with col4:
        st.subheader("4. Satisfaction with Remote Work by Work Mode")

        satisfaction_mode = (
            df.groupby(["Work_Location", "Satisfaction_with_Remote_Work"])
            .size()
            .reset_index(name="Count")
        )

        fig4 = px.bar(
            satisfaction_mode,
            x="Work_Location",
            y="Count",
            color="Satisfaction_with_Remote_Work",
            barmode="group"
        )

        fig4.update_traces(
            hovertemplate="Work Mode: %{x}<br>Satisfaction: %{legendgroup}<br>Count: %{y}"
        )

        st.plotly_chart(fig4, use_container_width=True)

    st.success("""
    **Systemic Insight Summary:**  
    High productivity does not automatically imply low stress or better sleep.
    Access to mental health resources appears linked to stronger work-life balance outcomes.
    Hybrid workers may show distinct satisfaction patterns compared to fully remote or onsite employees.
    Work mode alone is not a sufficient predictor of well-being.
    """)

elif act_selection == "Employee Persona Spotlight":
    st.header("👤 Employee Persona Spotlight")

    # ==================================================
    # 🔥 Persona 1: High-Risk Performer
    # Definition: Increased Productivity + High Stress + Poor Sleep
    # ==================================================

    high_risk = df[
        (df["Productivity_Change"].str.lower().str.contains("increase")) &
        (df["Stress_Level"].str.lower().str.contains("high")) &
        (df["Sleep_Quality"].str.lower().str.contains("poor"))
    ]

    st.subheader("🔥 High-Risk Performer Count")
    st.write(len(high_risk))

    if not high_risk.empty:
        risk_dist = (
            high_risk.groupby("Work_Location")
            .size()
            .reset_index(name="Count")
        )

        fig_risk = px.bar(
            risk_dist,
            x="Work_Location",
            y="Count",
            text_auto=True,
            title="High-Risk Performers by Work Mode"
        )

        st.plotly_chart(fig_risk, use_container_width=True)
    else:
        st.info("No employees match Increased Productivity + High Stress + Poor Sleep.")
