from json import loads
import sqlite3
from os import path as PATH
from FontInit import FontData


class RuningStatus:
    def __init__(self) -> None:
        self.runing: bool = True
        self.fps: int = 60
        self.bgColor: list[int, int, int] \
            = [255, 255, 255]
        self.blockSize: list[int, int] \
            = [50, 50]
        
        self.cameraPosMap: list[int, int] \
            = [40, 40]
        self.cameraPixelPos: list[int, int] \
            = [0, 0]
        self.moveSpeed: int = 10

        self.MOUSE_EVT_INIT: list[int, int, int] \
            = [None, None, None]
        self.mouseEvt: list[int, int, int] \
            = self.MOUSE_EVT_INIT
        
        self.ScreenMapSize: tuple[int, int]
        self.saveProc: bool = False
        self.worldName: str = None


class FixedData:
    def __init__(self):
        self.__loadData()

    def __getitem__(self, index: str | int) -> None:
        """
        ここで__loadDataで読み込んだjson形式のworldデータ
        を返す、最初のifでindexが文字列でデータのキーが合うか一部があったら
        そのデータをdictで返す
        """
        if type(index) is str:
            if index in self.data:
                return {"key": index, "value": self.data[index]}
            else:
                for part in self.data:
                    if index.upper() in str(part).upper():
                        return {"key": part, "value": self.data[part]}
                else:
                    raise ValueError
        else:
            raise TypeError

    def __loadData(self) -> None:
        try:
            with open("world.json", "r") as file:
                self.data: dict = loads(file.read())
        except FileNotFoundError as err:
            print(err)


class PlayerStatus:
    def __init__(self, worldName: str) -> None:
        self.__worldName = worldName

    def GetRuningStats(self, runingStats: RuningStatus) -> None:
        self.__runingStats = runingStats
        self.__load()

    def __load(self) -> bool:
        try:
            if PATH.isdir(self.__worldName):
                self.__connect = sqlite3.connect(f"world/{self.__worldName}/player.db")
                self.__cursor = self.__connect.cursor()
                self.__runingStats.worldName = self.__worldName
                return True
            else:
                raise FileNotFoundError
        except (FileNotFoundError, sqlite3.Error):
            self.__connect = sqlite3.connect(f"world/sub/player.db")
            self.__cursor = self.__connect.cursor()
            self.__runingStats.worldName = "sub"

            return False