import requests
from api_keys import primary_key, secondary_key
from pprint import pprint

start_point = "West Hampstead Underground Station"
start_point1 = "Stratford Underground Station"
end_point = "Baker Street Underground Station"


get_request = requests.get(
    f"https://api.tfl.gov.uk/journey/journeyresults/{start_point}/to/{end_point}&app_id={primary_key}&app_key={secondary_key}").json()


get_request1 = requests.get(
    f"https://api.tfl.gov.uk/journey/journeyresults/{start_point1}/to/{end_point}&app_id={primary_key}&app_key={secondary_key}").json()


pprint(get_request)
print("*" * 50)
pprint(get_request1)
