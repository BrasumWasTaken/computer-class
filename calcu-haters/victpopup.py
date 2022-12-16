import pygame
class VictPopup:
    def __init__(self,Surf1,Surf2):
        self.surf1=Surf1
        self.surf2=Surf2
        self.active=True
    def flip(self):
        self.active=not(self.active)
    def draw(self):
        if self.active:
            return self.surf1
        return self.surf2
