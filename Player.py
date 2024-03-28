import pygame, os, pickle
from Weapon import *

class Player:
    def __init__(self, display_window = None):
        self.max_health = 100
        self.current_health = 0
        self.score = 0
        self.display_window = display_window
        self.weapon = Weapon(self.display_window)
        self.data = self.load_player_data()
        print(self.display_window)

    def load_player_data(self):
        try:
            if not os.path.exists('savegames'):
                os.makedirs('savegames')
                with open("savegames/save1.sav", "wb") as player_data:
                    pickle.dump(self, player_data)
                    
            else:
                with open("savegames/save1.sav", "rb") as player_data:
                    self.data = pickle.load(player_data)
            
        except FileNotFoundError as fnf_error:
            print("First load failed...trying to create save file...")
            with open("savegames/save1.sav", "wb") as player_data:
                pickle.dump(self, player_data)
                print("Creating save file success!")
            
        except Exception as e:
            print(e)
            print("Loading Game Data Failed for", self.__class__.__name__)
        
    def get_screen_pos(self, spawn_bounds=None):
        sprite_size = self.anim["idle"].getFrame(0).get_size()
        if spawn_bounds == None:
            screen_size = self.display_window.get_size()
            x = (screen_size[0] - sprite_size[0])/2
            y = screen_size[1] - sprite_size[1]
        else:
            if spawn_bounds[0] > sprite_size[0] and spawn_bounds[1] > sprite_size[1]:
                x = (spawn_bounds[0] - sprite_size[0])/2
                y = spawn_bounds[1] - sprite_size[1]
            else:
                return (0,0)
        return (x, y)

    def render_player_details(self, size_to_scale_to=0, surface_to_render_to=None, anim_type="idle"):
        #Render Health
        #Render Score
        #Render Weapon Type and Bullets
        #Render other Misc Data
        pass

    def render_player_weapon(self, size_to_scale_to=0, surface_to_render_to=None, anim_type="idle"):
        #wrapper method to call the current weapon's render method...Automatically fetches blit position on screen
        self.weapon.render_sprite(size_to_scale_to, surface_to_render_to, anim_type)
pygame.init()
clock=pygame.time.Clock()
test_win = pygame.display.set_mode((1000, 600))
player = Player(test_win)
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            isRunning=False
            break        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            break        
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.render_player_weapon((108,127),None,"fire")
            print("Mouse Click")
        pygame.display.update()
        clock.tick(200)
