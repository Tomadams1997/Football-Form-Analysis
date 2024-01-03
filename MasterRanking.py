import os
import json
from collections import defaultdict

def merge_and_sort_files(directory):
    master_object = []

    # Get all JSON files in the directory
    file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.json')]

    # Iterate through each file and merge their content into master_object
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            data = json.load(file)
            master_object.extend(data)

    # Group teams by their leagues
    teams_by_league = defaultdict(list)
    for team in master_object:
        teams_by_league[team['league_id']].append(team)

    # Update the league position for each team within its league
    for league_teams in teams_by_league.values():
        league_teams.sort(key=lambda x: x['average_opponent_form'], reverse=False)
        for index, team in enumerate(league_teams, start=1):
            team['average_opponent_form_league_ranking'] = index
            team['league_position_opponent_form_differntial'] = team['final_standing'] - index

    # Flatten the grouped data for all leagues into a single list
    flattened_data = [team for league_teams in teams_by_league.values() for team in league_teams]

    # Sort flattened_data by 'average_opponent_form' in descending order
    sorted_data = sorted(flattened_data, key=lambda x: x['average_opponent_form'], reverse=True)

    # Writing the sorted and updated data to the output master file
    output_folder = '/Users/tomadams/Documents/FootballAPI V2/Datasets/MasterRanking'
    season = file_paths[0].split('_')[3].split('.')[0]  # Extracting season from the first file name
    output_file_name = f'Master_{season}.json'
    output_file_path = os.path.join(output_folder, output_file_name)
    with open(output_file_path, 'w') as output_file:
        json.dump(sorted_data, output_file, indent=2)

    return sorted_data
