import requests

team_id = "cc85cc50-09c7-42ab-8abb-136cec334e71"
url = "https://api.frame.io/v2/teams/" + team_id + "/projects"

payload = {
    "name" : "teste  "
}

headers = {
  "Content-Type": "application/json",
  "Authorization": "Bearer fio-u-KCOIl1lTWtAsW5lQzWa7ohesowh3dPqOeNOYaUd0wZid_8a4UgXSWK1O04sd7VJv"
}

response = requests.post(url, json=payload, headers=headers)

data = response.json()
print(data)