import sqlite3
import pandas as pd
from pprint import pprint


def sqlify_station(station: str) -> str:
    return '_'.join(
        station.replace("&", 'ampersand').lower().replace(' underground station', '').replace("'", "").replace(".",
                                                                                                               "").replace(
            "-", " ").split(' '))


def create_lookup(df):
    with sqlite3.connect('../meetup.db') as conn:
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS lookup;")
        c.execute("CREATE TABLE lookup (station_full text, station_short text);")

        for station in list(df.columns)[2:]:
            query = f"ALTER TABLE lookup ADD {sqlify_station(station)} integer;"
            conn.execute(query)
        conn.commit()


def populate_lookup(df):
    with sqlite3.connect('../meetup.db') as conn:
        c = conn.cursor()
        for idx in list(df.index):
            values = list(df.iloc[idx])
            print(values[1], sqlify_station(values[1]))

            query = f"""INSERT INTO lookup VALUES ("{values[1]}", '{sqlify_station(values[1])}', {', '.join([sqlify_station(str(x)) for x in list(values[2:])])});"""
            c.execute(query)
        conn.commit()


if __name__ == '__main__':
    # def get_df():
    #     with sqlite3.connect('../meetup.db') as conn:
    #         c = conn.cursor()
    #         data = pd.DataFrame(c.execute("SELECT * FROM lookup;"))
    #         return data
    #
    #
    # df = get_df()
    # print(df.head())

    conn = sqlite3.connect('../meetup.db')
    c = conn.cursor()

    # df = pd.read_csv(r"D:\GitHub\tfl_api\tubes_df.csv")
    # create_lookup(df)
    # populate_lookup(df)

    df = pd.DataFrame(c.execute("SELECT station_full, station_short FROM lookup;"))
    pd.set_option('display.max_rows', None)
    print(list(df[0]))
    # station_list = ['charing_cross', 'baker_street', 'embankment']
    # station_nums = 4
    # query = f"SELECT station, {', '.join(station_list)}, ({' + '.join(station_list)}) AS added_time " \
    #         f"FROM lookup" \
    #         f";"
    #
    # print(query)
    # c.execute(query)
    #
    # # print(c.fetchall())
    #
    # data = pd.DataFrame(c.fetchall())
    # data.sort_values(by=4, axis=1)
    # print(data.head())