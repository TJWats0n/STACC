# coding: utf-8

# std
import timeit
import os
import argparse

# mabed
from pyMABED.mabed.corpus import Corpus
from pyMABED.mabed.mabed import MABED
import pyMABED.mabed.utils as utils


__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

def main(args):

    print('Parameters:')
    print(
        '   Corpus: {}\n   k: {}\n   Stop-words: {}\n   Min. abs. word frequency: {}\n   Max. rel. word frequency: {}'\
            .format(args['i'], args['k'], args['sw'], str(args['maf']), str(args['mrf'])))

    print('   p: %d\n   theta: %f\n   sigma: %f' % (args['p'], args['t'], args['s']))

    print('Loading corpus...')
    start_time = timeit.default_timer()
    my_corpus = Corpus(args['i'], args['sw'], args['maf'], args['mrf'], args['sep'])
    elapsed = timeit.default_timer() - start_time
    print('Corpus loaded in %f seconds.' % elapsed)

    time_slice_length = args['tsl']
    print('Partitioning tweets into %d-minute time-slices...' % time_slice_length)
    start_time = timeit.default_timer()
    my_corpus.discretize(time_slice_length)
    elapsed = timeit.default_timer() - start_time
    print('Partitioning done in %f seconds.' % elapsed)

    print('Running MABED...')
    k = args['k']
    p = args['p']
    theta = args['t']
    sigma = args['s']
    start_time = timeit.default_timer()
    mabed = MABED(my_corpus)
    mabed.run(k=k, p=p, theta=theta, sigma=sigma)
    mabed.print_events()
    elapsed = timeit.default_timer() - start_time
    print('Event detection performed in %f seconds.' % elapsed)

    if args['o'] is not None:
        utils.save_events(mabed, args['o'])
        print('Events saved in %s' % args['o'])


if __name__ == '__main__':
    main()
