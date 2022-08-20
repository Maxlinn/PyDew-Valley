import pygame
from player import Player
from overlay import Overlay
from settings import *
from sprites import *
# 地图是用开源工具Tiled制作的，这里使用预制的图
from pytmx.util_pygame import load_pygame

class Level(object):
	def __init__(self):
		# pygame里可以创建虚拟的面，就是一个二维面，用来贴材质或其他
		# 使用`pygame.Surface()`即可
		# 这里直接画在显示的面上（单例）
		self.display_surface = pygame.display.get_surface()
		self.all_sprites = CameraGroup()

		tmx_data = load_pygame('../data/map.tmx')
		# 在tiles中，设计单位是格子
		# 	在pygame中，设计的单位是像素，两者通过`TILE_SIZE`转换
		# `HouseFurnitureBottom`是在tiles中给定的类名字
		for x, y, surface in tmx_data.get_layer_by_name(
				'HouseFurnitureBottom').tiles():
			GenericSprite(pos=(x*TILE_SIZE, y*TILE_SIZE),
						  surface=surface,
						  groups=self.all_sprites,
						  z=LAYERS['house bottom'])




		# sprite groups 用来管理 sprites
		self.player = Player(pos=(640, 480), group=self.all_sprites)

		# 将sprite加到group的方法是，在实例化时向Sprite类传入group
		# ！注意：创建`sprite`的顺序和更新`sprite`的顺序是一样的，注意顺序
		# 	为了避免这个问题，为`CameraGroup`引入了`LAYERS`的概念
		self.ground = GenericSprite(
			pos=(0,0), groups=self.all_sprites, z=LAYERS['ground'],
			surface=pygame.image.load('../graphics/world/ground.png').convert_alpha()
		)
		self.overlay = Overlay(player=self.player)

	def run(self, dt:float):
		# 将背景设置为黑色
		self.display_surface.fill('black')
		# 被摄像机拍到的先画
		self.all_sprites.draw_camera(self.player)
		# 其他无论如何都会显示的后画
		self.overlay.draw()

		# 提醒所有`sprite`更新
		# 	注意，`Group`的update会调用其所有`children`的update
		# 	并且参数和你调用的一样
		self.all_sprites.update(dt)


class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self._display_surface = pygame.display.get_surface()
		# 根据玩家的逻辑位置，动态计算各`sprite`绘制的`rect`
		self._offset = pygame.math.Vector2()

	def draw_camera(self, player):
		self._offset.x = player.rect.centerx - SCREEN_WIDTH / 2
		self._offset.y = player.rect.centery - SCREEN_HEIGHT / 2

		for layer in LAYERS.values():
			for sprite in self.sprites():
				if sprite.z == layer:
					rect_t = sprite.rect.copy()
					rect_t.center -= self._offset
					self._display_surface.blit(sprite.image, rect_t)



