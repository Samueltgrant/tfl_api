import asyncio
import time

from flask import Blueprint, render_template, Response, request, url_for, redirect, session
import json
import pandas as pd
from website.backend_functions import suggested_station_lookup, routes_request, average_station_scores, \
    gen_lollipop_diagrams
from website.api_keys import primary_key, secondary_key
from pprint import pprint
import sqlite3
from itertools import product

views = Blueprint('views', __name__)


def get_df():
    with sqlite3.connect('meetup.db') as conn:
        c = conn.cursor()
        data = pd.DataFrame(c.execute("SELECT * FROM lookup;"))
        return data


df = get_df()


def check_input(value):
    pass


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        start = time.perf_counter()
        session['station_options'] = {}
        users = request.form.getlist('user_list')
        stations = request.form.getlist('station_list')
        colours = ["mediumpurple", "cadetblue", "rosybrown", "mediumaquamarine", "cyan", 'palevioletred','crimson',
                   'sienna', 'darkslategrey']

        data_zip = zip(stations, users, colours)
        user_data = {}
        for tup in data_zip:
            user_data[tup[0]] = {'user': tup[1], 'colour': tup[2]}

        suggested_stations = suggested_station_lookup(stations)

        for station in suggested_stations:
            session['station_options'][station] = {'routes': {}}

        all_routes = [(x[0], x[1]) for x in list(product(suggested_stations, stations))]
        asyncio.run(routes_request(session, all_routes, user_data))
        average_station_scores(session, suggested_stations)
        gen_lollipop_diagrams(session)

        end = time.perf_counter()
        print(f"gathering results took: {round(end - start, 2)}s")

        return redirect(url_for('views.results'))

        # journey_cards = shortlisted_journeys(input_data, 3, df)
        #
        # session['journey_cards'] = journey_cards
        # # print(session['journey_cards'])
        #
        # return redirect(url_for('views.results'))
    return render_template('index.html')


@views.route('/results',  methods=['GET', 'POST'])
def results():
    # if 'journey_cards' in session:
    #     journey_cards = session['journey_cards']
    #     return render_template('results.html', journey_cards=journey_cards)
    #
    # print("Redirecting to index.html -> no session data.")
    # return redirect(url_for('views.home'))

    if request.method == 'POST':
        session['journey'] = request.form['go_button']
        return redirect(url_for('views.journey'))
    return render_template('results.html')


@views.route('/journey')
def journey():
    return render_template('journey.html')
    # if ('journey_cards' in session) and ('journey' in session):
    #     return render_template('journey.html')
    # return redirect(url_for('views.home'))
