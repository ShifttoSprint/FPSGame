import pyganim, pygame, Enemy
from collections import OrderedDict

class Renderer:
    def __init__(self):
        self.render_queue = OrderedDict()
        self.dequeue_list = set()

    #Method to queue objects for rendering in order.
    #Accepts the object to be rendered,
    #type of animation of the object(optional if surface or pyganimation passed),
    #and the surface for sprite to be rendered on.
    #If SURFACE or PYGANIMATION is passed as object, to be
    #passed in a tuple, in the following format:
    #(surface or pyganimation reference, position on screen to render on) --> will be first parameter, rest remains same.
    #---------------------------------------------------------------------------------------------------------------------
    #If a class instance is passed, ensure the class
    #has a self.anim type variable that is a dict with the
    #required animation types. If only single animation is
    #required, keep a single item with the key as 'default'.
    #Also, ensure that the object has a self.pos variable
    #for tracking coordinates to be rendered at.
    def enqueue_object(self, object_to_blit, screen_to_blit_on, anim_type="default"):
        if hash(object_to_blit) not in self.render_queue:
            self.render_queue[hash(object_to_blit)] = [object_to_blit, anim_type, screen_to_blit_on]

    #Internal method to dequeue items after rendering. Not advised to call independently.
    def dequeue_objects(self):
        for i in self.dequeue_list:
            if i in self.render_queue:
                del self.render_queue[i]
                print("deleting object ", i)
                
            self.dequeue_list = set()

    #Method to actually call render methods of all queued items.
    def render(self):
        for hcode, render_details in self.render_queue.items():
            if type(render_details[0]).__name__ == "tuple":
                if type(render_details[0][0]).__name__ == "Surface":
                    render_details[2].blit(render_details[0][0], render_details[0][1])
                    self.dequeue_list.add(hcode)
                    
                elif type(render_details[0][0]).__name__ == "PygAnimation":
                    render_details[0][0].blit(render_details[2], render_details[0][1])
                    if render_details[0][0]._state == pyganim.STOPPED:
                        self.dequeue_list.add(hcode)
                    
            else:
                render_details[0].anim[render_details[1]].blit(render_details[2], render_details[0].pos)
                if render_details[0].anim[render_details[1]]._state == pyganim.STOPPED:
                    self.dequeue_list.add(hcode)                
            
    
test = Renderer()
surf1 = pygame.surface.Surface((10,10))
surf1.fill((255,255,255))
surf_test = pygame.surface.Surface((600,200))
surf2 = pyganim.PygAnimation([("weapons/frame_1.gif",100),("weapons/frame_2.gif",100),("weapons/frame_3.gif",100),("weapons/frame_4.gif",100),("weapons/frame_5.gif",100)],loop=False)
surf3 = Enemy.Enemy()
test.enqueue_object(surf3, surf_test, "walking")
test.enqueue_object((surf2, (10,40)), surf_test, "fire")
test.enqueue_object((surf1, (100,100)), surf_test)
clock = pygame.time.Clock()
win = pygame.display.set_mode((600,400))
print("Render Queue: ", test.render_queue)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    win.fill((255, 0, 0))
    surf_test.fill((0,0,0))
    surf2.anchor(pyganim.SOUTH)
    if surf2._state == pyganim.STOPPED:
        surf2.play()
    test.enqueue_object(surf3, surf_test, "walking")
    test.enqueue_object((surf2, (10,40)), surf_test, "fire")
    test.enqueue_object((surf1, (100,100)), surf_test)
    test.enqueue_object((surf2, (10,40)), surf_test, "fire")
    test.render()
    win.blit(surf_test, (0,0))
    test.dequeue_objects()
    pygame.display.update()

