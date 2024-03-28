import pygame

pygame.init()

class Timer:
    def __init__(self):
        self.start=int(pygame.time.get_ticks())
        self.start_ms = pygame.time.get_ticks()
        self.seconds=0
        self.seconds_ms=0
    def timing(self):
        self.seconds=int((pygame.time.get_ticks()-self.start)/1000)
        return self.seconds
    def timing_with_precision(self):
        self.seconds_ms = pygame.time.get_ticks()-self.start_ms
        return self.seconds_ms
    def reset(self):
        self.start=int(pygame.time.get_ticks())
        self.start_ms = pygame.time.get_ticks()
