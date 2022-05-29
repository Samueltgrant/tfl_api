import pandas as pd
import requests
from website.api_keys import primary_key, secondary_key
from datetime import datetime as dt
from operator import getitem
from collections import OrderedDict
import concurrent.futures
import matplotlib.pyplot as plt
import sqlite3
import aiohttp
import asyncio
from pprint import pprint


def sqlify_station(station: str) -> str:
    return '_'.join(
        station.replace("&", 'ampersand').lower().replace(' underground station', '').replace("'", "").replace(".",
                                                                                                               "").replace(
            "-", " ").split(' '))

def variance(data: list) -> float:
    mean = sum(data) / len(data)
    deviations = [(x - mean) ** 2 for x in data]
    return sum(deviations) / len(data)


def timed(fn):
    """Times the function its called on. Prints out time taken for sc"""
    from time import perf_counter
    from functools import wraps

    @wraps(fn)
    def inner(*args, **kwargs):
        start = perf_counter()
        result = fn(*args, **kwargs)
        end = perf_counter()
        elapsed = end - start

        print(f"{fn.__name__} took {elapsed:.3f}s to run.")
        return result
    return inner


@timed
def suggested_station_lookup(input_stations: list, return_number: int = 3):
    """get the n (return_number) number of stations that are quickest to get to for all stations.
    This function is where a lot more logic needs to be put. Needs to share the distance out better should try
    and find the halfway pointish.This will always just query the lookup table for speed. Actual journeys to be
    in following functions.
    """
    input_stations = [sqlify_station(x) for x in input_stations]
    with sqlite3.connect('meetup.db') as conn:
        c = conn.cursor()
        c.execute(f"SELECT station_full FROM ("
                  f"SELECT station_full, {', '.join(input_stations)}, ({' + '.join(input_stations)}) AS added_time "
                  f"FROM lookup "
                  f"ORDER BY added_time ASC "
                  f"LIMIT {return_number});")
        return [x[0] for x in c.fetchall()]


#
# @timed
# def route_details(start_point, end_point, user, colour):
#     """Returns only the useful information of the journey between two locations"""
#     journey_legs = {}
#     if start_point == end_point:
#         return {'user': user,
#                 'colour': colour,
#                 'total_duration': 0,
#                 'total_cost': 0,
#                 'journey': journey_legs}
#
#     get_request = requests.get(
#         f"https://api.tfl.gov.uk/journey/journeyresults/{start_point}/to/{end_point}&app_id={primary_key}&app_key={secondary_key}").json()
#
#     try:
#         journey = get_request['journeys'][0]  # select earliest route?
#     except KeyError as e:
#         # first 0 needs to actually order the list based on highest matchQualityScore - also not sure the .split will
#         # always work.
#         if 'fromLocationDisambiguation' in get_request.keys():
#             start_point_new, end_point_new = start_point, end_point
#             if get_request['fromLocationDisambiguation'].get('disambiguationOptions', 0) !=0:
#                 print(f"Disambiguation: {start_point}")
#                 start_point_new = get_request['fromLocationDisambiguation']['disambiguationOptions'][0]['place']['commonName'].split(",")[0]
#             elif get_request['toLocationDisambiguation'].get('disambiguationOptions', 0) !=0:
#                 print(f"Disambiguation: {end_point}")
#                 end_point_new = get_request['fromLocationDisambiguation']['disambiguationOptions'][0]['place']['commonName'].split(",")[0]
#             else:
#                 print("GET not working")
#             get_request = requests.get(
#                 f"https://api.tfl.gov.uk/journey/journeyresults/{start_point_new}/to/{end_point_new}&app_id={primary_key}&app_key={secondary_key}").json()
#             journey = get_request['journeys'][0]  # select earliest route?
#
#         elif get_request.get('httpStatusCode') == 404:
#             print("404 Code Error.")
#         else:
#             print(f"JOURNEY {start_point}-> {end_point} NOT FOUND BY API")  # NEED PROPER EXCEPTION ROUTE HERE
#
#     for leg in journey['legs']:
#         journey_legs[leg['instruction']['summary']] = {
#             'transport_mode': leg['mode']['name'],
#             'departure_time': dt.strptime(leg['departureTime'], '%Y-%m-%dT%H:%M:%S').strftime("%H:%M"),
#             'departure_tdelta': (dt.strptime(leg['departureTime'], '%Y-%m-%dT%H:%M:%S') - dt.now()).seconds // 60,
#             'arrival_time': dt.strptime(leg['arrivalTime'], '%Y-%m-%dT%H:%M:%S').strftime("%H:%M"),
#             'departure_point': leg['departurePoint'],  # .get('commonName')
#             'arrival_point': leg['arrivalPoint'],  # .get('commonName')
#             'journey_summary': leg['instruction']['summary'],
#             'duration': leg['duration'],
#             'stop_points': [x.get('name') for x in leg['path']['stopPoints']]
#
#         }
#         stop_points = journey_legs[leg['instruction']['summary']]['stop_points']
#         if len(stop_points) > 2:
#             journey_legs[leg['instruction']['summary']]['stop_points'] = [x.replace(" Underground Station", "") for x in stop_points[:-1]]
#
#     journey_legs = OrderedDict(sorted(journey_legs.items(), key=lambda x: dt.strptime(getitem(x[1], 'departure_time'), "%H:%M")))
#     try:
#         cost = int(journey['fare']['totalCost'])
#     except KeyError as e:
#         cost = 0
#         print(f"KeyError {e} does not exist between {start_point} -> {end_point}.")
#
#     return {'user': user,
#             'colour': colour,
#             'total_duration': journey['duration'],
#             'total_cost': cost,
#             'journey': journey_legs}

def gen_lollipop(station_dict: dict, suggested_station) -> None:
    data = []
    for key, value in station_dict['routes'].items():
        data.append({'user': value['user'], 'duration': value['total_duration'], 'colour': value['colour']})
    df = pd.DataFrame(data)
    duration = df['duration']
    fig, ax = plt.subplots()

    plt.axis('off')
    plt.axhline(y=duration.mean(), color='grey', linestyle='-')

    for t, y, c in zip(df["user"], df["duration"], df['colour']):
        ax.plot([t, t], [0, y], color=c, marker="o", markevery=(1, 2), linewidth=4, markersize=20,
                markerfacecolor=c, alpha=1,
                )

    ax.scatter(df['user'], df['duration'], c='red')
    ax.set_ylim(0, max(duration) * 1.2)

    fig.tight_layout()
    plt.savefig(
        fr"D:\GitHub\tfl_api\tfl_api\website\static\img\{suggested_station}.png")
    plt.close()



def gen_lollipop_diagrams(session) -> None:
    """Produces figure to be used as journey image in results page.

    inputs:
    session data"""
    for key, value in session['station_options'].items():
        gen_lollipop(value, key)





async def routes_request(session, routes, user_data):
    async with aiohttp.ClientSession() as sess:
        tasks = []
        for suggested_station, station_input in routes:
            url = f"https://api.tfl.gov.uk/journey/journeyresults/{station_input}/to/{suggested_station}&app_id={primary_key}&app_key={secondary_key}"
            tasks.append(asyncio.ensure_future(get_station(sess, url, station_input, suggested_station, user_data)))

        total_journeys = await asyncio.gather(*tasks)
        for index, journey in enumerate(total_journeys):
            station_input = journey['start_point']
            suggested_station = journey['end_point']
            session['station_options'][suggested_station]['routes'][station_input] = journey


# @timed
# def get_local_dict(suggested_station, input_stations, users, colours, number):
#     initial_dict = {'suggested_station': suggested_station.replace(" Underground Station", ""), 'routes': {}}
#     local_dict = routes_request(initial_dict, suggested_station, input_stations, users, colours)
#     pprint("local dict", local_dict)
#
#     # for route_index, input_station in enumerate(input_stations):
#     #     local_dict['routes'][f'route_{route_index + 1}'] = route_details(input_station, suggested_station,
#     #                                                                      user=users[route_index],
#     #                                                                      colour=colours[route_index])
#
#     duration_list = [value['total_duration'] for key, value in local_dict['routes'].items() if key.startswith("route_")]
#     cost_list = [value['total_cost'] for key, value in local_dict['routes'].items() if key.startswith("route_")]
#
#     local_dict['avg_duration'] = int(sum(duration_list) / len(duration_list))
#     local_dict['avg_cost'] = round(sum(cost_list) / len(cost_list) / 100, 2)
#     local_dict['equality_cost'] = round(variance([(x / 100) for x in cost_list]), 2)
#     local_dict['equality_duration'] = round(variance(duration_list), 2)
#
#     graph_data = [{'name': v['user'], 'duration': v['total_duration'],
#                    'colour': v['colour']} for k, v in local_dict['routes'].items()]
#     gen_lollipop(graph_data, suggested_station)
#
#     return local_dict


# @timed
# def shortlisted_journeys(user_data:list, return_number: int, df) -> dict:
#     """Takes the input_stations and the shortest stations to get to from the get_total_times func and returns the
#     updated times, as well as the journey information from each input station."""
#     input_stations, users, colours = user_data
#     suggested_stations = suggested_station_lookup(df, input_stations, return_number)
#
#     journey_dict = {}
#     idx = 1
#     for station in suggested_stations:
#         journey_dict[f'option_{idx}'] = get_local_dict(station, input_stations, users, colours, idx)
#         idx += 1
#     # with concurrent.futures.ProcessPoolExecutor() as executor:
#     #     results_index = 1
#     #     results = [executor.submit(get_local_dict, station, input_stations, users, colours, results_index) for station in suggested_stations]
#     #     for f in concurrent.futures.as_completed(results):
#     #         journey_dict[f'option_{results_index}'] = f.result()
#     #         results_index += 1
#     return journey_dict


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
            print("new end point:", end_point)
        else:
            print("GET not working")

        get_request = requests.get(f"https://api.tfl.gov.uk/journey/journeyresults/{start_point}/to/{end_point}&app_id={primary_key}&app_key={secondary_key}").json()
        try:
            return get_request['journeys'][0]  # select earliest route?
        except KeyError:
            pprint(get_request)
            return None

    elif get_request.get('httpStatusCode') == 404:
        print("404 Code Error.")
    else:
        print(f"JOURNEY {start_point}-> {end_point} NOT FOUND BY API")  # NEED PROPER EXCEPTION ROUTE HERE


async def get_station(session, url, start_point, end_point, user_data):
    async with session.get(url) as resp:
        journey_legs = {}
        journey_dict = {
                    'user': user_data[start_point].get('user'),
                    'colour': user_data[start_point].get('colour'),
                    'start_point': start_point,
                    'end_point': end_point,
                    'total_duration': 0,
                    'total_cost': 0,
                    'journey': journey_legs}

        get_request = await resp.json()

        if start_point == end_point:
            return journey_dict

        try:
            journey = get_request['journeys'][0]  # select earliest route?
        except KeyError as e:
            journey = api_key_error(get_request, start_point, end_point)
            if journey is None:
                return journey_dict # error

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


def average_station_scores(session, suggested_stations):
    for key in session['station_options'].keys():
        total_duration = [session['station_options'][key]['routes'][x].get('total_duration') for x in session['station_options'][key]['routes'].keys()]
        total_cost = [session['station_options'][key]['routes'][x].get('total_cost') for x in session['station_options'][key]['routes'].keys()]
        session['station_options'][key]['avg_duration'] = sum(total_duration) / len(total_duration)
        session['station_options'][key]['avg_cost'] = sum(total_cost) / len(total_cost)
        session['station_options'][key]['equality_cost'] = 1
        session['station_options'][key]['equality_duration'] = 1


# if __name__ == "__main__":
    # conn = sqlite3.connect('../meetup.db')
    # df = pd.read_sql_query("SELECT * FROM lookup", conn)
    #
    #
    # shortlisted_journeys(["Baker Street Underground Station",
    #                       "Holborn Underground Station",
    #                       "High Street Kensington Underground Station",
    #                       'Aldgate East Underground Station'], 3)








