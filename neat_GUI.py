import threading

import arcade
from os import path
import time
import math
import pyautogui
import csv
import numpy as np
import neat_implement

# Function for Angelspeed dependend on Speed 0.256 *(x-0.75)**(3)-1.344 *(x-0.75)**(2)+1.152 *(x-0.75)+1.728
# Use this variable to count merges: 1

# TODO:
# Nothing in particular


DIR = path.dirname(path.abspath(__file__))

SPRITE_SCALING_PLAYERS = 1  # 23 * 67 px
carDiag = 35.41  # len of diagonal
carAngularAdd = [19, 161, -161, -19]  # angles to add for calculation
carViewNum = 5
carViewAngle = 200
carViewDis = 500
playerViewLen = list()
playerKeyState = list()

P1_MAX_HEALTH = 1

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
SCREEN_HEIGHT = int(SCREEN_HEIGHT * 0.9)
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

lastCars = 1500





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




class MyGame(arcade.Window):
    global SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_TITLE

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.wall_list = None
        self.street_list = None
        self.wallhit = None
        self.players = list()

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

        self.importTrack()



    def on_draw(self):

        arcade.start_render()

        arcade.dr

        if self.linie < 20:
            if self.click0 > 1:
                arcade.draw_line_strip(self.xy0_list, arcade.color.BLACK, 1)

            if self.click0 >= 1:
                arcade.draw_point(self.xy0_list[0][0], self.xy0_list[0][1], arcade.color.BLACK, 1)

            if self.click1 > 1:
                arcade.draw_line_strip(self.xy1_list, arcade.color.BLACK, 1)

            if self.click1 >= 1:
                arcade.draw_point(self.xy1_list[0][0], self.xy1_list[0][1], arcade.color.BLACK, 1)

        player_list.draw()

        arcade.draw_text(len(player_list), 10, 90, arcade.color.BLACK)

        arcade.finish_render()

    def on_update(self, delta_time):
        global player_list

        with open('playerData.csv', 'r') as f:
            data = list()
            player_list.clear()
            reader = csv.reader(f)

            for row in reader:
                data.append(row)

            for id,elem in enumerate(data):
                player_list.append(Player("Mclaren Daniel Riccardo.png", SPRITE_SCALING_PLAYERS))
                player_list[id].center_x = float(elem[0])
                player_list[id].center_y = float(elem[1])
                player_list[id].angle = float(elem[2])




    def importTrack(self):
        print("importing")

        self.xy0_list = list()
        self.xy1_list = list()

        dataList00 = list()
        dataList01 = list()
        dataList10 = list()
        dataList11 = list()

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


def main():
    window = MyGame()
    window.setup()
    arcade.set_background_color(arcade.color.WHITE)
    arcade.run()



if __name__ == "__main__":
    main()






