import pygame

class Timer(object):
    '''自己实现的计时器'''

    def __init__(self, duration:float, callback=None):
        self._duration = duration
        self._callback = callback
        self._is_active = False
        self._start_ts = 0

    def activate(self):
        self._is_active = True
        self._start_ts = pygame.time.get_ticks()

    def deactivate(self):
        self._is_active = False
        self._start_ts = 0

    def update(self):
        '''update会被反复调用'''
        current_ts = pygame.time.get_ticks()
        # 时间未到
        if current_ts < self._start_ts + self._duration:
            return

        self.deactivate()
        if self._callback is not None:
            self._callback()

    @property
    def is_active(self):
        return self._is_active