import quandl
import pickle

api_key = open('api_key.txt', 'r').read()

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

def mortgage_30y():
    df = quandl.get("FMAC/MORTG", trim_start="1975-01-01", authtoken=api_key)
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('M').mean()

    with open('Pickles/30_Year_Mort_Rate.pickle', 'wb') as pickle_out:
        pickle.dump(df, pickle_out)

#grab_initial_state_data()
#HPI_Benchmark()
#mortgage_30y()


with open('Pickles/fiddy_states3.pickle', 'rb') as pickle_in:
    HPI_data = pickle.load(pickle_in)

with open('Pickles/united_states.pickle', 'rb') as pickle_in:
    HPI_Bench = pickle.load(pickle_in)

with open('Pickles/30_Year_Mort_Rate.pickle', 'rb') as pickle_in:
    m30 = pickle.load(pickle_in)

print("Joining HPI Benchmark and Mortgage data")
m30.columns = ['M30']
HPI = HPI_Bench.join(m30)
print(HPI.head())
print()

print("Correlation data between the HPI benchmark and the 30 Year Mortgage Rate")
print(HPI.corr())
print()

print("Correlation between the 30 Year mortgage rate and each state")
state_HPI_30 = HPI_data.join(m30)
print(state_HPI_30.corr())
print()

print("Selecting just the M30 column for each state")
state_HPI_30 = HPI_data.join(m30)
print(state_HPI_30.corr()['M30'])
print()

print("Using .describe() on the M30 column")
state_HPI_30 = HPI_data.join(m30)
print(state_HPI_30.corr()['M30'].describe())
print()

