import neat
import os
import csv
import math
import time
import pyautogui
import numpy as np
import random
import visualize

train_AI = True
use_Gen = False
Gen_File = "neat-checkpoint-815"
numMaxGen = 100

random_tracks = True
max_tracks = 4
change_prop = 5
use_track = 2

draw_net = False

POPULATION = 150

maxTicks = 1000
increaseMaxTicks = 50
absMaxTicks = 6000

calcTime = False  # Print deltatime of on_update

###
### DON'T touch this stuff unless you know what you do
###

SPRITE_SCALING_PLAYERS = 1  # 23 * 67 px
carDiag = 35.41  # len of diagonal
carAngularAdd = [19, 161, -161, -19]  # angles to add for calculation
carViewNum = 5
carViewAngle = 180
carViewDis = 100
playerKeyState = list()
window = None

trackNow = 0

t0 = 0

P1_MAX_HEALTH = 1

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
SCREEN_HEIGHT = int(SCREEN_HEIGHT * 0.9)

ACCELERATION = 0.05
DECELERATION = 0.1
MAX_SPEED = 3
MIN_SPEED = 0
ANGLE_SPEED = 2
FRICTION = 0.01

RESET_X = 500
RESET_Y = 150


keep = 5
countTicks = 0

cars_alive = POPULATION
all_cars_dead = False
cars_dead = 0

p = None

gen = 0
deltatime = 1


class testConnetc():

    def ccw(self, A, B, C):
        return ((C[1] - A[1]) * (B[0] - A[0])) > ((B[1] - A[1]) * (C[0] - A[0]))

    def intersect(self, A, B, C, D):
        return self.ccw(A, C, D) != self.ccw(B, C, D) and self.ccw(A, B, C) != self.ccw(A, B, D)

    def line_intersection(self, line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y




class Player():

    def __init__(self):
        self.speed = 0
        self.angle = 90
        self.center_x = RESET_X
        self.center_y = RESET_Y
        self.speed = 0
        self.distance = 0

        self.viewLen = list()
        for i in range(5):
            self.viewLen.append(carViewDis)

        self.lastDis = -1

        self.change_angle = 0

        self.acc = False
        self.dec = False
        self.lef = False
        self.rig = False

        self.dead = False

        self.carLines = list()
        self.carView = list()
        self.carViewHit = list()

        self.isAlive = True

    def update(self):
        self.angle += self.change_angle

        self.angle = self.angle % 360

        self.center_x += -self.speed * math.sin(math.radians(self.angle))
        self.center_y += self.speed * math.cos(math.radians(self.angle))


class MyGame():

    def __init__(self):

        self.wallhit = 0

        self.cars_alive = POPULATION
        self.all_cars_dead = 0
        self.carDiag = carDiag
        self.carAngularAdd = carAngularAdd
        self.carViewNum = carViewNum
        self.FRICTION = FRICTION
        self.ACCELERATION = ACCELERATION
        self.DECELERATION = DECELERATION
        self.MAX_SPEED = MAX_SPEED
        self.MIN_SPEED = MIN_SPEED
        self.player_list = list()

        self.x = 0
        self.y = 0
        self.temp_list = [0, 0]
        self.xy0_list = list()
        self.xy1_list = list()
        self.difflist = list()
        self.sectorlinecoords = list()
        self.count0 = 0
        self.click0 = 0
        self.click1 = 0
        self.linie = 0
        self.olddis = 2060

        self.players = list()
        self.playerViewLen = list()

        player_sprite = None
        self.wall_sprite = None
        self.street_sprite = None

        self.p1_health = None

        self.background = None

        self.W = False
        self.A = False
        self.S = False
        self.D = False

    def setup(self):
        global RESET_Y, POPULATION, carViewNum, playerKeyState

        self.wallhit = testConnetc()
        self.start = False

        for i in range(POPULATION):

            helpList = list()
            for j in range(4):
                helpList.append(False)
            playerKeyState.append(helpList)

            helpList.clear()
            for j in range(self.carViewNum):
                helpList.append(carViewDis)
            self.playerViewLen.append(helpList)

    def on_update(self):
        hitCalc = 170

        for index, player in enumerate(self.player_list):
            if player.isAlive:
                carDied = False
                carAng = player.angle
                carX = player.center_x
                carY = player.center_y
                player.carLines.clear()

                ###
                ### Calculate hitbox of car
                ###

                for i in range(4):
                    tempList = [0, 0]
                    tempList[0] = (carX + math.cos(-math.radians(90 - (carAng + self.carAngularAdd[i]))) * self.carDiag)
                    tempList[1] = (carY + math.sin(-math.radians(90 - (carAng + self.carAngularAdd[i]))) * self.carDiag)
                    player.carLines.append(list(tempList))
                player.carLines.append(player.carLines[0])

                wallHit = False

                ###
                ### Look if car hitbox intersects with line
                ### t: 1001500
                ###

                for i in range(0, len(self.xy0_list) - 1, 1):
                    if carX - hitCalc < self.xy0_list[i][0] < carX + hitCalc and carY - hitCalc < self.xy0_list[i][
                        1] < carY + hitCalc:
                        for j in range(4):
                            if self.wallhit.intersect(self.xy0_list[i], self.xy0_list[i + 1], player.carLines[j],
                                                      player.carLines[j + 1]):
                                wallHit = True
                                break
                    if wallHit:
                        break
                for i in range(0, len(self.xy1_list) - 1, 1):
                    if carX - hitCalc < self.xy1_list[i][0] < carX + hitCalc and carY - hitCalc < self.xy1_list[i][
                        1] < carY + hitCalc:
                        for j in range(4):
                            if self.wallhit.intersect(self.xy1_list[i], self.xy1_list[i + 1], player.carLines[j],
                                                      player.carLines[j + 1]):
                                wallHit = True
                                break

                    if wallHit:
                        break

                ###
                ### If car intersects, kill car
                ###

                if wallHit:
                    self.kill(index)

                ###
                ### If car did not die continue wit calculating
                ###

                if not carDied:
                    player.carView.clear()

                    ###
                    ### Create view lines of car
                    ###

                    for i in range(carViewNum):
                        alpha = carViewAngle / (carViewNum - 1)

                        player.carView.append(list([carX, carY]))
                        tempList = [0, 0]
                        tempList[0] = (carX + math.sin(-math.radians(carAng + alpha * i - carViewAngle / 2)) * carViewDis)
                        tempList[1] = (carY + math.cos(-math.radians(carAng + alpha * i - carViewAngle / 2)) * carViewDis)
                        player.carView.append(list(tempList))

                    player.carViewHit.clear()

                    pointRange = list()
                    rayDis = list()

                    helpList = list()

                    ###
                    ### Calculate distances to next line of track
                    ###

                    for id3, playerView in enumerate(player.carView):
                        if id3 % 2 == 1:
                            for i in range(0, len(self.xy0_list) - 1, 1):
                                if carX - hitCalc < self.xy0_list[i][0] < carX + hitCalc and carY - hitCalc < \
                                        self.xy0_list[i][1] < carY + hitCalc:
                                    if id3 < len(player.carView):
                                        if self.wallhit.intersect(self.xy0_list[i], self.xy0_list[i + 1], playerView,
                                                                  [carX, carY]):

                                            if (carY - playerView[0]) != 0:
                                                if -0.01 < (self.xy0_list[i + 1][0] - self.xy0_list[i][0]) < 0.01:
                                                    self.xy0_list[i][0] += 0.1
                                                m1 = (self.xy0_list[i+1][1] - self.xy0_list[i][1]) / (self.xy0_list[i+1][0] - self.xy0_list[i][0])

                                                b1 = -(m1 * self.xy0_list[i][0]) + self.xy0_list[i][1]
                                                if -0.01 < (carX - playerView[0]) < 0.01:
                                                    playerView[0] += 0.1
                                                m2 = (carY - playerView[1]) / (carX - playerView[0])

                                                b2 = -(m2 * playerView[0]) + playerView[1]

                                                xi = (b2 - b1) / (m1 - m2)
                                                yi = m2 * xi + b2

                                                dis = math.sqrt((carX - xi) ** 2 + (carY - yi) ** 2)
                                                pointRange.append([dis, xi, yi])

                            for i in range(0, len(self.xy1_list) - 1, 1):
                                if carX - hitCalc < self.xy1_list[i][0] < carX + hitCalc and carY - hitCalc < \
                                        self.xy1_list[i][1] < carY + hitCalc:
                                    if id3 < len(player.carView):
                                        if self.wallhit.intersect(self.xy1_list[i], self.xy1_list[i + 1], playerView,
                                                                  [carX, carY]):

                                            if (carY - playerView[0]) != 0:
                                                if -0.01 < (self.xy1_list[i + 1][0] - self.xy1_list[i][0]) < 0.01:
                                                    self.xy1_list[i][0] += 0.1
                                                m1 = (self.xy1_list[i + 1][1] - self.xy1_list[i][1]) / (
                                                            self.xy1_list[i + 1][0] - self.xy1_list[i][0])

                                                b1 = -(m1 * self.xy1_list[i][0]) + self.xy1_list[i][1]
                                                if -0.01 < (carX - playerView[0]) < 0.01:
                                                    playerView[0] += 0.1
                                                m2 = (carY - playerView[1]) / (carX - playerView[0])

                                                b2 = -(m2 * playerView[0]) + playerView[1]

                                                xi = (b2 - b1) / (m1 - m2)
                                                yi = m2 * xi + b2

                                                dis = math.sqrt((carX - xi) ** 2 + (carY - yi) ** 2)
                                                pointRange.append([dis, xi, yi])
                            pointRange.append([carViewDis, 0, 0])

                            ###
                            ### Select shortest length for each ray
                            ###

                            if pointRange:
                                pr = list(zip(*pointRange))
                                mind = pr[0].index(min(pr[0]))

                                if mind != -1:
                                    player.carViewHit.append([pointRange[mind][1], pointRange[mind][2]])
                                    helpList.append(pointRange[mind][0])
                                else:
                                    helpList.append(carViewDis)

                            pointRange.clear()

                    player.viewLen = helpList;

                    pointRange.clear()

                    if index < len(self.playerViewLen) and len(self.playerViewLen) > 1:
                        self.playerViewLen[index] = helpList
                        player.viewList = helpList

                    ###
                    ### Apply normal amount of breaking
                    ###

                    if player.speed > self.FRICTION:
                        player.speed -= self.FRICTION
                    elif player.speed < -self.FRICTION:
                        player.speed += self.FRICTION
                    else:
                        player.speed = 0

                    ###
                    ### Look for input left right break accelerate
                    ###

                    if player.acc and not player.dec:
                        player.speed += self.ACCELERATION
                    elif player.dec and not player.acc:
                        player.speed += -self.DECELERATION
                    if player.lef and not player.rig:
                        player.change_angle = 0.256 * (player.speed - 0.75) ** 3 - 1.344 * (
                                player.speed - 0.75) ** 2 + 1.152 * player.speed - 0.75 + 1.728
                    elif player.rig and not player.lef:
                        player.change_angle = -(0.256 * (player.speed - 0.75) ** 3 - 1.344 * (
                                player.speed - 0.75) ** 2 + 1.152 * player.speed - 0.75 + 1.728)

                    if player.speed > self.MAX_SPEED:
                        player.speed = self.MAX_SPEED
                    elif player.speed < -self.MAX_SPEED:
                        player.speed = -self.MAX_SPEED
                    elif player.speed < -self.MIN_SPEED:
                        player.speed = -self.MIN_SPEED
                    player.update()

    def acc(self, id, tf):
        self.player_list[id].acc = tf

    def dec(self, id, tf):
        self.player_list[id].dec = tf

    def rig(self, id, tf):
        self.player_list[id].lef = tf

    def lef(self, id, tf):
        self.player_list[id].rig = tf

    def getViewLen(self, i):
        return self.playerViewLen[i]

    def importTrack(self):
        global trackNow, random_tracks, max_tracks, change_prop, use_track
        if random.randint(0,change_prop) == 1 or not self.xy0_list:
            print("importing")

            self.xy0_list = list()
            self.xy1_list = list()

            dataList00 = list()
            dataList01 = list()
            dataList10 = list()
            dataList11 = list()

            data = list()
            trackNow = use_track
            if random_tracks:
                trackNow = random.randint(0, max_tracks)
                print(trackNow)
            with open(f'track_{trackNow}.csv', 'r') as f:
                reader = csv.reader(f)

                for row in reader:
                    data.append(row)
                    print(row)

            print("done importing")

            dataList00 = data[0]
            dataList01 = data[1]
            dataList10 = data[2]
            dataList11 = data[3]

            for id, elem in enumerate(dataList00):
                hl = list()
                hl.append(int(elem))
                hl.append(int(dataList01[id]))
                self.xy0_list.append(list(hl))
                hl.clear()
            for id, elem in enumerate(dataList10):
                hl = list()
                hl.append(int(elem))
                hl.append(int(dataList11[id]))
                self.xy1_list.append(list(hl))
                hl.clear()
            self.linie = 2
            self.click0 = 100
            self.click1 = 100

    def resetAll(self):
        global all_cars_dead, cars_dead, cars_alive, POPULATION
        for id, car in enumerate(self.player_list):
            self.reset(id)
            car.center_x = RESET_X
            car.center_y = RESET_Y
            car.distance = 0
            car.isAlive = True
        self.all_cars_dead = False
        self.cars_dead = 0
        self.cars_alive = POPULATION

    def reset(self, pid):
        global RESET_X, RESET_Y
        self.player_list[pid].center_x = RESET_X
        self.player_list[pid].center_y = RESET_Y
        self.player_list[pid].speed = 0
        self.player_list[pid].angle = 90

    def kill(self, pid):
        self.cars_dead += 1
        self.all_cars_dead = self.cars_dead == POPULATION
        self.cars_alive -= 1
        self.player_list[pid].isAlive = False
        carDied = True

def run(config_file):
    global train_AI, use_Gen, Gen_File, numMaxGen, draw_net
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.

    p = None

    if train_AI and not use_Gen:
        p = neat.Population(config)

        # Add a stdout reporter to show progress in the terminal.
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        p.add_reporter(neat.Checkpointer(10))



    elif train_AI and use_Gen:
        p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-815")

        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        p.add_reporter(neat.Checkpointer(10))

    elif not train_AI and use_Gen:
        p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-815")

    if p is not None:
        winner = p.run(eval_genomes, numMaxGen)
        if draw_net:
            node_names = {-1: 'Line1', -2: 'Line2', -3: 'Line3', -4: 'Line4', -5: 'Line5', -6: 'Speed', 0: 'A', 1: 'D', 2: 'W', 3: 'S'}
            visualize.draw_net(config, winner, True, node_names=node_names)
    #visualize.draw_net(config, winner, True, prune_unused=True)
    #visualize.plot_stats(stats, ylog=False, view=True)
    #visualize.plot_species(stats, view=True)

    print('\nBest genome:\n{!s}'.format(winner))


def init():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)


def eval_genomes(genomes, config):
    global calcTime, increaseMaxTicks, calcTime, cars_dead, all_cars_dead, window, player_list, t0, gen, cars_alive, keep, deltatime, minfit, countTicks, maxTicks
    window.player_list.clear()

    """
    runs the simulation of the current population of
    s and sets their fitness based on the distance they
    reach in the game.
    """
    gen += 1

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    #  object that uses that network to play
    nets = []
    cars = list()
    ge = []
    print(len(ge))
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        window.player_list.append(Player())
        ge.append(genome)

    run = True
    t0 = time.time()
    c = 0
    window.resetAll()
    while True:
        if window.cars_alive > 0:
            if calcTime:
                dt = time.time_ns()
                window.on_update()
                updatePlayerList()
                print(f"{(time.time_ns() - dt):,d}")
            else:
                window.on_update()
                updatePlayerList()

            carDied = False
            for i, elem in enumerate(window.player_list):
                if elem.isAlive:
                    if countTicks == 100 and ge[i].fitness <= 10 and train_AI:
                        window.kill(i)

                    if carDied:
                        break
                    if not carDied:
                        inputList = elem.viewLen

                        allInputs = [inputList[0], inputList[1], inputList[2], inputList[3], inputList[4], elem.speed]
                        output = nets[i].activate(allInputs)
                        if output[0] > 0.5:  # Left
                            elem.lef = True
                        else:
                            elem.lef = False

                        if output[1] > 0.5:  # Right
                            elem.rig = True
                        else:
                            elem.rig = False

                        if output[2] > 0.5:  # Gas
                            elem.acc = True
                        else:
                            elem.acc = False
                        if output[3] > 0.5:  # Break
                            elem.dec = True
                        else:
                            elem.dec = False

                        ge[i].fitness -= 0.1
                        ge[i].fitness += elem.speed


            countTicks += 1
        else:
            countTicks = 0
            maxTicks += increaseMaxTicks
            if maxTicks > absMaxTicks:
                maxTicks = absMaxTicks
            break
        if countTicks > maxTicks:
            countTicks = 0
            maxTicks += 50
            if maxTicks > absMaxTicks:
                maxTicks = absMaxTicks
            break

    if random_tracks:
        window.importTrack()

    window.resetAll()


def main():
    global window
    window = MyGame()
    window.setup()
    window.importTrack()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)


def updatePlayerList():
    playerExport = list()

    for id, element in enumerate(window.player_list):
        if element.isAlive:
            tmpList = list()
            tmpList.append(element.center_x)
            tmpList.append(element.center_y)
            tmpList.append(element.angle)
            playerExport.append(tmpList)

    with open('playerData.csv', "w") as f:
        f.truncate()
    with open('playerData.csv', 'w', newline='') as f:

        writer = csv.writer(f)

        # write the data
        writer.writerow(np.array([trackNow]))
        for elem in playerExport:
            writer.writerow(np.array(elem))



if __name__ == "__main__":
    main()
