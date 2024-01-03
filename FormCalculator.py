import json
from datetime import datetime
import os
def process_football_data(file_location):
    with open(file_location, 'r') as f:
        data = json.load(f)['response']

    unique_teams = sorted(set([x['teams']['home']['name'] for x in data]))

    team_matches = {team: [] for team in unique_teams}

    # Mapping dictionary
    form_mapping = {
        "null": 0,
        "W": 3,
        "D": 1,
        "L": 0
    }
    weightings = {
        "Weight_GS" : 0.3,
        "Weight_GC" : 0.2,
        "Weight_NRV": 0.5
    }
   

    def calculate_team_form(team_name, data):
        results_home = [x for x in data if x['teams']['home']['name'] == team_name]
        results_away = [x for x in data if x['teams']['away']['name'] == team_name]
        results = results_home + results_away

        for result in results:
            result['fixture']['date'] = datetime.fromisoformat(result['fixture']['date'].replace('Z', '+00:00')).isoformat()

        single_team_season = sorted(results, key=lambda x: x['fixture']['date'])

        matches = []


        for idx, match in enumerate(single_team_season):
            match_date = match["fixture"]["date"]
            selected_team = next(team for team in match["teams"].values() if team["name"] == team_name)

            if selected_team["winner"] is True:
                result = "W"
            elif selected_team["winner"] is False:
                result = "L"
            else:
                result = "D"

            if match['teams']['home']['name'] == team_name:
                home_away = 'home'
                other_team_name = match['teams']['away']['name']
                form_goals_scored = match['goals']['home']  # Assign match goals to form goals
                form_goals_conceded = match['goals']['away']  # Assign match goals to form goals
            else:
                home_away = 'away'
                other_team_name = match['teams']['home']['name']
                form_goals_scored = match['goals']['away']  # Assign match goals to form goals
                form_goals_conceded = match['goals']['home']  # Assign match goals to form goals

            form_length = min(idx, 5)
            form = [matches[i]["result"] for i in range(idx - form_length, idx)] if form_length > 0 else []
            total_goals_scored = sum([matches[i]['goals_scored'] for i in range(idx - form_length, idx)]) if form_length > 0 else 0
            total_goals_conceded = sum([matches[i]['goals_conceded'] for i in range(idx - form_length, idx)]) if form_length > 0 else 0
            
        
            while len(form) < 5:
                form.insert(0, None)


            matches.append({
                "date": match_date,
                "name": team_name,
                "home_away": home_away,
                "opponent": other_team_name,
                "result": result,
                "form": form[:],
                "goals_scored": form_goals_scored,  
                "goals_conceded": form_goals_conceded,  
                "total_goals_scored": total_goals_scored,  
                "total_goals_conceded": total_goals_conceded,
                "form_score": sum(form_mapping.get(item, 0) / 5 for item in form),
                "form_weighted" : round((weightings['Weight_GS'] * total_goals_scored) - (weightings['Weight_GC'] * total_goals_conceded) + (weightings['Weight_NRV'] * sum(form_mapping.get(item, 0) / 5 for item in form)), 2)

            })

        team_matches[team_name] = matches

    for team in unique_teams:
        calculate_team_form(team, data)

    def merge_opponent_form(team_name, team_matches):
        for game in team_matches[team_name]:
            opponent_name = game['opponent']
            opponent_data = next((opponent_game for opponent_game in team_matches[opponent_name] if opponent_game['date'] == game['date']), None)
            if opponent_data:
                game['opponent_form'] = opponent_data['form_score']
                game['opponent_form_weighted'] = opponent_data['form_weighted']
            else:
                game['opponent_form'] = None

        return team_matches[team_name]

    updated_team_matches = {team_name: merge_opponent_form(team_name, team_matches) for team_name in team_matches}

        # Generate output file name based on input file
    file_name = os.path.basename(file_location)
    output_file = f"/Users/tomadams/Documents/FootballAPI V2/Datasets/FormCalculatorOutput/team_matches_{file_name.split('_')[1]}_{file_name.split('_')[2].split('.')[0]}.json"

        # Write to a file with the generated output file name
    with open(output_file, 'w') as json_file:
        json.dump(updated_team_matches, json_file, indent=2)

    return updated_team_matches




