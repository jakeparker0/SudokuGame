#Sudoku GUI

import tkinter as tk
from Backend import Board

b = [[0, 0, 0, 8, 0, 2, 0, 0, 0],
          [4, 1, 7, 3, 6, 9, 0, 0, 8],
          [0, 0, 0, 0, 0, 0, 0, 6, 3],
          [6, 0, 0, 0, 0, 0, 3, 0, 9],
          [0, 8, 5, 6, 0, 0, 2, 0, 0],
          [0, 0, 0, 5, 9, 0, 7, 0, 0],
          [1, 0, 8, 9, 4, 7, 0, 0, 0],
          [7, 0, 3, 0, 0, 0, 0, 1, 5],
          [0, 6, 9, 1, 3, 0, 0, 0, 4]]
s= [[5, 3, 6, 8, 1, 2, 4, 9, 7],
         [4, 1, 7, 3, 6, 9, 5, 2, 8],
         [8, 9, 2, 7, 5, 4, 1, 6, 3],
         [6, 7, 1, 4, 2, 8, 3, 5, 9],
         [9, 8, 5, 6, 7, 3, 2, 4, 1],
         [3, 2, 4, 5, 9, 1, 7, 8, 6],
         [1, 5, 8, 9, 4, 7, 6, 3, 2],
         [7, 4, 3, 2, 8, 6, 9, 1, 5],
         [2, 6, 9, 1, 3, 5, 8, 7, 4]]

class display_board: 
    def __init__(self, grid, sol, matrix):
        self.grid = grid
        self.sol = sol
        self.matrix= matrix
        self.selected = None 
        self.count = 0
        
    
    def selectCell(self, cell):
        if self.selected == None: 
            #If no cell currently selected
            self.selected = cell
        else: 
            self.selected.unselect(None)
            #Otherwise replace the selected cell
            self.selected = cell
        
    
    def writeToCell(self, event):
        if self.selected != None:
            #A cell must be selected
            x = event.char
            if x.isdigit(): #Input must be a number
                if self.correctPlacement(int(x)):#Must be a correct Place
                    self.selected.changeNum(int(x))
                    self.grid[self.selected.pos[0]][self.selected.pos[1]] = int(x) 
                    #Update grid
                    self.selected.unselect(None)
                else:
                    #Count mistakes 
                    self.count += 1
                    print("wrong")
        if self.GameOver():
            gameWindow.EndGame(self)
    
    def correctPlacement(self, n):
        #Returns if the input number equals the same cell in solution
        return self.selected.correct == n
    
    def GameOver(self):
        #Game completed or mistakes exhausted 
        return self.grid == self.sol or self.count > 2

        
            

        
class dis_cell: 
    def __init__(self, num, pos, notes, master, board):
        self.num= num 
        self.pos = pos 
        self.imut = False 
        self.notes = notes
        self.master = master 
        self.board = board
        self.cell = tk.Frame(self.master, bg  = "white")
        self.text = ""
        self.correct = self.board.sol[self.pos[0]][self.pos[1]]
        
        self.master.create_window((self.pos[0]*90) + 47, (self.pos[1]*90) + 47,
                                  window = self.cell, width =80, height = 80)
        if self.num != 0:
            self.text = str(num)
            self.imut = True
        
        self.label = tk.Label(master = self.cell, text = self.text, 
                              font = "Helvetica 20 bold", bg = "white" )
        self.label.pack( pady = 20)
        
        self.cell.bind("<Button 1>", self.select)
    
    
    def select(self, event): 
        self.cell.config(bg = "#cdfec9")
        self.label.config(bg = "#cdfec9")
        self.board.selectCell(self)
        for c in self.board.matrix[self.pos[0]]:
            if c != self: 
                c.cell.config(bg = "#e3e3e3")
                c.label.config(bg = "#e3e3e3")
        for c in [x[self.pos[1]] for x in self.board.matrix]:
            if c!= self:
                c.cell.config(bg = "#e3e3e3")
                c.label.config(bg = "#e3e3e3")
        root.bind("<Key>", self.board.writeToCell)
        self.cell.bind("<Button 1>", self.unselect)
        
        
    
    def unselect(self, event): 
        self.cell.config(bg = "white")
        self.label.config(bg = "white")
        for c in self.board.matrix[self.pos[0]]:
            if c != self: 
                c.cell.config(bg = "white")
                c.label.config(bg = "white")
        for c in [x[self.pos[1]] for x in self.board.matrix]:
            if c!= self:
                c.cell.config(bg = "white")
                c.label.config(bg = "white")
        self.board.selected = None
        self.cell.bind("<Button 1>", self.select)
        
        
    def changeNum(self, n):
        if self.num == 0:
            self.num = n
            self.text = str(n)
            self.label.config(text = self.text)
            self.label.config(bg = "white")
            # self.label = tk.Label(master = self.cell, text = self.text, 
            #                   font = "Helvetica 20 bold", bg = "white" )
            # self.label.pack(pady = 20)
        root.bind("<BackSpace>", self.erase)
     
    def toString(self):
        return "Num " + str(self.num) + " correct: " + str(self.correct) + " pos " + str(self.pos)
    
    def erase(self, event):
        if not self.imut: 
            self.num = 0 
            self.text = ""
            self.label.destroy()
        #root.unbind("<BackSpace>", self.erase)
            
    def addNote(self, n):
        self.notes.append(n)

        return False 
    
    
        

class GameWindow:
    def __init__(self, master, load = True):
        self.master = master 
        master.title("Game Window")
        self.load = load
        if load:
            self.gridFrame = tk.Frame(master, width =830, height = 830,
                                      pady = 15, padx = 15 )
            self.gridFrame.pack()

            self.canvas = tk.Canvas(self.gridFrame, width = 810, height = 810)
            self.canvas.pack(fill = tk.BOTH)

            self.start = tk.Button(master, text = "start",
                                   command = lambda : self.loadBoard(b))
            self.start.pack()

            self.clear = tk.Button(master, text = "clear",
                                   command = self.canvas.destroy)
            self.clear.pack()

            self.solve_but = tk.Button(master, text = "solve",
                                       command = lambda : self.solve(s) )
            self.solve_but.pack()
        
    def loadBoard(self, grid):
        #add try exception block for if canvas is not drawn yet 
        board = Board(grid)
        vis_Board = display_board(board.orig, board.grid, [])
        for r in range(9):
            row = []
            for c in range(9):
                #Create Each cel and Add it to Array 
                h = dis_cell(board.orig[r][c], (r,c), [], self.canvas, vis_Board)
                row.append(h)
            vis_Board.matrix.append(row)
        #Create Grid Lines on canvas
        for i in range(0,810,90):
            self.canvas.create_line([(i,0), (i,810)])
        for i in range(0,810, 90):
            self.canvas.create_line([(0,i), (810,i)])
        for i in range (0,810, 270): 
            self.canvas.create_line([(i,0), (i,810)], width = 3)
            self.canvas.create_line([(0,i), (810,i)], width = 3)
        self.canvas.pack(fill = tk.BOTH)
        
    def solve(self, solution):
        #Remove Canvas
        #Easier the looping through the board to remove each cell
        self.canvas.destroy()
        self.canvas = tk.Canvas(self.gridFrame, width = 810, height = 810)
        self.canvas.pack(fill = tk.BOTH)
        self.loadBoard(solution)
    
    def EndGame(self, board):
        if board.count > 2: 
            print("failed")
            failed = tk.Frame(self.master, width = 830, height = 830, bg = "white")
            failed.place(x = 0, y = 0)
            failed_label = tk.Label(failed, text = "Game Over", font = "Helvetica 40 bold ", bg = "white")
            failed_label.place( x = 275, y = 300)
            retry_but = tk.Button(failed, text = "Retry")
            
        else: 
            print("Completed")
        

        
class MainMenu: 
    
    def __init__(self, master):
        self.master = master 
        self.master.title("Main Menu")
        
        self.mainFrame = tk.Frame(self.master, width = 830, height = 1000)
        self.mainFrame.pack()
        
        self.canvas = tk.Canvas(self.mainFrame, width = 830, height = 1000, 
                                bg = "Blue")
        self.canvas.pack()
        
        self.label = tk.Label(self.canvas, text = "Sudoku" )
        
        self.east_Bt = tk.Button(self.canvas, text = "Easy" )
        self.east_Bt.pack()
        
        self.medium_Bt = tk.Button(self.canvas, text = "Medium")
        self.medium_Bt.pack()
        
        self.hard_Bt = tk.Button(self.canvas, text = "Hard")
        self.hard_Bt.pack()
        
        
        

                
    
    
    
if __name__ == "__main__":
    root = tk.Tk()
    main = MainMenu(root)
    gameWindow = GameWindow(root, False)
    root.mainloop()
