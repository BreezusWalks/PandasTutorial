import quandl
import pandas as pd
import pickle
from matplotlib import style

api_key = open('api_key.txt', 'r').read()
style.use('fivethirtyeight')

def state_abbvs():
    fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return fiddy_states[0][1][2:]

def grab_initial_state_data():
    main_df = pd.DataFrame()

    for abbv in state_abbvs():
        query = "FMAC/HPI_" + abbv
        df = quandl.get(query, authtoken=api_key)
        df.drop(columns=['NSA Value'], inplace=True)
        df.columns = [abbv]

        df[abbv] = (df[abbv] - df[abbv][0]) / df[abbv][0] * 100.0

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)

    with open('pickles/fiddy_states3.pickle', 'wb') as pickle_out:
        pickle.dump(main_df, pickle_out)

def HPI_Benchmark():
    df = quandl.get('FMAC/HPI_USA', authtoken=api_key)
    df.drop(columns=['NSA Value'], inplace=True)
    df.columns = ['United States']
    df['United States'] = (df["United States"]-df["United States"][0]) / df["United States"][0] * 100.0
    with open('pickles/united_states.pickle', 'wb') as pickle_out:
        pickle.dump(df, pickle_out)

#grab_initial_state_data()

HPI_data = pd.read_pickle('pickles/fiddy_states3.pickle')
HPI_State_Correlation = HPI_data.corr()
print(HPI_State_Correlation.describe())