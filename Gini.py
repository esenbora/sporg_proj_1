import pandas as pd
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import matplotlib.cm as cm


# League file paths
league_files = {
    "Premier League": "Premier_League_2015_to_2025.csv",
    "Serie A": "data/omer/Serie_A_2015_to_2025.csv",
    "Bundesliga": "data/omer/Bundesliga_2015_to_2025.csv",
    "La Liga": "data/omer/La_Liga_2015_to_2025.csv",
    "Ligue 1": "data/omer/Ligue_1_2015_to_2025.csv",
    "Super Lig": "data/omer/Super_Lig_2015_to_2025.csv",
}


def gini(array):
    array = np.sort(array)
    n = len(array)
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * array) / np.sum(array) / n) - (n + 1) / n
gini_all = {}
gini_top5 = {}
gini_middle = {}
gini_bottom5 = {}

# Her lig için hesaplama

for league, file_path in league_files.items():
    df = pd.read_csv(file_path)
    df["Pts/Match"] = pd.to_numeric(df["Pts/Match"], errors="coerce")
    df["Position"] = pd.to_numeric(df["Position"], errors="coerce")

    gini_all_seasons = []
    gini_top5_seasons = []
    gini_middle_seasons = []
    gini_bottom5_seasons = []

    target_seasons = ["24/25"]
    for season in target_seasons:
        season_df = df[df["Season"] == season].sort_values("Position")

        # All teams
        pts_all = season_df["Pts/Match"].dropna().values
        if len(pts_all) > 1:
            gini_all_seasons.append(gini(pts_all))

        # Top 5
        top5 = season_df.nsmallest(5, "Position")["Pts/Match"].dropna().values
        if len(top5) > 1:
            gini_top5_seasons.append(gini(top5))

        # Middle (positions 6–14)
        middle = season_df[(season_df["Position"] >= 6) & (season_df["Position"] <= 14)]["Pts/Match"].dropna().values
        if len(middle) > 1:
            gini_middle_seasons.append(gini(middle))

        # Bottom 5
        bottom5 = season_df.nlargest(5, "Position")["Pts/Match"].dropna().values
        if len(bottom5) > 1:
            gini_bottom5_seasons.append(gini(bottom5))

    # Ortalama Gini’ler
    gini_all[league] = np.mean(gini_all_seasons) if gini_all_seasons else None
    gini_top5[league] = np.mean(gini_top5_seasons) if gini_top5_seasons else None
    gini_middle[league] = np.mean(gini_middle_seasons) if gini_middle_seasons else None
    gini_bottom5[league] = np.mean(gini_bottom5_seasons) if gini_bottom5_seasons else None



gini_df = pd.DataFrame({
    "League": list(league_files.keys()),
    "All Teams": [gini_all[l] for l in league_files.keys()],
    "Top 5": [gini_top5[l] for l in league_files.keys()],
    "Middle (6–14)": [gini_middle[l] for l in league_files.keys()],
    "Bottom 5": [gini_bottom5[l] for l in league_files.keys()]
})

print("\nAverage Gini Index by League:")


print(gini_df.round(3))


plt.style.use("seaborn-v0_8-muted")
categories = ["All Teams", "Top 5", "Middle (6–14)", "Bottom 5"]
colors = ["#2E8B57", "#1E90FF", "#DAA520", "#DC143C"]

for i, cat in enumerate(categories):
    plt.figure(figsize=(8, 6))
    sorted_df = gini_df.sort_values(by=cat, ascending=False)
    bars = plt.bar(sorted_df["League"], sorted_df[cat], color=colors[i], alpha=0.85)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 0.002, f"{height:.3f}",
                 ha="center", fontsize=9, fontweight="bold")
    plt.title(f"Average Gini Index of Pts/Match – {cat}")
    plt.ylabel("Average Gini Index")
    plt.xlabel("League")
    plt.ylim(0, 0.3)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.show()

