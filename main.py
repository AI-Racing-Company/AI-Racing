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
MAX_MOVEMENT_SPEED = 10
MOVEMENT_SPEED = 2
ANGLE_SPEED = 2
START_TIME = 0
END_TIME = 0
DELTA_TIME = 0

winner = None

class Player1(arcade.Sprite):

    def __init__(self, image, scale):

        super().__init__(image, scale)

        self.max_speed = 10
        self.speed = 0
        self.acceleration = 0.1

    def update(self):
        angle_rad = math.radians(self.angle)

        self.angle += self.change_angle

        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)



class MyGame(arcade.Window):


    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)

        self.player1_list = None
        self.wall_list = None

        self.player1_sprite = None

        self.p1_health = None

        self.background = None

        self.set_mouse_visible(False)

    def setup(self):

        self.background = arcade.load_texture(f"{DIR}\\Monaco.png")

        self.player1_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        self.p1_health = P1_MAX_HEALTH

        self.player1_sprite = Player1("Mclaren Daniel Riccardo.png",SPRITE_SCALING_PLAYERS)
        self.player1_sprite.center_x = SCREEN_WIDTH/2
        self.player1_sprite.center_y = 50
        self.player1_list.append(self.player1_sprite)

        arcade.set_background_color(arcade.color.BLACK)

        #self.physics_engine1 = arcade.PhysicsEngineSimple(self.player1_sprite, self.wall_list)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT, self.background)

        self.player1_list.draw()

    def on_update(self, delta_time):

        self.player1_list.update()

    def on_key_press(self, key, modifiers):

        if key == arcade.key.W:
            if MOVEMENT_SPEED < MAX_MOVEMENT_SPEED:
                self.player1_sprite.speed = MOVEMENT_SPEED
                movement_speed = MOVEMENT_SPEED + ACCELERATION
            else:
                self.player1_sprite.speed = MOVEMENT_SPEED

        elif key == arcade.key.S:
            self.player1_sprite.speed = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player1_sprite.change_angle = ANGLE_SPEED
        elif key == arcade.key.D:
            self.player1_sprite.change_angle = -ANGLE_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.player1_sprite.speed = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player1_sprite.change_angle = 0





def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
