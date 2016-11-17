"""
    Program that takes a Word Puzzle, words and searches for the words
    Created by Luis Palomino Trevilla and Sergio Alvarado
"""

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

        self.buttons.append(Button(master, text="Accept", width=10, command=self.destroy_content))
        self.buttons[0].grid(row=3, column=1)

    def destroy_content(self):
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
            WordSearchSolver(root, self.rows, self.columns, self.numwords)
        except ValueError:
            messagebox.showwarning(title='WARNING!', message='Please enter numbers only')
            for i in self.myEntries.values():
                i.delete(0, END)


class WordSearchSolver:
    def __init__(self, master, rows, columns, numwords):
        master.title('WordSearch Solver v. 0.0.1')
        frame = Frame(master, padx=10, pady=2)
        frame.grid(row=0, column=0)
        self.crossWordEntries = [[] for j in range(rows)]  # Entries of the word search grid
        self.wordsEntries = []  # Entries of the words to search for
        self.rows = rows  # Number of rows
        self.columns = columns  # Number of columns
        self.numwords = numwords  # number of words to search for
        self.words = ()
        self.colorCells = []
        for i in range(rows):
            for j in range(columns):
                self.crossWordEntries[i].append(Entry(frame, text="", width=6, justify='center'))
                self.crossWordEntries[i][j].bind("<Leave>", self.make_upper)
                self.crossWordEntries[i][j].bind("<FocusOut>", self.make_upper)
                self.crossWordEntries[i][j].grid(row=i, column=j)

        frameAux = Frame(master)
        frameAux.grid(row=1, column=0)
        # Use file to create word puzzle

        Label(frameAux, text='Or use a text file instead...').grid(row=0, column=0, columnspan=self.columns // 2)
        Button(frameAux, text='Create new text file', command=self.input_word_puzzle).grid(row=1, column=0,
                                                                                           columnspan=self.columns // 2)
        Button(frameAux, text='Load file to solver', command=self.load_word_puzzle_file).grid(row=2, column=0,
                                                                                              columnspan=self.columns // 2)
        Button(frameAux, text='Delete all Cells', command=self.delete_grid).grid(row=3, column=0,
                                                                                 columnspan=self.columns // 2)

        # Use image to create word puzzle
        Label(frameAux, text='Or upload an image instead...').grid(row=0, column=self.columns // 2,
                                                                   columnspan=self.columns // 2)
        Label(frameAux, text='Image name (with filename extension)').grid(row=1, column=self.columns // 2,
                                                                          columnspan=self.columns // 2)
        self.img_name = Entry(frameAux)
        self.img_name.grid(row=2, column=self.columns // 2, columnspan=self.columns // 2)
        Button(frameAux, text='Upload', command=self.upload_image).grid(row=3, column=self.columns // 2,
                                                                        columnspan=self.columns // 2)

        # Create entries for words
        frame2 = Frame(master, padx=10, pady=10)
        frame2.grid(row=0, column=1)
        Label(frame2, text="Words to search for:", justify='center').grid(row=0, column=0, columnspan=2)
        for i in range(numwords):
            Label(frame2, text="Word " + str(i + 1) + ":").grid(row=i + 1, column=0)
            self.wordsEntries.append(Entry(frame2, text="", justify='center'))
            self.wordsEntries[i].bind("<Leave>", self.check_if_number)
            self.wordsEntries[i].bind("<FocusOut>", self.check_if_number)
            self.wordsEntries[i].grid(row=i + 1, column=1)
        btn_Search = Button(frame2, text='Begin Search', width=12, command=self.search_algorithm)
        btn_Search.grid(row=i + 2, column=1)
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def input_word_puzzle(self):
        if messagebox.askquestion(title='CONTINUE?', message='Are you sure you want to create a new file?') == 'yes':
            f = open('wordPuzzle.txt', 'w')
            f.write(
                "# Please Ignore these lines of text:\n# Start by typing the wordPuzzle after these lines!\n# Don't use numbers or leave empty spaces!\n# Make sure you save the file before you upload it to the solver")
            f.close()
            '''
            import webbrowser
            webbrowser.open("wordPuzzle.txt")
            '''
            import os
            os.startfile('wordPuzzle.txt')

    def load_word_puzzle_file(self):
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
            messagebox.showerror(title='OOPS...',
                                 message='The file seems to be empty...\nMake sure there are no empty lines on the file after the comments\nMake sure you save your file before you close it')
        f.close()

    def upload_image(self):
        if self.img_name.get() != '':
            try:
                from PIL import Image
                import pytesseract
                inconsistencies = []  # List where we have inconsistencies
                file_name = self.img_name.get()
                img_file = Image.open(file_name)
                raw_words = pytesseract.image_to_string(img_file, lang='eng').split('\n')
                img_words = []  # List containing rows of uppercase words
                r = 1

                for i in range(len(raw_words)):
                    if raw_words[i] != "":
                        img_words.append(raw_words[i].replace(" ", ""))
                        if len(raw_words[i].replace(" ", "")) != self.columns and r <= self.rows:
                            inconsistencies.append(r)
                        r += 1

                for i in range(self.rows):
                    for j in range(self.columns):
                        self.crossWordEntries[i][j].delete(0, END)
                        try:
                            if not img_words[i][j].isdigit():
                                self.crossWordEntries[i][j].insert(0, img_words[i][j].upper())
                        except IndexError:
                            pass

                if len(inconsistencies) != 0:
                    message = 'There were some inconsistencies on rows'
                    for row in inconsistencies:
                        message += '\n'
                        message += str(row)
                    messagebox.showwarning(title='Inconsistencies', message=message)

                self.clear_background()

            except FileNotFoundError:
                messagebox.showerror(title='File not found',
                                     message='The file was not found! Make sure it is in the respective directory')
        else:
            messagebox.showwarning(title='No filename given', message='Please enter a file name before uploading')

    def delete_grid(self):
        """
            Delete every content of the grid incluiding background
        """
        if messagebox.askquestion(title='DELETE ALL', message='Are you sure?') == 'yes':
            for i in range(self.rows):
                for j in range(self.columns):
                    self.crossWordEntries[i][j].delete(0, END)
            self.clear_background()

    def make_upper(self, event):
        """
        Check if the word search solver's grid has numbers
        If not, then make sure the character is uppercase
        """
        if not any(char.isdigit() for char in event.widget.get()):
            upper = event.widget.get().upper()
            event.widget.delete(0, END)
            event.widget.insert(0, upper)
        else:
            messagebox.showwarning(title='WARNING!', message='You are not allowed to enter numbers!')
            event.widget.delete(0, END)

    def check_if_number(self, event):
        """
            Check if there's a number in the words to search fields
            If a number is found send a message
        """
        if any(char.isdigit() for char in event.widget.get()):
            messagebox.showwarning(title='WARNING!', message='You are not allowed to enter numbers!')
            event.widget.delete(0, END)

    def check_errors(self):
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

    def search_algorithm(self):
        words_not_found = []  # list that stores words not found during the algorithm
        if not self.check_errors():
            self.clear_background()
            aux = list(self.words)
            for i in range(self.numwords):
                aux.append(self.wordsEntries[i].get().upper())
            self.words = tuple(aux)
            for word in self.words:
                is_word_found = False
                for row in range(self.rows):
                    for column in range(self.columns):
                        if self.crossWordEntries[row][column].get() == word[0]:
                            if self.check_right(row, column, word):
                                is_word_found = True
                                break
                            if self.check_left(row, column, word):
                                is_word_found = True
                                break
                            if self.check_up(row, column, word):
                                is_word_found = True
                                break
                            if self.check_down(row, column, word):
                                is_word_found = True
                                break
                            if self.check_up_right(row, column, word):
                                is_word_found = True
                                break
                            if self.check_up_left(row, column, word):
                                is_word_found = True
                                break
                            if self.check_down_right(row, column, word):
                                is_word_found = True
                                break
                            if self.check_down_left(row, column, word):
                                is_word_found = True
                                break
                    if is_word_found:
                        break
                if not is_word_found:  # If word was not found then add it to the list
                    words_not_found.append(word)
            self.words = ()
            if len(words_not_found) != 0:
                message = "The following words were not found: "
                for word_not_found in words_not_found:
                    message += "\n"
                    message += word_not_found.lower()
                messagebox.showinfo(title="Words not found", message=message)

        else:
            messagebox.showwarning(title='WARNING!',
                                   message='Please make sure you have filled out every entry. (The grid entries must contain only one letter)')

    def color_word(self):
        for coordinate in self.colorCells:
            self.crossWordEntries[coordinate[0]][coordinate[1]].config(bg='#008ae6')
        self.colorCells = []

    def clear_background(self):
        """
            Clears the background color for the grid
        """
        for i in range(self.rows):
            for j in range(self.columns):
                self.crossWordEntries[i][j].config(bg='white')

    def check_right(self, row, column, word):
        """
        :param row: the row index were the first character was found
        :param column: the column index were the first character was found
        :param word: The word we want to search for
        :return: True if the word is found by searching to the right/False if not found
        """
        aux = 1
        self.colorCells.append([row, column])
        word_compare = self.crossWordEntries[row][column].get()
        if word_compare == word:
            self.color_word()
            return True
        for i in range(column + 1, self.columns):
            if self.crossWordEntries[row][i].get() == word[aux]:
                word_compare += self.crossWordEntries[row][i].get()
                self.colorCells.append([row, i])
                aux += 1
                if word_compare == word:
                    self.color_word()
                    return True
            else:
                self.colorCells = []
                return False
        self.colorCells = []
        return False

    def check_left(self, row, column, word):
        """
        :param row: the row index were the first character was found
        :param column: the column index were the first character was found
        :param word: The word we want to search for
        :return: True if the word is found by searching to the left/False if not found
        """
        aux = 1
        self.colorCells.append([row, column])
        word_compare = self.crossWordEntries[row][column].get()
        if word_compare == word:
            self.color_word()
            return True
        for i in range(column - 1, -1, -1):
            if self.crossWordEntries[row][i].get() == word[aux]:
                word_compare += self.crossWordEntries[row][i].get()
                self.colorCells.append([row, i])
                aux += 1
                if word_compare == word:
                    self.color_word()
                    return True
            else:
                self.colorCells = []
                return False
        self.colorCells = []
        return False

    def check_up(self, row, column, word):
        """
        :param row: the row index were the first character was found
        :param column: the column index were the first character was found
        :param word: The word we want to search for
        :return: True if the word is found by searching up/False if not found
        """
        aux = 1
        self.colorCells.append([row, column])
        word_compare = self.crossWordEntries[row][column].get()
        if word_compare == word:
            self.color_word()
            return True
        for i in range(row - 1, -1, -1):
            if self.crossWordEntries[i][column].get() == word[aux]:
                word_compare += self.crossWordEntries[i][column].get()
                self.colorCells.append([i, column])
                aux += 1
                if word_compare == word:
                    self.color_word()
                    return True
            else:
                self.colorCells = []
                return False
        self.colorCells = []
        return False

    def check_down(self, row, column, word):
        """
        :param row: the row index were the first character was found
        :param column: the column index were the first character was found
        :param word: The word we want to search for
        :return: True if the word is found by searching down/False if not found
        """
        aux = 1
        self.colorCells.append([row, column])
        word_compare = self.crossWordEntries[row][column].get()
        if word_compare == word:
            self.color_word()
            return True
        for i in range(row + 1, self.rows):
            if self.crossWordEntries[i][column].get() == word[aux]:
                word_compare += self.crossWordEntries[i][column].get()
                self.colorCells.append([i, column])
                aux += 1
                if word_compare == word:
                    self.color_word()
                    return True
            else:
                self.colorCells = []
                return False
        self.colorCells = []
        return False

    def check_up_right(self, row, column, word):
        """
        :param row: the row index were the first character was found
        :param column: the column index were the first character was found
        :param word: The word we want to search for
        :return: True if the word is found by searching up-right/False if not found
        """
        aux = 1
        self.colorCells.append([row, column])
        word_compare = self.crossWordEntries[row][column].get()
        if word_compare == word:
            self.color_word()
            return True
        i = row - 1
        j = column + 1

        while i >= 0 and j < self.columns:
            if self.crossWordEntries[i][j].get() == word[aux]:
                word_compare += self.crossWordEntries[i][j].get()
                self.colorCells.append([i, j])
                aux += 1
                if word_compare == word:
                    self.color_word()
                    return True
            else:
                self.colorCells = []
                return False
            i -= 1
            j += 1
        self.colorCells = []
        return False

    def check_up_left(self, row, column, word):
        """
        :param row: the row index were the first character was found
        :param column: the column index were the first character was found
        :param word: The word we want to search for
        :return: True if the word is found by searching up-left/False if not found
        """
        aux = 1
        self.colorCells.append([row, column])
        word_compare = self.crossWordEntries[row][column].get()
        if word_compare == word:
            self.color_word()
            return True
        i = row - 1
        j = column - 1

        while i >= 0 and j >= 0:
            if self.crossWordEntries[i][j].get() == word[aux]:
                word_compare += self.crossWordEntries[i][j].get()
                self.colorCells.append([i, j])
                aux += 1
                if word_compare == word:
                    self.color_word()
                    return True
            else:
                self.colorCells = []
                return False
            i -= 1
            j -= 1
        self.colorCells = []
        return False

    def check_down_right(self, row, column, word):
        """
        :param row: the row index were the first character was found
        :param column: the column index were the first character was found
        :param word: The word we want to search for
        :return: True if the word is found by searching down_right/False if not found
        """
        aux = 1
        self.colorCells.append([row, column])
        word_compare = self.crossWordEntries[row][column].get()
        if word_compare == word:
            self.color_word()
            return True
        i = row + 1
        j = column + 1

        while i < self.rows and j < self.columns:
            if self.crossWordEntries[i][j].get() == word[aux]:
                word_compare += self.crossWordEntries[i][j].get()
                self.colorCells.append([i, j])
                aux += 1
                if word_compare == word:
                    self.color_word()
                    return True
            else:
                self.colorCells = []
                return False
            i += 1
            j += 1
        self.colorCells = []
        return False

    def check_down_left(self, row, column, word):
        """
        :param row: the row index were the first character was found
        :param column: the column index were the first character was found
        :param word: The word we want to search for
        :return: True if the word is found by searching down_left/False if not found
        """
        aux = 1
        self.colorCells.append([row, column])
        word_compare = self.crossWordEntries[row][column].get()
        if word_compare == word:
            self.color_word()
            return True
        i = row + 1
        j = column - 1

        while i < self.rows and j >= 0:
            if self.crossWordEntries[i][j].get() == word[aux]:
                word_compare += self.crossWordEntries[i][j].get()
                self.colorCells.append([i, j])
                aux += 1
                if word_compare == word:
                    self.color_word()
                    return True
            else:
                self.colorCells = []
                return False
            i += 1
            j -= 1
        self.colorCells = []
        return False

    @staticmethod
    def on_closing():
        f = open('wordPuzzle.txt', 'w')
        f.write(
            "# Please Ignore these lines of text:\n# Start by typing the wordPuzzle after these lines!\n# Don't use numbers or leave empty spaces!\n# Make sure you save the file before you upload it to the solver")
        f.close()
        root.destroy()


root = Tk()
hey = MyWindow(root)
root.mainloop()