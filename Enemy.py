import pyganim, random, json
from pygame import Rect

class Enemy:
    spawned_positions_on_screen = []
    
    def __init__(self,enemy_type="enemy",spawn_bounds=None):
        self.enemy_type = enemy_type
        self.data = None
        self.load_json_data()
        self.anim = self.get_anim_data()
        self.pos = self.get_spawn_pos(spawn_bounds)
        self.spawned_positions_on_screen.append(self.pos)
        self.collider = None
        self.update_collider(0,0)
        
    def load_json_data(self):
        try:
            json_data = open("gamedat.json")
            game_data = json.load(json_data)
            self.data = game_data[self.enemy_type]
        except Exception as e:
            print(e)
            print("Loading Game Data Failed for", self.__class__.__name__)
    
    def get_anim_data(self):
        return pyganim.PygAnimation(self.data["frames"])

    def update_collider(self, surface_x, surface_y):
        sprite_size = self.anim.getFrame(1).get_size()
        self.collider = Rect(self.pos[0]- abs(surface_x), self.pos[1]- abs(surface_y), sprite_size[0], sprite_size[1])
        return self.collider
        
    def get_spawn_pos(self, spawn_bounds):
        if spawn_bounds == None:
            x = random.choice([320,398,502,636])
            y = 400
        else:
            x = random.randint(spawn_bounds[0][0], spawn_bounds[0][1])
            y = random.randint(spawn_bounds[1][0], spawn_bounds[1][1])
        if (x,y) in self.spawned_positions_on_screen:
            x,y = self.get_spawn_pos(spawn_bounds)
        return (x, y)


        
