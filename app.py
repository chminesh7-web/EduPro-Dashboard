
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="EduPro Learner Analytics Dashboard",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 EduPro Learner Demographics & Course Enrollment Dashboard")
st.markdown("---")

# ----------------------------------
# LOAD DATA
# ----------------------------------

@st.cache_data
def load_data():
    df = pd.read_excel("Merged_EduPro.xlsx")

    # Convert Transaction Date
    df["TransactionDate"] = pd.to_datetime(df["TransactionDate"])

    df["Month"] = df["TransactionDate"].dt.strftime("%b")
    df["Year"] = df["TransactionDate"].dt.year

    return df

df = load_data()

# ----------------------------------
# SIDEBAR FILTERS
# ----------------------------------

st.sidebar.header("Dashboard Filters")

gender = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["Gender"].dropna().unique()),
    default=sorted(df["Gender"].dropna().unique())
)

age_group = st.sidebar.multiselect(
    "Age Group",
    options=df["AgeGroup"].unique(),
    default=df["AgeGroup"].unique()
)

course_category = st.sidebar.multiselect(
    "Course Category",
    options=sorted(df["CourseCategory"].unique()),
    default=sorted(df["CourseCategory"].unique())
)

course_level = st.sidebar.multiselect(
    "Course Level",
    options=sorted(df["CourseLevel"].unique()),
    default=sorted(df["CourseLevel"].unique())
)

course_type = st.sidebar.multiselect(
    "Course Type",
    options=sorted(df["CourseType"].unique()),
    default=sorted(df["CourseType"].unique())
)

year = st.sidebar.multiselect(
    "Year",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

# ----------------------------------
# APPLY FILTERS
# ----------------------------------

filtered_df = df[
    (df["Gender"].isin(gender))
    & (df["AgeGroup"].isin(age_group))
    & (df["CourseCategory"].isin(course_category))
    & (df["CourseLevel"].isin(course_level))
    & (df["CourseType"].isin(course_type))
    & (df["Year"].isin(year))
]

# ----------------------------------
# KPI CALCULATIONS
# ----------------------------------

total_learners = filtered_df["UserID"].nunique()

total_courses = filtered_df["CourseID"].nunique()

total_enrollments = filtered_df["TransactionID"].count()

avg_courses = (
    round(total_enrollments / total_learners, 2)
    if total_learners > 0 else 0
)

avg_age = (
    round(filtered_df["Age"].mean(), 1)
    if not filtered_df.empty else 0
)

popular_category = (
    filtered_df["CourseCategory"].mode()[0]
    if not filtered_df.empty else "-"
)

popular_level = (
    filtered_df["CourseLevel"].mode()[0]
    if not filtered_df.empty else "-"
)

male_percent = round(
    (
        filtered_df[filtered_df["Gender"] == "Male"]["UserID"].nunique()
        / total_learners
    ) * 100,
    1,
) if total_learners > 0 else 0

female_percent = round(
    (
        filtered_df[filtered_df["Gender"] == "Female"]["UserID"].nunique()
        / total_learners
    ) * 100,
    1,
) if total_learners > 0 else 0

# ----------------------------------
# ADDITIONAL KPI CALCULATIONS
# ----------------------------------

# Repeat Learners
repeat_learners = (
    filtered_df.groupby("UserID")["TransactionID"]
    .count()
    .gt(1)
    .sum()
)

repeat_percentage = round(
    (repeat_learners / total_learners) * 100,
    1
) if total_learners > 0 else 0

# Beginner %
beginner_percentage = round(
    (
        filtered_df[filtered_df["CourseLevel"] == "Beginner"]
        .shape[0]
        / total_enrollments
    ) * 100,
    1
) if total_enrollments > 0 else 0

# Intermediate %
intermediate_percentage = round(
    (
        filtered_df[filtered_df["CourseLevel"] == "Intermediate"]
        .shape[0]
        / total_enrollments
    ) * 100,
    1
) if total_enrollments > 0 else 0

# Advanced %
advanced_percentage = round(
    (
        filtered_df[filtered_df["CourseLevel"] == "Advanced"]
        .shape[0]
        / total_enrollments
    ) * 100,
    1
) if total_enrollments > 0 else 0

# Category Popularity Index
category_share = (
    filtered_df["CourseCategory"]
    .value_counts(normalize=True)
    .mul(100)
    .round(1)
)

category_popularity = (
    f"{category_share.iloc[0]}%"
    if not category_share.empty else "0%"
)

# Active User Ratio
active_user_ratio = round(
    (repeat_learners / total_learners) * 100,
    1
) if total_learners > 0 else 0


# ----------------------------------
# KPI SECTION
# ----------------------------------

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👨‍🎓 Total Learners", total_learners)

with col2:
    st.metric("📚 Total Courses", total_courses)

with col3:
    st.metric("📝 Total Enrollments", total_enrollments)

with col4:
    st.metric("📖 Avg Courses / Learner", avg_courses)

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric("🎂 Average Age", avg_age)

with col6:
    st.metric("🏆 Popular Category", popular_category)

with col7:
    st.metric("⭐ Popular Level", popular_level)

with col8:
    st.metric(
        "👥 Gender Ratio",
        f"M {male_percent}% | F {female_percent}%"
    )
    
    
col9, col10, col11, col12 = st.columns(4)

with col9:
    st.metric(
        "🔁 Repeat Learners",
        repeat_learners
    )

with col10:
    st.metric(
        "🎯 Active User Ratio",
        f"{active_user_ratio}%"
    )

with col11:
    st.metric(
        "📈 Beginner %",
        f"{beginner_percentage}%"
    )

with col12:
    st.metric(
        "⭐ Intermediate %",
        f"{intermediate_percentage}%"
    )
    
col13, col14 = st.columns(2)

with col13:
    st.metric(
        "🚀 Advanced %",
        f"{advanced_percentage}%"
    )

with col14:
    st.metric(
        "🏆 Category Popularity Index",
        category_popularity
    )        

st.markdown("---")



kpi_summary = pd.DataFrame({
    "KPI": [
        "Total Learners",
        "Total Courses",
        "Total Enrollments",
        "Average Courses",
        "Average Age",
        "Gender Ratio",
        "Repeat Learners",
        "Active User Ratio",
        "Beginner %",
        "Intermediate %",
        "Advanced %",
        "Category Popularity"
    ],
    "Value": [
        total_learners,
        total_courses,
        total_enrollments,
        avg_courses,
        avg_age,
        f"M {male_percent}% | F {female_percent}%",
        repeat_learners,
        f"{active_user_ratio}%",
        f"{beginner_percentage}%",
        f"{intermediate_percentage}%",
        f"{advanced_percentage}%",
        category_popularity
    ]
})

st.dataframe(
    kpi_summary,
    use_container_width=True,
    hide_index=True
)


# ==========================================================
# LEARNER DEMOGRAPHICS ANALYSIS
# ==========================================================

st.header("👨‍🎓 Learner Demographics Analysis")

# ----------------------------------------------------------
# Gender Distribution
# ----------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("Gender Distribution")

    gender_count = (
        filtered_df.groupby("Gender")["UserID"]
        .nunique()
        .reset_index(name="Learners")
    )

    fig_gender = px.pie(
        gender_count,
        names="Gender",
        values="Learners",
        hole=0.45,
        title="Gender Participation Ratio"
    )

    fig_gender.update_traces(textposition="inside", textinfo="percent+label")

    st.plotly_chart(fig_gender, use_container_width=True)

# ----------------------------------------------------------
# Age Group Distribution
# ----------------------------------------------------------

with col2:

    st.subheader("Age Group Distribution")

    age_group_count = (
        filtered_df.groupby("AgeGroup")["UserID"]
        .nunique()
        .reset_index(name="Learners")
    )

    fig_agegroup = px.bar(
        age_group_count,
        x="AgeGroup",
        y="Learners",
        color="AgeGroup",
        text="Learners",
        title="Learners by Age Group"
    )

    fig_agegroup.update_layout(showlegend=False)

    st.plotly_chart(fig_agegroup, use_container_width=True)

# ----------------------------------------------------------
# Age Distribution Histogram
# ----------------------------------------------------------

st.subheader("Age Distribution")

fig_age = px.histogram(
    filtered_df,
    x="Age",
    nbins=15,
    color="Gender",
    marginal="box",
    title="Distribution of Learner Ages"
)

st.plotly_chart(fig_age, use_container_width=True)

# ----------------------------------------------------------
# Gender Participation Table
# ----------------------------------------------------------

st.subheader("Gender Participation Summary")

gender_summary = (
    filtered_df.groupby("Gender")
    .agg(
        Total_Learners=("UserID", "nunique"),
        Total_Enrollments=("TransactionID", "count")
    )
    .reset_index()
)

st.dataframe(
    gender_summary,
    use_container_width=True,
    hide_index=True
)

# ----------------------------------------------------------
# Age Group Participation
# ----------------------------------------------------------

st.subheader("Participation by Age Group")

age_summary = (
    filtered_df.groupby("AgeGroup")
    .agg(
        Learners=("UserID", "nunique"),
        Enrollments=("TransactionID", "count")
    )
    .reset_index()
)

fig_age_summary = px.bar(
    age_summary,
    x="AgeGroup",
    y=["Learners", "Enrollments"],
    barmode="group",
    text_auto=True,
    title="Learners vs Enrollments by Age Group"
)

st.plotly_chart(fig_age_summary, use_container_width=True)

# ----------------------------------------------------------
# Age Group Statistics
# ----------------------------------------------------------

st.subheader("Age Group Statistics")

age_stats = (
    filtered_df.groupby("AgeGroup")
    .agg(
        Average_Age=("Age", "mean"),
        Learners=("UserID", "nunique"),
        Enrollments=("TransactionID", "count")
    )
    .round(1)
    .reset_index()
)

st.dataframe(
    age_stats,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")



# ==========================================================
# COURSE ENROLLMENT ANALYSIS
# ==========================================================

st.header("📚 Course Enrollment Analysis")

# ----------------------------------------------------------
# Course Category Popularity
# ----------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("Course Category Popularity")

    category_df = (
        filtered_df.groupby("CourseCategory")
        .size()
        .reset_index(name="Enrollments")
        .sort_values("Enrollments", ascending=False)
    )

    fig_category = px.bar(
        category_df,
        x="CourseCategory",
        y="Enrollments",
        color="Enrollments",
        text="Enrollments",
        title="Enrollments by Course Category"
    )

    fig_category.update_layout(
        xaxis_title="Course Category",
        yaxis_title="Enrollments",
        showlegend=False
    )

    st.plotly_chart(fig_category, use_container_width=True)

# ----------------------------------------------------------
# Course Category Percentage
# ----------------------------------------------------------

with col2:

    st.subheader("Category Popularity (%)")

    fig_category_pie = px.pie(
        category_df,
        names="CourseCategory",
        values="Enrollments",
        hole=0.45,
        title="Category Share"
    )

    fig_category_pie.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    st.plotly_chart(fig_category_pie, use_container_width=True)

# ----------------------------------------------------------
# Course Type Analysis
# ----------------------------------------------------------

st.subheader("Course Type Analysis")

course_type_df = (
    filtered_df.groupby("CourseType")
    .size()
    .reset_index(name="Enrollments")
    .sort_values("Enrollments", ascending=False)
)

fig_type = px.bar(
    course_type_df,
    x="CourseType",
    y="Enrollments",
    color="CourseType",
    text="Enrollments",
    title="Enrollments by Course Type"
)

fig_type.update_layout(showlegend=False)

st.plotly_chart(fig_type, use_container_width=True)

# ----------------------------------------------------------
# Course Level Distribution
# ----------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("Course Level Distribution")

    level_df = (
        filtered_df.groupby("CourseLevel")
        .size()
        .reset_index(name="Enrollments")
    )

    fig_level = px.pie(
        level_df,
        names="CourseLevel",
        values="Enrollments",
        hole=0.50,
        title="Course Level Distribution"
    )

    fig_level.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    st.plotly_chart(fig_level, use_container_width=True)

with col2:

    st.subheader("Course Level Comparison")

    fig_level_bar = px.bar(
        level_df,
        x="CourseLevel",
        y="Enrollments",
        color="CourseLevel",
        text="Enrollments",
        title="Enrollments by Course Level"
    )

    fig_level_bar.update_layout(showlegend=False)

    st.plotly_chart(fig_level_bar, use_container_width=True)

# ----------------------------------------------------------
# Monthly Enrollment Trend
# ----------------------------------------------------------

st.subheader("Monthly Enrollment Trend")

month_order = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

monthly_df = (
    filtered_df.groupby("Month")
    .size()
    .reset_index(name="Enrollments")
)

monthly_df["Month"] = pd.Categorical(
    monthly_df["Month"],
    categories=month_order,
    ordered=True
)

monthly_df = monthly_df.sort_values("Month")

fig_month = px.line(
    monthly_df,
    x="Month",
    y="Enrollments",
    markers=True,
    title="Monthly Enrollment Trend"
)

st.plotly_chart(fig_month, use_container_width=True)

# ----------------------------------------------------------
# Top 10 Most Popular Courses
# ----------------------------------------------------------

st.subheader("🏆 Top 10 Most Popular Courses")

top_courses = (
    filtered_df.groupby("CourseName")
    .size()
    .reset_index(name="Enrollments")
    .sort_values("Enrollments", ascending=False)
    .head(10)
)

fig_top = px.bar(
    top_courses,
    x="Enrollments",
    y="CourseName",
    orientation="h",
    color="Enrollments",
    text="Enrollments",
    title="Top 10 Courses by Enrollment"
)

fig_top.update_layout(
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig_top, use_container_width=True)

# ----------------------------------------------------------
# Course Enrollment Summary Table
# ----------------------------------------------------------

st.subheader("Enrollment Summary")

summary_df = (
    filtered_df.groupby(
        ["CourseCategory", "CourseType", "CourseLevel"]
    )
    .agg(
        Enrollments=("TransactionID", "count"),
        Learners=("UserID", "nunique")
    )
    .reset_index()
)

st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")



# ==========================================================
# ADVANCED ANALYTICS
# ==========================================================

st.header("📈 Advanced Analytics")

# ----------------------------------------------------------
# Age Group vs Course Category Heatmap
# ----------------------------------------------------------

st.subheader("🔥 Age Group vs Course Category")

heatmap_age_category = pd.crosstab(
    filtered_df["AgeGroup"],
    filtered_df["CourseCategory"]
)

fig_heatmap = px.imshow(
    heatmap_age_category,
    text_auto=True,
    color_continuous_scale="Blues",
    aspect="auto",
    labels=dict(
        x="Course Category",
        y="Age Group",
        color="Enrollments"
    )
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# ----------------------------------------------------------
# Gender vs Course Level
# ----------------------------------------------------------

st.subheader("👨👩 Gender vs Course Level")

gender_level = (
    filtered_df.groupby(["Gender","CourseLevel"])
    .size()
    .reset_index(name="Enrollments")
)

fig_gender_level = px.bar(
    gender_level,
    x="CourseLevel",
    y="Enrollments",
    color="Gender",
    barmode="group",
    text="Enrollments",
    title="Course Level Preference by Gender"
)

st.plotly_chart(fig_gender_level, use_container_width=True)

# ----------------------------------------------------------
# Gender vs Course Category
# ----------------------------------------------------------

st.subheader("📚 Gender vs Course Category")

gender_category = (
    filtered_df.groupby(["CourseCategory","Gender"])
    .size()
    .reset_index(name="Enrollments")
)

fig_gender_category = px.bar(
    gender_category,
    x="CourseCategory",
    y="Enrollments",
    color="Gender",
    barmode="group",
    text="Enrollments"
)

st.plotly_chart(fig_gender_category, use_container_width=True)

# ----------------------------------------------------------
# Age Group vs Course Level
# ----------------------------------------------------------

st.subheader("🎯 Age Group vs Course Level")

age_level = (
    filtered_df.groupby(["AgeGroup","CourseLevel"])
    .size()
    .reset_index(name="Enrollments")
)

fig_age_level = px.bar(
    age_level,
    x="AgeGroup",
    y="Enrollments",
    color="CourseLevel",
    barmode="group",
    text="Enrollments"
)

st.plotly_chart(fig_age_level, use_container_width=True)

# ----------------------------------------------------------
# Age Group vs Course Type
# ----------------------------------------------------------

st.subheader("📖 Age Group vs Course Type")

age_type = (
    filtered_df.groupby(["AgeGroup","CourseType"])
    .size()
    .reset_index(name="Enrollments")
)

fig_age_type = px.bar(
    age_type,
    x="AgeGroup",
    y="Enrollments",
    color="CourseType",
    barmode="group",
    text="Enrollments"
)

st.plotly_chart(fig_age_type, use_container_width=True)

# ----------------------------------------------------------
# Course Category vs Course Level
# ----------------------------------------------------------

st.subheader("📊 Course Category vs Course Level")

category_level = (
    filtered_df.groupby(["CourseCategory","CourseLevel"])
    .size()
    .reset_index(name="Enrollments")
)

fig_category_level = px.bar(
    category_level,
    x="CourseCategory",
    y="Enrollments",
    color="CourseLevel",
    barmode="stack",
    text="Enrollments"
)

st.plotly_chart(fig_category_level, use_container_width=True)

# ----------------------------------------------------------
# Crosstab Tables
# ----------------------------------------------------------

st.subheader("📋 Crosstab Analysis")

tab1, tab2 = st.tabs([
    "Age Group × Category",
    "Gender × Level"
])

with tab1:

    st.dataframe(
        heatmap_age_category,
        use_container_width=True
    )

with tab2:

    gender_level_table = pd.crosstab(
        filtered_df["Gender"],
        filtered_df["CourseLevel"]
    )

    st.dataframe(
        gender_level_table,
        use_container_width=True
    )

# ----------------------------------------------------------
# Percentage Distribution
# ----------------------------------------------------------

st.subheader("📈 Course Level Preference (%)")

level_percent = (
    filtered_df["CourseLevel"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
    .reset_index()
)

level_percent.columns = [
    "Course Level",
    "Percentage"
]

fig_level_percent = px.bar(
    level_percent,
    x="Course Level",
    y="Percentage",
    color="Course Level",
    text="Percentage"
)

st.plotly_chart(fig_level_percent, use_container_width=True)

st.markdown("---")



# ==========================================================
# LEARNER BEHAVIOR ANALYSIS
# ==========================================================

st.header("👨‍💻 Learner Behavior Analysis")

# ----------------------------------------------------------
# Average Courses Per Learner
# ----------------------------------------------------------

st.subheader("📖 Average Courses per Learner")

learner_courses = (
    filtered_df.groupby(["UserID", "UserName"])
    .agg(
        TotalCourses=("CourseID", "count")
    )
    .reset_index()
)

avg_courses_per_learner = round(
    learner_courses["TotalCourses"].mean(), 2
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Courses/Learner",
        avg_courses_per_learner
    )

with col2:
    st.metric(
        "Maximum Courses by One Learner",
        learner_courses["TotalCourses"].max()
    )

with col3:
    st.metric(
        "Minimum Courses by One Learner",
        learner_courses["TotalCourses"].min()
    )

# ----------------------------------------------------------
# Top 10 Active Learners
# ----------------------------------------------------------

st.subheader("🏆 Top 10 Active Learners")

top_learners = (
    learner_courses
    .sort_values("TotalCourses", ascending=False)
    .head(10)
)

fig_top_users = px.bar(
    top_learners,
    x="TotalCourses",
    y="UserName",
    orientation="h",
    color="TotalCourses",
    text="TotalCourses",
    title="Top 10 Learners by Number of Enrollments"
)

fig_top_users.update_layout(
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(
    fig_top_users,
    use_container_width=True
)

# ----------------------------------------------------------
# Enrollment Concentration
# ----------------------------------------------------------

st.subheader("📊 Enrollment Concentration")

fig_hist = px.histogram(
    learner_courses,
    x="TotalCourses",
    nbins=15,
    title="Distribution of Courses Taken per Learner",
    text_auto=True
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# ----------------------------------------------------------
# Active vs Less Active Learners
# ----------------------------------------------------------

st.subheader("📈 Learner Activity Levels")

activity_df = learner_courses.copy()

activity_df["ActivityLevel"] = pd.cut(
    activity_df["TotalCourses"],
    bins=[0,2,5,100],
    labels=[
        "Low Activity",
        "Moderate Activity",
        "Highly Active"
    ]
)

activity_summary = (
    activity_df.groupby("ActivityLevel")
    .size()
    .reset_index(name="Learners")
)

fig_activity = px.pie(
    activity_summary,
    names="ActivityLevel",
    values="Learners",
    hole=0.45,
    title="Learner Activity Distribution"
)

st.plotly_chart(
    fig_activity,
    use_container_width=True
)

# ----------------------------------------------------------
# Repeat Enrollment Analysis
# ----------------------------------------------------------

st.subheader("🔁 Repeat Enrollment Analysis")

repeat_df = (
    filtered_df.groupby("UserID")
    .agg(
        Enrollments=("TransactionID","count")
    )
    .reset_index()
)

repeat_learners = (
    repeat_df["Enrollments"] > 1
).sum()

single_learners = (
    repeat_df["Enrollments"] == 1
).sum()

repeat_summary = pd.DataFrame({

    "Learner Type":[
        "Single Enrollment",
        "Repeat Enrollment"
    ],

    "Count":[
        single_learners,
        repeat_learners
    ]

})

fig_repeat = px.bar(
    repeat_summary,
    x="Learner Type",
    y="Count",
    color="Learner Type",
    text="Count"
)

st.plotly_chart(
    fig_repeat,
    use_container_width=True
)

# ----------------------------------------------------------
# Average Courses by Gender
# ----------------------------------------------------------

st.subheader("👨👩 Average Courses by Gender")

gender_courses = (
    filtered_df.groupby(["Gender","UserID"])
    .agg(
        Courses=("CourseID","count")
    )
    .reset_index()
)

gender_avg = (
    gender_courses.groupby("Gender")
    .agg(
        AverageCourses=("Courses","mean")
    )
    .round(2)
    .reset_index()
)

fig_gender_avg = px.bar(
    gender_avg,
    x="Gender",
    y="AverageCourses",
    color="Gender",
    text="AverageCourses"
)

st.plotly_chart(
    fig_gender_avg,
    use_container_width=True
)

# ----------------------------------------------------------
# Average Courses by Age Group
# ----------------------------------------------------------

st.subheader("🎯 Average Courses by Age Group")

age_courses = (
    filtered_df.groupby(["AgeGroup","UserID"])
    .agg(
        Courses=("CourseID","count")
    )
    .reset_index()
)

age_avg = (
    age_courses.groupby("AgeGroup")
    .agg(
        AverageCourses=("Courses","mean")
    )
    .round(2)
    .reset_index()
)

fig_age_avg = px.bar(
    age_avg,
    x="AgeGroup",
    y="AverageCourses",
    color="AgeGroup",
    text="AverageCourses"
)

fig_age_avg.update_layout(showlegend=False)

st.plotly_chart(
    fig_age_avg,
    use_container_width=True
)

# ----------------------------------------------------------
# Learner Behavior Summary Table
# ----------------------------------------------------------

st.subheader("📋 Learner Behavior Summary")

behavior_table = learner_courses.describe()

st.dataframe(
    behavior_table,
    use_container_width=True
)

st.markdown("---")



# ==========================================================
# BUSINESS INSIGHTS & RECOMMENDATIONS
# ==========================================================

st.header("💡 Business Insights")

highest_category = (
    filtered_df["CourseCategory"]
    .value_counts()
    .idxmax()
)

highest_level = (
    filtered_df["CourseLevel"]
    .value_counts()
    .idxmax()
)

highest_age_group = (
    filtered_df["AgeGroup"]
    .value_counts()
    .idxmax()
)

highest_gender = (
    filtered_df["Gender"]
    .value_counts()
    .idxmax()
)

highest_course = (
    filtered_df["CourseName"]
    .value_counts()
    .idxmax()
)

st.success(f"""
### Key Insights

• Total Learners : **{total_learners}**

• Total Enrollments : **{total_enrollments}**

• Most Active Age Group : **{highest_age_group}**

• Highest Participation Gender : **{highest_gender}**

• Most Popular Course Category : **{highest_category}**

• Most Preferred Course Level : **{highest_level}**

• Most Enrolled Course : **{highest_course}**

• Average Courses per Learner : **{avg_courses_per_learner}**
""")

st.markdown("---")

# ==========================================================
# RECOMMENDATIONS
# ==========================================================

st.header("🎯 Recommendations")

recommendations = pd.DataFrame({

"Recommendation":[

"Increase course offerings in the most popular category.",

"Develop more beginner-friendly courses to attract new learners.",

"Launch targeted marketing campaigns for underrepresented age groups.",

"Introduce personalized course recommendations based on learner demographics.",

"Encourage repeat enrollments through certificates and reward programs.",

"Improve promotion of low-enrollment course categories.",

"Expand advanced-level courses for experienced learners.",

"Monitor monthly enrollment trends for better planning."

]

})

st.table(recommendations)

st.markdown("---")

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

st.header("📑 Executive Summary")

st.info(f"""

The EduPro Learner Demographics and Course Enrollment Dashboard provides a
comprehensive overview of learner participation and enrollment behavior.

Key Findings

• {total_learners} unique learners enrolled in {total_courses} courses.

• The platform recorded {total_enrollments} enrollments.

• {highest_age_group} is the most active learner group.

• {highest_category} is the most popular course category.

• {highest_level} courses receive the highest enrollments.

• {highest_gender} learners contribute the highest participation.

These insights support data-driven decisions for course planning,
learner engagement, targeted marketing, and platform growth.

""")

st.markdown("---")

# ==========================================================
# DOWNLOAD FILTERED DATA
# ==========================================================

st.header("📥 Download Filtered Dataset")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(

label="⬇ Download CSV",

data=csv,

file_name="EduPro_Filtered_Data.csv",

mime="text/csv"

)

st.markdown("---")

# ==========================================================
# DATASET PREVIEW
# ==========================================================

st.header("🗂 Filtered Dataset Preview")

st.dataframe(

filtered_df,

use_container_width=True,

height=400

)

st.markdown("---")

# ==========================================================
# PROJECT SUMMARY
# ==========================================================

st.header("📌 Project Objectives Covered")

checklist = pd.DataFrame({

"Requirement":[

"Data Integration",

"Learner Demographics",

"Age Group Analysis",

"Gender Analysis",

"Course Category Analysis",

"Course Type Analysis",

"Course Level Analysis",

"Monthly Enrollment Trend",

"Age Group vs Course Category",

"Gender vs Course Level",

"Average Courses per Learner",

"Top Active Learners",

"Enrollment Concentration",

"Interactive Dashboard",

"Download Filtered Dataset",

"Business Insights",

"Executive Summary",

"Recommendations"

],

"Status":[

"✅",

"✅",

"✅",

"✅",

"✅",

"✅",

"✅",

"✅",

"✅",

"✅",

"✅",

"✅",

"✅",

"✅",

"✅",

"✅",

"✅",

"✅"

]

})

st.dataframe(

checklist,

hide_index=True,

use_container_width=True

)

st.markdown("---")

# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
"""
---
### 🎓 EduPro Learner Demographics and Course Enrollment Behavior Analysis

**Developed using:** Streamlit, Pandas, Plotly

**Project Objectives Achieved:**

✔ Learner Demographics Analysis

✔ Enrollment Distribution Analysis

✔ Behavioral Insights

✔ Interactive Dashboard

✔ Executive Summary

✔ Government Stakeholder Recommendations

**© EduPro Analytics Dashboard**
"""
)