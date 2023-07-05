import time
import pygame

def lerp(a, b, t):
    return (1-t)*a + b*t

def draw_text(screen, text, font, col, x, y):
    img = font.render(text, True, col)
    screen.blit(img, (x,y))

class Alarm():

    def __init__(self):
        self.current_time = time.time()
        self.time = 0.001

    def get(self):
        return 1 - (time.time() - self.current_time)/self.time
    
    def is_done(self):
        return self.get() <= 0
    
    def set(self, time_):
        self.time = time_
        self.current_time = time.time()