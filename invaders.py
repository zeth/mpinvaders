"""MicroPython Invaders by Zeth"""

# pylint: disable=import-error,too-many-instance-attributes
from microbit import display, Image, button_a, button_b, sleep

def row_generator(x_pos=2):
    """Make a single row of the cannon."""
    i = 0
    while i != 5:
        if i == x_pos:
            yield '9'
        else:
            yield '0'
        i = i + 1

class Game:
    """Save the world from invading aliens!"""
    def __init__(self):
        self.score = 0
        self.sky = ""
        self.cannon_row = ""
        self.cannon_x_pos = 2
        self.cannon_direction = 1
        self.bullet_x = 0
        self.bullet_y = -1
        self.invader_direction = 1
        self.sky_matrix = []
        self.clear_sky()
        self.insert_row()
        self.update_sky()
        self.update_cannon()

    def clear_sky(self):
        """Create an empty sky."""
        self.sky_matrix = ["00000" for i in range(3)]

    def drop_invaders(self):
        """Drop the invaders down a line."""
        bottom = self.sky_matrix.pop()
        if '8' in bottom:
            return -1
        self.insert_row()

    def move_cannon(self):
        """Move the cannon one LED across."""
        if self.cannon_direction == 1 and self.cannon_x_pos < 4:
            self.cannon_x_pos += 1
        elif self.cannon_direction == 1 and self.cannon_x_pos == 4:
            self.cannon_direction = 0
            self.cannon_x_pos = 3
        elif self.cannon_direction == 0 and self.cannon_x_pos == 0:
            self.cannon_direction = 1
            self.cannon_x_pos = 1
        else:
            self.cannon_x_pos -= 1

    def update_cannon(self):
        """Update the latest state of the bottom row."""
        self.cannon_row = ''.join(row_generator(self.cannon_x_pos))

    def update_sky(self):
        """Convert the sky matrix to a string."""
        self.sky = ':'.join(self.sky_matrix) + ':'

    def show(self):
        """Update the game screen."""
        image = Image(self.sky + self.cannon_row)
        display.show(image)

    def fire(self):
        """Fire the cannon."""
        if (self.bullet_x, self.bullet_y) == (0, -1):
            self.bullet_x = self.cannon_x_pos
            self.bullet_y = 3
            self.update_bullet_cell("9")

    def update_bullet_cell(self, char):
        """Update the bullet cell."""
        out_str = ""
        for indi, value in enumerate(self.sky_matrix[self.bullet_y]):
            if indi == self.bullet_x:
                out_str += char
            else:
                out_str += value
        self.sky_matrix[self.bullet_y] = out_str

    def update_bullet(self):
        """Move the bullet."""
        if self.bullet_y != -1:
            self.update_bullet_cell("0")
            self.bullet_y -= 1
            if self.bullet_y == -1:
                self.bullet_x = 0
            else:
                cell = self.sky_matrix[self.bullet_y][self.bullet_x]
                if cell == "0":
                    self.update_bullet_cell("9")
                elif cell == "8":
                    self.update_bullet_cell("0")
                    self.bullet_x = 0
                    self.bullet_y = -1
                    self.score += 1

    def invaders_move(self):
        """Have them fly back and forth."""
        if self.invader_direction == 1:
            if all((i[4] == "0" for i in self.sky_matrix)):
                self.sky_matrix = [("0" + i[0:-1]) for i in self.sky_matrix]
            else:
                self.invader_direction = 0
        else:
            if all((i[0] == "0" for i in self.sky_matrix)):
                self.sky_matrix = [(i[1:] + "0") for i in self.sky_matrix]
            else:
                self.invader_direction = 1

    def insert_row(self):
        """Insert a new row."""
        self.sky_matrix.insert(0, "88880")

    def run(self):
        """Run the game."""
        i = 0
        wave = 200
        wiggle = 80
        while wave > 20:
            self.show()
            if button_a.was_pressed():
                self.move_cannon()
                self.update_cannon()
            if button_b.was_pressed():
                self.fire()
            self.update_sky()
            self.update_bullet()
            i += 1
            if i % wiggle == 0:
                self.invaders_move()
            if i == wave:
                if self.drop_invaders() == -1:
                    break
                i = 0
                wave -= 1
                if wiggle > 20:
                    wiggle -= 5

def main():
    """Run on start."""
    game = Game()
    game.run()
    score_str = str(game.score)
    display.show("GAME OVER You Scored %s" % score_str)
    sleep(1)
    while 1:
        display.show("--- %s ---" % score_str)
        display.show(Image.HAPPY)
        sleep(1)

if __name__ == "__main__":
    main()
