import argparse
import csv
import simulation

def main():
    parser = argparse.ArgumentParser(description='ARQ Simulation')
    parser.add_argument('--simulation', '-s', default='abq', action='store', nargs='?', choices=['abq', 'abq_nak',
                                                                                                 'gbn', 'graph'],
                        help='what simulation to run')
    args = parser.parse_args()

    if args.simulation == 'abq':
        csv_filename = 'ABP.csv'
        simulation.simulate_ABP(csv_filename)
    elif args.simulation == 'abq_nak':
        csv_filename = 'ABP_NAK.csv'
        simulation.simulate_ABP(csv_filename, enable_NAK=True)
    elif args.simulation == 'gbn':
        csv_filename = 'GBN.csv'
        simulation.simulate_GBN(csv_filename)
    elif args.simulation == 'graph':
        res_q1 = list(csv.reader(open('ABP.csv')))
        res_q2 = list(csv.reader(open('ABP_NAK.csv')))
        res_q3 = list(csv.reader(open('GBN.csv')))

        res_q1 = [[float(val) for val in r] for r in res_q1]
        res_q2 = [[float(val) for val in r] for r in res_q2]
        res_q3 = [[float(val) for val in r] for r in res_q3]

        simulation.graph_q1_q2(res_q1, res_q2)
        simulation.graph_q1_q3(res_q1, res_q3)
    else:
        assert False

if __name__ == '__main__':
    main()
