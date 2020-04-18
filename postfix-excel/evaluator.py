import sys 

class Cell():
    def __init__(self, name, row, expression):
       self.name = name 
       self.row = row 
       self.expression = expression 


class PostFix():
    def evaluate(self, expression, output_cells):
        operands = {'+': self.add, '-': self.subtract, '/': self.divide, '*':self.multiply}
        numbers = []
        for x in expression.split():
            if x in output_cells.keys(): #substitute cell ref for its value
                numbers.append(output_cells[x].expression)
            elif x in operands.keys():
                if len(numbers) > 1:
                    second = numbers.pop()
                    first = numbers.pop()
                    numbers.append(operands[x](first,second))
                else: 
                    print("Invalid postfix expression! Too many operands. Found " + expression)
                    exit()
            else: 
                numbers.append(x)
        if len(numbers) != 1: #too many numbers 
            print("Invalid postfix expression! Found " + expression)
            exit()
        else:
            return numbers.pop()
        
    def add(self, first, second):
        try: 
            return float(first)+float(second)
        except ValueError:
            print("Invalid Type! Only numbers and cell references should appear in expressions. Found " + str(first)  + " and " + str(second))
            exit()

    def subtract(self, first, second):
        try: 
            return float(first)-float(second)
        except ValueError:
            print("Invalid Type! Only numbers and cell references should appear in expressions. Found " + str(first) + " and " + str(second))
            exit()   

    def divide(self, first, second):
        try: 
            return float(first)/float(second)
        except ValueError:
            print("Invalid Type! Only numbers and cell references should appear in expressions. Found " + str(first) + " and " + str(second))
            exit() 

    def multiply(self, first, second):
        try: 
            return float(first)*float(second)
        except ValueError:
            print("Invalid Type! Only numbers and cell references should appear in expressions. Found " + str(first) + " and " + str(second))
            exit()        


class CellEvaluator(): 
    def __init__(self, input_file, output_file): 
        self.input_file = input_file
        self.output_file = output_file
        self.postfix = PostFix()
        self.cells, self.cell_order = self.read_cells()
        self.output_cells = {}
        return

    def name_cell(self, row, prev_cell): #Generate proper cell names following Excel standard
        if prev_cell == "": #first cell in the file 
            return "A1"
        if prev_cell.row != row: # if row numbers are different, return A + new row number 
            return "A" + str(row)
        else: 
            prev_cellname = prev_cell.name
            prev_cellname = [x for x in list(prev_cellname) if x not in list(str(prev_cell.row))] #only letters
            new_cell = ""
            while len(prev_cellname) > 0: 
                letter = prev_cellname.pop()
                if letter == "Z":
                    new_cell = new_cell + "A"
                    if len(prev_cellname) == 0: #if that was the last letter, we have to add a new one
                        new_cell = new_cell + "A"
                else: 
                    new_cell = new_cell + chr(ord(letter) + 1) #increment the current letter
                    new_cell = new_cell + ''.join(prev_cellname) 
                    break
            return new_cell[::-1] + str(row) #must reverse string to get letter then number order - e.g. A1 instead of 1A

    def read_cells(self):
        cells = {}
        cell_order = []
        try:
            i = 0
            with open(self.input_file, "r") as infile:  
                prev_cell = ""
                for line in infile:
                    i += 1 # new line = new row number 
                    row = line.split(',')
                    for rowitem in row: 
                        cellname = self.name_cell(i, prev_cell)
                        cell_order.append(cellname)
                        new_cell = Cell(cellname, i, rowitem)
                        cells[cellname] = new_cell 
                        prev_cell = new_cell
            return cells, cell_order
        except FileNotFoundError:
            print("Unable to open file. Make sure the filepath is correct.")
            exit()
    
    def evaluate(self, to_evaluate):
        while len(to_evaluate) > 0:
            curr_cell = to_evaluate.pop(0)
            stack = self.get_stack(curr_cell, []) 
            self.evaluate_stack(stack)
            to_evaluate = [x for x in to_evaluate if x not in stack]
        return
    
    def get_stack(self, current_cell, stack):
        stack.append(current_cell)
        for x in self.cells[current_cell].expression.split():
            if x in self.cells.keys():
                if x in stack:
                    print("Error! Cyclical cell dependency found in cell " + x )
                    exit()
                else:
                    self.get_stack(x, stack)
        return stack

    def evaluate_stack(self, eval_stack):
        while len(eval_stack) > 0: 
            curr = eval_stack.pop()
            curr_cell = self.cells[curr]
            self.output_cells[curr] = Cell(curr_cell.name, curr_cell.row, self.postfix.evaluate(curr_cell.expression, self.output_cells))

    
    def get_cell_dependencies(self, current_cell, dependent_cells): #needs to be current-cell formatted
        for x in self.cells[current_cell].expression.split():
            if x in self.cells.keys():
                if x in dependent_cells:
                    print("Error! Cyclical cell dependency found in cell " + x )
                    exit()
                dependent_cells.append(x)
                self.get_cell_dependencies(x, dependent_cells)
        return dependent_cells
    
    def output(self):
        with open(self.output_file, "w+") as outfile:
            prev_row = 0
            for cell in self.cell_order:
                currcell = self.output_cells[cell]
                if currcell.row != prev_row:
                    if prev_row != 0:
                        outfile.write('\n')
                    outfile.write(str(self.output_cells[cell].expression))
                    prev_row = prev_row + 1
                else:
                    outfile.write(','+(str(self.output_cells[cell].expression)))
        outfile.close()

        
                    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Incorrect number of arguments! Please provide an input file and output file as arguments to the script.")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] 
        ce = CellEvaluator(input_file, output_file)
        ce.evaluate(ce.cell_order.copy())
        ce.output()