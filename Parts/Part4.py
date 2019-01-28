import quandl
import pandas as pd

api_key = open('api_key.txt', 'r').read()

df = quandl.get("FMAC/HPI_TX", authtoken=api_key)
df.drop(columns=['NSA Value'], inplace=True)

print(df.tail())
print()

print('List of dataframes on page')
fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
print(fiddy_states)
print()

print('Fifty states dataframe in list section 0')
print(fiddy_states[0])
for abbrv in fiddy_states[0][1][2:]:
    print(abbrv)
    print("FMAC/HPI_" + abbrv)