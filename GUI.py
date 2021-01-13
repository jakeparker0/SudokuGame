# Sudoku GUI

import tkinter as tk
from Backend import Board
from Puzzles import easy, medium, hard
from PIL import ImageTk, Image


b = [[0, 0, 0, 8, 0, 2, 0, 0, 0],
     [4, 1, 7, 3, 6, 9, 0, 0, 8],
     [0, 0, 0, 0, 0, 0, 0, 6, 3],
     [6, 0, 0, 0, 0, 0, 3, 0, 9],
     [0, 8, 5, 6, 0, 0, 2, 0, 0],
     [0, 0, 0, 5, 9, 0, 7, 0, 0],
     [1, 0, 8, 9, 4, 7, 0, 0, 0],
     [7, 0, 3, 0, 0, 0, 0, 1, 5],
     [0, 6, 9, 1, 3, 0, 0, 0, 4]]
s = [[5, 3, 6, 8, 1, 2, 4, 9, 7],
     [4, 1, 7, 3, 6, 9, 5, 2, 8],
     [8, 9, 2, 7, 5, 4, 1, 6, 3],
     [6, 7, 1, 4, 2, 8, 3, 5, 9],
     [9, 8, 5, 6, 7, 3, 2, 4, 1],
     [3, 2, 4, 5, 9, 1, 7, 8, 6],
     [1, 5, 8, 9, 4, 7, 6, 3, 2],
     [7, 4, 3, 2, 8, 6, 9, 1, 5],
     [2, 6, 9, 1, 3, 5, 8, 7, 4]]

width = 540
height = 960


class display_board:
    def __init__(self, grid, sol, matrix):
        # TODO: Remove Grid and just have array of cells
        # Could completely remove backend

        self.grid = grid  # Current Board
        self.sol = sol  # Solution
        self.matrix = matrix  # Board of stored display cells
        self.selected = None  # Selected Cell
        self.count = 0  # Error Count
        self.notestoggle = False  # Notes Toggle

    def selectCell(self, cell):
        """

        :param cell: Cell to Select
        If no cell is selected, store the selected cell
        if a cell is already selected, unselect that cell, and select new cell
        :return: None
        """
        if self.selected == None:
            # If no cell currently selected
            self.selected = cell
        else:
            self.selected.unselect(None)
            # Otherwise replace the selected cell
            self.selected = cell

    def writeToCell(self, event):
        """

        :param event: KeyPress
        if keypress is a number, write that number to the cell is it correct
        if incorrect, add 1 to the error count


        :return:
        """
        if self.selected != None:
            # A cell must be selected
            x = event.char
            if x.isdigit():  # Input must be a number
                if not self.notestoggle:
                    if self.correctPlacement(int(x)):  # Must be a correct Place
                        self.selected.changeNum(int(x))
                        self.grid[self.selected.pos[0]][self.selected.pos[1]] = int(x)
                        # Update grid
                        self.selected.unselect(None)
                    else:
                        # Count mistakes
                        self.count += 1
                        print("wrong")
                else:
                    self.selected.addNote(x)
                    self.selected.unselect(None)
        if self.GameOver():
            gameWindow.EndGame(self)

    def correctPlacement(self, n):
        # Returns if the input number equals the same cell in solution
        return self.selected.correct == n

    def GameOver(self):
        # Game completed or mistakes exhausted
        return self.grid == self.sol or self.count > 2

    def notestog(self):
        self.notestoggle = not self.notestoggle


class dis_cell:
    def __init__(self, num, pos, notes, master, board):
        self.num = num  # Number
        self.pos = pos  # Position
        self.imut = False  # Imutable, Can't change number after it has been correctly placed
        self.notes = notes  # Notes/Pencil on cell
        self.notelabels = []  # Labels for notes
        self.master = master
        self.board = board  # Board which the cell is in
        self.cell = tk.Frame(self.master, bg="#e8e8e8")
        self.text = ""
        self.correct = self.board.sol[self.pos[0]][self.pos[1]]  # Correct num for the cell

        self.master.create_window((self.pos[0] * 95) + 50, (self.pos[1] * 95) + 50,
                                  window=self.cell, width=93, height=93)
        if self.num != 0:  # If num is already placed
            self.text = str(num)
            self.imut = True
            self.mainlabel = tk.Label(master=self.cell, text=self.text,
                                      font="Calibri 50", bg="#e8e8e8")
            # self.mainlabel.grid(column=1, row=0)
            self.mainlabel.pack()
            self.mainlabel.bind("<Button 1>", self.select)

        # for i in range(3):  # Set grid for notes labels
        #     self.cell.grid_columnconfigure(index=i, minsize=31)
        #     self.cell.grid_rowconfigure(index=i, minsize=31)



        self.cell.bind("<Button 1>", self.select)  # Bind LMB to select when clicked


    def select(self, event):
        """

        :param event: MouseClick
        Selects and highlights the cell when clicked
        Highlights selected cell green and cell in the same row/col light grey
        Still need to do the box
        Could also highlight other cells with the same number in the board
        :return: None
        """
        # self.cell.config(bg="#c0e6a9")
        # if not self.imut:  # able to have notes
        #     for nl in self.notelabels:
        #         nl.config(bg="#c0e6a9")
        # self.mainlabel.config(bg="#c0e6a9")
        if self.board.selected != self:
            self.board.selectCell(self)
            for c in self.board.matrix[self.pos[0]]:
                if c != self:
                    c.cell.config(bg="#dbf3d9")
                    if not c.imut:
                        for nl in c.notelabels:
                            nl.config(bg="#dbf3d9")
                    try:
                        c.mainlabel.config(bg="#dbf3d9")
                    except AttributeError:
                        pass

            for c in [x[self.pos[1]] for x in self.board.matrix]:  # Col
                if c != self:
                    c.cell.config(bg="#dbf3d9")
                    if not c.imut:
                        for nl in c.notelabels:
                            nl.config(bg="#dbf3d9")
                    try:
                        c.mainlabel.config(bg="#dbf3d9")
                    except AttributeError:
                        pass
            topleft = (3+(95*(self.pos[0])), 3 + (95*(self.pos[1]))) #Top left coord of cell

            gameWindow.canvas.create_line([topleft, (topleft[0] + 95, topleft[1]),
                                           (topleft[0] + 95, topleft[1] + 95), (topleft[0], topleft[1]+95),
                                           topleft], fill = "red", width = 2)


            root.bind("<Key>", self.board.writeToCell)  # Bind key press to cell
            self.cell.bind("<Button 1>", self.unselect)
            try:
                self.mainlabel.bind("<Button 1>", self.unselect)
            except AttributeError:
                pass

    def unselect(self, event):
        """

        :param event: Mouseclick
        Reverse of select function
        sets colours of cells back to white
        Also run when player selects another cell
        :return: None
        """
        #self.cell.config(bg="#e8e8e8")
        #self.mainlabel.config(bg="#e8e8e8")
        #for nl in self.notelabels:
            #nl.config(bg="#e8e8e8")
        for c in self.board.matrix[self.pos[0]]:
            if c != self:
                c.cell.config(bg="#e8e8e8")
                for nl in c.notelabels:
                    nl.config(bg="#e8e8e8")
                try:
                    c.mainlabel.config(bg="#e8e8e8")
                except AttributeError:
                    pass
        for c in [x[self.pos[1]] for x in self.board.matrix]:
            if c != self:
                c.cell.config(bg="#e8e8e8")
                for nl in c.notelabels:
                    nl.config(bg="#e8e8e8")
                try:
                    c.mainlabel.config(bg="#e8e8e8")
                except AttributeError:
                    pass

        if len(gameWindow.canvas.find_all()) > 106:

            gameWindow.canvas.delete(gameWindow.canvas.find_all()[-1])




        self.board.selected = None
        self.cell.bind("<Button 1>", self.select)
        try:
            self.mainlabel.bind("<Button 1>", self.unselect)
        except AttributeError:
            pass

    def changeNum(self, n):
        """

        :param n: Number to change the cell to
        Change the cell number and label on the cell
        Removed all notes labels
        Binds backspace to erase the number
        Needs work as it number can only be placed if it is correct and then cannot be changed
        :return: None
        """
        if self.num == 0:
            self.num = n
            self.text = str(n)
            # self.mainlabel.config(text=self.text)
            # self.mainlabel.config(bg="white")
            for nl in self.notelabels:
                nl.destroy()
            self.mainlabel = tk.Label(master=self.cell, text=self.text,
                                  font="Calibri 50",fg = "#4f4f4f", bg="#e8e8e8")
            self.mainlabel.pack()
            self.mainlabel.bind("<Button 1>", self.select)
            #self.imut = True
        # TODO: Erasing, Might have to come after a settings menu
        root.bind("<BackSpace>", self.erase)


    def toString(self):
        return "Num " + str(self.num) + " correct: " + str(self.correct) + " pos " + str(self.pos)

    def erase(self, event):
        if not self.imut:
            self.num = 0
            self.text = ""
            self.mainlabel.destroy()

    def addNote(self, n):
        if n not in self.notes:
            self.notes.append(n)
            notelabel = tk.Label(master=self.cell, text=str(n), font="Calibri 20",
                                 bg="#e8e8e8", fg = "#4f4f4f")
            notelabel.pack()
            # col = ((len(self.notes) - 1) % 3)
            #
            # row = ((len(self.notes) - 1) // 3)
            # print("col", col, "row", row)
            # notelabel.grid(row=row, column=col)
            # self.notelabels.append(notelabel)


class GameWindow:
    def __init__(self, master, load=True):
        # TODO: Load from Main Menu
        self.master = master
        master.title("Game Window")
        self.load = load
        if load:
            self.gridFrame = tk.Frame(master, width=881, height=1200)
            self.gridFrame.pack(padx=10)

            bg_canvas = tk.Canvas(self.gridFrame, width = 881, height = 1200)
            bg_canvas.pack()

            self.canvas = tk.Canvas(bg_canvas, width=858, height=858)
            self.canvas.pack(padx=8, pady=100)

            bg = Image.open("assets/game_screen_bg.jpg")
            render_bg = ImageTk.PhotoImage(bg)
            bg_canvas.create_image(0, 0, image = render_bg)

            self.start = tk.Button(master, text="start",
                                   command=lambda: self.loadBoard(b))
            self.start.pack()

            self.clear = tk.Button(master, text="clear",
                                   command=self.canvas.destroy)
            self.clear.pack()

            self.solve_but = tk.Button(master, text="solve",
                                       command=lambda: self.solve(s))
            self.solve_but.pack()

    def loadBoard(self, grid):
        # add try exception block for if canvas is not drawn yet
        # TODO: Add Try expection block for when canvas is not drawn
        board = Board(grid)
        vis_Board = display_board(board.orig, board.grid, [])
        for r in range(9):
            row = []
            for c in range(9):
                # Create Each cel and Add it to Array
                h = dis_cell(board.orig[r][c], (r, c), [], self.canvas, vis_Board)
                row.append(h)
            vis_Board.matrix.append(row)
        #Create Grid Lines on canvas
        # TODO: Create variable and changing sizes for the board
        global height
        global width
        for i in range(0, 855, 95):
            self.canvas.create_line([(i+3, 3), (i+3, 858)])
        for i in range(0, 855, 95):
            self.canvas.create_line([(3, i+3), (858, i+3)])
        for i in range(0, 855, 285):
            # Inner Lines
            self.canvas.create_line([(i+3, 3), (i+3, 858)], width=2)
            self.canvas.create_line([(3, i+3), (858, i+3)], width=2)
        self.canvas.create_line([(3, 3), (858, 3), (858, 858), (3, 858), (3, 3)], width=3)
        self.canvas.pack(fill=tk.BOTH)
        self.notes_toggle_but = tk.Button(self.master, text="Notes", command=lambda: vis_Board.notestog())
        self.notes_toggle_but.pack()

    # TODO: Create a visual solving from where the player is in the game instead of just recreating the board
    def solve(self, solution):
        # Remove Canvas
        # Easier the looping through the board to remove each cell
        self.canvas.destroy()
        self.canvas = tk.Canvas(self.gridFrame, width=810, height=810)
        self.canvas.pack(fill=tk.BOTH)
        self.loadBoard(solution)

    def EndGame(self, board):
        """

        :param board: Game Board
        Check for end game, either 3 errors or completed board

        :return:
        """
        if board.count > 2:
            print("failed")
            failed = tk.Frame(self.master, width=830, height=830, bg="white")
            failed.place(x=0, y=0)
            failed_label = tk.Label(failed, text="Game Over", font="Helvetica 40 bold ", bg="white")
            failed_label.place(x=275, y=300)
            retry_but = tk.Button(failed, text="Retry")
            # TODO: Create proper End of game screen
        else:
            print("Completed")


class MainMenu:
    # TODO: Proper Main Menu
    # UI design

    def __init__(self, master):
        self.master = master
        self.master.title("Main Menu")

        self.mainFrame = tk.Frame(self.master, width=830, height=1000)
        self.mainFrame.pack()

        self.canvas = tk.Canvas(self.mainFrame, width=830, height=1000,
                                bg="Blue")
        self.canvas.pack()

        self.label = tk.Label(self.canvas, text="Sudoku")

        self.east_Bt = tk.Button(self.canvas, text="Easy", commmand=lambda: gameWindow.loadBoard(easy[0]))
        self.east_Bt.pack()

        self.medium_Bt = tk.Button(self.canvas, text="Medium", commmand=lambda: gameWindow.loadBoard(medium[0]))
        self.medium_Bt.pack()

        self.hard_Bt = tk.Button(self.canvas, text="Hard", commmand=lambda: gameWindow.loadBoard(hard[0]))
        self.hard_Bt.pack()


if __name__ == "__main__":
    root = tk.Tk()
    # main = MainMenu(root)
    gameWindow = GameWindow(root)
    root.mainloop()
