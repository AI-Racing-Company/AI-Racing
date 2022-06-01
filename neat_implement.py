import neat
import os
import main
import arcade

p = None
gen = 0
POPULATION = 3

def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    winner = p.run(eval_genomes, 3)

    print('\nBest genome:\n{!s}'.format(winner))



def init():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)


def eval_genomes(genomes, config):
    """
    runs the simulation of the current population of
    s and sets their fitness based on the distance they
    reach in the game.
    """
    global gen
    gen += 1

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    #  object that uses that network to play
    nets = []
    cars = list()
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)

        ge.append(genome)




    run = True
    while run and not main.all_cars_dead:

        for i in range(main.POPULATION):  # give each  a fitness of 0.1 for each frame it stays alive
            print(i)
            # send  location, top pipe location and bottom pipe location and determine from network whether to jump or not
            inputList = main.MyGame.getViewLen(None, i)
            output = nets[i].activate(inputList[0], inputList[1], inputList[2], inputList[3], inputList[4], player.speed)

            if output[0] > 0.5:  # Gas
                main.MyGame.acc(i,True)
            else:
                main.MyGame.acc(i,False)

            if output[1] > 0.5:  # Break
                main.MyGame.dec(i,True)
            else:
                main.MyGame.dec(i,False)

            if output[2] > 0.5:  # Left
                main.MyGame.lef(i,True)
            else:
                main.MyGame.lef(i,False)

            if output[3] > 0.5:  # Right
                main.MyGame.rig(i,True)
            else:
                main.MyGame.rig(i, False)





        # break if score gets large enough
        '''if score > 20:
            pickle.dump(nets[0],open("best.pickle", "wb"))
            break'''
