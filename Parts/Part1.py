import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style

start = datetime.datetime(2014, 1, 1)
end = datetime.datetime.now()

df = web.DataReader('TSLA', 'iex', start, end)

print(df.head())

style.use('fivethirtyeight')

df['high'].plot()
plt.legend()
plt.show()