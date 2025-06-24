from dataclasses import dataclass

@dataclass
class Config:
    CELL_SIZE: int = 10
    ROWS: int = 60
    COLS: int = 120
    
    @property
    def WIDTH(self):
        return self.COLS * self.CELL_SIZE
    
    @property
    def HEIGHT(self):
        return self.ROWS * self.CELL_SIZE

config = Config()
