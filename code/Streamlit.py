import streamlit as st
import pandas as pd
import numpy as np
import joblib
from collections import Counter
from sklearn.preprocessing import StandardScaler

# Load trained model
model = joblib.load('../model/poker_strategy_XG.pkl')
scaler = joblib.load('../model/XG_scaler.pkl')

# Title and description
st.title("Poker Action Predictor")
st.write("""
This app predicts the best poker action (Call, Raise, Fold) based on game details.
Fill in the information below, and get the optimal poker action for your hand.
""")

# --- Input Section ---
st.subheader("Input Game Details")

# Round selection
round_mapping = {"Pre-flop": 1, "Flop": 2, "Turn": 3, "River": 4}
round_label = st.selectbox("Round", options=list(round_mapping.keys()))
round_numeric = round_mapping[round_label]

# Pot and Player Stack
col1, col2 = st.columns(2)
with col1:
    pot = st.number_input("Pot Size", min_value=0, step=1, label_visibility="collapsed")
with col2:
    player_stack = st.number_input("Player Stack", min_value=0, step=1, label_visibility="collapsed")

# Card ranks and suits
col3, col4 = st.columns(2)
with col3:
    card1_rank = st.number_input("Card 1 Rank (2-14, where 14=Ace)", min_value=2, max_value=14, step=1)
with col4:
    card2_rank = st.number_input("Card 2 Rank (2-14, where 14=Ace)", min_value=2, max_value=14, step=1)

col5, col6 = st.columns(2)
with col5:
    card1_suit = st.selectbox("Card 1 Suit", options=[1, 2, 3, 4], format_func=lambda x: ["Clubs", "Diamonds", "Hearts", "Spades"][x-1])
with col6:
    card2_suit = st.selectbox("Card 2 Suit", options=[1, 2, 3, 4], format_func=lambda x: ["Clubs", "Diamonds", "Hearts", "Spades"][x-1])

# Community cards input
st.write("---")
st.subheader("Community Cards (if applicable)")

community1_rank, community2_rank, community3_rank, community4_rank, community5_rank = 0, 0, 0, 0, 0
community1_suit, community2_suit, community3_suit, community4_suit, community5_suit = 0, 0, 0, 0, 0

if round_numeric > 1:  # Flop, Turn, River
    col7, col8 = st.columns(2)
    with col7:
        community1_rank = st.number_input("Community Card 1 Rank", min_value=2, max_value=14, step=1)
        community2_rank = st.number_input("Community Card 2 Rank", min_value=2, max_value=14, step=1)
        community3_rank = st.number_input("Community Card 3 Rank", min_value=2, max_value=14, step=1)
    with col8:
        community1_suit = st.selectbox("Community Card 1 Suit", options=[1, 2, 3, 4], format_func=lambda x: ["Clubs", "Diamonds", "Hearts", "Spades"][x-1])
        community2_suit = st.selectbox("Community Card 2 Suit", options=[1, 2, 3, 4], format_func=lambda x: ["Clubs", "Diamonds", "Hearts", "Spades"][x-1])
        community3_suit = st.selectbox("Community Card 3 Suit", options=[1, 2, 3, 4], format_func=lambda x: ["Clubs", "Diamonds", "Hearts", "Spades"][x-1])

if round_numeric > 2:  # Turn, River
    col9, col10 = st.columns(2)
    with col9:
        community4_rank = st.number_input("Community Card 4 Rank", min_value=2, max_value=14, step=1)
    with col10:
        community4_suit = st.selectbox("Community Card 4 Suit", options=[1, 2, 3, 4], format_func=lambda x: ["Clubs", "Diamonds", "Hearts", "Spades"][x-1])

if round_numeric > 3:  # River
    col11, col12 = st.columns(2)
    with col11:
        community5_rank = st.number_input("Community Card 5 Rank", min_value=2, max_value=14, step=1)
    with col12:
        community5_suit = st.selectbox("Community Card 5 Suit", options=[1, 2, 3, 4], format_func=lambda x: ["Clubs", "Diamonds", "Hearts", "Spades"][x-1])

# --- Poker Hand Calculation ---
st.write("---")
st.subheader("Poker Hand Calculation")

all_ranks = [card1_rank, card2_rank, community1_rank, community2_rank, community3_rank, community4_rank, community5_rank]
all_suits = [card1_suit, card2_suit, community1_suit, community2_suit, community3_suit, community4_suit, community5_suit]

valid_ranks = [r for r in all_ranks if r > 0]
valid_suits = [s for s in all_suits if s > 0]

# Initialize poker_hand
poker_hand = 1  # Default: High Card

# Helper function to check for a straight
def has_straight(ranks):
    """Check if the ranks form a straight."""
    ranks = sorted(set(ranks))
    for i in range(len(ranks) - 4):
        if ranks[i+4] - ranks[i] == 4:
            return True
    return False

# Count occurrences of ranks and suits
rank_counts = Counter(valid_ranks)
suit_counts = Counter(valid_suits)

# Check hands
if suit_counts.most_common(1)[0][1] >= 5:
    main_suit = suit_counts.most_common(1)[0][0]
    suited_ranks = [r for r, s in zip(valid_ranks, valid_suits) if s == main_suit]
    if set(suited_ranks) >= {10, 11, 12, 13, 14}:
        poker_hand = 10
    elif has_straight(suited_ranks):
        poker_hand = 9
    else:
        poker_hand = 6
elif 4 in rank_counts.values():
    poker_hand = 8
elif 3 in rank_counts.values() and 2 in rank_counts.values():
    poker_hand = 7
elif has_straight(valid_ranks):
    poker_hand = 5
elif 3 in rank_counts.values():
    poker_hand = 4
elif list(rank_counts.values()).count(2) == 2:
    poker_hand = 3
elif 2 in rank_counts.values():
    poker_hand = 2

poker_hand_map = {
    10: "Royal Flush",
    9: "Straight Flush",
    8: "Four of a Kind",
    7: "Full House",
    6: "Flush",
    5: "Straight",
    4: "Three of a Kind",
    3: "Two Pair",
    2: "One Pair",
    1: "High Card"
}

# Prepare input data
input_data = pd.DataFrame({
    'round_label': [round_numeric],
    'pot': [pot],
    'player_stack': [player_stack],
    'poker_hand': [poker_hand],
    'card1_rank': [card1_rank],
    'card2_rank': [card2_rank],
    'card1_suit': [card1_suit],
    'card2_suit': [card2_suit],
    'community1_rank': [community1_rank],
    'community2_rank': [community2_rank],
    'community3_rank': [community3_rank],
    'community4_rank': [community4_rank],
    'community5_rank': [community5_rank],
    'community1_suit': [community1_suit],
    'community2_suit': [community2_suit],
    'community3_suit': [community3_suit],
    'community4_suit': [community4_suit],
    'community5_suit': [community5_suit],
})

scaled_input = scaler.transform(input_data)

# --- Prediction Section ---
st.write("---")
if st.button("Predict Action"):
    prediction = model.predict(scaled_input)[0]
    action_map = {0: "Call", 1: "Raise", 2: "Fold"}
    st.write(f"**Recommended Action:** {action_map[prediction]}")
    st.write(f"**Poker Hand:** {poker_hand_map[poker_hand]}")