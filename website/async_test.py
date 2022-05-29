import aiohttp
import asyncio
import time
import requests
from datetime import datetime as dt
from operator import getitem
from collections import OrderedDict
from pprint import pprint

start = time.perf_counter()
example_stations = ['Edgware Road Underground Station']
# example_stations = ['Edgware Road, Edgware Road (Circle Line) Underground Station']

primary_key = '3e15461aaf2140a5828d429de1843794'
secondary_key = 'ed66bcb37e82467cb50413448cb4a667'


def api_key_error(get_request, start_point, end_point):
    # first 0 needs to actually order the list based on highest matchQualityScore - also not sure the .split will
    # always work.
    if 'fromLocationDisambiguation' in get_request.keys():
        if get_request['fromLocationDisambiguation'].get('disambiguationOptions', 0) != 0:

            print(f"from Disambiguation: {start_point}")
            start_point = get_request['fromLocationDisambiguation']['disambiguationOptions'][0]['place']['commonName']
            print("new start point:", start_point)
        elif get_request['toLocationDisambiguation'].get('disambiguationOptions', 0) != 0:
            print(f"to Disambiguation: {end_point}")
            end_point = get_request['toLocationDisambiguation']['disambiguationOptions'][0]['place']['commonName']
            print("new end pont:", end_point)
        else:
            print("GET not working")

        get_request = requests.get(f"https://api.tfl.gov.uk/journey/journeyresults/{start_point}/to/{end_point}&app_id={primary_key}&app_key={secondary_key}").json()
        return get_request['journeys'][0]  # select earliest route?

    elif get_request.get('httpStatusCode') == 404:
        print("404 Code Error.")
    else:
        print(f"JOURNEY {start_point}-> {end_point} NOT FOUND BY API")  # NEED PROPER EXCEPTION ROUTE HERE


async def get_station(session, url, start_point, end_point, user, colour):
    async with session.get(url) as resp:
        journey_legs = {}
        journey_dict = {'user': user,
                    'colour': colour,
                    'total_duration': 0,
                    'total_cost': 0,
                    'journey': journey_legs}

        if start_point == end_point:
            return journey_dict

        get_request = await resp.json()
        try:
            journey = get_request['journeys'][0]  # select earliest route?
        except KeyError as e:
            journey = api_key_error(get_request, start_point, end_point)

        for leg in journey['legs']:
            journey_legs[leg['instruction']['summary']] = {
                'transport_mode': leg['mode']['name'],
                'departure_time': dt.strptime(leg['departureTime'], '%Y-%m-%dT%H:%M:%S').strftime("%H:%M"),
                'departure_tdelta': (dt.strptime(leg['departureTime'], '%Y-%m-%dT%H:%M:%S') - dt.now()).seconds // 60,
                'arrival_time': dt.strptime(leg['arrivalTime'], '%Y-%m-%dT%H:%M:%S').strftime("%H:%M"),
                'departure_point': leg['departurePoint'],  # .get('commonName')
                'arrival_point': leg['arrivalPoint'],  # .get('commonName')
                'journey_summary': leg['instruction']['summary'],
                'duration': leg['duration'],
                'stop_points': [x.get('name') for x in leg['path']['stopPoints']]

            }
            stop_points = journey_legs[leg['instruction']['summary']]['stop_points']
            if len(stop_points) > 2:
                journey_legs[leg['instruction']['summary']]['stop_points'] = [x.replace(" Underground Station", "") for
                                                                              x in stop_points[:-1]]

        journey_dict['journey_legs'] = OrderedDict(
            sorted(journey_legs.items(), key=lambda x: dt.strptime(getitem(x[1], 'departure_time'), "%H:%M")))

        journey_dict['total_duration'] = journey['duration']
        try:
            journey_dict['total_cost'] = int(journey['fare']['totalCost'])
        except KeyError as e:
            journey_dict['total_cost'] = 0
            print(f"KeyError {e} does not exist between {start_point} -> {end_point}.")
        return journey_dict


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for end_station in example_stations:
            initial_station = "Queen's Park Underground Station"
            url = f"https://api.tfl.gov.uk/journey/journeyresults/{initial_station}/to/{end_station}&app_id={primary_key}&app_key={secondary_key}"
            tasks.append(asyncio.ensure_future(get_station(session, url, initial_station, end_station, 'Sam', 'Blue')))

        total_journeys = await asyncio.gather(*tasks)
        for journey in total_journeys:
            print(journey)


asyncio.run(main())
end = time.perf_counter()
print(end - start)
