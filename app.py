import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Billionaire Insights", layout="wide")
st.title("Billionaire Insights, 1997–2024")

@st.cache_data
def load_data():
    return pd.read_csv("billionaire_cleaned.csv", dtype={"self_made": "boolean"})

df = load_data()

# --- Sidebar filters ---
st.sidebar.header("Filters")

years = sorted(df["year"].unique())
selected_range = st.sidebar.slider(
    "Select year range",
    min_value=int(min(years)),
    max_value=int(max(years)),
    value=(int(min(years)), int(max(years)))
)

countries = sorted(df["country_of_citizenship"].dropna().unique())
selected_countries = st.sidebar.multiselect(
    "Select countries (leave empty for all)",
    options=countries
)

filtered_df = df[(df["year"] >= selected_range[0]) & (df["year"] <= selected_range[1])]

if selected_countries:
    filtered_df = filtered_df[filtered_df["country_of_citizenship"].isin(selected_countries)]

top_n = 10
# --- Headline stats ---
col1, col2, col3 = st.columns(3)

total_billionaires = filtered_df["full_name"].nunique()
total_wealth = filtered_df["net_worth"].sum()
avg_age = filtered_df["age"].mean()

col1.metric("Unique Billionaires", f"{total_billionaires:,}")
col2.metric("Total Net Worth", f"${total_wealth:,.0f}B")
col3.metric("Average Age", f"{avg_age:.1f}")

st.markdown("""
### Key Takeaway

Between 1997 and 2024, the composition of the world's billionaires shifted significantly.
The United States has consistently held the largest share, but China's rise, particularly
in technology and manufacturing, has reshaped the global distribution of billionaire wealth
over the past two decades.
""")

# --- Country and Category charts side by side ---
col_country, col_category = st.columns(2)

with col_country:
    st.subheader("Top Countries by Billionaire Count")

    country_counts = (
        filtered_df.drop_duplicates(subset="full_name")["country_of_citizenship"]
        .value_counts()
        .head(top_n)
        .reset_index()
    )
    country_counts.columns = ["country_of_citizenship", "count"]

    fig_country = px.bar(
        country_counts,
        x="count",
        y="country_of_citizenship",
        orientation="h",
        color="country_of_citizenship",
        labels={"count": "Number of Billionaires", "country_of_citizenship": "Country"}
    )
    fig_country.update_layout(yaxis={"categoryorder": "total ascending"}, showlegend=False)

    st.plotly_chart(fig_country, use_container_width=True)

with col_category:
    st.subheader("Top Business Categories by Billionaire Count")

    category_counts = (
        filtered_df[filtered_df["business_category"] != "Unspecified Category"]
        .drop_duplicates(subset="full_name")["business_category"]
        .value_counts()
        .head(top_n)
        .reset_index()
    )
    category_counts.columns = ["business_category", "count"]

    fig_category = px.bar(
        category_counts,
        x="count",
        y="business_category",
        orientation="h",
        color="business_category",
        labels={"count": "Number of Billionaires", "business_category": "Category"}
    )
    fig_category.update_layout(yaxis={"categoryorder": "total ascending"}, showlegend=False)

    st.plotly_chart(fig_category, use_container_width=True)


st.subheader("Billionaire Count Over Time")

trend_countries = st.multiselect(
    "Select countries to compare (defaults to top 5)",
    options=countries,
    default=df["country_of_citizenship"].value_counts().head(5).index.tolist()
)

trend_df = df[df["country_of_citizenship"].isin(trend_countries)]
trend_counts = trend_df.groupby(["year", "country_of_citizenship"]).size().reset_index(name="count")

fig_trend = px.line(
    trend_counts,
    x="year",
    y="count",
    color="country_of_citizenship",
    markers=True,
    labels={"count": "Number of Billionaires", "year": "Year", "country_of_citizenship": "Country"}
)

st.plotly_chart(fig_trend, use_container_width=True)

st.write(f"Showing {len(filtered_df)} rows for years {selected_range[0]}–{selected_range[1]}")
st.write(filtered_df.head())