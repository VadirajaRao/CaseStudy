# Program for lexical analysis of C programs

# Library for using Regular Expression
import re

class lexical_analyser:
    """Class that contains all the functions necessary for lexical analysis."""
    def __init__(self, *args, **kwargs):
        self.code = open("program.c", "r") # Opening the input file in 'read' mode.
        self.result_code = open("result.c", "w") # Opening the intermediate file in 'write' mode.
        self.line_array = self.code.readlines() # Obtaining an array of strings, where each string is a line from the input file.

    def remove_empty_lines(self):
        """To remove blank lines in the given program."""
        # Looping over all the lines in the input file.
        for line in self.line_array:
            # Checking if the line is empty.
            if line != "\n":
                self.result_code.write(line) # Writing the non-empty line onto the intermediate file.
        self.result_code.close() # Closing the intermediate file.

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

    # NOTE: This function is not yet completed.
    def remove_comment_lines(self):
        """To remove comment lines in the give program."""
        self.result_code = open("result.c", "r") # Opening the intermediate file in 'read' mode.
        self.line_array = self.result_code.readlines() # Obtaining an array of strings, where each string is a line from the intermediate file.
        self.result_code.close() # Closing the intermediate file.

        self.result_code = open("result.c", "w") # Opening the intermediate file in 'write' mode.

        """
        comment = False
        for line in self.line_array:
            if (line[0:2] != "//") or (line[0:2] != "/*") or comment:
                self.result_code.write(line)

            else:
                comment = True
                new_line_obj = re.match(r'.*\*/', line[2:], re.M)
                if new_line_obj:
                    comment = False
        """
        comment = False
        for line in self.line_array:
            if comment:
                #print(line)
                comment_match = re.match(r'.*\*/', line, re.M)
                if comment_match:
                    comment = False
                    continue
                else:
                    continue
            
            comment_match = re.match(r'.*//', line, re.M)
            if comment_match:
                for c in range(0, len(line)-1):
                    if (line[c]+line[c+1]) == '//':
                        index = c
                        break
                if c == 0:
                    self.result_code.write(line[:index])
                else:
                    self.result_code.write(line[:index] + "\n")

            else:
                comment_match = re.match(r'.*/\*', line, re.M)
                if comment_match:
                    comment_match = re.match(r'.*\*/', line, re.M)
                    if comment_match:
                        for c in range(0, len(line)-1):
                            if (line[c] + line[c+1]) == "/*":
                                index = c
                                break
                        if index == 0:
                            self.result_code.write(line[:index])
                        else:
                            self.result_code.write(line[:index] + "\n")
                    else:
                        comment = True

                else:
                    self.result_code.write(line)

        self.result_code.close() # Closing the intermediate file.

if __name__ == '__main__':
    la = lexical_analyser() # Creating object for the class.
    la.remove_empty_lines()
    la.remove_tab_space()
    la.remove_comment_lines()