import math
import random
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QMessageBox
import os

from Tile import Tile

class Minesweeper(qtw.QMainWindow):
    path = os.getcwd()
    os.chdir(path)
    ROWS = 8
    COL = 10
    BOMBS = 10
    symbols = {
        'empty': "_",  # empty is the visible display
        "bomb": "*",
        'tile': "#"  # tile is hiding and not seen
    }
    DIFFICULTY = {
        #        row, column, bombs
        'Easy': (8, 10, 10),
        'Normal': (14, 18, 40),
        'Hard': (20, 24, 99)
    }

    # let's say:
    # _ = empty
    # * = bomb
    # number = number
    def __init__(self):
        super().__init__()
        self.setWindowIcon(qtg.QIcon("images/bomb_64x64.png"))
        self.setWindowTitle("Minesweeper")
        self.board = []
        self.is_first_move = True
        self.end_game = False
        self.flag_counter = self.BOMBS
        # create the main layout
        self.main_widget = qtw.QWidget()
        self.main_layout = qtw.QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # set the font stuff after the title creation
        self.create_header()
        self.create_and_set_font()
        # self.main_layout.addWidget(self.title, 1)
        self.main_layout.addWidget(self.header, 1)

        # now the actual game layout
        self.game_widget = qtw.QWidget()
        self.grid_layout = qtw.QGridLayout()
        self.create_tiles()
        self.game_widget.setLayout(self.grid_layout)
        # self.button = qtw.QPushButton()
        self.main_layout.addWidget(self.game_widget, 5)




        # for row in range(self.ROWS):
        #     current = []
        #     for column in range(self.COL):
        #         current.append(Tile(row, column, self.symbols['tile']))
        #     self.board.append(current)
        # print(self.board)
        self.show()

    def create_header(self):
        # header is the whole top
        self.header = qtw.QWidget()
        self.header.setLayout(qtw.QVBoxLayout())
        self.title = qtw.QLabel("Minesweeper")
        self.header.layout().addWidget(self.title)
        self.game_info_widget = qtw.QWidget()
        # game info widget it has difficult + timer + flag count
        self.game_info_layout = qtw.QGridLayout()
        self.game_info_widget.setLayout(self.game_info_layout)
        self.game_info_layout.setSpacing(0)
        self.game_info_layout.setHorizontalSpacing(0)
        self.game_info_layout.setVerticalSpacing(0)
        self.diff_list = self.difficulty_list()
        # self.header.layout().addWidget(self.diff_list)
        self.diff_list.currentTextChanged.connect(self.update_difficulty)
        # addWidget(QWidget, int r, int c, int rowspan, int columnspan) Adds a widget at specified row and column and having specified width and/or height
        # self.game_info_layout.addWidget(self.diff_list, 1, 1, 1, 1)
        self.difficulty_list_widget = qtw.QWidget()
        self.difficulty_list_widget.setLayout(qtw.QVBoxLayout())

        self.difficulty_list_widget.layout().addWidget(self.diff_list)
        self.game_info_layout.addWidget(self.difficulty_list_widget, 1, 1, 1, 1)
        # self.timer_label = qtw.QLabel("000")
        # self.timer_label.setPicture()
        # self.timer_label.setAlignment(qtc.Qt.AlignCenter)
        # self.timer_label.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        # self.game_info_layout.addWidget(self.timer_label, 1, 2, 1, 1, alignment=qtc.Qt.AlignCenter)

        self.flag_label = qtw.QLabel(f"Flag: {self.flag_counter}")

        self.game_info_layout.addWidget(self.create_timer(), 1, 2, 1, 1, alignment=qtc.Qt.AlignCenter)
        self.game_info_layout.addWidget(self.flag_label, 1, 3, 1, 1, alignment=qtc.Qt.AlignRight)
        self.header.layout().addWidget(self.game_info_widget)


    def create_timer(self):
        self.timer_widget = qtw.QWidget()
        self.timer_widget.setLayout(qtw.QHBoxLayout())
        self.timer_label = qtw.QLabel("000")
        self.timer_img = qtw.QLabel(alignment=qtc.Qt.AlignRight)
        self.timer_img.setPixmap(qtg.QPixmap("images/stopwatch.png"))
        # unfortunately you need to rescale it like this keep that in mind for the rescaling
        img_size_change = self.timer_img.pixmap().scaled(32, 32)
        self.timer_img.setPixmap(img_size_change)
        self.timer_widget.layout().addWidget(self.timer_img)
        self.timer_widget.layout().addWidget(self.timer_label)
        # self.timer is the actual timer everything else is just GUI Stuff
        self.timer = qtc.QTimer(self)
        self.seconds_count = 0
        # adding action to timer
        self.timer.timeout.connect(self.showTime)
        # update the timer every 1 second
        # self.timer.start(1000)
        return self.timer_widget

    # method called by timer
    # https://www.geeksforgeeks.org/pyqt5-digital-stopwatch/
    def showTime(self):
        self.seconds_count+=1
        # getting text from seconds_count
        text = str(self.seconds_count)
        # idk how to do a real string buffer appropriately
        # 3, cause we want like 000
        zeroes_to_add = 3 - len(text)
        zeroes_string = "0"
        if zeroes_to_add > 0:
            for i in range(zeroes_to_add):
                text = zeroes_string + text
        # showing text
        self.timer_label.setText(text)
        return



    def difficulty_list(self):
        diff_list = qtw.QComboBox()
        diff_list.setSizePolicy(qtw.QSizePolicy.Maximum, qtw.QSizePolicy.Maximum)
        diff_list.addItem("Easy")
        diff_list.addItem("Normal")
        diff_list.addItem("Hard")
        return diff_list

    def update_difficulty(self, text):
        self.ROWS, self.COL, self.BOMBS = self.DIFFICULTY[text]
        self.reset_board()


    def create_tiles(self):
        self.grid_layout.setSpacing(0)
        self.grid_layout.setHorizontalSpacing(0)
        self.grid_layout.setVerticalSpacing(0)
        # this kind of works? not really?
        # self.grid_layout.setContentsMargins(-1, -1, -1, -1)
        for r in range(self.ROWS):
            current = []
            for c in range(self.COL):
                tile = Tile(r, c, self.symbols['tile'])
                # tile.clicked.connect(lambda: self.pick_spot(tile.get_pos()))
                self.grid_layout.addWidget(tile, r, c, 1, 1)
                tile.coords.connect(self.pick_spot)
                # adding the flag counter watcher
                tile.flagged.connect(self.flag_counter_update)
                current.append(tile)
                # current[-1].clicked.connect(lambda: self.pick_spot(tile.get_pos()))
            self.board.append(current)

    def reset_board(self):
        self.board = []
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)
        self.is_first_move = True
        self.create_tiles()
        self.timer_label.setText("000")
        self.seconds_count=0
        self.flag_counter=self.BOMBS
        self.flag_label.setText(f"Flag: {self.flag_counter}")
        self.timer.stop()


    def pretty_print_board(self):
        # two spaces for the buffer
        column_headers = "  "
        for x in range(self.COL):
            column_headers += str(x) + " "
        row_headers = ""
        for x in range(self.ROWS):
            row_headers += str(x)
        print(column_headers + " |||||||| " + column_headers)
        for row in range(self.ROWS):
            string = ""
            visible_string = ""
            for column in range(self.COL):
                # string += str(self.board[row][column].to_string()) + " "
                string += self.board[row][column].show_value() + " "
                visible_string += str(self.board[row][column].get_value()) + " "
            # string += "\n"
            print(row_headers[row] + " " + string + " |||||||| " + row_headers[row] + " " + visible_string)

    def game_over_screen(self, isWon=False):
        self.msg = QMessageBox()
        self.msg.setWindowIcon(qtg.QIcon("images/bomb_64x64.png"))

        # TODO  icon if you lose and also need one if you won
        if not isWon:
            # self.msg.setIconPixmap(qtg.QPixmap("images/bomb_64x64.png"))
            self.msg.setIconPixmap(qtg.QPixmap("images/mumei_sad.png"))
            self.msg.setWindowTitle("Game Over!")
            self.msg.setText("Game Over!")
            self.msg.setInformativeText("Do you want to continue?")
        else:
            # place winner icon here
            self.msg.setIconPixmap(qtg.QPixmap("images/happy.png"))
            self.msg.setWindowTitle("You won!")
            self.msg.setText("You won!")
            self.msg.setInformativeText("Do you want to continue?")
        # self.msg.setIcon()
        self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.msg.buttonClicked.connect(self.continue_game_check)
        # voodoo shit to make it run
        x = self.msg.exec_()
        # print("chic")
        return self.end_game

    def continue_game_check(self, i):
        # print(i.text())
        # print(self.windowTitle())
        if i.text() == "&Yes":
            self.end_game = False
            self.reset_board()
        else:
            self.end_game = True
            quit()

    def check_game_over(self, isGameOver=False):
        if isGameOver:
            return self.game_over_screen()
        not_shown_tiles = 0
        for row in range(self.ROWS):
            for column in range(self.COL):
                # if you're not visible add to counter
                if not self.board[row][column].isVisible:
                    not_shown_tiles += 1
        # if the only remaining tiles is equal to bombs then game is over, they won
        # print("not shown", not_shown_tiles)
        if not_shown_tiles == self.BOMBS:
            # print("You win!")
            return self.game_over_screen(True)
            # exit()
        return False

    def pick_spot(self, row, column):
        # so first move it generates everything
        # then after that is the normal generation
        # ans = input("What is your first move? (row, column)\n")
        row = int(row)
        column = int(column)
        # print(row, column)
        if self.is_first_move:
            self.first_move(row, column)
        else:
            self.search_explosion(row, column)
            # self.pretty_print_board()

    # start the timer with the first move
    def first_move(self, row, column):
        self.is_first_move = False
        self.timer.start(1000)
        self.generate_board(row, column)
        # self.pretty_print_board()

    def generate_board(self, row_given, column_given):
        for bomb in range(self.BOMBS):
            # this is terrible implementation
            # FIXME better random bomb placer plz
            while True:
                row, col = self.random_coords()
                # can't place a bomb where they chose
                if row == row_given and column_given == col:
                    pass
                # can't place a bomb on top of a bomb
                elif self.board[row][col].get_value() != self.symbols["bomb"]:
                    self.board[row][col].set_value(self.symbols["bomb"])
                    break

        # we have the bombs now we need to generate the numbers that are around bombs
        # then we need to generate the numbers that show bomb stuff
        self.generate_board_numbers()
        # then search explosion thing
        self.search_explosion(row_given, column_given)

    def random_coords(self):
        row = math.floor(random.random() * self.ROWS)
        col = math.floor(random.random() * self.COL)
        return row, col

    # this is bfs or dfs depending on what I decide
    def search_explosion(self, row, col):
        first_tile = self.board[row][col]
        first_tile.set_isVisible(True)
        if first_tile.isBomb:
            self.check_game_over(first_tile.isBomb)
        else:
            self.check_game_over()
        # no expansion if it's just a number, just the one
        # print(first_tile.get_value())
        if first_tile.get_value() != 0:
            return
        queue = []
        visited = []
        # add it to the queue and the visited
        queue.append(first_tile)
        visited.append(first_tile)
        while queue:
            current_tile = queue.pop(0)
            # duck me look in every direction
            row, col = current_tile.get_pos()
            # bottom left row+1, col - 1
            if not (row + 1 >= self.ROWS) and not (col - 1 < 0):
                self.search_explosion_helper(self.board[row + 1][col - 1], queue, visited)
            # left col - 1
            if not (col - 1 < 0):
                self.search_explosion_helper(self.board[row][col - 1], queue, visited)

            # top left row-1, col-1
            if not (row - 1 < 0) and not (col - 1 < 0):
                self.search_explosion_helper(self.board[row - 1][col - 1], queue, visited)

            # top
            if not (row - 1 < 0):
                self.search_explosion_helper(self.board[row - 1][col], queue, visited)

            # top right row-1, col +1
            if not (row - 1 < 0) and not (col + 1 >= self.COL):
                self.search_explosion_helper(self.board[row - 1][col + 1], queue, visited)

            # right row, col +1
            if not (col + 1 >= self.COL):
                self.search_explosion_helper(self.board[row][col + 1], queue, visited)

            # bottom right row+1, col+1
            if not (row + 1 >= self.ROWS) and not (col + 1 >= self.COL):
                self.search_explosion_helper(self.board[row + 1][col + 1], queue, visited)

            # bottom row+1, col
            if not (row + 1 >= self.ROWS):
                self.search_explosion_helper(self.board[row + 1][col], queue, visited)
        self.check_game_over()

    def search_explosion_helper(self, tile, queue, visited):
        if tile not in visited:
            visited.append(tile)
            # if it's an int it's blocking and shouldn't go further
            if tile.get_value() is self.symbols['bomb']:
                return
            # only show if not a bomb
            tile.set_isVisible(True)
            if tile.get_value() > 0:
                return
            queue.append(tile)
        return

    def generate_board_numbers(self):
        for row in range(self.ROWS):
            for column in range(self.COL):
                if not self.board[row][column].isBomb:
                    self.board[row][column].set_value(self.bomb_counter_check(row, column))
            # string += "\n"

    # assigns a number based on the 8 block range and the amount of bomb around it
    def bomb_counter_check(self, row, col):
        result = 0
        # bottom left row+1, col - 1
        if not (row + 1 >= self.ROWS) and not (col - 1 < 0):
            result += self.board[row + 1][col - 1].is_bomb_value()
        # left col - 1
        if not (col - 1 < 0):
            result += self.board[row][col - 1].is_bomb_value()

        # top left row-1, col-1
        if not (row - 1 < 0) and not (col - 1 < 0):
            result += self.board[row - 1][col - 1].is_bomb_value()

        # top
        if not (row - 1 < 0):
            result += self.board[row - 1][col].is_bomb_value()

        # top right row-1, col +1
        if not (row - 1 < 0) and not (col + 1 >= self.COL):
            result += self.board[row - 1][col + 1].is_bomb_value()

        # right row, col +1
        if not (col + 1 >= self.COL):
            result += self.board[row][col + 1].is_bomb_value()

        # bottom right row+1, col+1
        if not (row + 1 >= self.ROWS) and not (col + 1 >= self.COL):
            result += self.board[row + 1][col + 1].is_bomb_value()

        # bottom row+1, col
        if not (row + 1 >= self.ROWS):
            result += self.board[row + 1][col].is_bomb_value()

        # now set it to the empty tile if it is 0
        # if result == 0:
        #     return self.symbols['tile']
        return result

    def create_and_set_font(self):
        arcade_id = qtg.QFontDatabase.addApplicationFont('fonts/PressStart2P.ttf')
        family = qtg.QFontDatabase.applicationFontFamilies(arcade_id)[0]
        self.arcade_font = qtg.QFont(family, 8)
        self.title_font = qtg.QFont(family, 24)
        self.title.setFont(self.title_font)
        self.title.setAlignment(qtc.Qt.AlignCenter)
        self.setFont(self.arcade_font)

    def flag_counter_update(self, didPlaceFlag):
        if didPlaceFlag:
            self.flag_counter-=1
            self.flag_label.setText(f"Flag: {self.flag_counter}")
        else:
                self.flag_counter+=1
                self.flag_label.setText(f"Flag: {self.flag_counter}")
