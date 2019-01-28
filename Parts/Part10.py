import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style

api_key = open('api_key.txt', 'r').read()
style.use('fivethirtyeight')

def state_list():
    fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return fiddy_states[0][1][2:]

def grab_initial_state_data():
    states = state_list()
    main_df = pd.DataFrame()

    for abbv in states:
        query = "FMAC/HPI_" + str(abbv)
        print("Running query for: " + query)
        df = quandl.get(query, authtoken=api_key)
        df.drop(columns=['NSA Value'], inplace=True)
        df.columns = [abbv]
        df[abbv] = (df[abbv] - df[abbv][0]) / df[abbv][0] * 100.0

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)

    with open('Pickles/fiddy_states3.pickle', 'wb') as pickle_out:
        pickle.dump(main_df, pickle_out)

def HPI_Benchmark():
    print("Running query for: FMAC/HPI_USA")
    df = quandl.get("FMAC/HPI_USA", authtoken=api_key)
    df.drop(columns=['NSA Value'], inplace=True)
    df.columns = ['United States']
    df["United States"] = (df["United States"] - df["United States"][0]) / df["United States"][0] * 100.0
    with open('Pickles/united_states.pickle', 'wb') as pickle_out:
        pickle.dump(df, pickle_out)

#grab_initial_state_data()
#HPI_Benchmark()

with open('Pickles/fiddy_states3.pickle', 'rb') as pickle_in:
    HPI_data = pickle.load(pickle_in)
HPI_data['TX1yr'] = HPI_data['TX'].resample('A').mean()
print(HPI_data[['TX','TX1yr']])
print()

print("Dropping NaN data from dataframe")
HPI_data.dropna(inplace=True)
print(HPI_data[['TX', 'TX1yr']])
print()

print("Only drop dataframe row if the all cells in row are NaN")
with open('Pickles/fiddy_states3.pickle', 'rb') as pickle_in:
    HPI_data = pickle.load(pickle_in)
HPI_data['TX1yr'] = HPI_data['TX'].resample('A').mean()
HPI_data.dropna(how='all',inplace=True)
print(HPI_data[['TX', 'TX1yr']])
print()

print("Forward fill dropped data. Any case of missing data will be filled with the most recent non-missing data")
with open('Pickles/fiddy_states3.pickle', 'rb') as pickle_in:
    HPI_data = pickle.load(pickle_in)
HPI_data['TX1yr'] = HPI_data['TX'].resample('A').mean()
HPI_data.fillna(method='ffill', inplace=True)
HPI_data.dropna(inplace=True)
print(HPI_data[['TX', 'TX1yr']])
print()

print("Backwards fill dropped data. Any case of missing data will be filled with the last non-missing data")
with open('Pickles/fiddy_states3.pickle', 'rb') as pickle_in:
    HPI_data = pickle.load(pickle_in)
HPI_data['TX1yr'] = HPI_data['TX'].resample('A').mean()
HPI_data.fillna(method='bfill', inplace=True)
HPI_data.dropna(inplace=True)
print(HPI_data[['TX', 'TX1yr']])
print()

print("Replace missing data with set value")
with open('Pickles/fiddy_states3.pickle', 'rb') as pickle_in:
    HPI_data = pickle.load(pickle_in)
HPI_data['TX1yr'] = HPI_data['TX'].resample('A').mean()
HPI_data.fillna(value=-99999, inplace=True)
HPI_data.dropna(inplace=True)
print(HPI_data[['TX', 'TX1yr']])
print()

# fig = plt.figure()
# ax1 = plt.subplot2grid((1,1), (0,0))
#
# HPI_data['TX'].plot(ax=ax1)
# HPI_data['TX1yr'].plot(color='k',ax=ax1)
#
# plt.legend().remove()
# plt.show()