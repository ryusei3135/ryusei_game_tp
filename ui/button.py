

import pygame as pg
from ui.fonts import FontManager


class ButtonData:
    def __init__(self):
        self.fontSize: int = 0
        self.Size: list[int, int] = [50, 50]
        self.Pos: list[int, int] = [0, 0]
        self.text: str = "TEXT"
        self.textColor: list[int, int, int] = [0, 0, 0]
        self.buttonColor: list[int, int, int] = [255, 255, 255]
        self.pressKey: int = 0


class Button:
    def __init__(self, btnData: ButtonData) -> None:
        self.bd = btnData
        self.__font = FontManager()[self.bd.fontSize]
        self.__putText()
        self.__makeBase()

    def __makeBase(self) -> None:
        self.__base = pg.Rect(self.bd.Pos[:2], self.bd.Size[:2])
        self.__textRect = self.__textSurface.get_rect()
        self.__textRect.center = self.__base.center

    def __putText(self) -> None:
        self.__textSurface = self.__font.render(self.bd.text, True, self.bd.textColor)
    
    def event(self, mousePos: list[int, int], mousePress: list[bool, bool, bool]) -> bool:
        if self.__textRect.collidepoint(mousePos[:2]) and mousePress[self.bd.pressKey]:
            return True
        return False

    def draw(self, screen: pg.surface.Surface) -> None:
        pg.draw.rect(screen, self.bd.buttonColor, self.__base)
        screen.blit(self.__textSurface, self.__textRect)