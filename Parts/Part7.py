import quandl
import pandas as pd
import pickle

api_key = open('api_key.txt', 'r').read()

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

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)

    with open('Pickles/fiddy_states.pickle', 'wb') as pickle_out:
        pickle.dump(main_df, pickle_out)

#grab_initial_state_data()

with open('Pickles/fiddy_states.pickle', 'rb') as pickle_in:
    HPI_data = pickle.load(pickle_in)
    print(HPI_data)

#Pandas method of pickling
HPI_data.to_pickle('Pickles/pandas_pickle.pickle')
HPI_data2 = pd.read_pickle('Pickles/pandas_pickle.pickle')
print(HPI_data2)

