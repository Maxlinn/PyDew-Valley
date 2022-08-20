import pygame
from settings import *

class GenericSprite(pygame.sprite.Sprite):
    def __init__(self,
                 pos,
                 surface :pygame.Surface,
                 groups,
                 z=LAYERS['main']):
        super().__init__(groups)
        # 要与`pygame`的`sprite`兼容，这里命名不要改
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z