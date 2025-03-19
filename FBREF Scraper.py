import json
import requests
import urllib
import pandas as pd
import time
import re
from bs4 import BeautifulSoup
from functools import reduce
import sys
from urllib.error import HTTPError

"""
This program will get summary player data for each game played in the top 5 
European football leagues from the website fbref.com
"""


def get_data_info(league_index, season_index):
    # all possible leagues and seasons
    leagues = [
        {"id": "9", "name": "Premier-League"}, {"id": "12", "name": "La-Liga"},
        {"id": "11", "name": "Serie-A"}, {"id": "13", "name": "Ligue-1"}, {"id": "20", "name": "Bundesliga"}
    ]
    seasons = ["2017-2018", "2018-2019", "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "2024-2025"]

    league_id = leagues[league_index]["id"]
    league = leagues[league_index]["name"]
    season = seasons[season_index]

    url = f"https://fbref.com/en/comps/{league_id}/{season}/schedule/{season}-{league}-Scores-and-Fixtures"
    return url, league, season


def get_fixture_data(url, league, season):
    print("Getting fixture data...")
    # create empty data frame and access all tables in url
    fixture_data = pd.DataFrame([])
    tables = pd.read_html(url)

    # get fixtures
    fixtures = tables[0][
        ["Wk", "Day", "Date", "Time", "Home", "Away", "xG", "xG.1", "Score", "Attendance", "Referee"]].dropna()
    fixtures["season"] = season  # url.split("/")[6]
    fixture_data = pd.concat([fixture_data, fixtures])

    # assign id for each game
    fixture_data["game_id"] = fixture_data.index

    # export to csv file
    fixture_data.reset_index(drop=True).to_csv(
        f"data\\league-fixture\\csv\\{league.lower()}_{season.lower()}_fixture_data.csv",
        header=True, index=False, mode="w")
    print("Fixture data collected...")
    time.sleep(5)


def generate_json(directory):
    """
    Generate json file from all csv files located in a directory
    :param directory:
    :return: Success message
    """
    try:
        dic = {}
        for season in ["2017-2018", "2018-2019", "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024",
                       "2024-2025"]:
            for league in ["Premier-League", "La-Liga", "Serie-A", "Ligue-1", "Bundesliga"]:
                data = pd.read_csv(f"{directory}\\csv\\{league.lower()}_{season.lower()}_fixture_data.csv")
                dic[f"{season}_{league}"] = data.to_dict()

        with open(f'{directory}\\fixture_data.json', 'w') as fp:
            # fp.write(str(dict))
            json.dump(dic, fp, indent=4)
        return "Success"
    except Exception as e:
        return e


def get_match_links(url):
    print("Getting match links for a season...")
    # access and download content from url containing all fixture links
    match_links = []
    content = requests.get(url)
    print(content.status_code)

    soup = BeautifulSoup(content.text, "html.parser")  # switch to lxml
    rows = soup.find("tbody").find_all("td", attrs={"data-stat": "match_report"})
    match_links = []
    for row in rows:
        if row.find("a").get("href"):
            match_links.append(row.find("a").get("href"))

    time.sleep(5)


# def player_data(match_links, league, season):
#     # loop through all fixtures
#     player_data = pd.DataFrame([])
#     for count, link in enumerate(match_links):
#         try:
#             tables = pd.read_html(link)
#             for table in tables:
#                 try:
#                     table.columns = table.columns.droplevel()
#                 except Exception:
#                     continue
#
#             # get player data
#             def get_team_1_player_data():
#                 # outfield and goal keeper data stored in seperate tables
#                 data_frames = [tables[3], tables[9]]
#
#                 # merge outfield and goal keeper data
#                 df = reduce(lambda left, right: pd.merge(left, right,
#                                                          on=["Player", "Nation", "Age", "Min"], how="outer"),
#                             data_frames).iloc[:-1]
#
#                 # assign a home or away value
#                 return df.assign(home=1, game_id=count)
#
#             # get second teams  player data
#             def get_team_2_player_data():
#                 data_frames = [tables[10], tables[16]]
#                 df = reduce(lambda left, right: pd.merge(left, right,
#                                                          on=["Player", "Nation", "Age", "Min"], how="outer"),
#                             data_frames).iloc[:-1]
#                 return df.assign(home=0, game_id=count)
#
#             # combine both team data and export all match data to csv
#             t1 = get_team_1_player_data()
#             t2 = get_team_2_player_data()
#             player_data = pd.concat([player_data, pd.concat([t1, t2]).reset_index()])
#
#             print(f"{count + 1}/{len(match_links)} matches collected")
#             player_data.to_csv(f"{league.lower()}_{season.lower()}_player_data.csv",
#                                header=True, index=False, mode="w")
#         except:
#             print(f"{link}: error")
#         # sleep for 3 seconds after every game to avoid IP being blocked
#         time.sleep(3)


def get_match_data(url):
    # access and download content from url containing all fixture links
    req = urllib.request.Request(url)
    content = urllib.request.urlopen(req).read().decode('utf-8')  # requests is not working
    soup = BeautifulSoup(content, "lxml")  # switch to lxml

    cols = ["t1_captain", "t2_captain", "t1_formation", "t2_formation",
            "t1_possesion", "t2_possesion", "t1_passing", "t2_passing",
            "t1_shots", "t2_shots", "t1_saves", "t2_saves", "t1_cards", "t2_cards",
            "t1_fouls", "t2_fouls", "t1_corners", "t2_corners", "t1_crosses",
            "t2_crosses", "t1_touches", "t2_touches", "t1_tackles", "t2_tackles",
            "t1_interceptions", "t2_interceptions", "t1_aerials_won",
            "t2_aerials_won", "t1_clearances", "t2_clearances", "t1_offsides",
            "t2_offsides", "t1_goal_kicks", "t2_goal_kicks", "t1_throw_ins",
            "t2_throw_ins", "t1_long_balls", "t2_long_balls"]

    match_stats_df = pd.DataFrame(columns=cols)
    match_stats_df.to_csv("match_stats.csv", header=True, index=False, mode="w")
    # Getting captains
    datapoint_divs = soup.find_all("div", class_="datapoint")
    data_row = []
    for datapoint in datapoint_divs:
        if datapoint.a:
            data_row.append(datapoint.a.text)

    # Getting formations
    lineup_divs = soup.find_all("div", class_="lineup")
    for lineup in lineup_divs:
        data_row.append(re.findall(r"\([-\d]*\)", lineup.find_all("th")[0].text)[0])

    # Getting Possesion, Passing, Shots, Saves, Cards
    team_stats_div = soup.find("div", id="team_stats")
    tdatas = team_stats_div.find_all("td")
    for td in tdatas:
        data_row.append(td.text.strip("\n"))
        data_row = list(map(lambda x: x.replace("\xa0", " "), data_row))

    # Getting Fouls, Corners, Crosses, Touches, Tackles, Interceptions,
    # Aerials Won, Clearances, Offsides, Goal Kicks, Throw Ins, Long Balls
    team_stats_extra_div = soup.find("div", id="team_stats_extra")
    container_divs = team_stats_extra_div.find_all("div")
    for i, container in enumerate(container_divs):
        if len(container) < 20:
            try:
                int(container.text)
                data_row.append(container.text)
            except ValueError:
                pass

    match_stats_df.loc[0] = data_row
    match_stats_df.reset_index(drop=True).to_csv("match_stats.csv", header=False, index=False, mode="a")
    time.sleep(5)
    return match_stats_df

def main():
    # Get basic per match data
    for l_i in range(5):
        for s_i in range(8):
            url, league, season = get_data_info(l_i, s_i)
            get_fixture_data(url, league, season)
            # try taking match_links as input and see if they are same length
            # OR get each match's extra stats simultaneously.
            
            # match_links = get_match_links(url)

    generate_json("data\league-fixture")  # compile all csv files to generate a single json file

    # player_data(match_links, league, season)
    print("Data collected!")


if __name__ == "__main__":
    try:
        # main()
        x = get_match_data("https://fbref.com/en/matches/3a6836b4/Burnley-Manchester-City-August-11-2023-Premier-League")
        print(x)
    except HTTPError:
        print("The website refused access, try again later")
        time.sleep(5)
