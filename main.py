import arcade
import datetime
from os import path
import time
import math
import pyautogui
import neat

# Function for Angelspeed dependend on Speed 0.256 *(x-0.75)**(3)-1.344 *(x-0.75)**(2)+1.152 *(x-0.75)+1.728


DIR = path.dirname(path.abspath(__file__))

SPRITE_SCALING_PLAYERS = 1 #23 * 67 px
carDiag = 35.41 #len of diagonal
carAngularAdd = [19,161,-161,-19]# angles to add for calculation
carViewNum = 20
carViewAngle = 200

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

POPULATION = 3


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

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player_list = None
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
        global RESET_Y, POPULATION
        self.background = arcade.load_texture("Hintergrund.png")
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.street_list = arcade.SpriteList()

        self.wallhit = testConnetc()
        self.p1_health = P1_MAX_HEALTH

        for i in range(POPULATION):
            self.player_sprite = Player("Mclaren Daniel Riccardo.png", SPRITE_SCALING_PLAYERS)
            self.player_list.append(self.player_sprite)
            self.players.append(0)


        count = 0
        count1 = 0


    def on_mouse_press(self, x, y, button, key_modifiers):
        if self.linie == 1:
            self.x = x
            self.y = y
            self.temp_list[0] = self.x
            self.temp_list[1] = self.y
            if self.click1 > 1:
                kathete1 = self.xy1_list[self.click1-1][0]-self.xy1_list[0][0]
                kathete2 = self.xy1_list[self.click1-1][1]-self.xy1_list[0][1]
                hypotenuse = math.sqrt(kathete1**2 + kathete2**2)
                if hypotenuse < 50:
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
            if self.click0 > 1:
                kathete1 = self.xy0_list[self.click0-1][0]-self.xy0_list[0][0]
                kathete2 = self.xy0_list[self.click0-1][1]-self.xy0_list[0][1]
                hypotenuse = math.sqrt(kathete1**2 + kathete2**2)
                if hypotenuse < 50:

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





        arcade.draw_line_strip(self.player_list[0].carView, arcade.color.BLUE, 1)
        #arcade.draw_line_strip(self.carLines, arcade.color.RED, 1)

        for i in range(len(self.player_list)):
            for j in range(len(self.player_list[i].carViewHit)):
                arcade.draw_point(self.player_list[i].carViewHit[j][0], self.player_list[i].carViewHit[j][1], arcade.color.RED, 5)


        self.player_list.draw()

        arcade.draw_text(f"Distance: {self.player_sprite.distance:6.4f}", 10, 90, arcade.color.BLACK)
        arcade.draw_text(f"Angel: {self.player_sprite.angle:6.3f}", 10, 70, arcade.color.BLACK)
        arcade.draw_text(f"Speed: {self.player_sprite.speed:6.3f}", 10, 50, arcade.color.BLACK)
        arcade.draw_text(f"Angel_Speed: {self.player_sprite.change_angle:6.3f}", 10, 30, arcade.color.BLACK)

        arcade.finish_render()
    def on_update(self, delta_time):
        global carDiag, carAngularAdd, carViewNum, FRICTION, ACCELERATION, DECELERATION, MAX_SPEED, MIN_SPEED

        if self.linie >= 2:

            for index,player in enumerate(self.player_list):
                carAng = player.angle
                carX = player.center_x
                carY = player.center_y
                print(player.carView)
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
                    self.reset(index)


                player.carView.clear()

                for i in range(carViewNum):
                    alpha = carViewAngle / carViewNum
                    alpha += alpha / carViewNum
                    player.carView.append(list([carX,carY]))
                    tempList = [0, 0]
                    tempList[0] = (carX + math.sin(-math.radians(carAng+alpha*i-carViewAngle/2)) * 500)
                    tempList[1] = (carY + math.cos(-math.radians(carAng+alpha*i-carViewAngle/2)) * 500)
                    player.carView.append(list(tempList))

                player.carViewHit.clear()

                pointRange = list()
                rayDis = list()

                rayDis.clear()
                pointRange.clear()

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
                        pointRange.clear()

                if player.speed > FRICTION:
                    player.speed -= FRICTION
                elif player.speed < -FRICTION:
                    player.speed += FRICTION
                else:
                    player.speed = 0

                if self.W and not self.S:
                    player.speed += ACCELERATION
                elif self.S and not self.W:
                    player.speed += -DECELERATION
                if self.A and not self.D:
                    player.change_angle = 0.256 * (player.speed - 0.75) ** 3 - 1.344 * (player.speed - 0.75) ** 2 + 1.152 * player.speed - 0.75 + 1.728
                elif self.D and not self.A:
                    player.change_angle = -(0.256 * (player.speed - 0.75) ** 3 - 1.344 * (player.speed - 0.75) ** 2 + 1.152 * player.speed - 0.75 + 1.728)

                if player.speed > MAX_SPEED:
                    player.speed = MAX_SPEED
                elif player.speed < -MAX_SPEED:
                    player.speed = -MAX_SPEED
                elif player.speed < -MIN_SPEED:
                    player.speed = -MIN_SPEED
                player.update()

      #          if self.count0 == 0:
     #               if len(self.xy0_list) <= len(self.xy1_list):
  ###                      print("1.")
 #                       for i in range(len(self.xy0_list)):
#
 #                           for j in range(len(self.xy1_list)):
#
        #                        dis = math.sqrt((self.xy1_list[j][0] - self.xy0_list[i][0]) ** 2 + (self.xy1_list[j][1] - self.xy0_list[i][1]) ** 2)
       #                         if dis < self.olddis:
      #                              self.olddis = dis
     #                               self.difflist.append(self.olddis)
    #                                self.xy0 = [self.xy0_list[i][0], self.xy0_list[i][1]]
   #                                 self.xy1 = [self.xy1_list[j][0], self.xy1_list[j][1]]
  #                                  self.temp_list[0] = self.xy0
 #                                   self.temp_list[1] = self.xy1
#
 #                           self.olddis = 2060
#
 #                           self.sectorlinecoords.append(list(self.temp_list))
#
    #                    self.count0 +=1
   #                 if len(self.xy0_list) > len(self.xy1_list):
  #                      print("2.")
 #                       for i in range(len(self.xy1_list)):
#
 #                           for j in range(len(self.xy0_list)):
#
        #                        dis = math.sqrt((self.xy1_list[i][0] - self.xy0_list[j][0]) ** 2 + (self.xy1_list[i][1] - self.xy0_list[j][1]) ** 2)
       #                         if dis < self.olddis:
      #                              self.olddis = dis
     #                               self.difflist.append(self.olddis)
    #                                self.xy0 = [self.xy0_list[j][0], self.xy0_list[j][1]]
   #                                 self.xy1 = [self.xy1_list[i][0], self.xy1_list[i][1]]
  #                                  self.temp_list[0] = self.xy0
 #                                   self.temp_list[1] = self.xy1
#
 #                           self.olddis = 2060
#
 #                           self.sectorlinecoords.append(list(self.temp_list))
#
#                        self.count0 +=1





    def on_key_press(self, key, modifiers):
        global RESET_X,RESET_Y
        if key == arcade.key.W:
            self.W = True
        elif key == arcade.key.S:
            self.S = True
        elif key == arcade.key.A:
            self.A = True
        elif key == arcade.key.D:
            self.D = True
        if key == arcade.key.R:
            RESET_X = self._mouse_x
            RESET_Y = self._mouse_y

            for index,value in enumerate(self.player_list):
                self.reset(index)

    def on_key_release(self, key, modifiers):

        if key == arcade.key.W:
            self.W = False
        elif key == arcade.key.S:
            self.S = False
        elif key == arcade.key.A:
            self.A = False
        elif key == arcade.key.D:
            self.D = False

        for i in range(len(self.player_list)):
            if key == arcade.key.A:
                self.player_list[i].change_angle = 0
            elif key == arcade.key.D:
                self.player_list[i].change_angle = 0

    def reset(self, pid):
        global RESET_X,RESET_Y
        self.player_list[pid].center_x = RESET_X
        self.player_list[pid].center_y = RESET_Y
        self.player_list[pid].speed = 0
        self.player_list[pid].angle = 90

    def eval_genomes(self, genomes, config):
        for genome_id, genome in genomes:
            genome.fitness = 4.0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            for xi, xo in enumerate(self.players):
                output = net.activate(xi)
                genome.fitness -= (output[0] - xo[0]) ** 2

def main():
    window = MyGame()
    window.setup()
    arcade.set_background_color(arcade.color.WHITE)
    arcade.run()


if __name__ == "__main__":
    main()





