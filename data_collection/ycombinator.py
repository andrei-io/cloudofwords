import json

with open("data.json") as f:
    data = json.load(f)

companies = data['results'][0]['hits']

# with open('../ml_classification/data_input/ycombinator.json', 'w') as f:
#     json.dump(companies, f)
print(len(companies))