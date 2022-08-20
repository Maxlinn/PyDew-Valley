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

        # 画一个玩家（这里还没有贴材质），`Surface`有一些内置的绘制方法
        # x方向从左上角向右，y方向从左上角向下
        # ！注意：一个sprite一定要有`image`成员，否则pygame会崩溃
        self.image :pygame.Surface = pygame.Surface(size=(32, 64))
        self.image.fill('green')
        # 根据参考点（比如中心点）和surface
        #   计算图像的实际范围`Rect`对象，左上和右下
        #   因为这里的rect是从image构造出来的，所以先把image方是上面
        # ！注意：一个sprite一定要有`rect`成员，否则pygame会崩溃
        self.rect = self.image.get_rect(center=pos)

        # `pygame.math.Vector2()` 两个数的向量，成员有`x, y`
        #   常用来表示坐标
        #   这里用1表示朝右/朝下（顺着屏幕空间方向）
        #   用-1表示朝左/朝上
        #   方便可能的坐标计算
        self._direction = pygame.math.Vector2()

        # 由于`self.rect`的成员都是int
        #   而我们希望对象能按照帧时间（过去1145ms就应该用这个时间乘以速度
        #   所以这里也用Vector2
        self._pos = pygame.math.Vector2(self.rect.center)

        self._speed = 200 # pixels per second

    def input(self):
        '''管理用户的输入'''
        keys = pygame.key.get_pressed()

        # 同时可以能多个键被按下
        #   注意`input`在每个`update`都会被调用
        #   所以在没有按下时，应当记录没有朝向（否则一直使用刚刚的朝向）
        if keys[pygame.K_UP]:
            self._direction.y = -1
        elif keys[pygame.K_DOWN]:
            self._direction.y = 1
        else:
            self._direction.y = 0

        if keys[pygame.K_LEFT]:
            self._direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self._direction.x = 1
        else:
            self._direction.x = 0

    def move(self, dt:float):

        ## @Problem 这样的处理会让斜着的移动变快，因为横竖的速度都是`_speed`
        # 向量运算，同时算x和y
        #   方向乘以速度乘以时间等于距离
        # self._pos += self._direction * self._speed * dt

        ## @Solution 所以在计算位置前，先把横纵方向归一化
        #   使得斜向移动时速度平方和为1
        # 注意，当为全零向量时，无法normalize
        #   所以先判定是否为全零向量，判定方法是向量长度
        if self._direction.magnitude():
            self._direction = self._direction.normalize()

        # 拆分为横向和竖向的移动，用来处理碰撞
        self._pos.x += self._direction.x * self._speed * dt
        self.rect.centerx = self._pos.x

        self._pos.y += self._direction.y * self._speed * dt
        self.rect.centery = self._pos.y


    def update(self, dt:float) -> None:
        '''update是重写的Sprite的方法，当group被update时，所有children都会update'''
        self.input() # 输入检测
        self.move(dt) # 移动检测
