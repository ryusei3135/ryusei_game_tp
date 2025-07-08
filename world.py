from PIL import Image
from json import load
from os import path as PATH

import pygame as pg

import status as stats
from visual import BaseVisual


class WorldData:
    def __init__(self, worldFixedData: stats.FixedData) -> None:
        self.WFD = worldFixedData #  <- worldFixedData
        self.fileName = ""
        self.__loadWorldMap()

    def choiseFile(self, fileName: str) -> None:
        self.fileName: str = fileName

        if PATH.isfile(self.fileName):
            return
        else:
            raise FileNotFoundError
    
    def __loadWorldMap(self) -> None:
        """ファイルがなかったらデータを作る"""
        try:
            with open(self.fileName, "r") as file:
                self.worldMap = load(file.read())

        except FileNotFoundError:
            self.worldMap = self.__makeWorldMap()

    def saveWorldMap(self) -> None:
        try:
            with open(self.fileName, "w") as file:
                file.write(str(self.worldMap))
        except FileNotFoundError:
            with open("world.txt", "w") as file:
                file.write(str(self.worldMap))

    def __makeWorldMap(self) -> None:
        data = []
        with Image.open(self.WFD["initpath"]["value"]) as img:
            worldSize: tuple[int, int] = self.WFD["worldsize"]["value"]
            for y in range(worldSize[1]):
                xr = []
                for x in range(worldSize[0]):
                    pixel_rgb = img.getpixel((x, y))
                    if len(pixel_rgb) == 4:
                        r, g, b, a = pixel_rgb
                    else:
                        r, g, b = pixel_rgb

                    if r == 255 and g == 255 and b == 255:
                        xr.append({"block": 1.5, "struct": {}})
                    elif r == 255 and g == 0 and b == 0:
                        xr.append({"block": 2.0, "struct": {}})
                    elif r == 0 and g == 255 and b == 0:
                        xr.append({"block": 1.0, "struct": {}})
                    elif r == 0 and g == 0 and b == 255:
                        xr.append({"block": 3.0, "struct": {}})
                    elif r == 0 and g == 0 and b == 0:
                        xr.append({"block": 0.0, "struct": {}})
                    else:
                        xr.append({"block": 0.0, "struct": {}})

                data.append(xr)
        return data
    

class WorldEvtFunc:
    @staticmethod
    def keyPress(datas: 
                tuple[
                    list[int, int],
                    list[int, int],
                    stats.RuningStatus]) -> None:
        pixelPos = datas[0]
        blockSize = datas[1]
        runingStats = datas[2]
        
        if pixelPos[0] >= blockSize[0]:
            runingStats.cameraPosMap[0] -= 1
            runingStats.cameraPixelPos[0] = 0
        if pixelPos[0] <= -blockSize[0]:
            runingStats.cameraPosMap[0] += 1
            runingStats.cameraPixelPos[0] = 0
        if pixelPos[1] >= blockSize[1]:
            runingStats.cameraPosMap[1] -= 1
            runingStats.cameraPixelPos[1] = 0
        if pixelPos[1] <= -blockSize[1]:
            runingStats.cameraPosMap[1] += 1
            runingStats.cameraPixelPos[1] = 0

    @staticmethod
    def mousePress(datas: tuple[
            stats.RuningStatus,
            WorldData]) -> None:

        WD = datas[1]
        runingStats = datas[0]
        mouseEvt = runingStats.mouseEvt

        if mouseEvt[2]:
            pos = mouseEvt[0:2]
            WD.worldMap[pos[1]][pos[0]]["block"] = 50
            WD.saveWorldMap()


class World:
    def __init__(self) -> None:
        self.worldFixedData = stats.FixedData()

        self.WD = WorldData(self.worldFixedData) #  <- worldData
        self.worldVisual = BaseVisual("world")

    def getRuningStatus(self, runingStatus: stats.RuningStatus) -> None:
        self.runingStats = runingStatus
        self.worldVisual.makeVisual(self.runingStats.blockSize)

    def getScreenData(self, ScreenData: stats.ScreenData) -> None:
        self.screenData = ScreenData

        self.ScreenMapSize: list[int, int] = self.screenData.ScreenMapSize

    def update(self) -> None:
        KeyDatas = [
            self.runingStats.cameraPixelPos,
            self.runingStats.blockSize,
            self.runingStats
        ]
        MouseDatas = [
            self.runingStats.mouseEvt,
            self.WD
        ]

        WorldEvtFunc.keyPress(KeyDatas)
        if all(self.runingStats.mouseEvt):
            WorldEvtFunc.mousePress(MouseDatas)

    def draw(self, screen: pg.surface.Surface) -> None:
        CameraPosMap = self.runingStats.cameraPosMap

        for ScreenY in range(CameraPosMap[1], self.ScreenMapSize[1] + CameraPosMap[1] + 1):
            for ScreenX in range(CameraPosMap[0], self.ScreenMapSize[0] + CameraPosMap[0] + 1):
                nowTile = self.WD.worldMap[ScreenY][ScreenX]["block"]
                tilePos: tuple[int, int] = (
                    (ScreenX - CameraPosMap[0]) * 50 + self.runingStats.cameraPixelPos[0],
                    (ScreenY - CameraPosMap[1]) * 50 + self.runingStats.cameraPixelPos[1]
                )

                if nowTile == 0:
                    screen.blit(self.worldVisual["tile_2"], tilePos)
                if 1 <= nowTile < 2:
                    screen.blit(self.worldVisual["tile_1"], tilePos)
                    if nowTile == 1.5:
                        screen.blit(self.worldVisual["tile_5"], tilePos)
                if nowTile == 2:
                    screen.blit(self.worldVisual["tile_3"], tilePos)
                if nowTile == 3:
                    screen.blit(self.worldVisual["tile_4"], tilePos)