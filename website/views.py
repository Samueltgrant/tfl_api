from flask import Blueprint, render_template, Response, request, url_for, redirect, session
from website.forms import JourneyDetailsForm
import json
import pandas as pd
from website.backend_functions import shortlisted_journeys
from website.api_keys import primary_key, secondary_key
from pprint import pprint

views = Blueprint('views', __name__)


df = pd.read_csv(r"D:\GitHub\tfl_api\tubes_df.csv")
if "Unnamed: 0" in df.columns:
    df.drop("Unnamed: 0", axis=1, inplace=True)

def check_input(value):
    pass


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        users = request.form.getlist('user_list')
        stations = request.form.getlist('station_list')
        colours = ["mediumpurple", "cadetblue", "rosybrown", "mediumaquamarine", "cyan"]
        input_data = [stations, users, colours]
        journey_cards = shortlisted_journeys(input_data, 3, df)

        session['journey_cards'] = journey_cards
        # print(session['journey_cards'])

        return redirect(url_for('views.results'))
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
        if request.form['go_button'] == 'option_1':
            print("option_1 clicked")
            session['journey'] = 'option_1'
            return redirect(url_for('views.journey'))
        elif request.form['go_button'] == 'option_2':
            print("option_2 clicked")
            return redirect(url_for('views.journey'))
        elif request.form['go_button'] == 'option_3':
            session['journey'] = 'option_3'
            return redirect(url_for('views.journey'))
        else:
            return redirect(url_for('views.journey'))
    return render_template('results.html')


@views.route('/journey')
def journey():
    if ('journey_cards' in session) and ('journey' in session):
        return render_template('journey.html')
    return redirect(url_for('views.home'))
