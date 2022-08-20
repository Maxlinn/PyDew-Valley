from typing import Any

import pygame
from settings import *

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, group):
        '''

        :param pos: 玩家当前的位置
        :param group: 玩家sprite所属的group
        '''
        super().__init__(group)

        # 画一个玩家（这里还没有贴材质）
        self.image = pygame.Surface(size=(64, 32))
        # Surface有一些内置的绘制方法
        self.image.fill('green')
        # ?
        self.rect = self.image.get_rect(center=pos)

    def input(self):
        '''管理用户的输入'''
        keys = pygame.key.get_pressed()

        # 同时可以能多个键被按下
        if keys[pygame.K_UP]:
            print('up is pressed')
        elif keys[pygame.K_DOWN]:
            print('down is pressed')


    def update(self, dt:float) -> None:
        '''update是重写的Sprite的方法，当group被update时，所有children都会update'''
        self.input() # 输入检测
