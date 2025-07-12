from PIL import Image
from json import load
from os import path as PATH

import pygame as pg

import status as stats
from visual import BaseVisual


class WorldData:
    def __init__(self, worldFixedData: stats.FixedData) -> None:
        self.WFD = worldFixedData #  <- worldFixedData
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

        except (FileNotFoundError, AttributeError):
            self.worldMap = self.__makeWorldMap()

    def saveWorldMap(self) -> None:
        try:
            with open(self.fileName, "w") as file:
                file.write(str(self.worldMap))
        except (FileNotFoundError, AttributeError):
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
    def mousePress(
            datas: tuple[
            list,
            WorldData],
            cameraPos: list[int, int]) -> None:

        WD = datas[1]
        mouseEvt = datas[0]

        if mouseEvt[2]:
            WD.worldMap[
                mouseEvt[1] + cameraPos[1]][
                    mouseEvt[0] + cameraPos[0]]["struct"] = {"num": 1}


class World:
    def __init__(self) -> None:
        self.worldFixedData = stats.FixedData()

        self.WD = WorldData(self.worldFixedData) #  <- worldData
        self.worldVisual = BaseVisual("world")
        self.struct = BaseVisual("struct")

    def getRuningStatus(self, runingStatus: stats.RuningStatus) -> None:
        self.runingStats = runingStatus
        self.worldVisual.makeVisual(self.runingStats.blockSize)
        self.struct.makeVisual(self.runingStats.blockSize)

    def getScreenData(self, ScreenData: stats.RuningStatus) -> None:
        self.screenData = ScreenData

        self.ScreenMapSize: list[int, int] = self.screenData.ScreenMapSize

    def update(self) -> None:
        if self.runingStats.saveProc:
            self.WD.saveWorldMap()
            self.runingStats.saveProc = False
            print("save ok")

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
            WorldEvtFunc.mousePress(MouseDatas, self.runingStats.cameraPosMap)

    def __drawStruct(self, screen: pg.surface.Surface) -> None:
        if "num" in self.nowStruct and self.nowStruct["num"] is 1:
            screen.blit(self.struct["O_1"], self.tilePos)

    def draw(self, screen: pg.surface.Surface) -> None:
        CameraPosMap = self.runingStats.cameraPosMap

        for ScreenY in range(CameraPosMap[1], self.ScreenMapSize[1] + CameraPosMap[1] + 1):
            for ScreenX in range(CameraPosMap[0], self.ScreenMapSize[0] + CameraPosMap[0] + 1):
                self.nowTile = self.WD.worldMap[ScreenY][ScreenX]["block"]
                self.nowStruct = self.WD.worldMap[ScreenY][ScreenX]["struct"]
                self.tilePos: tuple[int, int] = (
                    (ScreenX - CameraPosMap[0]) * 50 + self.runingStats.cameraPixelPos[0],
                    (ScreenY - CameraPosMap[1]) * 50 + self.runingStats.cameraPixelPos[1]
                )

                if self.nowTile == 0:
                    screen.blit(self.worldVisual["tile_2"], self.tilePos)
                if 1 <= self.nowTile < 2:
                    screen.blit(self.worldVisual["tile_1"], self.tilePos)
                    if self.nowTile == 1.5:
                        screen.blit(self.worldVisual["tile_5"], self.tilePos)
                if self.nowTile == 2:
                    screen.blit(self.worldVisual["tile_3"], self.tilePos)
                if self.nowTile == 3:
                    screen.blit(self.worldVisual["tile_4"], self.tilePos)

                self.__drawStruct(screen)