import argparse
import sys

import Simulator


def report_config(sim: Simulator):
    stats = sim.get_stats()
    print(f'''SIMULATION CONFIGURATION
--------------------------------------
(-n) # layer5 msgs to be provided:      {stats['n_sim_max']}
(-d) avg layer5 msg interarrival time:  {stats['interarrival_time']}
(-z) transport protocol seqnum limit:   {stats['seqnum_limit']}
(-l) layer3 packet loss prob:           {stats['loss_prob']}
(-c) layer3 packet corruption prob:     {stats['corrupt_prob']}
(-s) simulation random seed:            {stats['random_seed']}
--------------------------------------''')

def report_results(sim: Simulator):
    stats = sim.get_stats()
    time = stats['time']

    if time > 0.0:
        tput = stats['n_to_layer5_B']/time
    else:
        tput = 0.0

    print(f'''\nSIMULATION SUMMARY
--------------------------------
# layer5 msgs provided to A:      {stats['n_sim']}
# elapsed time units:             {stats['time']}

# layer3 packets sent by A:       {stats['n_to_layer3_A']}
# layer3 packets sent by B:       {stats['n_to_layer3_B']}
# layer3 packets lost:            {stats['n_lost']}
# layer3 packets corrupted:       {stats['n_corrupt']}
# layer5 msgs delivered by A:     {stats['n_to_layer5_A']}
# layer5 msgs delivered by B:     {stats['n_to_layer5_B']}
# layer5 msgs by B/elapsed time:  {tput}
--------------------------------''')


def main(sim: Simulator):
    report_config(sim)
    sim.run()


if __name__ == '__main__':
    desc = 'Run a simulation of a reliable data transport protocol.'

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-n', type=int, default=10,
                        dest='num_msgs',
                        help=('number of messages to simulate'
                              ' [int, default: %(default)s]'))
    parser.add_argument('-d', type=float, default=100.0,
                        dest='interarrival_time',
                        help=('average time between messages'
                              ' [float, default: %(default)s]'))
    parser.add_argument('-z', type=int, default=16,
                        dest='seqnum_limit',
                        help=('seqnum limit for data transport protocol; '
                              'all packet seqnums must be >=0 and <limit'
                              ' [int, default: %(default)s]'))
    parser.add_argument('-l', type=float, default=0.0,
                        dest='loss_prob',
                        help=('packet loss probability'
                              ' [float, default: %(default)s]'))
    parser.add_argument('-c', type=float, default=0.0,
                        dest='corrupt_prob',
                        help=('packet corruption probability'
                              ' [float, default: %(default)s]'))
    parser.add_argument('-s', type=int,
                        dest='random_seed',
                        help=('seed for random number generator'
                              ' [int, default: %(default)s]'))
    parser.add_argument('-v', type=int, default=0,
                        dest='trace',
                        help=('level of event tracing'
                              ' [int, default: %(default)s]'))

    cb_A = None
    cb_B = None

    options = parser.parse_args()

    TRACE = options.trace
    sim = Simulator(options, cb_A, cb_B)

    main(sim)
    report_results(sim)
    sys.exit(0)


