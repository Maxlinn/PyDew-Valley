import pygame
from player import Player
from settings import *

class Level(object):
	def __init__(self):
		# pygame里可以创建虚拟的面，就是一个二维面，用来贴材质或其他
		# 使用`pygame.Surface()`即可
		# 这里直接画在显示的面上（单例）
		self.display_surface = pygame.display.get_surface()

		# sprite groups 用来管理 sprites，必须使用
		self.all_sprites = pygame.sprite.Group()

		# 自定义的初始化方法
		self.setup()

	def setup(self):
		# 将sprite加到group的方法是，在实例化时向Sprite类传入group
		self.player = Player(pos=(0,0), group=self.all_sprites)


	def run(self, dt:float):
		# 将显示面设置为黑色
		self.display_surface.fill('black')
		# 将sprite画在surface上
		self.all_sprites.draw(self.display_surface)
		# 注意，`Group`的update会调用其所有`children`的update
		# 并且参数和你调用的一样
		self.all_sprites.update(dt)