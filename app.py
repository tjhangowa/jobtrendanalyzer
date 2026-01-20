import streamlit as st
import pandas as pd

# 1. SETUP THE PAGE
st.set_page_config(page_title="Job Market Analyzer", page_icon="📊")
st.title("📊 Remote Job Market Analyzer")
st.badge("by: Tenzin Jhangowa")
st.write("This dashboard analyzes the latest backend jobs from WeWorkRemotely.")
st.link_button("WeWorkRemotely", url="https://www.weworkremotely.com")

# 2. LOAD THE DATA
# We use Pandas to read the CSV file you created in the previous step
try:
    df = pd.read_csv("real_jobs.csv")
    st.write(f"**Data Source:** Scanned {len(df)} job postings.")

    # Show the raw data table (interactive)
    with st.expander("View Raw Job List"):
        st.dataframe(df)

except FileNotFoundError:
    st.error("Could not find 'real_jobs.csv'. Please run scraper.py first!")
    st.stop()

# 3. ANALYZE THE DATA
# We need to count the keywords again based on the loaded data
keywords = {"Python": 0, "Java": 0, "Go": 0, "Spring": 0, "SQL": 0}

# Iterate through every row in the dataframe
for index, row in df.iterrows():
    title = str(row['title']).lower()

    # Check for keywords
    if "python" in title:
        keywords["Python"] += 1
    if "java" in title:
        keywords["Java"] += 1
    if "go" in title:
        keywords["Go"] += 1
    if "spring" in title:
        keywords["Spring"] += 1
    if "sql" in title:
        keywords["SQL"] += 1

# 4. VISUALIZE
st.subheader("🔥 Tech Stack Demand")

# Convert our dictionary to a Pandas DataFrame for charting
chart_data = pd.DataFrame({
    "Technology": list(keywords.keys()),
    "Job Count": list(keywords.values())
})

# specific Streamlit command to draw a bar chart
st.bar_chart(chart_data.set_index("Technology"))

# 5. INSIGHTS
top_tech = max(keywords, key=keywords.get)
st.success(f"**Insight:** The most in-demand technology right now is **{top_tech}**.")