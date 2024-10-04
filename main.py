from tkinter import Tk, BOTH, Canvas
import time

def main():
    num_rows = 12
    num_cols = 16
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)
    
    win.wait_for_close()

class Window():
    def __init__(self, width, height) -> None:
        self.__root = Tk()
        self.__root.title("Maze solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(master=self.__root, bg="white", width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__running = True
        
        while self.__running:
            self.redraw()
    
    def close(self):
        self.__running = False
        
    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Line():
    def __init__(self, point_1, point_2):
        self.point1 = point_1
        self.point2 = point_2
    
    def draw(self, canvas, fill_color):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2)
        
        
class Cell():
    def __init__(self, win, fill_color="black"):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win
        self.fill_color = fill_color
        
    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        
        if self.has_left_wall:
            left_wall = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(left_wall, self.fill_color)
        if self.has_right_wall:
            right_wall = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(right_wall, self.fill_color)
        if self.has_top_wall:
            top_wall = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(top_wall, self.fill_color)
        if self.has_bottom_wall:
            bottom_wall = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(bottom_wall, self.fill_color)


    def draw_move(self, to_cell, undo=False):
        half_length = abs(self._x2 - self._x1) // 2
        x_center = half_length + self._x1
        y_center = half_length + self._y1
        
        half_length2 = abs(to_cell._x2 - to_cell._x1) // 2
        x_center2 = half_length2 + to_cell._x1
        y_center2 = half_length2 = to_cell._y1

        fill_color = "red"
        if undo:
            fill_color = "gray"
            
        move = Line(Point(x_center, y_center), Point(x_center2, y_center2))
        self._win.draw_line(move, fill_color)
        
class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._create_cells()
        
    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
                

    def _draw_cell(self, i, j):
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j  * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        
    
    def _aminate(self):
        self._win.redraw()
        time.sleep(0.05)
        
if __name__ == '__main__':
    main()