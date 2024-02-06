class Button:
    def __init__(self, window, x, y, width, height, image):
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def draw(self):
        self.window.blit(self.image, (self.x, self.y))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False
