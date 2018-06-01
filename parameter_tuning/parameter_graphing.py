import matplotlib.pyplot as plt
import pickle

def normalize_unique_events(events):
    minimum = min(events)
    maximum = max(events)
    normalised = []

    for event in events:
        normalised.append((event-minimum)/(maximum-minimum))

    return normalised

font = {'family': 'serif',
        'weight': 'normal'}
# #map
# parameter_name = 'map'
# labels = ['8', '16', '24', '32']
# ticks = [1,2,3,4]
# p = [0.53, 0.63, 0.56, 0.38]
# mu = [11, 8, 13, 3]
# r = [0.52, 0.53, 0.72, 1.00]
# optimum = 3

# # #interval
# parameter_name = 'interval'
# labels = ['60', '180', '360', '480', '720']
# ticks = [1, 3, 6, 8, 12]
# p = [0, 0.33, 0.56, 0.45, 0.35]
# mu = [0, 1, 13, 15, 20]
# r = [0, 1.00, 0.72, 0.68, 0.45]
# optimum = 6

# #sliding window
# parameter_name = 'window'
# labels = ['5', '10', '15', '20', '25']
# ticks = [1,2,3,4,5]
# p = [0.66, 0.56, 0.58, 0.63, 0.58]
# mu = [15, 13, 16, 16, 15]
# r = [0.79, 0.72, 0.84, 0.8, 0.83]
# optimum = 4

# #Corpus Size
# parameter_name = 'clength'
# labels = ['0.5', '1', '2']
# ticks = [1,2,3]
# p = [0.67, 0.63, 0.89]
# mu = [14, 16, 9]
# r = [0.64, 0.8, 0.56]
# optimum = 2

# #Radius
# parameter_name = 'radius'
# labels = ['1', '2', '3', '4']
# ticks = [1,2,3,4]
# p = [0.54, 0.63, 0.71, 0.70]
# mu = [7, 16, 18, 17]
# r = [1, 0.8, 0.72, 0.65]
# optimum = 3

#overlap
parameter_name = 'overlap'
labels = ['0.6', '0.7', '0.8', '0.9']
ticks = [1,2,3,4]
p = [0.68, 0.72, 0.71, 0.71]
mu = [21, 21, 18, 16]
r = [0.63, 0.72, 0.72, 0.69]
optimum = 2 #at which tick is the optimum?


def main():
    plt.rc('font', **font)
    m = normalize_unique_events(mu)

    plt.gca().set_prop_cycle('color', ['#1b9e77', '#d95f02', '#7570b3'])


    # fig = plt.figure()
    plt.plot(ticks, p, marker='.')
    plt.plot(ticks, r, marker='.')
    plt.plot(ticks, m, marker='.')

    ax = plt.subplot(111)
    ax.legend(['Precision', 'Recall', 'Normalized Meaningful Unique Events'], loc='lower left')
    ax.grid(color='grey', linestyle='--', linewidth=0.3, alpha=0.4)
    plt.axvspan(optimum, optimum, color='#e41a1c', alpha=0.5)#highlights the chosen config
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels)
    ax.set_xlabel(parameter_name)


    # #tweet frequency distribution graph
    # series = pickle.load(open('/Users/juliankopp1/Documents/Ireland_II/tweet_frequency_dist.p', 'rb'))
    # plt.rc('font', **font)
    # plt.plot([i for i in range(24)], series, marker='.')
    #
    # ax = plt.subplot(111)
    # ax.grid(color='grey', linestyle='--', linewidth=0.3, alpha=0.4)
    # ax.legend(['# Tweets per Hour'], loc='lower right')
    # ax.set_xticks([i for i in range(0,24,2)])
    # ax.set_xlabel('Hour')

    plt.savefig('{}.pdf'.format(parameter_name), dpi=500, format='pdf')
    #plt.show()


if __name__ == '__main__':
    main()