import argparse
import simulation

def main():
    # parser = argparse.ArgumentParser(description='ARQ Simulation')
    # parser.add_argument('filenames', nargs='+')
    # parser.add_argument('--mode', '-m', default='solve', action='store', nargs='?', choices=['solve', 'e1', 'e2', 'e3'],
    #                     help='what mode to run it in i.e. solve a problem or do an experiment')
    # parser.add_argument('--algo', '-a', default='hill', action='store', nargs='?',
    #         choices=['hill', 'annealing', 'astar'],
    #         help='which algorithm to use to search for a solution, uses hill climbing defaulty')
    # parser.add_argument('--sideways', '-s', default=0, action='store', nargs='?', type=int,
    #                     help='how many side way moves allowed')
    # parser.add_argument('--tabu', '-t', default=0, action='store', nargs='?', type=int,
    #                     help='size of the tabu list')
    # parser.add_argument('--restart', '-r', default=0, action='store', nargs='?', type=int,
    #                     help='number of random restarts allowed')
    # parser.add_argument('--temperature', '-T', default=100, action='store', nargs='?', type=int,
    #                     help='initial temperature to use for simulated annealing')
    # parser.add_argument('--schedule', '-S', default='LINEAR', action='store', nargs='?',
    #         choices=['LINEAR', 'EXP', "LOG"], help='annealing schedule to use')

    # args = parser.parse_args()

    filename = ''

    simulation.simulate_ABQ(filename)

if __name__ == '__main__':
    main()
