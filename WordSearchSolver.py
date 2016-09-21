from tkinter import *
from tkinter import messagebox


class MyWindow:
    myLabels = []
    buttons = []
    myEntries = {}
    rows, columns, numwords = 0, 0, 0

    def __init__(self, master):
        self.myLabels.append(Label(master, text="Rows:"))
        self.myLabels.append(Label(master, text="Columns:"))
        self.myLabels.append(Label(master, text="Number of words:"))
        for i in self.myLabels:
            i.grid(row=self.myLabels.index(i), column=0)

        self.myEntries['row'] = Entry(master)
        self.myEntries['col'] = Entry(master)
        self.myEntries['words'] = Entry(master)
        self.myEntries['row'].grid(row=0, column=1)
        self.myEntries['col'].grid(row=1, column=1)
        self.myEntries['words'].grid(row=2, column=1)

        self.buttons.append(Button(master, text="Accept", width=10, command=self.destroyContent))
        self.buttons[0].grid(row=3, column=1)

    def destroyContent(self):
        self.rows = self.myEntries['row'].get()
        self.columns = self.myEntries['col'].get()
        self.numwords = self.myEntries['words'].get()
        try:
            self.rows = int(self.rows)
            self.columns = int(self.columns)
            self.numwords = int(self.numwords)
            for i in self.myLabels:
                i.grid_forget()
            for j in self.buttons:
                j.grid_forget()
            for k in self.myEntries.values():
                k.grid_forget()
            CrossWordSolver(root, self.rows, self.columns, self.numwords)
        except ValueError:
            messagebox.showwarning(title='WARNING!', message='Please enter numbers only')
            for i in self.myEntries.values():
                i.delete(0, END)

class CrossWordSolver:
    crossWordEntries = []
    wordsEntries = []
    words = ()
    rows, columns, numwords = 0, 0, 0
    colorCells = []

    def __init__(self, master, rows, columns, numwords):
        master.title('WordSearch Solver v. 0.0.1')
        frame = Frame(master, padx=10, pady=2)
        frame.grid(row=0, column=0)
        self.crossWordEntries = [[]for j in range(rows)]
        self.rows = rows
        self.columns = columns
        self.numwords = numwords
        for i in range(rows):
            for j in range(columns):
                self.crossWordEntries[i].append(Entry(frame, text="", width=6, justify='center'))
                self.crossWordEntries[i][j].bind("<Leave>", self.makeUpper)
                self.crossWordEntries[i][j].bind("<FocusOut>", self.makeUpper)
                self.crossWordEntries[i][j].grid(row=i, column=j)
        frameAux= Frame(master)
        frameAux.grid(row=1, column=0)
        Label(frameAux, text='Or use a text file instead...').grid(row=0, column=0, columnspan=self.columns)
        Button(frameAux, text='Create new text file', command=self.inputWordPuzzle).grid(row=1, column=0, columnspan=self.columns)
        Button(frameAux, text='Load file to solver', command=self.loadWordPuzzle).grid(row=2, column=0, columnspan=self.columns)
        Button(frameAux, text='Delete all Cells', command=self.deleteGrid).grid(row=3, column=0, columnspan=self.columns)

        # Create entries for words
        frame2 = Frame(master, padx=10, pady=10)
        frame2.grid(row=0, column=1)
        Label(frame2, text="Words to search for:", justify='center').grid(row=0, column=0, columnspan=2)
        for i in range(numwords):
            Label(frame2, text="Word "+str(i + 1)+":").grid(row=i + 1, column=0)
            self.wordsEntries.append(Entry(frame2, text="", justify='center'))
            self.wordsEntries[i].bind("<Leave>", self.checkIfNumber)
            self.wordsEntries[i].bind("<FocusOut>", self.checkIfNumber)
            self.wordsEntries[i].grid(row=i+1, column=1)
        btn_Search = Button(frame2, text='Begin Search', width=12, command=self.searchAlgorithm)
        btn_Search.grid(row=i+2, column=1)
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def inputWordPuzzle(self):
        if messagebox.askquestion(title='CONTINUE?', message='Are you sure you want to create a new file?') == 'yes':
            f = open('wordPuzzle.txt', 'w')
            f.write("# Please Ignore these lines of text:\n# Start by typing the wordPuzzle after these lines!\n# Don't use numbers or leave empty spaces!\n# Make sure you save the file before you upload it to the solver")
            f.close()
            import webbrowser
            webbrowser.open("wordPuzzle.txt")

    def loadWordPuzzle(self):
        lines = ""
        isEmpty = False
        f = open('wordPuzzle.txt', 'r')
        lines = f.readline().strip()
        while lines[0] == '#':
            lines = f.readline().strip()
            if lines == "":  # Break when next line is empty
                isEmpty = True
                break
        if not isEmpty:
            for i in range(self.rows):
                for j in range(self.columns):
                    self.crossWordEntries[i][j].delete(0, END)
                    try:
                        if not lines[j].isdigit():
                            self.crossWordEntries[i][j].insert(0, lines[j].upper())
                    except IndexError:
                        pass
                lines = f.readline().strip()
        else:
            messagebox.showerror(title='OOPS...', message='The file seems to be empty...\nMake sure there are no empty lines on the file\nMake sure you save your file')
        f.close()

    def deleteGrid(self):
        """
            Delete every content of the grid
        """
        if messagebox.askquestion(title='DELETE ALL', message='Are you sure?') == 'yes':
            for i in range(self.rows):
                for j in range(self.columns):
                    self.crossWordEntries[i][j].delete(0, END)

    def makeUpper(self, event):
        if not any(char.isdigit() for char in event.widget.get()):
            upper = event.widget.get().upper()
            event.widget.delete(0, END)
            event.widget.insert(0, upper)
        else:
            messagebox.showwarning(title='WARNING!', message='You are not allowed to enter numbers!')
            event.widget.delete(0, END)


    def checkIfNumber(self, event):
        if any(char.isdigit() for char in event.widget.get()):
            messagebox.showwarning(title='WARNING!', message='You are not allowed to enter numbers!')
            event.widget.delete(0, END)

    def checkErrors(self):
        """
        :return: True if there are errors/False if there arem't any
        """
        # Check every entry of the grid to see if there are blank spaces or two letters
        for i in range(self.rows):
            for j in range(self.columns):
                if len(self.crossWordEntries[i][j].get()) != 1:
                    return True
        for i in range(self.numwords):
            if self.wordsEntries[i].get() == '':
                return True
        return False

    def searchAlgorithm(self):
        if not self.checkErrors():
            self.clearBackground()
            aux = list(self.words)
            for i in range(self.numwords):
                aux.append(self.wordsEntries[i].get().upper())
            self.words = tuple(aux)
            for word in self.words:
                isWordFound = False
                for row in range(self.rows):
                    for column in range(self.columns):
                        if self.crossWordEntries[row][column].get() == word[0]:
                            if self.checkRight(row, column, word):
                                isWordFound = True
                                break
                    if isWordFound:
                        break
            self.words = ()
        else:
            messagebox.showwarning(title='WARNING!', message='Please make sure you have filled out every entry. (The grid entries must contain only one letter)')

    def colorWord(self):
        for coordinate in self.colorCells:
            self.crossWordEntries[coordinate[0]][coordinate[1]].config(bg='#008ae6')
        self.colorCells = []

    def clearBackground(self):
        """
            Clears the background color for the grid
        """
        for i in range(self.rows):
            for j in range(self.columns):
                self.crossWordEntries[i][j].config(bg='white')

    def checkRight(self, row, column, word):
        """
        :param row: the row index were the first character was found
        :param column: the column index were the first character was found
        :param word: The word we want to search for
        :return: True if the word is found by searching to the right/False if not found
        """
        aux = 1
        self.colorCells.append([row, column])
        wordCompare = self.crossWordEntries[row][column].get()
        if wordCompare == word:
            self.colorWord()
            return True
        for i in range(column + 1, self.columns):
            if self.crossWordEntries[row][i].get() == word[aux]:
                wordCompare += self.crossWordEntries[row][i].get()
                self.colorCells.append([row, i])
                aux += 1
                if wordCompare == word:
                    self.colorWord()
                    return True
            else:
                self.colorCells = []
                return False
        self.colorCells = []
        return False

    def on_closing(self):
        f = open('wordPuzzle.txt', 'w')
        f.write("# Please Ignore these lines of text:\n# Start by typing the wordPuzzle after these lines!\n# Don't use numbers or leave empty spaces!\n# Make sure you save the file before you upload it to the solver")
        f.close()
        root.destroy()


root = Tk()
hey = MyWindow(root)
root.mainloop()