import pygame as pg

from status import RuningStatus


class KeyPress:
    def getRuning(self, runingStatus: RuningStatus) -> None:
        self.__runingStats = runingStatus

    def update(self) -> None:
        key = pg.key.get_pressed()
        moveSpeed = self.__runingStats.moveSpeed

        if key[pg.K_a]:
            self.__runingStats.cameraPixelPos[0] += moveSpeed
        if key[pg.K_d]:
            self.__runingStats.cameraPixelPos[0] += -moveSpeed
        if key[pg.K_w]:
            self.__runingStats.cameraPixelPos[1] += moveSpeed
        if key[pg.K_s]:
            self.__runingStats.cameraPixelPos[1] += -moveSpeed


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