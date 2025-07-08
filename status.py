from json import loads


class RuningStatus:
    def __init__(self) -> None:
        self.runing: bool = True
        self.fps: int = 60
        self.bgColor: list[int, int, int] \
            = [255, 255, 255]
        self.blockSize: list[int, int] \
            = [50, 50]
        
        self.cameraPosMap: list[int, int] \
            = [0, 0]
        self.cameraPixelPos: list[int, int] \
            = [0, 0]
        self.moveSpeed: int = 10

        self.MOUSE_EVT_INIT: list[int, int, int] \
            = [None, None, None]
        self.mouseEvt: list[int, int, int] \
            = self.MOUSE_EVT_INIT


class ScreenData:
    def __init__(self) -> None:
        self.ScreenMapSize: tuple[int, int]


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
                    if index.lower() in str(part).lower():
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