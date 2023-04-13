import math
from square import Square
from color import Color

class Path:
    def __init__(self, map_width, map_height, start, end):
        self.n_map_x = map_width
        self.n_map_y = map_height
        self.start_index = start
        self.end_index = end
        self.start_pos = (start % self.n_map_x, start // self.n_map_x)
        self.end_pos = (end % self.n_map_x, end // self.n_map_x)
        
    ## Manhattan distance - Number of steps to get from one point to another
    def get_man_distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    ## Euclidian distance - Straight line distance between two points
    def get_euc_distance(self, a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    
    
    def find_entropic_path(self, squares, screen, center_x, center_y, sq_size):
        import sys
        sys.setrecursionlimit(10000)
        
        entropy = 0 
        new_map = []
        
        # determine the color of the square based on its entropy
        # entropy is the number of steps it takes to get to that square
        def color_factor(entropy):
            if entropy == 0:
                return (0, 0, 0)
            red = 355 * (entropy / 6000) - 100 * (entropy / 6000)
            green = 255 * (entropy / 4000)
            blue = 128 * (entropy / 8000) + 128
            return(red, green, blue)
        
        # define recursive function to look at the next 4 squares(above, below, left, right)
        # and check if that square is a path square
        # if it is, and it has not been added to the new map, add it to the new map
        # and call the function again on that square
        def check_next_square(x, y, entropy):
            nonlocal new_map
            nonlocal squares
                    
            # if the current square is out of bounds
            if x < 0 or x >= self.n_map_x or y < 0 or y >= self.n_map_y:
                return
            
            index = y * self.n_map_x + x
            square = squares[index]
            
            # if the current square is not a path square
            if not square.path:
                return
            
            # if the current square has already been added to the new map
            for sq in new_map:
                if sq.index == index:
                    if sq.entropy > entropy:
                        sq.entropy = entropy
                        sq.color = color_factor(entropy)
                    return
            
            print("added square: ", x, y, entropy)
            new_map.append(Square(screen, center_x, center_y, self.n_map_x, x, y, sq_size, color_factor(entropy), True, 0))

            entropy += 1
            check_next_square(x + 1, y, entropy)
            check_next_square(x - 1, y, entropy)
            check_next_square(x, y + 1, entropy)
            check_next_square(x, y - 1, entropy)

        
        check_next_square(self.end_pos[0], self.end_pos[1] + 1, entropy)
            
        for sq in new_map:
            squares[sq.index] = sq
    
    def find_linear_path(self):
        print("manhatton distance: ", self.get_man_distance(self.start_pos, self.end_pos))