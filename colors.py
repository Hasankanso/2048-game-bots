

from abc import abstractmethod


class TileColor():
    
    def __init__(self, number_color : (int, int, int), background_color : (int, int, int)):
        self.number_color = None
        self.background_color = None

    @abstractmethod
    def tileToColor(tile):
        number_dark = (119,110,102)
        number_color = number_dark

        if(tile.number == 0):
            background_color = (205,193,181)
        elif tile.number == 2:
            background_color = (238,228,219)
        elif tile.number == 4:
            background_color = (238,225,203)
        elif tile.number == 8:
            background_color = (245,178,127)
            number_color = (249,246,242)
        elif tile.number == 16:
            background_color = (249,150,107)
            number_color = (249,246,242)
        elif tile.number == 32:
            background_color = (251,123,101)
            number_color = (249,246,242)
        else:
            background_color = (251,96,71)
            number_color = (249,246,242)
        
        return TileColor(background_color=background_color, number_color=number_color)

