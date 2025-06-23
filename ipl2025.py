import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("ipl_2025_deliveries.csv")

# Page configuration
st.set_page_config(page_title="IPL 2025 Deliveries Dashboard", layout="wide")
st.title("🏏 IPL 2025 Deliveries Data Dashboard")

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
selected_teams = st.sidebar.multiselect("Select Batting Teams:", df["batting_team"].unique(), default=df["batting_team"].unique())
selected_bowling_teams = st.sidebar.multiselect("Select Bowling Teams:", df["bowling_team"].unique(), default=df["bowling_team"].unique())
selected_innings = st.sidebar.multiselect("Select Innings:", df["innings"].unique(), default=df["innings"].unique())

# Filtered Data
filtered_df = df[
    (df["batting_team"].isin(selected_teams)) &
    (df["bowling_team"].isin(selected_bowling_teams)) &
    (df["innings"].isin(selected_innings))
]

# Striker (batter) search with stats
st.sidebar.header("🔎 Player Lookup")
search_player = st.sidebar.text_input("Enter player (striker) name")
if search_player:
    player_data = df[df["striker"].str.contains(search_player, case=False, na=False)]
    if not player_data.empty:
        st.subheader(f"📋 Stats for Striker: {search_player}")
        
        total_runs = player_data["runs_of_bat"].sum()
        total_balls = len(player_data)
        total_fours = len(player_data[player_data["runs_of_bat"] == 4])
        total_sixes = len(player_data[player_data["runs_of_bat"] == 6])
        strike_rate = round((total_runs / total_balls) * 100, 2) if total_balls else 0

        # Count dismissals if available
        dismissal_data = df[df["player_dismissed"] == search_player]
        dismissals = len(dismissal_data)
        batting_average = round(total_runs / dismissals, 2) if dismissals else "NA"

        st.markdown(f"""
        - 🏏 **Total Runs Scored:** {total_runs}  
        - 🎯 **Total Balls Faced:** {total_balls}  
        - 💥 **Fours:** {total_fours} | **Sixes:** {total_sixes}  
        - ⚡ **Strike Rate:** {strike_rate}  
        - 📊 **Batting Average:** {batting_average}
        """)

        st.dataframe(player_data)
    else:
        st.warning("Player not found.")

# Bowler search with stats
st.sidebar.header("🎯 Bowler Lookup")
search_bowler = st.sidebar.text_input("Enter player (bowler) name")
if search_bowler:
    bowler_data = df[df["bowler"].str.contains(search_bowler, case=False, na=False)]
    if not bowler_data.empty:
        st.subheader(f"📋 Stats for Bowler: {search_bowler}")
        total_balls = len(bowler_data)
        total_runs = (bowler_data["runs_of_bat"] + bowler_data["extras"] - bowler_data["byes"] - bowler_data["legbyes"]).sum()
        total_wickets = bowler_data["player_dismissed"].notna().sum()
        overs = total_balls // 6 + (total_balls % 6) / 6
        economy = round(total_runs / overs, 2) if overs else 0

        st.markdown(f"""
        - 🎯 **Total Balls Bowled:** {total_balls}  
        - 💥 **Total Wickets Taken:** {total_wickets}  
        - 🎯 **Total Runs Conceded:** {total_runs}  
        - 📉 **Economy Rate:** {economy} runs per over
        """)

        st.dataframe(bowler_data)
    else:
        st.warning("Bowler not found.")

# Top 10 Run Scorers
st.subheader("🏅 Top 10 Run Scorers")
top_batters = (
    filtered_df.groupby("striker")["runs_of_bat"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig1, ax1 = plt.subplots()
bars = ax1.bar(top_batters.index, top_batters.values, color="mediumblue")
ax1.set_ylabel("Runs Scored")
ax1.set_title("Top 10 Batters by Total Runs")
ax1.set_xticklabels(top_batters.index, rotation=45, ha='right')
for bar in bars:
    height = bar.get_height()
    ax1.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3), textcoords="offset points", ha='center', fontsize=8)
st.pyplot(fig1)

# Top 10 Wicket Takers
st.subheader("🎯 Top 10 Wicket Takers")
wicket_df = filtered_df[filtered_df["player_dismissed"].notna()]
top_bowlers = (
    wicket_df.groupby("bowler")["player_dismissed"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

fig2, ax2 = plt.subplots()
bars = ax2.bar(top_bowlers.index, top_bowlers.values, color="darkgreen")
ax2.set_ylabel("Wickets Taken")
ax2.set_title("Top 10 Bowlers by Wickets")
ax2.set_xticklabels(top_bowlers.index, rotation=45, ha='right')
for bar in bars:
    height = bar.get_height()
    ax2.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3), textcoords="offset points", ha='center', fontsize=8)
st.pyplot(fig2)

# Run Distribution Bar Chart
st.subheader("📊 Run Type Distribution (Bar Chart)")
run_types = {
    "Batsman Runs": filtered_df["runs_of_bat"].sum(),
    "Extras": filtered_df["extras"].sum(),
    "Wides": filtered_df["wide"].sum(),
    "Leg Byes": filtered_df["legbyes"].sum(),
    "Byes": filtered_df["byes"].sum(),
    "No Balls": filtered_df["noballs"].sum()
}

labels = list(run_types.keys())
values = list(run_types.values())

fig3, ax3 = plt.subplots()
bars = ax3.bar(labels, values, color='orange')
ax3.set_ylabel("Total Runs")
ax3.set_title("Run Type Distribution")
ax3.set_xticklabels(labels, rotation=45, ha='right')
for bar in bars:
    height = bar.get_height()
    ax3.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3), textcoords="offset points", ha='center', fontsize=8)
st.pyplot(fig3)

# Venue Analysis
st.subheader("📍 Matches Played per Venue")
venue_counts = df.groupby("venue")["match_id"].nunique().sort_values(ascending=False)

fig4, ax4 = plt.subplots(figsize=(10, 5))
bars = ax4.bar(venue_counts.index, venue_counts.values, color="crimson")
ax4.set_ylabel("Matches")
ax4.set_title("Matches Played per Venue")
ax4.set_xticklabels(venue_counts.index, rotation=45, ha='right')
for bar in bars:
    height = bar.get_height()
    ax4.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3), textcoords="offset points", ha='center', fontsize=8)
st.pyplot(fig4)

# Download button
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_ipl_2025_data.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.markdown("IPL 2025 Data Dashboard")
