# Program for lexical analysis of C programs

import re

class lexical_analyser:
    """Class that contains all the functions necessary for lexical analysis."""
    def __init__(self, *args, **kwargs):
        self.code = open("program.c", "r")
        self.result_code = open("result.c", "w")
        self.line_array = self.code.readlines()

    def remove_empty_lines(self):
        """To remove blank lines in the given program."""
        for line in self.line_array:
            if line != "\n":
                self.result_code.write(line)
        self.result_code.close()

    def remove_tab_space(self):
        """To remove tab space in the given program."""
        self.result_code = open("result.c", "r")
        self.line_array = self.result_code.readlines()
        self.result_code.close()


        self.result_code = open("result.c", "w")
        for line in self.line_array:
            if line[0] == " ":
                for c in range(1, len(line)):
                    if line[c] != " ":
                        index = c
                        break
                self.result_code.write(line[index:])
            else:
                self.result_code.write(line)

        self.result_code.close()

    def remove_comment_lines(self):
        """To remove comment lines in the give program."""
        self.result_code = open("result.c", "r")
        self.line_array = self.result_code.readlines()
        self.result_code.close()

        self.result_code = open("result.c", "w")

        comment = False
        for line in self.line_array:
            # For single line comment
            if (line[0:2] != "//") or (line[0:2] != "/*") or comment:
                self.result_code.write(line)

            else:
                comment = True
                new_line_obj = re.match(r'.*\*/', line[2:], re.M)
                if new_line_obj:
                    comment = False
        
        self.result_code.close()

if __name__ == '__main__':
    la = lexical_analyser()
    la.remove_empty_lines()
    la.remove_tab_space()
    la.remove_comment_lines()