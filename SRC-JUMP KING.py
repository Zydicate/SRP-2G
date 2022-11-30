import arcade
import math

BREDDE = 800
HOEJDE = 600
TITEL = "Jump King 2.0"

#Skaler karakter billederne til spillet
KARAKTER_SKALERING = 1
JORD_SKALERING = 0.2
#Karakter hastighed
PLAYER_MOVEMENT_SPEED = 5


#3. Platformen
class Platform:
    def __init__(self, center_x, center_y, width, height, farve):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.farve = farve

    #
    def tegn(self):
        arcade.draw_rectangle_filled(BREDDE/2, HOEJDE/10-50,BREDDE,100, arcade.csscolor.DIM_GREY)

#2. Starter vores vindue
class Vindue(arcade.Window):
    def __init__(self, width, height, title):
        #Returner et objekt som symbolisere / repræsentere forældreren
        super().__init__(BREDDE,HOEJDE,TITEL)


        self.wall_list = None
        self.player_list = None

        #Vi brug
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.scene.get_sprite_list("Walls")
        )

        arcade.set_background_color(arcade.csscolor.BLACK)

        #Loader baggrunden
        self.background = arcade.load_texture("BACKGROUND STAR.jpg")



    #brugt når jeg skal tegne mit vindue
    def on_draw(self):
        #begynd at tegne
        arcade.start_render()
        arcade.draw_texture_rectangle(BREDDE / 2, HOEJDE / 2, BREDDE, HOEJDE, self.background)
        self.platform.tegn()
        #laver textur til platform. JPG bliver distorted hvis bredden er for stor så vi duplikere den 6 gange.

        #

        self.wall_list.draw()
        self.player_list.draw()

        #

    def setup(self):
        self.platform = Platform(BREDDE, HOEJDE/2,50,100, arcade.csscolor.BROWN)
        #Lave en liste med sprites
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        #Sætter en spiller ind. Billedet er taget fra https://api.arcade.academy/en/latest/resources.html
        image_source = ":resources:images/animated_characters/zombie/zombie_idle.png"
        self.player_sprite = arcade.Sprite(image_source, KARAKTER_SKALERING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 124
        self.player_list.append(self.player_sprite)

        #Indsætte jorden i en range
        for x in range(0, BREDDE+200, 150):
            wall = arcade.Sprite("BLOCK BILLED MC.png", JORD_SKALERING)
            wall.center_x = x
            wall.center_y = -12
            self.wall_list.append(wall)




#1.Først sætter jeg et main op som jeg kan bruge til at køre hele mit program. Dette starter selvfølgelig med at sætte et arcade window op
def main():
    vindue = Vindue(BREDDE, HOEJDE, TITEL)
    vindue.setup()


    arcade.run()
main()