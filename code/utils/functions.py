import os
import pygame

def import_folder(path:str):
    '''从当前层文件夹下导入所有文件，并生成`pygame.Surface`'''
    surface_ls = []

    for fname in os.listdir(path):
        # 动画的图片的文件名都按0.png, 1.png等存储了，所以进来就是顺序的
        filename = os.path.join(path, fname)
        # `.convert_alpha`会让`Surface`计算的更快
        surface = pygame.image.load(filename).convert_alpha()
        surface_ls.append(surface)

    return surface_ls