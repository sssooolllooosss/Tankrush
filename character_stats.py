from enum import Enum, auto

class CharacterType(Enum):
    USA = auto()
    UK = auto()
    FRANCE = auto()
    USSR = auto()
    GERMANY = auto()
    JAPAN = auto()
    ITALY = auto()

class CharacterStats:
    def __init__(self, char_type):
        self.char_type = char_type
        self._base_stats = {
            CharacterType.USA: {"health": 100, "attack": 20, "speed": 3, "reload_time": 1.5},
            CharacterType.UK: {"health": 120, "attack": 15, "speed": 2, "reload_time": 1.7},
            CharacterType.FRANCE: {"health": 130, "attack": 15, "speed": 2, "reload_time": 1.8},
            CharacterType.USSR: {"health": 90, "attack": 15, "speed": 3, "reload_time": 1.0},
            CharacterType.GERMANY: {"health": 100, "attack": 25, "speed": 4, "reload_time": 1.5},
            CharacterType.JAPAN: {"health": 80, "attack": 25, "speed": 3, "reload_time": 1.3},
            CharacterType.ITALY: {"health": 90, "attack": 12, "speed": 4, "reload_time": 1.2}
        }
    
    def get_current_stats(self):
        return self._base_stats[self.char_type]
