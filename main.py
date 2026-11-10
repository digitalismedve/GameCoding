import arcade, random, time, math

MAP_BOTTOM = -2176
MAP_TOP = 2160*2
MAP_LEFT = -3840
MAP_RIGHT = 3840*2

TREES=100
WINDOW_WIDTH = 1250
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"
TILE_SCALING = 0.5
PLAYER_DASH_LENGTH = 512
GRASS_TEXTURES = []
for i in range(10):
    GRASS_TEXTURES.append("/home/akocsis/ComputerStuff/PythonStuff/GameCoding/grass.png ")
for i in range(5):
    GRASS_TEXTURES.append("/home/akocsis/ComputerStuff/PythonStuff/GameCoding/grass"+str(i+1)+".png")
POSSIBLE_X = []
POSSIBLE_Y = []
for i in range(MAP_LEFT, MAP_RIGHT, 64):
    POSSIBLE_X.append(i)
for i in range(MAP_BOTTOM, MAP_TOP, 64):
    POSSIBLE_Y.append(i)

class GameView(arcade.Window):
    def __init__(self):
        self.last_change=time.time()
        
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, fullscreen=True)
        self.only_camera=False
        self.PLAYER_MOVEMENT_SPEED = 8
        self.tp_animation_frames = []
        self.tp_animation_index = 0
        self.tp_animation_elapsed = 0.0
        self.mouse_x=0
        self.mouse_y=0
        self.show_coordinates = False
        self.max_health = 100
        self.health = self.max_health
        self.dash_time = 0
        self.last_key=""
        self.game_camera = None
        self.player_texture_left_1 = arcade.load_texture("player_left.png")
        self.player_texture_left_2 = arcade.load_texture("player_left_2.png")
        self.player_texture_right_1 = arcade.load_texture("player_right.png")
        self.player_texture_right_2 = arcade.load_texture("player_right_2.png")
        self.blank_texture = arcade.load_texture("blank.png")
        self.axe_sprite = arcade.Sprite("box.png", scale=0.625)
        self.axe_sprite_list = arcade.SpriteList()
        self.axe_sprite_list.append(self.axe_sprite)
        self.tp_texture = arcade.load_texture("tp.png")
        self.tp1 = arcade.load_texture("tp_anim_1.png")
        self.tp2 = arcade.load_texture("tp_anim_2.png")
        self.tp3 = arcade.load_texture("tp_anim_3.png")

        #self.player_texture_left_left = arcade.load_texture("/home/akocsis/ComputerScactuff/PythonStuff/GameCoding/player_left_left.png")
        #self.player_texture_left_right = arcade.load_texture("/home/akocsis/ComputerStuff/PythonStuff/GameCoding/player_left_right.png")
        #self.player_texture_right_left = arcade.load_texture("/home/akocsis/ComputerStuff/PythonStuff/GameCoding/player_right_left.png")
        #self.player_texture_right_right = arcade.load_texture("/home/akocsis/ComputerStuff/PythonStuff/GameCoding/player_right_right.png")


        self.player_sprite = arcade.Sprite(self.player_texture_left_1)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list = arcade.SpriteList()
        self.tp=arcade.Sprite(self.blank_texture)
        self.player_list.append(self.player_sprite)
        self.player_list.append(self.tp)
        self.player_sprite.hit_box = arcade.hitbox.HitBox(points=[(-32, -32), (32, -32), (32, 32), (-32, 32)], position=self.player_sprite.position)

        self.game_camera=arcade.Camera2D()
        self.gui_camera=arcade.camera.Camera2D()
        self.hitboxes = False
        self.health_text = arcade.Text(
            f"{self.health}/{self.max_health}",
            560,
            77,
            arcade.color.WHITE,
            30,
            anchor_y="center",
        )
        self.coordinates_text = arcade.Text(
            "",
            24,
            self.height - 24,
            arcade.color.WHITE,
            18,
            anchor_y="top",
        )

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        self.ground_list = arcade.SpriteList()
        for y in range(MAP_BOTTOM, MAP_TOP, 64):
            for x in range(MAP_LEFT, MAP_RIGHT, 64):
                wall = arcade.Sprite(random.choice(GRASS_TEXTURES), scale=1)
                wall.center_y = y
                wall.center_x = x
                wall.hit_box = arcade.hitbox.HitBox(points=[(0, 0)], position=wall.position)
                self.ground_list.append(wall)



        self.wall_list = arcade.SpriteList(use_spatial_hash=True)        

        coordinate_list = [[0, 0]]
        for i in range(TREES):
            coordinate_list.append([random.choice(POSSIBLE_X), random.choice(POSSIBLE_Y)])
            

        for coordinate in coordinate_list:
            wall = arcade.Sprite(
                "tree2.png")
            wall.position =[coordinate[0]-32,coordinate[1]-32]
            wall.hit_box = arcade.hitbox.HitBox(points=[(0, 0), (64, 0), (64, -64), (0, -64)], position=wall.position)
            self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, walls=self.wall_list
        )

        self.mouse_list=arcade.SpriteList()
        self.mouse_sprite = arcade.Sprite("mouse_overlay.png")
        self.mouse_list.append(self.mouse_sprite)



    def setup(self):
        pass

    def change_health(self, amount):
        self.health = max(0, min(self.health + amount, self.max_health))
        self.health_text.text = f"{self.health}/{self.max_health}"
        

    def on_draw(self):
        self.clear()

        self.game_camera.use()

        # Use straight-alpha blending so each texture pixel's alpha is honored.
        alpha_blend = arcade.gl.BLEND_DEFAULT
        self.ground_list.draw(blend_function=alpha_blend)
        self.player_list.draw(blend_function=alpha_blend)
        self.wall_list.draw(blend_function=alpha_blend)
        self.mouse_list.draw(blend_function=alpha_blend)

        if self.hitboxes:
            self.player_list.draw_hit_boxes()
            self.wall_list.draw_hit_boxes()
            self.ground_list.draw_hit_boxes()
            self.mouse_list.draw_hit_boxes()

        



            
        self.gui_camera.match_window(position=True)
        self.gui_camera.use()
        health_bar_width = 240
        health_bar_height = 24
        health_bar_left = 24
        health_bar_bottom = 24
        health_ratio = max(0, min(self.health / self.max_health, 1))
        
        arcade.draw_lbwh_rectangle_filled(
            health_bar_left,
            health_bar_bottom,
            health_bar_width,
            health_bar_height,
            arcade.color.RED,
        )
        arcade.draw_lbwh_rectangle_filled(
            health_bar_left,
            health_bar_bottom,
            health_bar_width * health_ratio,
            health_bar_height,
            arcade.color.GREEN,
        )

        self.health_text.draw()

        inventory_slot_size = 56
        inventory_slot_gap = 8
        inventory_width = 5 * inventory_slot_size + 4 * inventory_slot_gap
        inventory_left = (self.width - inventory_width) / 2
        inventory_bottom = 24
        inventory_padding = 8
        arcade.draw_lbwh_rectangle_filled(
            inventory_left - inventory_padding,
            inventory_bottom - inventory_padding,
            inventory_width + 2 * inventory_padding,
            inventory_slot_size + 2 * inventory_padding,
            (24, 30, 42, 230),
        )

        for slot_index in range(5):
            slot_left = inventory_left + slot_index * (inventory_slot_size + inventory_slot_gap)
            slot_color = arcade.color.GOLD if slot_index == 0 else arcade.color.LIGHT_GRAY
            arcade.draw_lbwh_rectangle_filled(
                slot_left,
                inventory_bottom,
                inventory_slot_size,
                inventory_slot_size,
                slot_color,
            )
            arcade.draw_lbwh_rectangle_filled(
                slot_left + 3,
                inventory_bottom + 3,
                inventory_slot_size - 6,
                inventory_slot_size - 6,
                (42, 49, 64, 255),
            )
            arcade.draw_text(
                str(slot_index + 1),
                slot_left + 7,
                inventory_bottom + inventory_slot_size - 18,
                arcade.color.WHITE,
                12,
            )

        self.axe_sprite.center_x = inventory_left + inventory_slot_size / 2
        self.axe_sprite.center_y = inventory_bottom + inventory_slot_size / 2
        self.axe_sprite_list.draw()

        if self.show_coordinates:
            controlled_sprite = self.tp if self.only_camera else self.player_sprite
            self.coordinates_text.text = (
                f"Player: ({controlled_sprite.center_x:.0f}, "
                f"{controlled_sprite.center_y:.0f})  "
                f"Mouse: ({self.mouse_x:.0f}, {self.mouse_y:.0f})"
            )
            self.coordinates_text.y = self.height - 24
            self.coordinates_text.draw()




    def on_mouse_motion(self, x:int, y:int, dx:int, dy:int):
        world_x, world_y, _ = self.game_camera.unproject((x, y))
        self.mouse_x = world_x
        self.mouse_y = world_y
        self.mouse_sprite.center_x = round(world_x / 64) * 64
        self.mouse_sprite.center_y = round(world_y / 64) * 64


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.last_key="w"
            if self.only_camera:
                self.tp.change_y += self.PLAYER_MOVEMENT_SPEED
            else:
                self.player_sprite.change_y += self.PLAYER_MOVEMENT_SPEED

        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.last_key="s"
            if self.only_camera:
                self.tp.change_y += -self.PLAYER_MOVEMENT_SPEED
            else:
                self.player_sprite.change_y += -self.PLAYER_MOVEMENT_SPEED


        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.last_key="a"
            if self.only_camera:
                self.tp.change_x += -self.PLAYER_MOVEMENT_SPEED
            else:
                self.player_sprite.texture = self.player_texture_left_1
                self.player_sprite.change_x += -self.PLAYER_MOVEMENT_SPEED


        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.last_key="d"
            if self.only_camera:
                self.tp.change_x += self.PLAYER_MOVEMENT_SPEED
            else:
                self.player_sprite.texture = self.player_texture_right_1
                self.player_sprite.change_x += self.PLAYER_MOVEMENT_SPEED

        elif key == arcade.key.SPACE:
            if time.time() - self.dash_time > 5.0:
                if self.last_key=="w":
                    self.player_sprite.center_y += PLAYER_DASH_LENGTH

                elif self.last_key=="s":
                    self.player_sprite.center_y += -PLAYER_DASH_LENGTH

                elif self.last_key=="a":
                    self.player_sprite.center_x += -PLAYER_DASH_LENGTH

                elif self.last_key=="d":
                    self.player_sprite.center_x += PLAYER_DASH_LENGTH

                self.dash_time = time.time()

        elif key == arcade.key.ESCAPE:
            arcade.close_window()

        elif key == arcade.key.B:
            if not self.hitboxes:
                self.hitboxes = True
            elif self.hitboxes:
                self.hitboxes = False

        elif key == arcade.key.L:
            self.show_coordinates = not self.show_coordinates

        elif key == arcade.key.C:
            if self.tp_animation_frames:
                pass
            elif not self.only_camera:
                self.PLAYER_MOVEMENT_SPEED = 16
                self.only_camera=True
                self.player_sprite.texture = self.blank_texture
                self.tp_animation_frames = [self.tp3, self.tp2, self.tp1, self.tp_texture]
                self.tp_animation_index = 0
                self.tp_animation_elapsed = 0.0
                self.tp.texture = self.tp_animation_frames[0]
            else:
                self.only_camera=False
                self.PLAYER_MOVEMENT_SPEED = 8
                self.player_sprite.position=self.tp.position
                self.player_sprite.texture = self.blank_texture
                self.tp_animation_frames = [self.tp1, self.tp2, self.tp3]
                self.tp_animation_index = 0
                self.tp_animation_elapsed = 0.0
                self.tp.texture = self.tp_animation_frames[0]
                self.tp.texture=self.blank_texture

        elif key == arcade.key.Q:
            self.change_health(-5)

        elif key == arcade.key.E:
            self.change_health(5)

        elif key == arcade.key.R:
            self.player_sprite.center_x = round(self.player_sprite.center_x/64)*64
            self.player_sprite.center_y = round(self.player_sprite.center_y/64)*64

        

            

    def on_key_release(self, key, modifiers):
        controlled_sprite = self.tp if self.only_camera else self.player_sprite
        if key == arcade.key.UP or key == arcade.key.W:
            controlled_sprite.change_y = 0
            controlled_sprite.center_y = math.ceil(controlled_sprite.center_y/16)*16
        elif key == arcade.key.DOWN or key == arcade.key.S:
            controlled_sprite.change_y = 0
            controlled_sprite.center_y = math.floor(controlled_sprite.center_y/16)*16
        elif key == arcade.key.LEFT or key == arcade.key.A:
            controlled_sprite.change_x = 0
            controlled_sprite.center_x = math.floor(controlled_sprite.center_x/16)*16
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            controlled_sprite.change_x = 0
            controlled_sprite.center_x = math.ceil(controlled_sprite.center_x/16)*16

    def on_update(self, delta_time):
        self.physics_engine.update()

        if self.tp_animation_frames:
            self.tp_animation_elapsed += delta_time
            while self.tp_animation_elapsed >= 0.1:
                self.tp_animation_elapsed -= 0.1
                self.tp_animation_index += 1
                if self.tp_animation_index >= len(self.tp_animation_frames):
                    self.tp_animation_frames = []
                    if not self.only_camera:
                        self.player_sprite.texture = self.player_texture_left_1
                        self.tp.texture=self.blank_texture
                    break
                self.tp.texture = self.tp_animation_frames[self.tp_animation_index]

        if self.only_camera:
            self.tp.update(delta_time)
            self.game_camera.position = self.tp.position
        else:
            self.tp.position = self.player_sprite.position
            self.game_camera.position = arcade.math.lerp_2d(
                self.game_camera.position,
                self.player_sprite.position,
                0.1
            )



        if time.time() - self.last_change >= 1.3:
            if self.only_camera:
                pass            
            else:
                if self.player_sprite.texture == self.player_texture_left_1:
                    self.player_sprite.texture = self.player_texture_left_2
                elif self.player_sprite.texture == self.player_texture_left_2:
                    self.player_sprite.texture = self.player_texture_left_1
                elif self.player_sprite.texture == self.player_texture_right_1:
                    self.player_sprite.texture = self.player_texture_right_2
                elif self.player_sprite.texture == self.player_texture_right_2:
                    self.player_sprite.texture = self.player_texture_right_1

            self.last_change = time.time()

def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()