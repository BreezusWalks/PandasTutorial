import quandl
import pickle
import pandas as pd

api_key = open('api_key.txt', 'r').read()
pd.set_option("display.max_columns", 10)

def state_list():
    fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return fiddy_states[0][1][2:]

def grab_initial_state_data():
    states = state_list()
    main_df = pd.DataFrame()

    for abbv in states:
        query = "FMAC/HPI_" + str(abbv)
        print("Getting data for: " + query)
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
    print("Getting data for: FMAC/HPI_USA")
    df = quandl.get("FMAC/HPI_USA", authtoken=api_key)
    df.drop(columns=['NSA Value'], inplace=True)
    df.columns = ['US_HPI']
    df["US_HPI"] = (df["US_HPI"] - df["US_HPI"][0]) / df["US_HPI"][0] * 100.0
    with open('Pickles/united_states2.pickle', 'wb') as pickle_out:
        pickle.dump(df, pickle_out)

def mortgage_30y():
    print("Getting data for: FMAC/MORTG")
    df = quandl.get("FMAC/MORTG", trim_start="1975-01-01", authtoken=api_key)
    df.columns = ['M30']
    df["M30"] = (df["M30"]-df["M30"][0]) / df["M30"][0] * 100.0
    df = df.resample('M').mean()

    with open('Pickles/30_Year_Mort_Rate.pickle', 'wb') as pickle_out:
        pickle.dump(df, pickle_out)

def sp500_data():
    print("Getting data for: MULTPL/SP500_REAL_PRICE_MONTH")
    df = quandl.get('MULTPL/SP500_REAL_PRICE_MONTH', trim_start='1975-01-01', authtoken=api_key)
    df.columns = ['sp500']
    df["sp500"] = (df["sp500"] - df["sp500"][0]) / df["sp500"][0] * 100.0
    df = df.resample('M').mean()

    with open('Pickles/sp500.pickle', 'wb') as pickle_out:
        pickle.dump(df, pickle_out)

def gdp_data():
    print("Getting data for: BCB/4385")
    df = quandl.get('BCB/4385', trim_start='1975-01-01', authtoken=api_key)
    df.columns = ['GDP']
    df["GDP"] = (df["GDP"] - df["GDP"][0]) / df["GDP"][0] * 100.0
    df = df.resample('M').mean()

    with open('Pickles/gdp.pickle', 'wb') as pickle_out:
        pickle.dump(df, pickle_out)

def us_unemployment():
    print("Getting data for: FRED/UNRATE")
    df = quandl.get('FRED/UNRATE', trim_start='1975-01-01', authtoken=api_key)
    df.columns = ['Unemployment Rate']
    df["Unemployment Rate"] = (df["Unemployment Rate"] - df["Unemployment Rate"][0]) / df["Unemployment Rate"][0] * 100.0
    df = df.resample('M').mean()

    with open('Pickles/us_unemployment.pickle', 'wb') as pickle_out:
        pickle.dump(df, pickle_out)

# grab_initial_state_data()
# HPI_Benchmark()
# mortgage_30y()
# sp500_data()
# gdp_data()
# us_unemployment()

with open('Pickles/fiddy_states3.pickle', 'rb') as pickle_in:
    HPI_data = pickle.load(pickle_in)
with open('Pickles/united_states2.pickle', 'rb') as pickle_in:
    HPI_Bench = pickle.load(pickle_in)
with open('Pickles/30_Year_Mort_Rate.pickle', 'rb') as pickle_in:
    m30 = pickle.load(pickle_in)
with open('Pickles/sp500.pickle', 'rb') as pickle_in:
    sp500 = pickle.load(pickle_in)
with open('Pickles/gdp.pickle', 'rb') as pickle_in:
    gdp = pickle.load(pickle_in)
with open('Pickles/us_unemployment.pickle', 'rb') as pickle_in:
    unemployment = pickle.load(pickle_in)

HPI = HPI_Bench.join([m30, sp500, gdp, unemployment])
HPI.dropna(inplace=True)
print(HPI.corr())

with open('Pickles/HPI.pickle', 'wb') as pickle_out:
    pickle.dump(HPI, pickle_out)