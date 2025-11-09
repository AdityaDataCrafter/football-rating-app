import streamlit as st
import pandas as pd
import gspread as gs
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- Google Sheet setup ---
SHEET_NAME = "Football_Ratings"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials
creds = Credentials.from_service_account_file("football-ratingsapp-e25de5e18c9b.json", scopes=SCOPES)
client = gs.authorize(creds)
sheet = client.open("Football Ratings spreadsheet").sheet1

# --- Streamlit UI ---
st.set_page_config(page_title="Football Player Ratings", page_icon="⚽", layout="centered")
st.title("⚽ Daily Football Player Rating")
st.markdown("Rate your favourite player and see the live leaderboard below!")

# --- Input form ---
with st.form("rating_form"):
    player = st.text_input("Enter Player Name:")
    rating = st.slider("Rate this player (1 to 10):", 1, 10, 5)
    reviewer = st.text_input("Your Name (optional):")
    submitted = st.form_submit_button("Submit Rating")

if submitted:
    if player.strip():
        date_today = datetime.today().strftime('%Y-%m-%d')
        sheet.append_row([player, rating, reviewer, date_today])
        st.success(f"✅ Rating for *{player}* submitted successfully!")
    else:
        st.error("Please enter a player name before submitting.")

# --- Leaderboard ---
st.subheader("🏆 Live Leaderboard")

data = pd.DataFrame(sheet.get_all_records())
if not data.empty:
    leaderboard = (
        data.groupby("Player")["Rating"]
        .mean()
        .reset_index()
        .sort_values(by="Rating", ascending=False)
    )
    leaderboard["Rating"] = leaderboard["Rating"].round(2)
    st.dataframe(leaderboard, use_container_width=True)
    st.bar_chart(leaderboard.set_index("Player"))
else:
    st.info("No ratings yet. Be the first to rate!")
