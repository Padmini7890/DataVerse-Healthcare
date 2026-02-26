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
        st.subheader("3. Avg Virtual Meetings by Work Mode")

        meeting_avg = df.groupby("Work_Location")["Number_of_Virtual_Meetings"].mean().reset_index()

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
    Differences in stress, isolation, meetings, and work-life balance vary across work modes.
    Digital work does not automatically reduce isolation or stress.
    Work mode alone may not explain well-being differences.
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
    Company support and access to mental health resources appear linked with productivity outcomes.
    However, mental health condition may play a stronger role in determining performance shifts.
    Support policies should focus on both structural aid and psychological well-being.
    """)

elif act_selection == "Systemic Links":
    st.header("⚖️ Systemic Links")
    st.info("Systemic link analysis will be added here.")

elif act_selection == "Employee Persona Spotlight":
    st.header("👤 Employee Persona Spotlight")
    st.info("Employee personas will be added here.")
