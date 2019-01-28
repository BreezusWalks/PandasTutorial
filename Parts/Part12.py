import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')

bridge_height = {'meters':[10.26, 10.31, 10.27, 10.22, 10.23, 6212.42, 10.28, 10.25, 10.31]}
df = pd.DataFrame(bridge_height)

df.plot()
plt.show()

print("Get standard deviation for the current period and the previous period")
df['STD'] = df['meters'].rolling(2).std()
print(df)
print()

print("Print out stats for df using .describe()")
df_std = df.describe()
print(df_std)
print()

print("Access std specifically from the .describe()")
df_std = df.describe()['meters']['std']
print(df_std)
print()

print("Delete all rows where the standard deviation is greater than the average standard deviation of the df")
df = df[(df['STD'] < df_std)]
print(df)

df['meters'].plot()
plt.show()