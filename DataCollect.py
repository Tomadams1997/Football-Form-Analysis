from APICall import callApi
from FormCalculator import process_football_data
from RankingOutput import calculate_average_opponent_form
from CallFiles import process_folder
from MasterRanking import merge_and_sort_files


leagues = [39,78,61,135,140,94]
[callApi("e398bfba8fmsh0838226f51083d4p1f4897jsne333405c87d9", x, 2022) for x in leagues]

process_folder('/Users/tomadams/Documents/FootballAPI V2/Datasets/OriginalData',process_football_data)
process_folder('/Users/tomadams/Documents/FootballAPI V2/Datasets/FormCalculatorOutput',calculate_average_opponent_form)
merge_and_sort_files('/Users/tomadams/Documents/FootballAPI V2/Datasets/RankingOutput')
