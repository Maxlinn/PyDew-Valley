from typing import Any

import pygame
from settings import *
from utils import *
from constants import *

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, group):
        '''

        :param pos: 玩家当前的位置
        :param group: 玩家sprite所属的group
        '''
        super().__init__(group)

        # 需要先载入材质，因为等下设置`self.image`会用到
        self.import_assets()
        # 玩家的状态，所有的状态见`self.import_assets`
        #   默认使用`down_idle`，游戏中的状态需要通过游戏逻辑来判断
        self._status = 'down_idle'
        # 动画正在使用的图片下标
        self._frame_idx = 0

        # 画一个玩家（这里还没有贴材质），`Surface`有一些内置的绘制方法
        # x方向从左上角向右，y方向从左上角向下
        # ！注意：一个sprite一定要有`image`成员，否则pygame会崩溃
        self.image :pygame.Surface = self._animations[self._status][self._frame_idx]

        # 根据参考点（比如中心点）和surface
        #   计算图像的实际范围`Rect`对象，左上和右下
        #   因为这里的rect是从image构造出来的，所以先把image方是上面
        # ！注意：一个sprite一定要有`rect`成员，否则pygame会崩溃
        self.rect = self.image.get_rect(center=pos)
        # 绘制高度
        self.z = LAYERS['main']

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

        # 工具
        self.selected_tool = 'axe'
        self.selected_seed = 'corn'


        # 保存使用过的计时器
        self._timers = {
            # 使用工具的时间
            'tool_use': Timer(duration=350, callback=self.callback_use_tool),
            # 切换工具时，由于用户的一次按键会检测多次press，需要用延时来检测单次触发
            'tool_switch': Timer(duration=200)
        }

    def input(self):
        '''管理用户的输入'''
        keys = pygame.key.get_pressed()

        # 同时可以能多个键被按下
        #   注意`input`在每个`update`都会被调用
        #   所以在没有按下时，应当记录没有朝向（否则一直使用刚刚的朝向）
        def detect_vertical_move():
            if keys[pygame.K_UP]:
                self._direction.y = -1
                self._status = 'up'
            elif keys[pygame.K_DOWN]:
                self._direction.y = 1
                self._status = 'down'
            else:
                self._direction.y = 0

        def detect_horizontal_move():
            if keys[pygame.K_LEFT]:
                self._direction.x = -1
                self._status = 'left'
            elif keys[pygame.K_RIGHT]:
                self._direction.x = 1
                self._status = 'right'
            else:
                self._direction.x = 0

        def detect_tool_use():
            '''如果玩家按了空格，那么开始使用工具'''
            if keys[pygame.K_SPACE]:
                self._timers['tool_use'].activate()
                # 将direction设置为0，检测到使用工具就禁止玩家移动
                self._direction = pygame.math.Vector2()
                # 工具动画从0开始播放
                self._frame_idx = 0

        # 当正在使用工具时，禁止玩家移动
        if not self._timers['tool_use'].is_active:
            detect_vertical_move()
            detect_horizontal_move()

        detect_tool_use()

    def import_assets(self):
        # 在`graphics/character`下面所有的角色动画
        # `self_animations`是从动作名（如`up_axe`）到其动画`Surface`列表的映射
        self._animations = {k: list() for k in PLAYER_STATUS_LIST}

        # 将整个文件夹的图片都导入为Surface对象
        for animation in self._animations.keys():
            # code和graphics是同级别的文件夹
            self._animations[animation] = import_folder(f'../graphics/character/{animation}')

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

    def animate(self, dt:float):
        # 现在由于主循环里的fps没有确定，所以进来的dt长度也不一样
        # 等到给定fps（比如60）时，可以预测每个dt的大小就是float(60/1000)
        self._frame_idx = (self._frame_idx + 1) % (len(self._animations[self._status]))
        self.image = self._animations[self._status][self._frame_idx]

    def callback_use_tool(self):
        pass

    def detect_status(self):
        def detect_idle():
            '''如果玩家没有移动，那么将状态后面加上`_idle`来调用空闲时的动画'''
            if self._direction.magnitude() == 0:
                # 多次idle时，只加一个`_idle`后缀
                self._status = self._status.split('_')[0] + '_idle'

        def detect_tool_use():
            if self._timers['tool_use'].is_active:
                self._status = self._status.split('_')[0] + '_' + self.selected_tool

        detect_idle()
        detect_tool_use()

    def update_timers(self):
        for timer in self._timers.values():
            timer.update()

    def update(self, dt:float) -> None:
        '''update是重写的Sprite的方法，当group被update时，所有children都会update'''
        self.input() # 输入检测
        self.move(dt) # 移动检测
        self.detect_status() # 状态精细检测
        self.animate(dt) # 动画切换

        self.update_timers() # 更新所有时钟，不依赖dt，放哪儿都可以
