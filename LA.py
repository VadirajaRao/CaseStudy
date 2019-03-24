# Program for lexical analysis of C programs

# Library for using Regular Expression
import re

class lexical_analyser:
    """Class that contains all the functions necessary for lexical analysis."""
    def __init__(self, *args, **kwargs):
        self.code = open("program.c", "r") # Opening the input file in 'read' mode.
        self.result_code = open("result.c", "w") # Opening the intermediate file in 'write' mode.
        self.line_array = self.code.readlines() # Obtaining an array of strings, where each string is a line from the input file.
        self.code.close();

    def remove_empty_lines(self):
        """To remove blank lines in the given program."""
        self.result_code = open("result.c", "r") # Opening the intermediate file in 'read' mode.
        self.line_array = self.result_code.readlines() # Obtaining an array of strings, where each string is a line from the intermediate file.
        self.result_code.close() # Closing the intermediate file.
        self.result_code = open("result.c","w") #Opening the intermediate file in 'write' mode.
        # Looping over all the lines in the input file.
        for line in self.line_array:
            # Checking if the line is empty.
            if line != "\n":
                self.result_code.write(line) # Writing the non-empty line onto the intermediate file.
        self.result_code.close() # Closing the intermediate file.

    #NOTE: Can just use `str`.strip() to remove leading and trailing spaces and tabs
    def remove_tab_space(self):
        """To remove tab space in the given program."""
        self.result_code = open("result.c", "r") # Opening the intermediate file in 'read' mode.
        self.line_array = self.result_code.readlines() # Obtaining an array of strings, where each string is a line from the intermediate file.
        self.result_code.close() # Closing the intermediate file.

        self.result_code = open("result.c", "w") # Opening the intermediate file in 'write' mode.
        # Looping over all the lines in the input file.
        for line in self.line_array:
            # Checking if the line begins with a white space.
            if line[0] == " ":
                # Checking from which position the code begins over a loop, in order to remove the tab space.
                for c in range(1, len(line)):
                    if line[c] != " ":
                        index = c # Making note of the position from which the code begins in the line.
                        break
                self.result_code.write(line[index:]) # Writing the line without the tab space into the intermediate file.
            else:
                self.result_code.write(line) # Writing the entire line into the intermediate file in case there is no tab space at the beginning.

        self.result_code.close() # Closing the intermediate file.

    # NOTE: This function is made highly generalised for most kinda comments. But do test it
    def remove_comment_lines(self):
        flag_multi_comment = False #This flag is set to `True` only when theres a multi line comment
        count=0; # Just for debugging purpose. Keeps the count of the number of lines read from input file
        for line in self.line_array:
            count += 1
            if flag_multi_comment == True: # If it is a multi-line comment search for `*/` 
                if re.search(r"\*/",line): # If the line has a '*/' then print the contents after '*/' in that line
                    temp = re.split(r"\*/",line) # This function creates an array just before and after `*/`
                    flag_multi_comment = False # Multi-Line comment has ended
                    if len(temp[1].strip())>0: # Removes extra spaces and tabs.
                        self.result_code.write(temp[1].strip()) #The contents to the left of `*/` is written only if it is >0
            elif re.search("//",line):
                temp = re.split('//',line)
                if len(temp[0].strip())>0:
                    self.result_code.write(temp[0].strip())
                    self.result_code.write("\n")
            elif re.search(r"/\*",line): # Searches for /* in the line
                temp = re.split(r"/\*",line) # Divides the line into portion with /* as center
                flag_multi_comment=True # Sets multi-line flag to True
                if len(temp[0].strip())>0:  #contents to the left of /*
                    self.result_code.write(temp[0].strip()+" ")
                if re.search(r"\*/",line): # Checks if the */ occurs in the same line. 
                    flag_multi_comment = False # In which case its treated as a single line comment
                    temp = re.split(r"\*/",line) #contents to the right of */
                    if len(temp[1].strip())>0:
                        self.result_code.write(temp[1].strip()+"\n")
            elif flag_multi_comment == False : #if its normal line not having //or */ or /*
                self.result_code.write(line.strip()+"\n")

        print("Comment deleting.....")
        print("False Flag Status mean successfully removed comments line")
        print("Flag status: ",flag_multi_comment)
        print("Number of lines parsed: ",count)

        self.result_code.close() # Closing the intermediate file.

    def identifier_entry(self):
        """This function is used to look for the identifiers in the program and then making an entry about the identifier into the symbol table."""
        self.result_code = open("result.c", "r")
        self.line_array = self.result_code.readlines()
        self.result_code.close()

        self.symbol_table = open("symbol.csv", "w")
        
        self.identifiers = []
        self.array_structure = {}
        for line in self.line_array:
            # Checking for integer declarations.
            if re.search(r"int .*", line):
                decl = re.split(r"int ", line)
                
                self.temp = ""
                self.valid_identifier = ""
                self.structure = ""
                self.flag_array = False

                for c in decl[1]:
                    if self.flag_array:
                        if (c == "]"):
                            self.structure += c
                            self.flag_array = False
                            self.array_structure[self.identifiers[-1]] = self.structure
                            continue
                        elif (c == ","):
                            continue
                        elif (c == ";"):
                            print(self.structure)
                            break
                        else:
                            self.structure += c
                            continue

                    if c == "=":
                        self.identifiers += self.temp
                        break

                    elif c == "[":
                        self.identifiers += self.temp
                        self.temp = ""
                        self.structure += c
                        self.flag_array = True

                    elif c == "(":
                        self.temp = ""
                        break

                    elif c == ",":
                        self.identifiers += self.temp
                        self.temp = ""
                        continue

                    elif c == ";":
                        self.identifiers += self.temp
                        self.temp = ""
                        break

                    elif c == " ":
                        continue

                    else:
                        self.temp += c
                
        print(self.identifiers)
        print(self.array_structure)

        self.symbol_table.close()

if __name__ == '__main__':
    la = lexical_analyser() # Creating object for the class.
    la.remove_comment_lines()
    la.remove_empty_lines()
    la.remove_tab_space()
    la.identifier_entry()
