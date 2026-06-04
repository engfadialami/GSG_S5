import pandas as pd
import os

# Google Drive share links
chess_link = "https://drive.google.com/file/d/1eR3NZtwIC6ECN3vhtrynqmx8okG0twA7/view?usp=sharing"
player_registry_link = "https://drive.google.com/file/d/1wCSAkGagMzWiToedLC3ZGo_lGf_laF-k/view?usp=sharing"

# Convert Google Drive links to direct download links
chess_url = "https://drive.google.com/uc?id=" + chess_link.split("/")[-2]
player_registry_url = "https://drive.google.com/uc?id=" + player_registry_link.split("/")[-2]

# File paths
chess_path = "data/raw/chess_games.csv"
player_registry_path = "data/raw/player_registry.csv"

# Create folder
os.makedirs("data/raw", exist_ok=True)


# ---------- Chess Games ----------
if os.path.exists(chess_path):
    print(f"Loading from cache: {chess_path}")
    df_chess = pd.read_csv(chess_path)
else:
    print("Downloading chess_games.csv...")
    df_chess = pd.read_csv(chess_url)
    df_chess.to_csv(chess_path, index=False)
    print(f"Saved to {chess_path}")

# ---------- Player Registry ----------
if os.path.exists(player_registry_path):
    print(f"Loading from cache: {player_registry_path}")
    df_players = pd.read_csv(player_registry_path)
else:
    print("Downloading player_registry.csv...")
    df_players = pd.read_csv(player_registry_url)
    df_players.to_csv(player_registry_path, index=False)
    print(f"Saved to {player_registry_path}")

# Check datasets
print("Chess games shape:", df_chess.shape)
print(df_chess.columns.tolist())

print("\nPlayer registry shape:", df_players.shape)
print(df_players.columns.tolist())

print("\n--- Questions on chess_games.csv ---")

# Q1: How many records are there?
print("Q1 chess games Records:", len(df_chess))
print("Q1 player registry Records:", len(df_players))

# Q2: How many exact duplicate rows exist?
print("Q2 Exact duplicate rows:", df_chess.duplicated().sum())
print("Q2 Exact duplicate rows in player registry:", df_players.duplicated().sum())

# Q3: How many duplicate move sequences exist?
print("Q3 Duplicate move sequences:", df_chess["moves"].duplicated().sum())

# Q4: What percentage of opening_response is missing?
print("Q4 opening_response missing %:", df_chess["opening_response"].isna().mean() * 100)

# Q5: What percentage of opening_variation is missing?
print("Q5 opening_variation missing %:", df_chess["opening_variation"].isna().mean() * 100)

# Q6: What is the minimum number of turns?
print("Q6 Minimum turns:", df_chess["turns"].min())
print(df_chess[df_chess["turns"] == df_chess["turns"].min()])

print(50*"=")

# ---------- Stage 2: Build clean_chess pipeline ----------

# Start from the original chess dataframe
df_clean = df_chess.copy()

# 2a: Parse time_increment into time_base and time_inc
df_clean[["time_base", "time_inc"]] = (
    df_clean["time_increment"]
    .str.split("+", expand=True)
    .astype(int)
)
print(df_chess.shape)
print(df_chess.columns.tolist())
print(df_clean.shape)
print(df_clean.columns.tolist())

# 2b: Add rating difference
df_clean["rating_diff"] = (
    df_clean["white_rating"] - df_clean["black_rating"]
)
print(df_clean.shape)
print(df_clean.columns.tolist())

# 2c: Extract opening family before ":"
df_clean["opening_family"] = (
    df_clean["opening_fullname"]
    .str.split(":")
    .str[0]
    .str.strip()
)
print("Extracted opening family unique values:")
print(df_clean.shape)
print(df_clean.columns.tolist())
print(df_clean["opening_family"].head(10))

# Q9: How many unique opening families exist?
print("Q9: How many unique opening families exist?")
print("Unique opening families:", df_clean['opening_family'].nunique())

# 2d: Drop high-null column
df_clean = df_clean.drop(columns=["opening_response"])
print(df_clean.shape)
print(df_clean.columns.tolist())

# 2e: Flag short/suspicious games
df_clean["is_suspicious"] = df_clean["turns"] < 5
print(df_clean.shape)
print(df_clean.columns.tolist())

print("Q8: How many games are flagged as suspicious (< 5 turns)?")
print("Suspicious games:", df_clean["is_suspicious"].sum())

df_fadi = df_clean[df_clean["is_suspicious"] == False]
print(df_fadi.shape)

# 2f: Validate
assert df_clean["rating_diff"].notna().all()
assert df_clean.duplicated().sum() == 0

print("Unique opening families:", df_clean['opening_family'].nunique())
# print("Unique opening families:", df_clean['opening_family'].unique())
print("Q7: After adding rating_diff, what percentage of games did the higher-rated player win?")
df_clean["higher_rated"]= df_clean["rating_diff"].apply\
    (lambda x: "White" if x > 0 else ("Black" if x < 0 else "Equal"))
# higher_rated_won = (
#     ((df_clean['rating_diff'] > 0) & (df_clean['winner'] == 'White'))
#     |
#     ((df_clean['rating_diff'] < 0) & (df_clean['winner'] == 'Black'))
# )
higher_rated_won = (
    ((df_clean['higher_rated'] == "White") & (df_clean['winner'] == 'White'))
    |
    ((df_clean['higher_rated'] == "Black") & (df_clean['winner'] == 'Black'))
)
print(f"Higher rated won: {round(len(df_clean[higher_rated_won]) / len(df_clean) * 100, 2)}%")

print("Win percentages:")
print(df_clean['winner'].value_counts(normalize=True) * 100)

# # Show result
# print(df_clean.head())
# print(df_clean.shape)
# print(df_clean.columns.tolist())

# print("Suspicious games:", df_clean["is_suspicious"].sum())

# Q11: What is the most common way games end (victory_status)?
print("Q11: What is the most common way games end (victory_status)?")
print(df_clean['victory_status'].value_counts())
# print(df_clean['victory_status'].unique())