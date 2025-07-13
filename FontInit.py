from pygame import font
from pygame import surface


class FontData:
    """このオブジェクトはpygameを初期化してからインスタンス化すること"""
    def __init__(self) -> None:
        SizeData = [10, 20, 30]
        self.__fontData = (font.Font("mainFont/font/mainFont.ttf", size) for size in SizeData)

    def __getitem(self, index) -> font.Font:
        if type(index) is int and len(self.__fontData) >= index:
            return self.__fontData[index]
        else:
            # 例外はすべて一番小さいフォントにする
            return self.__fontData[0]
        
    def GetFont(self, 
                fontSize: int = 0,
                text: str = "null", 
                antialias: bool = True,
                color: tuple[int, int, int] = (255, 255, 255),
                pos: tuple[int, int] = [0, 0]) -> surface.Surface:
        textSurface = font.Font(self.__getitem[fontSize]).render(text, antialias, color)
        textRect = textSurface.get_rect()
        textRect.x = pos[0]
        textRect.y = pos[1]

        return textRect