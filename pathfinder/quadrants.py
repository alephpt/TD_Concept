from enum import Enum

## Top Left - ((0, Screen Width / 3), (0, Screen Height / 3))
## Top Right - ((Screen Width - Screen Width / 3, Screen Width), (0, Screen Height / 3))
## Bottom Left - ((0, Screen Width / 3), (Screen Height - Screen Height / 3, Screen Height))
## Bottom Right - ((Screen Width - Screen Width / 3, Screen Width), (Screen Height - Screen Height / 3, Screen Height))
class Quadrant(Enum):
    TOP_LEFT = 0
    BOTTOM_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_RIGHT = 3

    @staticmethod
    def get_random_quadrant():
        import random
        return random.choice(list(Quadrant))
    
    def get_starting_quadrant(self):
        if self == Quadrant.TOP_LEFT:
            return Quadrant.BOTTOM_RIGHT
        elif self == Quadrant.TOP_RIGHT:
            return Quadrant.BOTTOM_LEFT
        elif self == Quadrant.BOTTOM_LEFT:
            return Quadrant.TOP_RIGHT
        elif self == Quadrant.BOTTOM_RIGHT:
            return Quadrant.TOP_LEFT
    
    def get_end_quadrant_pos(self, map_sq_x, map_sq_y):
        if self == Quadrant.TOP_LEFT:
            return (0, map_sq_x // 3), (0, map_sq_y // 3)
        elif self == Quadrant.TOP_RIGHT:
            return (map_sq_x - map_sq_x // 3, map_sq_x), (0, map_sq_y // 3)
        elif self == Quadrant.BOTTOM_LEFT:
            return (0, map_sq_x // 3), (map_sq_y - map_sq_y // 3, map_sq_y)
        elif self == Quadrant.BOTTOM_RIGHT:
            return (map_sq_x - map_sq_x // 3, map_sq_x), (map_sq_y - map_sq_y // 3, map_sq_y)

    def get_start_quadrant_pos(self, map_sq_x, map_sq_y):
        if self == Quadrant.TOP_LEFT:
            return (0, map_sq_x // 2), (0, map_sq_y // 2)
        elif self == Quadrant.TOP_RIGHT:
            return (map_sq_x - map_sq_x // 2, map_sq_x), (0, map_sq_y // 2)
        elif self == Quadrant.BOTTOM_LEFT:
            return (0, map_sq_x // 2), (map_sq_y - map_sq_y // 2, map_sq_y)
        elif self == Quadrant.BOTTOM_RIGHT:
            return (map_sq_x - map_sq_x // 2, map_sq_x), (map_sq_y - map_sq_y // 2, map_sq_y)