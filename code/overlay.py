import pygame
import os
from settings import *
from constants import *

class Overlay(object):

    def __init__(self, player):
        # 绘制图层和玩家
        self._display_surface = pygame.display.get_surface()
        self._player = player

        # 导入`tools`和`seeds`的`Surface`对象
        load_overlay_image = lambda fname: pygame.image.load(
            os.path.join('../graphics/overlay', fname)
        ).convert_alpha()

        self._tools_surfaces = {
            tool: load_overlay_image(f'{tool}.png')
            for tool in TOOLS
        }

        self._seeds_surfaces = {
            seed: load_overlay_image(f'{seed}.png')
            for seed in SEEDS
        }

    def draw(self):
        def draw_tool():
            tool_surface :pygame.Surface = self._tools_surfaces[self._player.selected_tool]
            tool_rect = tool_surface.get_rect(midbottom=OVERLAY_POSITIONS['tool'])
            self._display_surface.blit(tool_surface, tool_rect)

        def draw_seed():
            seed_surface :pygame.Surface = self._seeds_surfaces[self._player.selected_seed]
            seed_rect = seed_surface.get_rect(midbottom=OVERLAY_POSITIONS['seed'])
            self._display_surface.blit(seed_surface, seed_rect)

        draw_tool()
        draw_seed()
