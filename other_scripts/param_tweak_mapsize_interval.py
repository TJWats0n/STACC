import preprocess_data
import numpy as np
from tqdm import tqdm
import pickle
import detect_crowded
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from matplotlib import cm


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

def construct_axis():
    x = []
    y = []
    avg = []
    perc = []

    for mapsize in mapsizes:
        print('mapsize:', mapsize)
        for interval in intervals:
            print('interval:', interval)
            # grid_tweets = preprocess_data.calc_grid(filtered_tweets, map_size=mapsize)
            #
            # pickle.dump(grid_tweets, open('other_scripts/grid_tweets_' + str(mapsize) + '_' + str(interval) + '.p', 'wb'))
            grid_tweets = pickle.load(open('other_scripts/grid_tweets_' + str(mapsize) + '_' + str(interval) + '.p', 'rb'))

            timeseries, oldest = detect_crowded.create_time_series(grid_tweets, interval=interval, map_size=mapsize)

            single_avg = calc_avg(timeseries, mapsize)
            # percentage of how many
            percentage = calc_fill_percentage(timeseries, mapsize)

            x.append(interval)
            y.append(mapsize)
            avg.append(single_avg)
            perc.append(percentage)

    #invert y to make plot more readable
    y = y[::-1]

    return x,y,avg,perc


def calc_metric_alt(x, y, percentage, avg):
    return (3*percentage*(2*avg+4*x))


def metric(x, y, percentage, avg):
    return (percentage * (avg + x))/y


def draw_surface(x,y, percentage, avg):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x1, y1 = np.meshgrid(x, y)
    zs = np.array([calc_metric_alt(x, y, percentage, avg) for x, y, percentage, avg in zip(np.ravel(x1), np.ravel(y1), percentage, avg)])
    z = zs.reshape(x1.shape)

    ax.plot_surface(x1, y1, z, cmap=cm.coolwarm, linewidth=0.5, edgecolors='grey')
    ax.set_title('(3*percentage*(2*avg+4*x))/y')

    ax.set_xticks([8, 16, 32])
    ax.set_xticklabels(["8", "16", "32"])

    ax.set_yticks([60, 180, 360, 540, 660])
    ax.set_yticklabels(["60", "180", "360", "540", "660"])

    ax.set_xlabel('x Mapsize in Cells')
    ax.set_ylabel('y: Interval in Min')
    ax.set_zlabel('Metric')
    return z

mapsizes = [8, 16, 32]
intervals = [60, 180, 360, 540, 660]


def main():

    # data = preprocess_data.load_data()
    # filtered_tweets = preprocess_data.filter_spam(data)
    # pickle.dump(filtered_tweets, open('other_scripts/filtered_tweets.p', 'wb'))
    #
    # filtered_tweets = pickle.load(open('other_scripts/filtered_tweets.p', 'rb'))
    #
    # x,y,avg,perc = construct_axis()
    #
    # obj = {
    #     'x': x,
    #     'y': y,
    #     'avg': avg,
    #     'perc': perc
    # }
    # pickle.dump(obj,open('obj.p', 'wb'))

    obj = pickle.load(open('obj.p', 'rb'))

    x = obj['x']
    y = obj['y']
    avg = obj['avg']
    perc = obj['perc']

    z = draw_surface(x=mapsizes, y=intervals, percentage=perc, avg=avg)
    print(x)
    print(y)
    print(z)
    print(avg)
    print(perc)
    plt.show()

if __name__ == '__main__':
    main()