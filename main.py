import pygame as pg

import status as stats
from world import World
import KeyMouse


class Game:
    def __init__(self) -> None:
        pg.init()
        self.runingStats = stats.RuningStatus()

        ScreenInitSize = pg.display.Info()
        ScreenSize = [
            ScreenInitSize.current_w,
            ScreenInitSize.current_h]
        
        self.runingStats.ScreenMapSize = [
            int(ScreenInitSize.current_w / 50), 
            int(ScreenInitSize.current_h / 50)]
        
        self.screen = pg.display.set_mode(ScreenSize, pg.FULLSCREEN)
        self.startGame: bool = False
        # self.__gameProc()

    def __playerProc(self, worldName: str = "sub") -> None:
        self.player = stats.PlayerStatus(worldName)
        self.player.GetRuningStats(self.runingStats)

    def __gameProc(self) -> None:
        self.worldClass = World()
        self.worldClass.WD.choiseFile("world.txt")
        self.worldClass.getScreenData(self.runingStats)
        self.worldClass.getRuningStatus(self.runingStats)
        self.KeyClass = KeyMouse.KeyPress()
        self.KeyClass.getRuning(self.runingStats)
        self.MouseClass = KeyMouse.MouseEvent()
        self.MouseClass.getRuning(self.runingStats)

    def startScreen(self, screen: pg.surface.Surface) -> None:
        pass

    def run(self) -> None:
        while self.runingStats.runing:
            for evt in pg.event.get():
                if evt.type == pg.QUIT:
                    self.runingStats.runing = False

            if self.startGame:
                self.screen.fill(self.runingStats.bgColor)
                self.KeyClass.update()
                self.MouseClass.update()
                self.worldClass.update()
                self.worldClass.draw(self.screen)
            else:
                self.startScreen(self.screen)
            pg.display.flip()
            pg.time.Clock().tick(self.runingStats.fps)
        
        self.worldClass.WD.saveWorldMap()


if __name__ == "__main__":
    game = Game()
    game.run()
    pg.quit()