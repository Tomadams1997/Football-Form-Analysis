import os
import json

def calculate_average_opponent_form(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
        
    with open("/Users/tomadams/Documents/FootballAPI V2/Datasets/LeagueIDs/leagueIDs.json", 'r') as league_file:
        league_data = json.load(league_file)
        
    with open("/Users/tomadams/Documents/FootballAPI V2/Datasets/Leagues_Standings/Standings_2022.json", 'r') as league_standing_file:
        league_standings = json.load(league_standing_file)

    # Create a dictionary to map league IDs to league names
    league_mapping = {league['league_id']: league['league_name'] for league in league_data}
    league_standing_mapping = {league_standing['team_name']:league_standing['league_position'] for league_standing in league_standings}
    # Your existing logic for calculating average opponent form
    team_stats = {}
    team_count = {}
    team_stats_weighted = {}

    for team, matches in data.items():
        for match in matches:
            team_name = match['name']
            opponent_form = match['opponent_form']
            opponent_form_weighted = match['opponent_form_weighted']
            
            if team_name not in team_stats:
                team_stats[team_name] = 0
                team_count[team_name] = 0
                

            if team_name not in team_stats_weighted:
                team_stats_weighted[team_name] = 0
                team_count[team_name] = 0
                
            team_stats[team_name] += opponent_form
            team_stats_weighted[team_name] += opponent_form_weighted
            team_count[team_name] += 1

    average_opponent_form = []
    
    for (team_name, total_form), (team_name_weighted, total_form_weighted) in zip(team_stats.items(), team_stats_weighted.items()):
        average_form = total_form / team_count[team_name]
        average_form_weighted = total_form_weighted / team_count[team_name]  # Use team_name to access team_count
        average_opponent_form.append({
            'team_name': team_name,
            'average_opponent_form': average_form,
            'average_opponent_form_weighted': average_form_weighted,
            'league_id': file_name.split('_')[2],
            'league_name': league_mapping[file_name.split('_')[2]],
            'final_standing': league_standing_mapping[team_name],
      
        })

    # Sorting the data by 'average_opponent_form' in descending order
    sorted_data = sorted(average_opponent_form, key=lambda x: x['average_opponent_form'], reverse=True)

    # Generating output file name
    league_id = file_name.split('_')[2]  # Extracting leagueId from file name
    season = file_name.split('_')[3].split('.')[0]  # Extracting season from file name
    output_file_name = f"ranking_output_{league_id}_{season}.json"

    # Path to output directory
    output_folder = '/Users/tomadams/Documents/FootballAPI V2/Datasets/RankingOutput'

    # Writing the sorted and calculated data to the output file
    output_file_path = os.path.join(output_folder, output_file_name)
    with open(output_file_path, 'w') as output_file:
        json.dump(sorted_data, output_file, indent=2)

# Example usage:
folder_path = '/Users/tomadams/Documents/FootballAPI V2/Datasets/FormCalculatorOutput'
file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.json')]

for file_path in file_paths:
    calculate_average_opponent_form(file_path)
