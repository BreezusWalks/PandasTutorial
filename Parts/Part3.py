import pandas as pd

print('Original CSV DF')
df = pd.read_csv('CSVs/FMAC-HPI_AUSTX.csv')
print(df.head())
print()

print('Replacing Date as DF index')
df.set_index('Date', inplace=True)
print(df.head())
print()

print('Reading updated Date indexed DF from created CSV')
df.to_csv('CSVs/newCSV2.csv')
df = pd.read_csv('CSVs/newCSV2.csv')
print(df.head())
print()

df = pd.read_csv('CSVs/FMAC-HPI_AUSTX.csv')
df.set_index('Date', inplace=True)
df['Value'].to_csv('CSVs/newCSV2.csv')
print('Reading CSV with only Values column')
df = pd.read_csv('CSVs/newCSV2.csv', index_col=0)
print(df.head())
print()

print("Changing column name to Housing_Prices")
df = pd.read_csv('CSVs/FMAC-HPI_AUSTX.csv')
df.set_index('Date', inplace=True)
df.columns = ['Housing_Prices']
print(df.head())
print()

df.to_csv('CSVs/newCSV3.csv')
df.to_csv('CSVs/newCSV4.csv', header=False)

print('Reading from CSV with now headers and adding them in the read_csv call')
df = pd.read_csv('CSVs/newCSV4.csv', names=['Date', 'Housing_Prices'], index_col=0)
print(df.head())

#Creating HTML output from Dataframe. Automatically assigned the class of dataframe
df.to_html('example.html')

df = pd.read_csv('CSVs/newCSV4.csv', names=['Date', 'Housing_Price'], index_col=0)
print(df.head())
print()

print('Changing column names')
df.rename(columns={'Housing_Price': 'Price'}, inplace=True)
print(df.head())