# GSG Advanced Course – Session 4 & 5

## Deep Data Handling & Pipelines

### Author

Fady Alami

---

# Project Overview

This project analyzes the `chess_games.csv` and `player_registry.csv` datasets as part of the GSG Advanced Course Sessions 4–5 assignment. The objective was to apply data profiling, cleaning, transformation, validation, merging, and visualization techniques using Python and Pandas.

The work was completed in a single Python script (`s5_1.py`) following the stages presented during the course.

---

# Dataset Information

## chess_games.csv

Raw dataset containing information about online chess games.

### Initial Profiling

* Total records: 20,058
* Exact duplicate rows: 0
* Duplicate move sequences: 1,138
* Missing opening_response: approximately 94%
* Missing opening_variation: approximately 28%
* Minimum number of turns: 1

### Observations

Games with only one turn were considered suspicious because a normal chess game typically contains more than one move. These games may represent resignations, abandoned games, or timeouts.

---

## player_registry.csv

Companion dataset containing player information such as usernames and countries.

Used later in the project for merge operations and country standardization.

---

# Stage 1 – Data Profiling

The dataset was profiled before any modifications.

The following checks were performed:

1. Dataset shape.
2. Duplicate rows.
3. Duplicate move sequences.
4. Missing value percentages.
5. Minimum turn counts.
6. General data quality inspection.

This stage helped identify which columns required cleaning and which columns were suitable for analysis.

---

# Stage 2 – Data Cleaning Pipeline

A cleaned dataframe (`df_clean`) was created from the original dataframe to preserve the raw data.

## 1. Parse time_increment

Original format:

```text
10+5
15+10
5+0
```

Converted into:

* time_base
* time_inc

Example:

```text
10+5 → time_base=10 , time_inc=5
```

This was implemented using:

```python
.str.split("+", expand=True)
.astype(int)
```

---

## 2. Rating Difference

A new column was created:

```python
rating_diff = white_rating - black_rating
```

Purpose:

To determine which player entered the game with the higher rating.

---

## 3. Opening Family Extraction

The opening family was extracted from the full opening name.

Example:

```text
"Sicilian Defense: Dragon Variation"
```

became

```text
"Sicilian Defense"
```

This allowed grouping openings at a higher level.

---

## 4. Dropping High-Null Columns

The column:

```text
opening_response
```

contained approximately 94% missing values.

Decision:

The column was dropped because the amount of missing data was too high to provide meaningful analytical value.

---

## 5. Suspicious Games

A new flag was added:

```python
is_suspicious = turns < 5
```

Purpose:

Identify games that were likely abandoned, resigned immediately, or otherwise unusual.

Result:

342 games were flagged.

---

## 6. Validation

The following validation checks were performed:

* rating_diff contains no missing values.
* No duplicate rows remain.

These checks confirmed that the transformed dataset was suitable for analysis.

---

# Stage 3 – Analytical Questions

## Q7 – Higher Rated Player Advantage

A new helper column was created:

```python
higher_rated
```

Possible values:

* White
* Black
* Equal

This allowed comparison between the stronger-rated player and the actual game winner.

Observation:

Higher-rated players won a majority of games, confirming that rating generally correlates with winning probability.

---

## Q8 – Suspicious Games

Games with:

```python
turns < 5
```

were counted.

Result:

342 suspicious games.

---

## Q9 – Opening Families

The number of unique opening families was calculated using:

```python
nunique()
```

Result:

227 unique opening families.

---

## Q10 – Win Rates

The percentage of:

* White wins
* Black wins
* Draws

was calculated.

Observation:

White had a slight advantage over Black.

---

## Q11 – Most Common Victory Status

The most frequent game ending method was determined using:

```python
value_counts()
```

Observation:

Resignation was the most common way games ended.

---

## Q12 – Victory Status Analysis

Game endings were grouped by victory status and compared.

Observation:

Drawn games tended to be among the longest games.

---

## Q13 – Most Popular Openings

Openings were analyzed separately for:

* White wins
* Black wins

Observation:

Sicilian Defense was the most common opening family for both White and Black victories.

---

## Q14 – Rated vs Unrated Games

White win rates were compared between:

* Rated games
* Unrated games

Observation:

The win rates were nearly identical.

---

## Q15 – Game Length Classification

Games were classified as:

* Short (<20 turns)
* Medium (20–60 turns)
* Long (>60 turns)

Implemented using:

```python
apply()
```

and a lambda expression.

Observation:

Most games fell into the Medium category.

---

# Stage 4 – Merge and Data Standardization

## Merge Operation

The chess dataset was merged with the player registry using:

```python
pd.merge()
```

The registry column:

```text
username
```

was renamed to:

```text
white_id
```

before merging.

This enabled matching players across both datasets.

---

## Missing Registry Entries

After merging, some players had no corresponding registry entry.

These were identified using:

```python
isna()
```

and counted both as:

* Missing rows
* Missing unique players

---

## Country Standardization

Multiple country representations existed:

Examples:

```text
US
USA
united states
```

```text
GB
UK
united kingdom
```

```text
RUS
russian federation
```

A mapping dictionary was created to standardize these values.

Purpose:

Improve consistency and prevent duplicate country categories.

---

# Visualizations

Three visualizations were produced.

## 1. Wins by Color

Bar chart showing:

* White wins
* Black wins
* Draws

Saved as:

```text
output/wins_by_color.png
```

---

## 2. White Rating vs Turns

Scatter plot showing:

* White Rating
* Number of Turns

Observation:

No strong correlation was visible. Higher-rated players do not necessarily play longer games.

Saved as:

```text
output/white_rating_vs_turns.png
```

---

# Challenges and Obstacles Encountered

## 1. Understanding apply()

Initially, it was unclear how:

```python
apply(lambda ...)
```

operated on each row or value.

Through experimentation, it became clear that `apply()` passes each value individually to the lambda function.

---

## 2. Understanding groupby()

One of the most difficult concepts was understanding:

```python
groupby()
```

and the difference between:

```python
groupby(...)
```

and

```python
groupby(...)[column]
```

Particular attention was required to understand aggregation functions such as:

```python
count()
mean()
sum()
```

---

## 3. Understanding merge()

The merge operation required additional investigation.

Challenges included:

* Understanding `on=`
* Understanding `how="left"`
* Understanding why `username` needed to be renamed to `white_id`

---

## 4. Understanding map()

The country-cleaning task introduced:

```python
map()
```

which was initially confusing because values not found in the dictionary became `NaN`.

The role of:

```python
fillna()
```

was later understood as a method to preserve original values.

---

## 5. Plotting

Additional setup was required because:

```python
matplotlib
```

was not installed in the virtual environment.

After installation, bar charts and scatter plots were successfully generated and saved.

---

# Key Lessons Learned

* Profile before cleaning.
* Keep raw data untouched.
* Use derived columns to simplify analysis.
* Validate assumptions after cleaning.
* GroupBy is one of the most important Pandas tools.
* Merge operations require careful key matching.
* Visualization often reveals patterns not obvious from tables.
* Git commits should be created after completing each stage.

---

# Final Result

The project successfully completed all four stages of the pipeline challenge:

* Data Profiling
* Data Cleaning
* Analysis
* Merge and Visualization

All questions were answered programmatically and the resulting plots were generated successfully.
