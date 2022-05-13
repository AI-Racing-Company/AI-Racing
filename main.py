import arcade
import datetime
from os import path
import time
import math

DIR = path.dirname(path.abspath(__file__))

SPRITE_SCALING_PLAYERS = 1

P1_MAX_HEALTH = 1

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 442
SCREEN_TITLE = "AI-Racing"

ACCELERATION = 0.1
DECELERATION = 0.05
MAX_SPEED = 3
ANGLE_SPEED = 2
FRICTION = 0.005


class Player1(arcade.Sprite):

    def __init__(self, image, scale):

        super().__init__(image, scale)

        self.speed = 0

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

        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player1_list = None
        self.wall_list = None

        self.player1_sprite = None

        self.p1_health = None

        self.background = None

        self.W = False
        self.A = False
        self.S = False
        self.D = False

        self.set_mouse_visible(False)

    def setup(self):

        self.background = arcade.load_texture(f"{DIR}\\Monaco.png")

        self.player1_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        self.p1_health = P1_MAX_HEALTH

        self.player1_sprite = Player1("Mclaren Daniel Riccardo.png", SPRITE_SCALING_PLAYERS)
        self.player1_sprite.center_x = SCREEN_WIDTH/2
        self.player1_sprite.center_y = 50
        self.player1_list.append(self.player1_sprite)

        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text(f"Speed: {self.player1_sprite.speed:6.3f}", 10, 50, arcade.color.BLACK)

        self.player1_list.draw()

    def on_update(self, delta_time):
        if self.player1_sprite.speed > FRICTION:
            self.player1_sprite.speed -= FRICTION
        elif self.player1_sprite.speed < -FRICTION:
            self.player1_sprite.speed += FRICTION
        else:
            self.player1_sprite.speed = 0

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
            self.player1_sprite.change_angle = ANGLE_SPEED
        elif self.D and not self.A:
            self.player1_sprite.change_angle = -ANGLE_SPEED

        if self.player1_sprite.speed > MAX_SPEED:
            self.player1_sprite.speed = MAX_SPEED
        elif self.player1_sprite.speed < -MAX_SPEED:
            self.player1_sprite.speed = -MAX_SPEED
        if self.player1_sprite.speed > MAX_SPEED:
            self.player1_sprite.speed = MAX_SPEED
        elif self.player1_sprite.speed < -MAX_SPEED:
            self.player1_sprite.speed = -MAX_SPEED
        self.player1_list.update()

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

        if key == arcade.key.A or key == arcade.key.D:
            self.player1_sprite.change_angle = 0



def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
