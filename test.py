import pygame
from decimal import *

surf1 = pygame.surface.Surface((200,300))
surf2 = pygame.surface.Surface((200,300))
test_list1 = (surf1, (20,30))
test_list2 = (surf1, (20,30))
print(repr(test_list1))
print(repr(test_list2))
print(repr(test_list1)==repr(test_list2))
for i in range(3):
    print("Hash1: ",hash(test_list1))
    print("Hash2: ",hash(test_list2))
    print("Hash comparison: ",hash(test_list1)==hash(test_list2))
