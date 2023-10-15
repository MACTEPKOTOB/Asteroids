import json
data = {
"previous_score" : 0
}


with open('data.json', 'w', encoding = 'utf-8') as file:
	json.dump(data, file, indent = 4)