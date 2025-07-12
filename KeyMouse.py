import pygame as pg

from status import RuningStatus
from status import FixedData


class KeyPress:
    def __init__(self) -> None:
        self.fixedData = FixedData()

    def getRuning(self, runingStatus: RuningStatus) -> None:
        self.__runingStats = runingStatus

    def update(self) -> None:
        key = pg.key.get_pressed()
        moveSpeed = self.__runingStats.moveSpeed
        cameraPos = self.__runingStats.cameraPosMap

        if any(key):
            self.__settingProcKey(key)

            if key[pg.K_a] and cameraPos[0] != 0:

                self.__runingStats.cameraPixelPos[0] += moveSpeed
            if key[pg.K_d] and self.fixedData["WORLDSIZE"]["value"][0] != \
                    cameraPos[0] + self.__runingStats.ScreenMapSize[0]:
                
                self.__runingStats.cameraPixelPos[0] += -moveSpeed
            if key[pg.K_w] and cameraPos[1] != 0:
                
                self.__runingStats.cameraPixelPos[1] += moveSpeed
            if key[pg.K_s] and self.fixedData["WORLDSIZE"]["value"][1] != \
                    cameraPos[1] + self.__runingStats.ScreenMapSize[1]:
                
                self.__runingStats.cameraPixelPos[1] += -moveSpeed

    def __settingProcKey(self, key: pg.key) -> None:
        if key[pg.K_F1]:
            self.__runingStats.saveProc = True


class MouseEvent:
    def __init__(self) -> None:
        pass

    def getRuning(self, runingStatus: RuningStatus) -> None:
        self.runingStats = runingStatus
        self.MOUSE_EVT_INIT = self.runingStats.MOUSE_EVT_INIT

    def update(self) -> None:
        mousePos = pg.mouse.get_pos()
        mouseBtn = pg.mouse.get_pressed()

        if mouseBtn[0]:
            pos = [int(mousePos[0] / 50), int(mousePos[1] / 50)]
            self.runingStats.mouseEvt = [pos[0], pos[1], 1]
        else:
            self.runingStats.mouseEvt = self.MOUSE_EVT_INIT