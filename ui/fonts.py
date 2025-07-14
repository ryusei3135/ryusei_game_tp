import pygame as pg


class FontManager:
    def __init__(self):
        fontSize = [10, 20, 30]
        self.__fonts = tuple(pg.font.Font("ui/mainFont.ttf", size) for size in fontSize)

    def __getitem__(self, index: int) -> pg.font.Font:
        try:
            if type(index) is int:
                return self.__fonts[index]
            else:
                raise IndexError
        except IndexError:
            return self.__fonts[0]