class ScreenToWorld:
    def __init__(self, boardHeight, boardWidth, screenHeight, screenWidth):
        self.boardHeight = boardHeight
        self.boardWidth = boardWidth
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth

    def transformToWorld(self, x, y):
        xworld = x * self.boardWidth/self.screenWidth
        yworld = y * self.boardHeight/self.screenHeight
        return xworld, yworld
    
    def transformToScreen(self, x, y):
        xworld = x * self.screenWidth/self.boardWidth
        yworld = y * self.screenHeight/self.boardHeight
        return xworld, yworld

        