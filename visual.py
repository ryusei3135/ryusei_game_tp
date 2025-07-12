from json import loads
from os import path as PATH

import pygame as pg


class BaseVisual:
    def __init__(self, visualName: str) -> None:
        self.__visualName = visualName

        if not PATH.isdir("img"):
            raise FileNotFoundError
        else:
            self.__loadImgPath()

    def __loadImgPath(self) -> None:
        with open("visual.json", "r") as file:
            self.__pathData = loads(file.read())[self.__visualName]

    def makeVisual(self, size: tuple[int, int]) -> None:
        makeImg = lambda path, size: pg.transform.scale(pg.image.load(path), size)
        self.__errImg: pg.surface.Surface = makeImg("img/err.png", size)
        
        self.__ImgData = {
            str(path): makeImg(
                f"img/{self.__pathData[str(path)]}", size) for path in self.__pathData
        }

    def __getitem__(self, index) -> pg.surface.Surface:
        try:
            if type(index) is str:
                return self.__ImgData[index]
            elif type(index) is int:
                count = 0
                for img in self.__ImgData:
                    if count < index:
                        return self.__ImgData[str(img)]
                    count += 1
                else:
                    raise ValueError
        except AttributeError:
            return self.__errImg