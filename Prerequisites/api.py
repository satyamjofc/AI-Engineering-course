import requests
import json
import time

url = "https://api.genderize.io?name=luc"

# response = requests.get(url)
# data = response.json()
# new_data = json.dumps(data, indent = 4)

# with open("api_ans.txt", "w") as file:
#     file.write(data)


retry = 3

for attempt in range(retry):
    try:
        response = requests.get(url)
        response.raise_for_status()

        print(response.json())
        break
    
    except requests.exceptions.RequestException as e:
        print(f"Attempt {attempt + 1} failed")

        if attempt < retry - 1:
            time.sleep(2)
        else:
            print("All retries failed")