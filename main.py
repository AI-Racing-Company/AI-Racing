import arcade
import datetime
from os import path
import time
import math

# Function for Angelspeed dependend on Speed 0.256 *(x-0.75)**(3)-1.344 *(x-0.75)**(2)+1.152 *(x-0.75)+1.728


DIR = path.dirname(path.abspath(__file__))

SPRITE_SCALING_PLAYERS = 1 #25 * 69 px
carDiag = 35.41 #len of diagonal
carAngularAdd = [19,161,-161,-19]# angles to add for calculation
carViewNum = 15
carViewAngle = 200

P1_MAX_HEALTH = 1

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "AI-Racing"

ACCELERATION = 0.05
DECELERATION = 0.1
MAX_SPEED = 3
MIN_SPEED = 0
ANGLE_SPEED = 2
FRICTION = 0.005


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


class Player1(arcade.Sprite):

    def __init__(self, image, scale):

        super().__init__(image, scale)

        self.speed = 0
        self.angle = 90

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

        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)


class MyGame(arcade.Window):



    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player1_list = None
        self.wall_list = None
        self.street_list = None
        self.wallhit = None
        self.carLines = list()
        self.carView = list()
        self.carViewHit = list()

        self.x = 0
        self.y = 0
        self.temp_list = [0,0]
        self.xy0_list = list()
        self.xy1_list = list()
        self.click0 = 0
        self.click1 = 0
        self.linie = 0

        self.player1_sprite = None
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

        self.background = arcade.load_texture("Hintergrund.png")
        self.player1_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.street_list = arcade.SpriteList()



        self.wallhit = testConnetc()


        self.p1_health = P1_MAX_HEALTH
        strecke = [11,12,13,14,15,16,17,18,21,28,31,38,41,48,51,58,61,68,71,78,81,88,91,98,101,108,111,118,121,128,131,138,141,148,151,158,161,162,163,164,165,166,167,168]

        self.player1_sprite = Player1("Mclaren Daniel Riccardo.png", SPRITE_SCALING_PLAYERS)
        self.player1_sprite.center_x = SCREEN_WIDTH / 2
        self.player1_sprite.center_y = 140
        self.player1_list.append(self.player1_sprite)

        self.player1_sprite.center_x = 500
        self.player1_sprite.center_y = 150
        self.player1_sprite.speed = 0
        self.player1_sprite.angle = 90

        count = 0
        count1 = 0

       # for x in range(0, 18):
       #     for y in range(0, 10):
       #         if count1 == len(strecke) or not count == strecke[count1]:
       #             self.wall_sprite = Wall("Barriere.png", SPRITE_SCALING_PLAYERS)
       #             self.wall_sprite.center_x = 50 + x * 100
       #             self.wall_sprite.center_y = 950 - y * 100
       #             self.wall_list.append(self.wall_sprite)
       #
       #         else:
       #
       #             count1 += 1
       #         count += 1
       #
       # for z in range(0, len(strecke)):
       #     for x in range(0, 18):
       #         for y in range(0, 10):
       #             y = strecke[z] % 10
       #             x = int(strecke[z] / 10)
       #             self.street_sprite = Wall("Street.png", SPRITE_SCALING_PLAYERS)
       #             self.street_sprite.center_x = 50 + x * 100
       #             self.street_sprite.center_y = 950 - y * 100
       #             self.street_list.append(self.street_sprite)

    def on_mouse_press(self, x, y, button, key_modifiers):
        if self.linie == 1:
            self.x = x
            self.y = y
            self.temp_list[0] = self.x
            self.temp_list[1] = self.y
            self.xy1_list.append(list(self.temp_list))
            self.click1 += 1
            kathete1 = self.xy1_list[self.click1-1][0]-self.xy1_list[0][0]
            kathete2 = self.xy1_list[self.click1-1][1]-self.xy1_list[0][1]
            hypotenuse = math.sqrt(kathete1**2 + kathete2**2)
            if hypotenuse < 50 and self.click1 > 1:
                self.temp_list[0] = self.xy1_list[0][0]
                self.temp_list[1] = self.xy1_list[0][1]
                self.xy1_list.append(list(self.temp_list))
                self.linie += 1


        if self.linie == 0:
            self.x = x
            self.y = y
            self.temp_list[0] = self.x
            self.temp_list[1] = self.y
            self.xy0_list.append(list(self.temp_list))
            self.click0 += 1
            print(self.xy0_list)
            kathete1 = self.xy0_list[self.click0-1][0]-self.xy0_list[0][0]
            kathete2 = self.xy0_list[self.click0-1][1]-self.xy0_list[0][1]
            hypotenuse = math.sqrt(kathete1**2 + kathete2**2)
            if hypotenuse < 50 and self.click0 > 1:

                self.temp_list[0] = self.xy0_list[0][0]
                self.temp_list[1] = self.xy0_list[0][1]
                self.xy0_list.append(list(self.temp_list))
                self.linie += 1




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


        #arcade.draw_line_strip(self.carView, arcade.color.BLUE, 1)
        #arcade.draw_line_strip(self.carLines, arcade.color.RED, 1)

        for i in range(len(self.carViewHit)):
            arcade.draw_point(self.carViewHit[i][0], self.carViewHit[i][1], arcade.color.RED, 5)


        #self.street_list.draw()
        #self.wall_list.draw()
        self.player1_list.draw()
        #count1 = 0
        """Da um zu wissen welche Barriere wo ist"""
        #for x in range(0, 18):
        #    for y in range(0, 10):
        #        arcade.draw_text(count1,  50 + x*100,  950 - y*100, arcade.color.WHITE)
        #        count1 += 1


        arcade.draw_text(f"Speed: {self.player1_sprite.speed:6.3f}", 10, 50, arcade.color.BLACK)
        arcade.draw_text(f"Angel_Speed: {self.player1_sprite.change_angle:6.3f}", 10, 30, arcade.color.BLACK)
        arcade.draw_text(f"Angel: {self.player1_sprite.angle:6.3f}", 10, 70, arcade.color.BLACK)
        arcade.finish_render()
    def on_update(self, delta_time):
        global carDiag, carAngularAdd, carViewNum
        #
        # upper left corner angle add: 20
        # upper right: -20
        # lower left: 160
        # lower right: -160
        #

        if self.linie >= 2:

            carAng = self.player1_sprite.angle
            carX = self.player1_sprite.center_x
            carY = self.player1_sprite.center_y

            self.carLines.clear()

            for i in range(4):
                tempList = [0,0]
                tempList[0]=(carX+math.cos(-math.radians(90-(carAng + carAngularAdd[i]))) * carDiag)
                tempList[1]=(carY+math.sin(-math.radians(90-(carAng + carAngularAdd[i]))) * carDiag)
                self.carLines.append(list(tempList))
            self.carLines.append(self.carLines[0])

            wallHit = False

            for i in range(0, len(self.xy0_list)-1, 1):
                for j in range(4):
                    if self.wallhit.intersect(self.xy0_list[i], self.xy0_list[i+1], self.carLines[j], self.carLines[j+1]):
                        wallHit = True
            for i in range(0, len(self.xy1_list)-1, 1):
                for j in range(4):
                    if self.wallhit.intersect(self.xy1_list[i], self.xy1_list[i+1], self.carLines[j], self.carLines[j+1]):
                        wallHit = True

            if wallHit:
                self.player1_sprite.center_x = 500
                self.player1_sprite.center_y = 150
                self.player1_sprite.speed = 0
                self.player1_sprite.angle = 90


            self.carView.clear()

            for i in range(carViewNum):
                alpha = (carViewAngle+carViewAngle / carViewNum) / carViewNum # Don't touch, it works!!!
                self.carView.append(list([carX,carY]))
                tempList = [0, 0]
                tempList[0] = (carX + math.sin(-math.radians(carAng+alpha*i-carViewAngle/2)) * 500)
                tempList[1] = (carY + math.cos(-math.radians(carAng+alpha*i-carViewAngle/2)) * 500)
                self.carView.append(list(tempList))

            self.carViewHit.clear()

            pointRange = list()

            rayDis = list()
            rayDis.clear()
            pointRange.clear()

            for j in range(len(self.carView) - 1):
                for i in range(0, len(self.xy0_list)-1, 1):
                    if self.wallhit.intersect(self.xy0_list[i], self.xy0_list[i+1], self.carView[j], self.carView[j+1]):

                        m1 = (self.xy0_list[i+1][1] - self.xy0_list[i][1]) / (self.xy0_list[i+1][0] - self.xy0_list[i][0])
                        b1 = -(m1 * self.xy0_list[i][0]) + self.xy0_list[i][1]

                        m2 = (self.carView[j+1][1] - self.carView[j][1]) / (self.carView[j+1][0] - self.carView[j][0])
                        b2 = -(m2 * self.carView[j][0]) + self.carView[j][1]

                        xi = (b2 - b1) / (m1 - m2)
                        yi = m2 * xi + b2

                        dis = math.sqrt((carX-xi)**2 + (carY-yi)**2)
                        pointRange.append([dis, xi, yi])

                for i in range(0, len(self.xy1_list) - 1, 1):
                    if self.wallhit.intersect(self.xy1_list[i], self.xy1_list[i + 1], self.carView[j],self.carView[j + 1]):

                        m1 = (self.xy1_list[i + 1][1] - self.xy1_list[i][1]) / (self.xy1_list[i + 1][0] - self.xy1_list[i][0])
                        b1 = -(m1 * self.xy1_list[i][0]) + self.xy1_list[i][1]

                        m2 = (self.carView[j + 1][1] - self.carView[j][1]) / (self.carView[j + 1][0] - self.carView[j][0])
                        b2 = -(m2 * self.carView[j][0]) + self.carView[j][1]

                        xi = (b2 - b1) / (m1 - m2)
                        yi = m2 * xi + b2

                        dis = math.sqrt((carX - xi) ** 2 + (carY - yi) ** 2)
                        pointRange.append([dis, xi, yi])

                min = -1
                minLen = 1920
                for j in range(len(pointRange)):
                    print(pointRange[j][0])
                    print(j)
                    if j == 0:
                        minLen = pointRange[j][0]
                        min = j
                    else:
                        if pointRange[j][0] < minLen:
                            minLen = pointRange[j][0]
                            min = j

                if min != -1:
                    self.carViewHit.append([pointRange[min][1], pointRange[min][2]])
                pointRange.clear()



            # for i in range(0, len(self.xy1_list)-1, 1):
            #     for j in range(len(self.carView)-1):
            #         if self.wallhit.intersect(self.xy1_list[i], self.xy1_list[i+1], self.carView[j], self.carView[j+1]):
            #             print("hit " + str(time.time()))

        # if self.player1_sprite.collides_with_list(self.wall_list):
        #     self.player1_sprite.center_x = 500
        #     self.player1_sprite.center_y = 150
        #     self.player1_sprite.speed = 0
        #     self.player1_sprite.angle = 90



        if self.player1_sprite.speed > FRICTION:
            self.player1_sprite.speed -= FRICTION
        elif self.player1_sprite.speed < -FRICTION:
            self.player1_sprite.speed += FRICTION
        else:
            self.player1_sprite.speed = 0

        if self.W and not self.S:
            self.player1_sprite.speed += ACCELERATION
        elif self.S and not self.W:
            self.player1_sprite.speed += -DECELERATION
        if self.A and not self.D:
            self.player1_sprite.change_angle = 0.256 * (self.player1_sprite.speed-0.75)**3-1.344 * (self.player1_sprite.speed-0.75)**2 + 1.152 * self.player1_sprite.speed-0.75+1.728
        elif self.D and not self.A:
            self.player1_sprite.change_angle = -(0.256 * (self.player1_sprite.speed-0.75)**3 - 1.344 * (self.player1_sprite.speed-0.75)**2+1.152 * self.player1_sprite.speed-0.75+1.728)

        if self.player1_sprite.speed > MAX_SPEED:
            self.player1_sprite.speed = MAX_SPEED
        elif self.player1_sprite.speed < -MAX_SPEED:
            self.player1_sprite.speed = -MAX_SPEED
        elif self.player1_sprite.speed < -MIN_SPEED:
            self.player1_sprite.speed = -MIN_SPEED
        self.player1_list.update()



        #any_collisions = arcade.check_for_collision_with_list(self.player1_sprite,self.xy1_list)
        #if len(any_collisions) > 0:
        #    print("dead")

    def on_key_press(self, key, modifiers):

        if key == arcade.key.W:
            self.W = True
        elif key == arcade.key.S:
            self.S = True
        elif key == arcade.key.A:
            self.A = True
        elif key == arcade.key.D:
            self.D = True

    def on_key_release(self, key, modifiers):

        if key == arcade.key.W:
            self.W = False
        elif key == arcade.key.S:
            self.S = False
        elif key == arcade.key.A:
            self.A = False
        elif key == arcade.key.D:
            self.D = False

        if key == arcade.key.A:
            self.player1_sprite.change_angle = 0
        elif key == arcade.key.D:
            self.player1_sprite.change_angle = 0



def main():
    window = MyGame()
    window.setup()
    arcade.set_background_color(arcade.color.WHITE)
    arcade.run()


if __name__ == "__main__":
    main()





