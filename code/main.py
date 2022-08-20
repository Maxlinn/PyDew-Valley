import pygame, sys
from settings import *
from level import Level


class Game:
    def __init__(self):
        # 全局只需要执行一次pygame.init()
        pygame.init()

        # 屏幕，时钟，关卡控制器
        self.screen = pygame.display.set_mode(
            size=(SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.level = Level()

        # 设置窗口名
        pygame.display.set_caption('PyDew Valley')

    def run(self):
        # 主循环
        while True:
            # 如果接收到pygame.QUIT事件就退出，否则执行时间步
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # 主循环没有规定时间片大小，只要有机会就会循环一次
            #  `tick(fps)`可以指定framerate才返回一次（不然会阻塞在tick）

            # `self.clock.tick()`返回距离上一次调用过去了多少**毫秒**(int)
            # 	这里计算过去的秒数
            dt: float = self.clock.tick() / 1000
            # 控制器感知过去的秒数
            self.level.run(dt)
            # pygame更新画面
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
