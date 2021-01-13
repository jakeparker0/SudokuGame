# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 18:58:27 2020

@author: jakeb
"""


# BackEnd

def transpose(m): # Transpose a matrix
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]


def sequence(l):#checks that sequence is correct, May not be needed anymore
    for i in range(1, 10):
        if i not in l or l.count(i) != 1:
            return False
    return True




class cell:
    def __init__(self, num, l, pos):
        self.num = num
        self.l = l
        self.pos = pos

    def replaceNum(self, new):
        self.num = new

    def toString(self):
        return str(self.num) + " pos: (" + str(self.pos[0]) + ", " + str(self.pos[1]) + ")" + str(self.l)

    def possible(self, grid, n):
        for i in range(9):
            if grid[self.pos[0]][i] == n or grid[i][self.pos[1]] == n:
                return False
        x = ((self.pos[1]) // 3) * 3
        y = ((self.pos[0]) // 3) * 3
        for i in range(3):
            for j in range(3):
                if grid[y + i][x + j] == n:
                    return False
        return True

    def allPossible(self, grid):
        for n in range(9):
            if self.possible(grid, n):
                self.l.append(n)




class Board:
    def __init__(self, grid):
        self.grid = grid
        self.board = []
        self.orig = []
        for r in range(9):
            row = []
            self.orig.append(grid[r].copy())
            for c in range(9):
                c = cell(self.grid[r][c], [], (r, c))
                row.append(c)
            self.board.append(row)
        self.solve()

    def getPossible(self):
        for row in self.board:
            for c in row:
                c.checkPossible(self.grid)

    def updateBoard(self):
        for row in range(9):
            for col in range(9):
                self.board[row][col].num = self.grid[row][col]
        self.getPossible()

    def resetBoard(self):
        for row in self.board:
            for c in row:
                c.num = self.orig[c.pos[0]][c.pos[1]]

    def toString(self):
        out = ""
        for r in self.grid:
            out += str(r) + '\n'
        return out

    def completed(self):
        #TODO: Rename variables to more useful names
        boxes = []
        for i in range(0, 2):
            for j in range(0, 2):
                p = self.grid[i * 3:(i * 3) + 3]
                temp = []
                for l in p:
                    temp += l[j * 3:(j * 3) + 3]
            boxes.append(temp)
        rows = map(sequence, self.grid)
        cols = map(sequence, transpose(self.grid))
        box = map(sequence, boxes)
        return not ((False in rows) or (False in cols) or (False in box))

    def solve(self):
        for x in range(9):
            for y in range(9):
                if self.grid[y][x] == 0:
                    for n in range(1, 10):
                        if self.board[y][x].possible(self.grid, n):
                            self.grid[y][x] = n
                            if self.solve():
                                return True
                            self.grid[y][x] = 0
                    return False
        return True


    def isValid(self):
        # When uncompleted, checks that there is a unique solution
        return False


b = Board([[0, 0, 0, 8, 0, 2, 0, 0, 0],
           [4, 1, 7, 3, 6, 9, 0, 0, 8],
           [0, 0, 0, 0, 0, 0, 0, 6, 3],
           [6, 0, 0, 0, 0, 0, 3, 0, 9],
           [0, 8, 5, 6, 0, 0, 2, 0, 0],
           [0, 0, 0, 5, 9, 0, 7, 0, 0],
           [1, 0, 8, 9, 4, 7, 0, 0, 0],
           [7, 0, 3, 0, 0, 0, 0, 1, 5],
           [0, 6, 9, 1, 3, 0, 0, 0, 4]])

b2 = Board([[0, 1, 0, 0, 0, 8, 4, 0, 0],
            [0, 0, 0, 0, 0, 5, 1, 6, 0],
            [0, 2, 0, 4, 0, 0, 5, 0, 0],
            [3, 0, 0, 7, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 3, 0, 9],
            [5, 0, 0, 0, 6, 0, 0, 7, 0],
            [7, 9, 0, 3, 8, 0, 0, 0, 0],
            [0, 0, 1, 6, 0, 0, 7, 8, 3],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]])


print(b2.toString())