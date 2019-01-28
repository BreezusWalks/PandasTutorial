import pandas as pd

df1 = pd.DataFrame({'HPI':[80,85,88,85],
                    'Int_rate':[2, 3, 2, 2],
                    'US_GDP_Thousands':[50, 55, 65, 55]},
                   index = [2001, 2002, 2003, 2004])

df2 = pd.DataFrame({'HPI':[80,85,88,85],
                    'Int_rate':[2, 3, 2, 2],
                    'US_GDP_Thousands':[50, 55, 65, 55]},
                   index = [2005, 2006, 2007, 2008])

df3 = pd.DataFrame({'HPI':[80,85,88,85],
                    'Unemployment':[7, 8, 9, 6],
                    'Low_tier_HPI':[50, 52, 50, 53]},
                   index = [2001, 2002, 2003, 2004])

print(pd.merge(df1, df3, on='HPI'))
print()
print(pd.merge(df1, df2, on=['HPI', 'Int_rate']))
print()

df4 = pd.merge(df1, df3, on='HPI')
df4.set_index('HPI', inplace=True)
print(df4)
print()

df1.set_index('HPI', inplace=True)
df3.set_index('HPI', inplace=True)
joined = df1.join(df3)
print(joined)
print()

df1 = pd.DataFrame({
                    'Int_rate':[2, 3, 2, 2],
                    'US_GDP_Thousands':[50, 55, 65, 55],
                    'Year':[2001, 2002, 2003, 2004]
                    })

df3 = pd.DataFrame({
                    'Unemployment':[7, 8, 9, 6],
                    'Low_tier_HPI':[50, 52, 50, 53],
                    'Year':[2001, 2003, 2004, 2005]})

print("Default merge action, no index set")
merged = pd.merge(df1, df3, on='Year')
print(merged)
print()

#Index and key are interchangeable
print("Default merge action - inner")
merged = pd.merge(df1, df3, on='Year')
merged.set_index('Year', inplace=True)
print(merged)
print()

print("Left merge on keys")
merged = pd.merge(df1, df3, on='Year', how='left')
merged.set_index('Year', inplace=True)
print(merged)
print()

print("Right merge on keys")
merged = pd.merge(df1, df3, on='Year', how='right')
merged.set_index('Year', inplace=True)
print(merged)
print()

print("Union of keys")
merged = pd.merge(df1, df3, on='Year', how='outer', sort=True)
merged.set_index('Year', inplace=True)
print(merged)
print()

print("Only intersection of keys")
merged = pd.merge(df1, df3, on='Year', how='inner')
merged.set_index('Year', inplace=True)
print(merged)
print()

print("Outer join of df3 on df1")
df1.set_index('Year', inplace=True)
df3.set_index('Year', inplace=True)
joined = df1.join(df3, how="outer")
print(joined)