import preprocess_data
import numpy as np
from tqdm import tqdm
import pickle
import detect_crowded
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import plotly.offline as py
import plotly.graph_objs as go


def calc_avg(timeseries, mapsize):
    print('calc_avg()')
    timeseries_avg = []
    for timeframe in tqdm(range(len(timeseries))):
        timeframe_avg = []
        for y in range(mapsize):
            timeframe_avg.append(np.average(timeseries[timeframe,y]))
        timeseries_avg.append(np.average(timeframe_avg))

    return np.average(timeseries_avg)


def calc_fill_percentage(timeseries, mapsize):
    print('calc_fill_percentage()')
    zero_counter = 0
    for timeframe in tqdm(range(len(timeseries))):
        for y in range(mapsize):
            zero_counter = zero_counter + (timeseries[timeframe, y] == 0).sum()

    all_numbers = len(timeseries) * mapsize * mapsize
    not_zero_counter = all_numbers - zero_counter

    return not_zero_counter/all_numbers


def calc_metric(avg, percentage, interval, mapsize):
    return (percentage * (avg + mapsize))/interval

def calc_metric_alt(avg, percentage, interval, mapsize):
    return percentage*(avg+mapsize-(interval/100))


def draw_graph(x,y,z, mapsize, interval):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x,y,z, c='skyblue', s=20)


def draw_surface(x,y,z,mapsize, interval):
    fig = plt.figure()
    ax = Axes3D(fig)
    surf = ax.plot_trisurf(x,y,z,cmap=plt.cm, linewidth=0.1, vmin=0, vmax=6)
    fig.colorbar(surf, shrink=0.5, aspect=5)

labels = [1, 3, 6, 9, 11]

def draw_plotly(z,y,x):
    data = [go.Surface(z=z)]
    # Xaxis = go.XAxis(
    #     tickmode='array',
    #     ticktext=labels,
    #     tickvals=[0, 1, 2, 3, 4],
    #     title='This is another testing Title'
    # )

    go.Figure()

    layout = go.Layout(
        title='Test',
        autosize=False,
        width=500,
        height=500,
        margin=dict(
            l=65,
            r=50,
            b=65,
            t=90,
        ),
        yaxis = dict(
            tickmode='array',
            tickvals=[1,2,3],
            ticktext=[8, 16, 32],
            title='This is a testing title'
        ),
        xaxis = dict(
            tickmode='array',
            tickvals=[1,2,3,4,5],
            ticktext=[60, 180, 360, 540, 660],
            title='This is a testing title',
            showticklabels=True
        )
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='test.html')


mapsizes = [8, 16, 32]
intervals = [60, 180, 360, 540, 660]


def main():

    # data = preprocess_data.load_data()
    # filtered_tweets = preprocess_data.filter_spam(data)
    # pickle.dump(filtered_tweets, open('other_scripts/filtered_tweets.p', 'wb'))

    filtered_tweets = pickle.load(open('other_scripts/filtered_tweets.p', 'rb'))
    x = []
    y = []
    z = []
    avg_ = []
    perc = []

    # for mapsize in mapsizes:
    #     print('mapsize:', mapsize)
    #     for interval in intervals:
    #         print('interval', interval)
    #         # grid_tweets = preprocess_data.calc_grid(filtered_tweets, map_size=mapsize)
    #         #
    #         # pickle.dump(grid_tweets, open('other_scripts/grid_tweets_' + str(mapsize) + '_' + str(interval) + '.p', 'wb'))
    #         grid_tweets = pickle.load(open('other_scripts/grid_tweets_' + str(mapsize) + '_' + str(interval) + '.p', 'rb'))
    #
    #         timeseries, oldest = detect_crowded.create_time_series(grid_tweets, interval=interval, map_size=mapsize)
    #
    #         avg = calc_avg(timeseries, mapsize)
    #         # percentage of how many
    #         percentage = calc_fill_percentage(timeseries, mapsize)
    #
    #         metric = calc_metric(avg, percentage, interval, mapsize )
    #
    #         x.append(interval)
    #         y.append(mapsize)
    #         z.append(metric*100)
    #         avg_.append(avg)
    #         perc.append(percentage)
    #
    # y = y[::-1]
    #
    # obj = {
    #     'x': x,
    #     'y': y,
    #     'z': z,
    #     'avg': avg_,
    #     'perc': perc
    # }
    #
    # pickle.dump(obj,open('obj.p', 'wb'))
    mapsize = None
    interval = None

    obj = pickle.load(open('obj.p', 'rb'))

    x = obj['x']
    y = obj['y']
    z = obj['z']
    z = np.array([z[0:5], z[5:10], z[10:15]])
    avg_ = obj['avg']
    perc = obj['perc']

    draw_plotly(z,y,x)
    print(x)
    print(y)
    print(z)
    print(avg_)
    print(perc)
    #plt.show()

if __name__ == '__main__':
    main()