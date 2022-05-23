import pandas as pd
import requests
from pprint import pprint
from website.api_keys import primary_key, secondary_key
from datetime import datetime as dt
from operator import getitem
from collections import OrderedDict
import concurrent.futures
import matplotlib.pyplot as plt


def variance(data: list) -> float:
    # print("VARIANCE", data)
    n = len(data)
    mean = sum(data) / n
    deviations = [(x - mean) ** 2 for x in data]
    return sum(deviations) / n


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
def get_total_times(df, input_stations: list, return_number):
    """get the n (return_number) number of stations that are quickest to get to for all stations.
    This function is where a lot more logic needs to be put. Needs to share the distance out better should try
    and find the halfway pointish.This will always just query the lookup table for speed. Actual journeys to be
    in following functions.
    """
    df['average_duration'] = sum([df[x] for x in input_stations]) / len(input_stations)
    df.sort_values("average_duration", inplace=True)
    return list(df['station'])[:return_number]


@timed
def route_details(start_point, end_point, user, colour):
    """Returns only the useful information of the journey between two locations"""
    journey_legs = {}
    if start_point == end_point:
        return {'user': user,
                'colour': colour,
                'total_duration': 0,
                'total_cost': 0,
                'journey': journey_legs}

    get_request = requests.get(
        f"https://api.tfl.gov.uk/journey/journeyresults/{start_point}/to/{end_point}&app_id={primary_key}&app_key={secondary_key}").json()

    try:
        journey = get_request['journeys'][0]  # select earliest route?
    except KeyError as e:
        # first 0 needs to actually order the list based on highest matchQualityScore - also not sure the .split will
        # always work.
        if 'fromLocationDisambiguation' in get_request.keys():
            start_point_new, end_point_new = start_point, end_point
            if get_request['fromLocationDisambiguation'].get('disambiguationOptions', 0) !=0:
                print(f"Disambiguation: {start_point}")
                start_point_new = get_request['fromLocationDisambiguation']['disambiguationOptions'][0]['place']['commonName'].split(",")[0]
            elif get_request['toLocationDisambiguation'].get('disambiguationOptions', 0) !=0:
                print(f"Disambiguation: {end_point}")
                end_point_new = get_request['fromLocationDisambiguation']['disambiguationOptions'][0]['place']['commonName'].split(",")[0]
            else:
                print("GET not working")
            get_request = requests.get(
                f"https://api.tfl.gov.uk/journey/journeyresults/{start_point_new}/to/{end_point_new}&app_id={primary_key}&app_key={secondary_key}").json()
            journey = get_request['journeys'][0]  # select earliest route?

        elif get_request.get('httpStatusCode') == 404:
            print("404 Code Error.")
        else:
            print(f"JOURNEY {start_point}-> {end_point} NOT FOUND BY API")  # NEED PROPER EXCEPTION ROUTE HERE

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
            journey_legs[leg['instruction']['summary']]['stop_points'] = [x.replace(" Underground Station", "") for x in stop_points[:-1]]

    journey_legs = OrderedDict(sorted(journey_legs.items(), key=lambda x: dt.strptime(getitem(x[1], 'departure_time'), "%H:%M")))
    try:
        cost = int(journey['fare']['totalCost'])
    except KeyError as e:
        cost = 0
        print(f"KeyError {e} does not exist.")

    return {'user': user,
            'colour': colour,
            'total_duration': journey['duration'],
            'total_cost': cost,
            'journey': journey_legs}


def gen_lollipop(data, suggested_station):
    df = pd.DataFrame(data)
    duration = df['duration']
    fig, ax = plt.subplots()

    plt.axis('off')
    plt.axhline(y=duration.mean(), color='grey', linestyle='-')

    for t, y, c in zip(df["name"], df["duration"], df['colour']):
        ax.plot([t, t], [0, y], color=c, marker="o", markevery=(1, 2), linewidth=4, markersize=20,
                markerfacecolor=c, alpha=1,
                )

    ax.scatter(df['name'], df['duration'], c='red')
    ax.set_ylim(0, max(duration) * 1.2)

    fig.tight_layout()
    plt.savefig(
        fr"D:\GitHub\tfl_api\tfl_api\website\static\img\{suggested_station}.png")
    plt.close()


@timed
def get_local_dict(suggested_station, input_stations, users, colours, number):
    local_dict = {'suggested_station': suggested_station.replace(" Underground Station", ""), 'routes': {}}
    for route_index, input_station in enumerate(input_stations):
        local_dict['routes'][f'route_{route_index + 1}'] = route_details(input_station, suggested_station,
                                                                         user=users[route_index],
                                                                         colour=colours[route_index])

    duration_list = [value['total_duration'] for key, value in local_dict['routes'].items() if key.startswith("route_")]
    cost_list = [value['total_cost'] for key, value in local_dict['routes'].items() if key.startswith("route_")]

    local_dict['avg_duration'] = int(sum(duration_list) / len(duration_list))
    local_dict['avg_cost'] = round(sum(cost_list) / len(cost_list) / 100, 2)
    local_dict['equality_cost'] = round(variance([(x / 100) for x in cost_list]), 2)
    local_dict['equality_duration'] = round(variance(duration_list), 2)

    graph_data = [{'name': v['user'], 'duration': v['total_duration'],
                   'colour': v['colour']} for k, v in local_dict['routes'].items()]
    gen_lollipop(graph_data, suggested_station)

    return local_dict


@timed
def shortlisted_journeys(user_data:list, return_number: int, df) -> dict:
    """Takes the input_stations and the shortest stations to get to from the get_total_times func and returns the
    updated times, as well as the journey information from each input station."""
    input_stations, users, colours = user_data
    suggested_stations = get_total_times(df, input_stations, return_number)

    journey_dict = {}
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results_index = 1
        results = [executor.submit(get_local_dict, station, input_stations, users, colours, results_index) for station in suggested_stations]
        for f in concurrent.futures.as_completed(results):
            journey_dict[f'option_{results_index}'] = f.result()
            results_index += 1
    return journey_dict


if __name__ == "__main__":
    df = pd.read_csv(r"/tfl_api/tubes_df.csv")

    if "Unnamed: 0" in df.columns:
        df.drop("Unnamed: 0", axis=1, inplace=True)

    shortlisted_journeys(["Baker Street Underground Station",
                          "Holborn Underground Station",
                          "High Street Kensington Underground Station",
                          'Aldgate East Underground Station'], 3)
