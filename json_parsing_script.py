import json
import os
import pandas as pd

# Path where your JSON files are stored
json_folder = 'C:\\Users\\gadie\\json_files'  # Update this to your folder if needed

# List to store ball-by-ball records
all_balls = []

for filename in os.listdir(json_folder):
    if filename.endswith('.json'):
        filepath = os.path.join(json_folder, filename)
        with open(filepath, 'r') as file:
            match = json.load(file)
            
            match_id = filename.replace('.json', '')
            city = match.get('info', {}).get('city', 'Unknown')
            venue = match.get('info', {}).get('venue', 'Unknown')
            date = match.get('info', {}).get('dates', ['Unknown'])[0]
            teams = ', '.join(match.get('info', {}).get('teams', []))
            
            for inning in match.get('innings', []):
                team = inning.get('team', 'Unknown')
                
                for over_info in inning.get('overs', []):
                    over_number = over_info.get('over', -1)
                    
                    for delivery in over_info.get('deliveries', []):
                        record = {
                            'match_id': match_id,
                            'city': city,
                            'venue': venue,
                            'date': date,
                            'teams': teams,
                            'batting_team': team,
                            'over': over_number,
                            'batter': delivery.get('batter', None),
                            'bowler': delivery.get('bowler', None),
                            'non_striker': delivery.get('non_striker', None),
                            'batter_runs': delivery.get('runs', {}).get('batter', 0),
                            'extras_runs': delivery.get('runs', {}).get('extras', 0),
                            'total_runs': delivery.get('runs', {}).get('total', 0),
                            'extras_type': ', '.join(delivery.get('extras', {}).keys()) if 'extras' in delivery else None,
                            'wicket_kind': None,
                            'player_out': None,
                            'fielders': None
                        }
                        
                        # Handle wickets if present
                        if 'wickets' in delivery:
                            wicket = delivery['wickets'][0]
                            record['wicket_kind'] = wicket.get('kind', None)
                            record['player_out'] = wicket.get('player_out', None)
                            fielders = wicket.get('fielders', [])
                            record['fielders'] = ', '.join([f.get('name', 'Unknown') for f in fielders]) if fielders else None

                        all_balls.append(record)

# Convert to DataFrame
df = pd.DataFrame(all_balls)

# Export to CSV
df.to_csv('ball_by_ball_data.csv', index=False)
print("All JSON files converted to ball_by_ball_data.csv")
