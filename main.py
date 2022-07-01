import threading

import arcade
from os import path
import time
import math
import pyautogui
import csv
import numpy as np
from numpy import *
import neat_implement



# Function for Angelspeed dependend on Speed 0.256 *(x-0.75)**(3)-1.344 *(x-0.75)**(2)+1.152 *(x-0.75)+1.728
# Use this variable to count merges: 1

#TODO:
# Nothing in particular


DIR = path.dirname(path.abspath(__file__))

SPRITE_SCALING_PLAYERS = 1 #23 * 67 px
carDiag = 35.41 #len of diagonal
carAngularAdd = [19,161,-161,-19]# angles to add for calculation
carViewNum = 5
carViewAngle = 180
carViewDis = 500
playerViewLen = list()
playerKeyState = list()
ft = True


P1_MAX_HEALTH = 1

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
SCREEN_HEIGHT = int(SCREEN_HEIGHT*0.9)
SCREEN_TITLE = "AI-Racing"

ACCELERATION = 0.05
DECELERATION = 0.1
MAX_SPEED = 3
MIN_SPEED = 0
ANGLE_SPEED = 2
FRICTION = 0.01

RESET_X = 500
RESET_Y = 150

POPULATION = 2
all_cars_dead = False
cars_dead = 0

player_list = arcade.SpriteList()

p = None


class testConnetc():
    def ccw(self, A, B, C):

        return ((C[1] - A[1]) * (B[0] - A[0])) > ((B[1] - A[1]) * (C[0] - A[0]))

    def intersect(self, A, B, C, D):
        return self.ccw(A, C, D) != self.ccw(B, C, D) and self.ccw(A, B, C) != self.ccw(A, B, D)


    def perp(self, a):
        b = empty_like(a)
        b[0] = -a[1]
        b[1] = a[0]
        return b

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


class Wall(arcade.Sprite):

    def __init__(self, image, scale):

        super().__init__(image, scale)


class Player(arcade.Sprite):

    def __init__(self, image, scale):

        super().__init__(image, scale)

        self.speed = 0
        self.angle = 90
        self.center_x = RESET_X
        self.center_y = RESET_Y
        self.speed = 0
        self.distance = 0
        self.lastTime = time.time()

        self.acc = False
        self.dec = False
        self.lef = False
        self.rig = False

        self.dead = False

        self.carLines = list()
        self.carView = list()
        self.carViewHit = list()

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left < 0:
            self.left = 0
            self.change_x = 0  # Zero x speed
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1
            self.change_x = 0

        if self.bottom < 0:
            self.bottom = 0
            self.change_y = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1
            self.change_y = 0
        angle_rad = math.radians(self.angle)

        self.angle += self.change_angle

        self.angle = self.angle % 360

        self.distance += self.speed * (time.time() - self.lastTime)/100
        self.lastTime = time.time()

        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)


class MyGame(arcade.Window):
    global SCREEN_HEIGHT,SCREEN_WIDTH,SCREEN_TITLE

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.wall_list = None
        self.street_list = None
        self.wallhit = None
        self.players = list()

        self.x = 0
        self.y = 0
        self.temp_list = [0,0]
        self.xy0_list = list()
        self.xy1_list = list()
        self.difflist = list()
        self.sectorlinecoords = list()
        self.count0 = 0
        self.click0 = 0
        self.click1 = 0
        self.linie = 0
        self.olddis = 2060

        player_sprite = None
        self.wall_sprite = None
        self.street_sprite = None

        self.p1_health = None

        self.background = None

        self.W = False
        self.A = False
        self.S = False
        self.D = False

        self.set_mouse_visible(True)

    def setup(self):
        global RESET_Y, POPULATION, carViewNum, player_list, playerKeyState
        self.background = arcade.load_texture("Hintergrund.png")

        self.wall_list = arcade.SpriteList()
        self.street_list = arcade.SpriteList()

        self.wallhit = testConnetc()
        self.p1_health = P1_MAX_HEALTH

        self.start = False

        for i in range(POPULATION):
            self.player_sprite = Player("Mclaren Daniel Riccardo.png", SPRITE_SCALING_PLAYERS)
            player_list.append(self.player_sprite)
            self.players.append(0)
            helpList = list()
            for j in range(4):
                helpList.append(False)
            playerKeyState.append(helpList)

            helpList.clear()
            for j in range(carViewNum):
                helpList.append(carViewDis)
            playerViewLen.append(helpList)



    def on_mouse_press(self, x, y, button, key_modifiers):
        if self.linie == 1:
            self.x = x
            self.y = y
            self.temp_list[0] = self.x
            self.temp_list[1] = self.y
            self.xy1_list.append(list(self.temp_list))

            if self.click1 > 0:


                kathete3 = self.xy1_list[self.click1][0] - self.xy1_list[self.click1 - 1][0]
                kathete4 = self.xy1_list[self.click1][1] - self.xy1_list[self.click1 - 1][1]
                hypotenuse1 = math.sqrt(kathete3 ** 2 + kathete4 ** 2)

                if hypotenuse1 > 80:
                    hi = math.ceil(hypotenuse1 / 80)

                    xtemp0 = self.xy1_list[self.click1 - 1][0]
                    ytemp0 = self.xy1_list[self.click1 - 1][1]
                    xtemp1 = self.xy1_list[self.click1][0]
                    ytemp1 = self.xy1_list[self.click1][1]
                    self.xy1_list.pop(self.click1)
                    self.click1 -= 1
                    xdiff = (xtemp1 - xtemp0) / hi
                    ydiff = (ytemp1 - ytemp0) / hi

                    for i in range(hi):
                        xtemp0 = xtemp0 + xdiff
                        ytemp0 = ytemp0 + ydiff
                        self.temp_list[0] = xtemp0
                        self.temp_list[1] = ytemp0
                        self.xy1_list.append(list(self.temp_list))
                        self.click1 += 1

                kathete1 = self.xy1_list[self.click1][0] - self.xy1_list[0][0]
                kathete2 = self.xy1_list[self.click1][1] - self.xy1_list[0][1]
                hypotenuse0 = math.sqrt(kathete1 ** 2 + kathete2 ** 2)

                if hypotenuse0 < 50 and self.click1 > 1:
                    self.temp_list[0] = self.xy1_list[0][0]
                    self.temp_list[1] = self.xy1_list[0][1]
                    self.linie += 1
                    self.xy1_list.append(list(self.temp_list))

            self.click1 += 1

        if self.linie == 0:
            self.x = x
            self.y = y
            self.temp_list[0] = self.x
            self.temp_list[1] = self.y
            self.xy0_list.append(list(self.temp_list))

            if self.click0 > 0:

                if self.x == self.xy0_list[len(self.xy0_list)-2][0]:
                    hy = self.xy0_list[len(self.xy0_list)-1][1]
                    self.xy0_list.pop(len(self.xy0_list) - 1)
                    self.temp_list[0] = self.x + 10
                    self.temp_list[1] = hy
                    self.xy0_list.append(list(self.temp_list))

                kathete3 = self.xy0_list[self.click0][0] - self.xy0_list[self.click0 - 1][0]
                kathete4 = self.xy0_list[self.click0][1] - self.xy0_list[self.click0 - 1][1]
                hypotenuse1 = math.sqrt(kathete3 ** 2 + kathete4 ** 2)

                if hypotenuse1 > 80:
                    hi = math.ceil(hypotenuse1 / 80)

                    xtemp0 = self.xy0_list[self.click0 - 1][0]
                    ytemp0 = self.xy0_list[self.click0 - 1][1]
                    xtemp1 = self.xy0_list[self.click0][0]
                    ytemp1 = self.xy0_list[self.click0][1]
                    self.xy0_list.pop(self.click0)
                    self.click0 -= 1
                    xdiff = (xtemp1 - xtemp0) / hi
                    ydiff = (ytemp1 - ytemp0) / hi

                    for i in range(hi):
                        xtemp0 = xtemp0 + xdiff
                        ytemp0 = ytemp0 + ydiff
                        self.temp_list[0] = xtemp0
                        self.temp_list[1] = ytemp0
                        self.xy0_list.append(list(self.temp_list))
                        self.click0 += 1

                kathete1 = self.xy0_list[self.click0][0] - self.xy0_list[0][0]
                kathete2 = self.xy0_list[self.click0][1] - self.xy0_list[0][1]
                hypotenuse0 = math.sqrt(kathete1 ** 2 + kathete2 ** 2)

                if hypotenuse0 < 50 and self.click0 > 1:
                    self.temp_list[0] = self.xy0_list[0][0]
                    self.temp_list[1] = self.xy0_list[0][1]
                    self.linie += 1
                    self.xy0_list.append(list(self.temp_list))

            self.click0 += 1


    def on_draw(self):

        arcade.start_render()

        if self.linie < 20:
            if self.click0 > 1:
                arcade.draw_line_strip(self.xy0_list, arcade.color.BLACK, 1)

            if self.click0 >= 1:
                arcade.draw_point(self.xy0_list[0][0], self.xy0_list[0][1], arcade.color.BLACK, 1)

            if self.click1 > 1:
                arcade.draw_line_strip(self.xy1_list, arcade.color.BLACK, 1)

            if self.click1 >= 1:
                arcade.draw_point(self.xy1_list[0][0], self.xy1_list[0][1], arcade.color.BLACK, 1)
            #for i in range(len(self.sectorlinecoords)-1):
            #    arcade.draw_line(self.sectorlinecoords[i][0][0],self.sectorlinecoords[i][0][1],self.sectorlinecoords[i][1][0],self.sectorlinecoords[i][1][1], arcade.color.BLUE, 2)





        arcade.draw_line_strip(player_list[0].carView, arcade.color.BLUE, 1)
        #arcade.draw_line_strip(self.carLines, arcade.color.RED, 1)

        for i in range(len(player_list)):
            for j in range(len(player_list[i].carViewHit)):
                arcade.draw_point(player_list[i].carViewHit[j][0], player_list[i].carViewHit[j][1], arcade.color.RED, 5)


        player_list.draw()

        arcade.draw_text(f"Distance driven: {self.player_sprite.distance:6.4f}", 10, 90, arcade.color.BLACK)
        arcade.draw_text(f"Angel: {self.player_sprite.angle:6.3f}", 10, 70, arcade.color.BLACK)
        arcade.draw_text(f"Speed: {self.player_sprite.speed:6.3f}", 10, 50, arcade.color.BLACK)
        arcade.draw_text(f"Angel_Speed: {self.player_sprite.change_angle:6.3f}", 10, 30, arcade.color.BLACK)

        for i in range(carViewNum):
            arcade.draw_text(f"distance: {playerViewLen[0][i]:6.3f}", 10, 110 + i*20, arcade.color.BLACK)

        arcade.finish_render()





    def on_update(self, delta_time):
        global carViewDis, playerViewLen, all_cars_dead, cars_dead, carDiag, carAngularAdd, carViewNum, FRICTION, ACCELERATION, DECELERATION, MAX_SPEED, MIN_SPEED, ft

        if self.linie >= 2:

            if ft:
                for i in range(1,len(self.xy1_list)):
                    if self.xy1_list[i-1][0] == self.xy1_list[i][0]:
                        hy = self.xy1_list[i][1]
                        self.xy1_list.pop(i)
                        self.temp_list[0] = self.xy1_list[i-1][0] + 0.1
                        self.temp_list[1] = hy
                        self.xy1_list.append(list(self.temp_list))
                for i in range(1,len(self.xy0_list)):
                    if self.xy0_list[i-1][0] == self.xy0_list[i][0]:
                        hy = self.xy0_list[i][1]
                        self.xy0_list.pop(i)
                        self.temp_list[0] = self.xy0_list[i-1][0] + 0.1
                        self.temp_list[1] = hy
                        self.xy0_list.append(list(self.temp_list))

            for index,player in enumerate(player_list):
                carAng = player.angle
                carX = player.center_x
                carY = player.center_y
                #print(player.carView)
                player.carLines.clear()

                for i in range(4):
                    tempList = [0,0]
                    tempList[0]=(carX+math.cos(-math.radians(90-(carAng + carAngularAdd[i]))) * carDiag)
                    tempList[1]=(carY+math.sin(-math.radians(90-(carAng + carAngularAdd[i]))) * carDiag)
                    player.carLines.append(list(tempList))
                player.carLines.append(player.carLines[0])

                wallHit = False

                for i in range(0, len(self.xy0_list)-1, 1):
                    for j in range(4):
                        if self.wallhit.intersect(self.xy0_list[i], self.xy0_list[i+1], player.carLines[j], player.carLines[j+1]):
                            wallHit = True
                for i in range(0, len(self.xy1_list)-1, 1):
                    for j in range(4):
                        if self.wallhit.intersect(self.xy1_list[i], self.xy1_list[i+1], player.carLines[j], player.carLines[j+1]):
                            wallHit = True

                if wallHit:
                    cars_dead += 1
                    if cars_dead == POPULATION:
                        all_cars_dead = True
                    self.reset(index)


                player.carView.clear()

                for i in range(carViewNum):
                    alpha = carViewAngle / (carViewNum-1)

                    player.carView.append(list([carX,carY]))
                    tempList = [0, 0]
                    tempList[0] = (carX + math.sin(-math.radians(carAng+alpha*i-carViewAngle/2)) * carViewDis)
                    tempList[1] = (carY + math.cos(-math.radians(carAng+alpha*i-carViewAngle/2)) * carViewDis)
                    player.carView.append(list(tempList))

                player.carViewHit.clear()

                pointRange = list()
                rayDis = list()

                rayDis.clear()
                pointRange.clear()

                helpList = list()

                for id3,playerView in enumerate(player.carView):
                    if id3%2 == 1:

                        for i in range(0, len(self.xy0_list)-1, 1):

                            if id3 < len(player.carView):

                                if self.wallhit.intersect(self.xy0_list[i], self.xy0_list[i+1], playerView, [carX,carY]):
                                    if (carY - playerView[0]) != 0:
                                        m1 = (self.xy0_list[i+1][1] - self.xy0_list[i][1]) / (self.xy0_list[i+1][0] - self.xy0_list[i][0])
                                        b1 = -(m1 * self.xy0_list[i][0]) + self.xy0_list[i][1]

                                        m2 = (carY - playerView[1]) / (carX - playerView[0])

                                        b2 = -(m2 * playerView[0]) + playerView[1]

                                        xi = (b2 - b1) / (m1 - m2)
                                        yi = m2 * xi + b2

                                        dis = math.sqrt((carX-xi)**2 + (carY-yi)**2)
                                        pointRange.append([dis, xi, yi])

                        for i in range(0, len(self.xy1_list) - 1, 1):

                            if id3 < len(player.carView):
                                if self.wallhit.intersect(self.xy1_list[i], self.xy1_list[i + 1], playerView,[carX,carY]):

                                    if (carY - playerView[0]) != 0:
                                        m1 = (self.xy1_list[i + 1][1] - self.xy1_list[i][1]) / (self.xy1_list[i + 1][0] - self.xy1_list[i][0])
                                        b1 = -(m1 * self.xy1_list[i][0]) + self.xy1_list[i][1]
                                        m2 = (carY - playerView[1]) / (carX - playerView[0])
                                        b2 = -(m2 * playerView[0]) + playerView[1]

                                        xi = (b2 - b1) / (m1 - m2)
                                        yi = m2 * xi + b2

                                        dis = math.sqrt((carX - xi) ** 2 + (carY - yi) ** 2)
                                        pointRange.append([dis, xi, yi])


                        min = -1
                        minLen = 1920
                        for j in range(len(pointRange)):
                            if j == 0:
                                minLen = pointRange[j][0]
                                min = j
                            else:
                                if pointRange[j][0] < minLen:
                                    minLen = pointRange[j][0]
                                    min = j

                        if min != -1:
                            player.carViewHit.append([pointRange[min][1], pointRange[min][2]])
                            helpList.append(pointRange[min][0])
                        else:
                            helpList.append(carViewDis)
                        pointRange.clear()
                playerViewLen[index] = helpList;

                if player.speed > FRICTION:
                    player.speed -= FRICTION
                elif player.speed < -FRICTION:
                    player.speed += FRICTION
                else:
                    player.speed = 0


                if player.acc and not player.dec:
                    player.speed += ACCELERATION
                elif player.dec and not player.acc:
                    player.speed += -DECELERATION
                if player.lef and not player.rig:
                    player.change_angle = 0.256 * (player.speed - 0.75) ** 3 - 1.344 * (player.speed - 0.75) ** 2 + 1.152 * player.speed - 0.75 + 1.728
                elif player.rig and not player.lef:
                    player.change_angle = -(0.256 * (player.speed - 0.75) ** 3 - 1.344 * (player.speed - 0.75) ** 2 + 1.152 * player.speed - 0.75 + 1.728)

                if player.speed > MAX_SPEED:
                    player.speed = MAX_SPEED
                elif player.speed < -MAX_SPEED:
                    player.speed = -MAX_SPEED
                elif player.speed < -MIN_SPEED:
                    player.speed = -MIN_SPEED
                player.update()

        if(self.start):
            print(len(player_list))
            #neat_implement.init()
            self.start = False



    def on_key_press(self, key, modifiers):
        global RESET_X,RESET_Y, playerKeyState
        w,a,s,d =False,False,False,False
        if key == arcade.key.W:
            player_list[0].acc = True
        elif key == arcade.key.S:
            player_list[0].dec = True
        elif key == arcade.key.A:
            player_list[0].lef = True
        elif key == arcade.key.D:
            player_list[0].rig = True

        if key == arcade.key.UP:
            player_list[1].acc = True
        elif key == arcade.key.DOWN:
            player_list[1].dec = True
        elif key == arcade.key.LEFT:
            player_list[1].lef = True
        elif key == arcade.key.RIGHT:
            player_list[1].rig = True

        if key == arcade.key.E:
            self.exportTrack()
        if key == arcade.key.I:
            self.importTrack()

        if key == arcade.key.R:
            RESET_X = self._mouse_x
            RESET_Y = self._mouse_y

            for index,value in enumerate(player_list):
                self.reset(index)

    def on_key_release(self, key, modifiers):
        global playerKeyState
        if key == arcade.key.W:
            player_list[0].acc = False
        elif key == arcade.key.S:
            player_list[0].dec = False
        elif key == arcade.key.A:
            player_list[0].lef = False
        elif key == arcade.key.D:
            player_list[0].rig = False

        if key == arcade.key.UP:
            player_list[1].acc = False
        elif key == arcade.key.DOWN:
            player_list[1].dec = False
        elif key == arcade.key.LEFT:
            player_list[1].lef = False
        elif key == arcade.key.RIGHT:
            player_list[1].rig = False


        if key == arcade.key.A:
            player_list[0].change_angle = 0
        elif key == arcade.key.D:
            player_list[0].change_angle = 0
        if key == arcade.key.LEFT:
            player_list[1].change_angle = 0
        elif key == arcade.key.RIGHT:
            player_list[1].change_angle = 0

    def reset(self, pid):
        global RESET_X,RESET_Y
        player_list[pid].center_x = RESET_X
        player_list[pid].center_y = RESET_Y
        player_list[pid].speed = 0
        player_list[pid].angle = 90

    def acc(self, id, tf):
        player_list[id].acc = tf
    def dec(self, id, tf):
        player_list[id].dec = tf
    def rig(self, id, tf):
        player_list[id].lef = tf
    def lef(self, id, tf):
        player_list[id].rig = tf
    def getViewLen(self, i):
        return playerViewLen[i]

    def exportTrack(self):
        print("exporting")

        data = ["",""]

        #Tabelle1 = [[5, 35], [76, 24], [97, 75]]
        TempT0 = list()
        TempT1 = list()
        for id, element in enumerate(self.xy0_list):
            TempT0.append(element[0])
            TempT1.append(element[1])

        Tabelle_x0 = list(map(str, TempT0))
        Tabelle_y0 = list(map(str, TempT1))

        TempT0.clear()
        TempT1.clear()


        for id, element in enumerate(self.xy1_list):
            TempT0.append(element[0])
            TempT1.append(element[1])

        Tabelle_x1 = list(map(str, TempT0))
        Tabelle_y1 = list(map(str, TempT1))

        TempT0.clear()
        TempT1.clear()

        print(Tabelle_x0)
        print(Tabelle_y0)
        print(Tabelle_x1)
        print(Tabelle_y1)

        ttx1 = list()
        tty1 = list()
        ttx2 = list()
        tty2 = list()

        for id,elem in enumerate(self.xy0_list):
            ttx1.append(elem[0])
            tty1.append(elem[1])
        for id,elem in enumerate(self.xy1_list):
            ttx2.append(elem[0])
            tty2.append(elem[1])


        with open('track.csv', 'w', newline='') as f:
            writer = csv.writer(f)

            # write the data

            writer.writerow(np.array(ttx1))
            writer.writerow(np.array(tty1))
            writer.writerow(np.array(ttx2))
            writer.writerow(np.array(tty2))
        print("done exporting")

    def importTrack(self):
        print("importing")

        self.xy0_list = list()
        self.xy1_list = list()

        dataList00 = list()
        dataList01 = list()
        dataList10 = list()
        dataList11= list()

        data = list()

        with open('track.csv', 'r') as f:
            reader = csv.reader(f)

            for row in reader:
                data.append(row)
                print(row)


        print("done importing")

        dataList00 = data[0]
        dataList01 = data[1]
        dataList10 = data[2]
        dataList11 = data[3]

        for id,elem in enumerate(dataList00):
            hl = list()
            hl.append(int(elem))
            hl.append(int(dataList01[id]))
            self.xy0_list.append(list(hl))
            hl.clear()
        for id,elem in enumerate(dataList10):
            hl = list()
            hl.append(int(elem))
            hl.append(int(dataList11[id]))
            self.xy1_list.append(list(hl))
            hl.clear()
        self.linie = 2
        self.click0 = 100
        self.click1 = 100


def main():

    window = MyGame()
    window.setup()
    arcade.set_background_color(arcade.color.WHITE)
    arcade.run()

def getPlayerList():
    return player_list


if __name__ == "__main__":

    main()






