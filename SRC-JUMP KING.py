import arcade



SCREEN_BREDDE = 800
SCREEN_HOEJDE = 600
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
KARAKTER_SKALERING = 1

# Movement speed of player, in pixels per frame
KARAKTER_HASTIGHED = 5

TYNGDEKRAFT = 1

KARAKTER_HOPPEHASTIGHED = 20


class Ret_Linje:
    def __init__(self, fast_punkt, retningsvektor, farve, sporlaengde=None):
        self.fast_punkt = fast_punkt
        self.retningsvektor = retningsvektor
        self.punkt = self.fast_punkt
        self.farve = farve
        self.sporlaengde = sporlaengde
        self.linjetex = arcade.load_texture("STEN PLATFORM.png")
        if self.sporlaengde:
            self.spor = list()
    def opdater(self, delta_tid):
        if self.sporlaengde:
            self.spor.append(self.punkt)
        if self.sporlaengde and len(self.spor) >= self.sporlaengde:
            self.spor.pop(0)
        x, y = self.punkt
        vx, vy = self.retningsvektor
        x += vx * delta_tid
        y += vy * delta_tid
        self.punkt = (x, y)
    def tegn(self):
        x, y = self.punkt
        arcade.draw_circle_filled(x, y, 5, self.farve)
        for punkt in self.spor:
            x, y = punkt
            arcade.draw_circle_filled(x, y, 2, self.farve)
            arcade.draw_texture_rectangle(x,y,50,50, self.linjetex)

class JumpKing(arcade.Window):

    def __init__(self):
        #kalde på forældreren
        super().__init__(SCREEN_BREDDE, SCREEN_HOEJDE, SCREEN_TITLE)
        #Vi nød til at sætte en scene i gang
        self.scene = None
        self.player_sprite = None
        #vores sprite / karakter
        #physics engine som skal bruges til colission og tyngdekraft
        self.physics_engine = None
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.background = arcade.load_texture("BACKGROUND STAR.jpg")


    def setup(self):
        # vi starter en scene
        self.scene = arcade.Scene()
        image_source = ":resources:images/animated_characters/zombie/zombie_idle.png"
        #karaktere som er oploaded fra https://api.arcade.academy/en/latest/resources.html
        self.player_sprite = arcade.Sprite(image_source, KARAKTER_SKALERING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)
        #vi laver vores karakter og indsætter
        #Vi laver jorden. Med en x værdi fra 0-1250 og intervallet
        for x in range(0, 1250, 64):
            wall = arcade.Sprite("BLOCK BILLED MC.png", 0.1)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        #Så vil jeg lave nogle platforme
        coordinate_list = \
            [[512, 220],
             [256, 220]]

        for coordinate in coordinate_list:
            # Laver platformene
            wall = arcade.Sprite(
                "STEN PLATFORM.png", 0.1
            )
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)


        # Create the 'physics engine'

        self.physics_engine = arcade.PhysicsEnginePlatformer(

            self.player_sprite, gravity_constant=TYNGDEKRAFT, walls=self.scene["Walls"]

        )
        #laver den rette linje
        self.ret_linje = Ret_Linje((0, SCREEN_HOEJDE / 2), (50, 0), arcade.csscolor.RED, 2)
    #karakter bevægelse
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = KARAKTER_HOPPEHASTIGHED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -KARAKTER_HASTIGHED
        elif key == arcade.key.D:
            self.player_sprite.change_x = KARAKTER_HASTIGHED
        # så karakteren ikke bliver ved med at bevæge sig i den retning

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
    def on_draw(self):
        #tegner skærmen og frigøre den
        self.clear()
        arcade.draw_texture_rectangle(SCREEN_BREDDE / 2, SCREEN_HOEJDE / 2, SCREEN_BREDDE, SCREEN_HOEJDE,
                                      self.background)
        self.scene.draw()
        self.ret_linje.tegn()

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.ret_linje.opdater(delta_time)
        #opdatere den

#main funktion hvor vi køre det hele
def main():
    window = JumpKing()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()