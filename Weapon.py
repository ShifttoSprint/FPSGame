import pyganim, json
from pygame import Rect, draw

class Weapon:
    def __init__(self, screen_to_be_blit_on, weapon_type="default", crosshair_color = (255,255,255), spawn_bounds=None):
        self.weapon_type = weapon_type
        self.data = None
        self.load_json_data()
        self.anim = {"idle":self.get_anim_data("idle"), "fire":self.get_anim_data("fire")}
        self.display_window = screen_to_be_blit_on
        self.pos = self.get_screen_pos(spawn_bounds)
        self.collider = self.get_collider()
        self.crosshair_color = crosshair_color

    def load_json_data(self):
        try:
            with open("gamedat.json") as json_data:
                game_data = json.load(json_data)
                self.data = game_data["weapons"][self.weapon_type]
        except Exception as e:
            print(e)
            print("Loading Game Data Failed for", self.__class__.__name__)
    
    def get_anim_data(self, anim_to_fetch):
        return pyganim.PygAnimation(self.data["frames"][anim_to_fetch], loop=False)

    def get_collider(self, crosshair_width=5, anim_type="idle"):
        sprite_size = self.anim[anim_type].getFrame(1).get_size()
        self.collider = Rect(self.pos[0] + (sprite_size[0] - crosshair_width)/2, self.pos[1], crosshair_width, crosshair_width)
        return self.collider
        
    def get_screen_pos(self, spawn_bounds=None, anim_type="idle"):
        sprite_size = self.anim[anim_type].getFrame(1).get_size()
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

    def render_sprite(self, size_to_scale_to=0, surface_to_render_to=None, anim_type="idle", crosshair_width=5):
        if size_to_scale_to != 0:
            self.anim[anim_type].scale(size_to_scale_to)
        self.pos = self.get_screen_pos(None, anim_type)
        self.get_collider(crosshair_width, anim_type)
        if surface_to_render_to == None:
            self.anim[anim_type].play()
            self.anim[anim_type].blit(self.display_window, self.pos)
            draw.rect(self.display_window, self.crosshair_color, self.collider, 2)
        else:
            self.anim[anim_type].play()
            self.anim[anim_type].blit(surface_to_render_to, self.pos)
            draw.rect(surface_to_render_to, self.crosshair_color, self.collider, 2)


    
