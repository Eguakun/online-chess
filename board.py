from piece import Bishop
from piece import King
from piece import Rook
from piece import Pawn
from piece import Queen
from piece import Knight
import time
import pygame


class Board:
    rectangle = (113, 113, 525, 525)
    starting_x = rectangle[0]
    starting_y = rectangle[1]
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns

        self.ready = False

        self.last = None

        self.copy = True

        self.board = [[0 for x in range(8)] for _ in range(rows)]

        self.board[0][0] = Rook(0, 0, "b")
        self.board[0][1] = Knight(0, 1, "b")
        self.board[0][2] = Bishop(0, 2, "b")
        self.board[0][3] = Queen(0, 3, "b")
        self.board[0][4] = King(0, 4, "b")
        self.board[0][5] = Bishop(0, 5, "b")
        self.board[0][6] = Knight(0, 6, "b")
        self.board[0][7] = Rook(0, 7, "b")

        self.board[1][0] = Pawn(1, 0, "b")
        self.board[1][1] = Pawn(1, 1, "b")
        self.board[1][2] = Pawn(1, 2, "b")
        self.board[1][3] = Pawn(1, 3, "b")
        self.board[1][4] = Pawn(1, 4, "b")
        self.board[1][5] = Pawn(1, 5, "b")
        self.board[1][6] = Pawn(1, 6, "b")
        self.board[1][7] = Pawn(1, 7, "b")

        self.board[7][0] = Rook(7, 0, "w")
        self.board[7][1] = Knight(7, 1, "w")
        self.board[7][2] = Bishop(7, 2, "w")
        self.board[7][3] = Queen(7, 3, "w")
        self.board[7][4] = King(7, 4, "w")
        self.board[7][5] = Bishop(7, 5, "w")
        self.board[7][6] = Knight(7, 6, "w")
        self.board[7][7] = Rook(7, 7, "w")

        self.board[6][0] = Pawn(6, 0, "w")
        self.board[6][1] = Pawn(6, 1, "w")
        self.board[6][2] = Pawn(6, 2, "w")
        self.board[6][3] = Pawn(6, 3, "w")
        self.board[6][4] = Pawn(6, 4, "w")
        self.board[6][5] = Pawn(6, 5, "w")
        self.board[6][6] = Pawn(6, 6, "w")
        self.board[6][7] = Pawn(6, 7, "w")

        self.p1Name = "Player 1"
        self.p2Name = "Player 2"

        self.turn = "w"

        self.time1 = 900
        self.time2 = 900

        self.storedTime1 = 0
        self.storedTime2 = 0

        self.winner = None

        self.startTime = time.time()

    def update_moves(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    self.board[i][j].update_valid_moves(self.board)

    def draw(self, win, color):
        if self.last and color == self.turn:
            y, x = self.last[0]
            y1, x1 = self.last[1]

            xx = (4 - x) +round(self.starting_x + (x * self.rectangle[2] / 8))
            yy = 3 + round(self.starting_y + (y * self.rectangle[3] / 8))
            pygame.draw.circle(win, (0,0,255), (xx+32, yy+30), 34, 4)
            xx1 = (4 - x) + round(self.starting_x + (x1 * self.rectangle[2] / 8))
            yy1 = 3+ round(self.starting_y + (y1 * self.rectangle[3] / 8))
            pygame.draw.circle(win, (0, 0, 255), (xx1 + 32, yy1 + 30), 34, 4)

        s = None
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    self.board[i][j].draw(win, color)
                    if self.board[i][j].isSelected:
                        s = (i, j)


    def get_danger_moves(self, color):
        danger_moves = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    if self.board[i][j].color != color:
                        for move in self.board[i][j].move_list:
                            danger_moves.append(move)

        return danger_moves

    def is_checked(self, color):
        self.update_moves()
        danger_moves = self.get_danger_moves(color)
        king_pos = (-1, -1)
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    if self.board[i][j].king and self.board[i][j].color == color:
                        king_pos = (j, i)

        if king_pos in danger_moves:
            return True

        return False

    def select(self, column, row, color):
        changed_move = False
        previous = (-1, -1)
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    if self.board[i][j].selected:
                        previous = (i, j)

        # if piece
        if self.board[row][column] == 0 and previous!=(-1,-1):
            moves = self.board[previous[0]][previous[1]].move_list
            if (column, row) in moves:
                changed_move = self.move(previous, (row, column), color)

        else:
            if previous == (-1,-1):
                self.reset()
                if self.board[row][column] != 0:
                    self.board[row][column].selected = True
            else:
                if self.board[previous[0]][previous[1]].color != self.board[row][column].color:
                    moves = self.board[previous[0]][previous[1]].move_list
                    if (column, row) in moves:
                        changed_move = self.move(previous, (row, column), color)

                    if self.board[row][column].color == color:
                        self.board[row][column].selected = True

                else:
                    if self.board[row][column].color == color:
                        #castling
                        self.reset()
                        if self.board[previous[0]][previous[1]].moved == False and self.board[previous[0]][previous[1]].rook and self.board[row][column].king and column != previous[1] and previous!=(-1,-1):
                            castle = True
                            if previous[1] < column:
                                for j in range(previous[1]+1, column):
                                    if self.board[row][j] != 0:
                                        castle = False

                                if castle:
                                    changed_move = self.move(previous, (row, 3), color)
                                    changed_move = self.move((row,column), (row, 2), color)
                                if not changed_move:
                                    self.board[row][column].selected = True

                            else:
                                for j in range(column+1,previous[1]):
                                    if self.board[row][j] != 0:
                                        castle = False

                                if castle:
                                    changed_move = self.move(previous, (row, 6), color)
                                    changed_move = self.move((row,column), (row, 5), color)
                                if not changed_move:
                                    self.board[row][column].selected = True
                            
                        else:
                            self.board[row][column].selected = True

        if changed_move:
            if self.turn == "w":
                self.turn = "b"
                self.reset()
            else:
                self.turn = "w"
                self.reset()

    def reset(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] != 0:
                    self.board[i][j].selected = False

    def check_mate(self, color):
        if self.is_checked(color):
            king = None
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.board[i][j] != 0:
                        if self.board[i][j].king and self.board[i][j].color == color:
                            king = self.board[i][j]
            if king is not None:
                valid_moves = king.valid_moves(self.board)

                danger_moves = self.get_danger_moves(color)

                danger_count = 0

                for move in valid_moves:
                    if move in danger_moves:
                        danger_count += 1
                return danger_count == len(valid_moves)

        return False

    def move(self, start, end, color):
        checkedBefore = self.is_checked(color)
        changed_move = True
        newBoard = self.board[:]
        if newBoard[start[0]][start[1]].pawn:
            newBoard[start[0]][start[1]].first = False

        newBoard[start[0]][start[1]].change_pos((end[0], end[1]))
        newBoard[end[0]][end[1]] = newBoard[start[0]][start[1]]
        newBoard[start[0]][start[1]] = 0
        self.board = newBoard

        if self.is_checked(color) or (checkedBefore and self.is_checked(color)):
            changed_move = False
            newBoard = self.board[:]
            if newBoard[end[0]][end[1]].pawn:
                newBoard[end[0]][end[1]].first = True

            newBoard[end[0]][end[1]].change_pos((start[0], start[1]))
            newBoard[start[0]][start[1]] = newBoard[end[0]][end[1]]
            newBoard[end[0]][end[1]] = 0
            self.board = newBoard
        else:
            self.reset()

        self.update_moves()
        if changed_move:
            self.last = [start, end]
            if self.turn == "w":
                self.storedTime1 += (time.time() - self.startTime)
            else:
                self.storedTime2 += (time.time() - self.startTime)
            self.startTime = time.time()

        return changed_move



