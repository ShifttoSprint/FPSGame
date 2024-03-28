import pyganim, random, json
from pygame import Rect

class Enemy:
    spawned_positions_on_screen = []
    
    def __init__(self,enemy_type="default",spawn_bounds=None,spawn_size=[50,80]):
        self.enemy_type = enemy_type
        self.data = None
        self.load_json_data()
        self.anim = self.get_anim_data()
        for title,anim in self.anim.items():
            anim.scale(spawn_size)
        self.pos = self.get_spawn_pos(spawn_bounds)
        self.spawned_positions_on_screen.append(self.pos)
        self.collider = None
        self.size = spawn_size
        self.update_collider([0,0])
        
    def load_json_data(self):
        """Loads all data required for a particular enemy type"""
        try:
            with open("gamedat.json") as json_data:
                game_data = json.load(json_data)
                self.data = game_data["enemies"][self.enemy_type]
        except Exception as e:
            print(e)
            print("Loading Game Data Failed for", self.__class__.__name__)
    
    def get_anim_data(self):
        """This functions gets all the animations for a particular enemy sprite from the game data files"""
        anim_dict = {}
        for anim_type, anim_frames in self.data["frames"].items():
            anim_dict[anim_type] = pyganim.PygAnimation(anim_frames, loop=False)
        return anim_dict

    def update_collider(self, surface_blit_pos, anim_type="walking"):
        """Updates the collider based on scaling and position"""
        sprite_size = self.size
        self.collider = Rect(self.pos[0]- abs(surface_blit_pos[0]), self.pos[1]- abs(surface_blit_pos[1]), sprite_size[0], sprite_size[1])
        return self.collider

    #def get_spawn_pos(self, spawn_bounds):
    #    return (398, 502)
    def get_spawn_pos(self, spawn_bounds):
        """Gets the spawn position of the sprite w.r.t certain spawn bounds or by default returns one of four choices"""
        if spawn_bounds == None:
            x = random.choice([320,398,502,636])
            y = 400
        else:
            x = random.randint(spawn_bounds[0][0], spawn_bounds[0][1])
            y = random.randint(spawn_bounds[1][0], spawn_bounds[1][1])
        if (x,y) in self.spawned_positions_on_screen:
            x,y = self.get_spawn_pos(spawn_bounds)
        return (x, y)

    def render_sprite(self, size_to_scale_to, blit_coords_of_surface, surface_to_render_to, anim_type="walking"):
        """Preps the sprite and animation to be rendered on to screen"""
        render_anim = self.anim[anim_type]
        if render_anim._state == pyganim.STOPPED:
            render_anim.play()
        if size_to_scale_to!=self.size:
            render_anim.clearTransforms()
            render_anim.scale(size_to_scale_to)
            self.size = size_to_scale_to.copy()
            
        self.update_collider(blit_coords_of_surface)
        render_anim.blit(surface_to_render_to, self.pos)
