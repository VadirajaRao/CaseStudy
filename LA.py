# Program for lexical analysis of C programs

# Library for using Regular Expression
import re
import csv

class lexical_analyser:
    """Class that contains all the functions necessary for lexical analysis."""
    def __init__(self, *args, **kwargs):
        self.code = open("program.c", "r") # Opening the input file in 'read' mode.
        self.result_code = open("result.c", "w") # Opening the intermediate file in 'write' mode.
        self.line_array = self.code.readlines() # Obtaining an array of strings, where each string is a line from the input file.
        self.code.close()
        self.identifiers = []
        self.array_structure = {}
        self.temp = ""
        self.valid_identifier = ""
        self.structure = ""
        self.flag_array = False
        filename = "sym.csv"
        fields = ['Token_Name','datatype','Variable_name','value','address']
        with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
      
    # writing the fields 
            csvwriter.writerow(fields)
            csvfile.close()

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
        count=0 # Just for debugging purpose. Keeps the count of the number of lines read from input file
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

    def check(self, c_name):
        filename1 ="sym.csv"
        redc = False    #setting the identifier redundancy flag to false
        with open(filename1) as csvfile1: 
            # creating a csv writer object 
            csvreader1 = csv.DictReader(csvfile1)
            #skips the header name in the csv file(first row.)
            lcount = 0
            for line in csvreader1:
                if lcount == 0:
                    pass
                else:
                    if c_name is line['Variable_name']:   #checking for redundant identifiers in the csv file(symbol table)
                            redc = True     #setting the redundancy flag to true
                            print("Duplicate declaration of Identifier: "+c_name)
                            break
                    else:
                        pass
                lcount += 1
            csvfile1.close()
        return redc     #returning true /false depending on the redundancy check

    def process_declaration(self, decl,datatype):

        """This function is used to process the declaration statements of variables independent of the type."""
        # Looping character by character in the string which contains only the part where variables are mentioned(without the datatype keyword).
        filename = "sym.csv"
        name = ""
        i=0
        pos=-1
        flag=0 #used to track identifiers with having digits
        with open(filename, 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            for c in decl:
                
                pos += 1
                i=0
                # Checking if the variable mentioned is an array declaration. This will be executed only if '[' character has been encountered earlier.
                if self.flag_array:
                    # Checks if the '[' has a matching ']'
                    if (c == "]"):
                        self.structure += c # Saving the current status of the array structure.
                        self.flag_array = False # Setting flag to say that the array declaration has been processed completely.
                        self.array_structure[self.identifiers[-1]] = self.structure # Saving the array structure(or dimension) into a dictionary.
                        continue # Jumping into the next iteration.
                    # Checks if next variable is going to be declared.
                    elif (c == ","):
                        continue # Jumping to the next iteration.
                    # Checks if declaration statement is ending.
                    elif (c == ";"):
                        print(self.structure)
                        break # Breaking out of the loop. It can also be return.
                    # If none of the conditions match then it is the dimension being mentioned.
                    else:
                        self.structure += c # Saving the dimension into the variable that is used for saving the overall structure of the array.
                        continue # Jumping to the next iteration.

                # Checking if the variable is being assigned with a value during the declaration.
               
                if c == "=":
                    flag=1 #this means the encountered digits are values
                    self.identifiers += self.temp # Saving the characters parsed so far as an identifier, since '=' operator marks the end of the identifier and beginning of the value.

                    if(len(name.strip())>0 and re.search(r"[a-zA-Z_][a-zA-Z_0-9]*",name.strip()) and not(self.check(name.strip()))):
                        if(re.search(r"[0-9]", decl).start()):
                            indexValue = re.search(r"[0-9\.]+", decl[pos:]).start()
                            lastValue = re.search(r"[0-9\.]+", decl[pos:]).end()
                            value = decl[pos+indexValue:pos+lastValue]
                            csvwriter.writerow(['Identifier',datatype,name.strip(),value,''])
                            name=""
                            
                            continue
                        csvwriter.writerow(['Identifier',datatype,name.strip(),'',''])
                        name = ""
                        
                    

                # Checking if an array is being declared.
                elif c == "[":
                    self.identifiers += self.temp # String read so far is saved as an identifier, since '[' marks the end of identifier name and begin of the dimension.
                    self.temp = "" # Emptying the string which contained the name of the identifier.
                    if len(name.strip())>0 and re.search(r"[a-zA-Z_][a-zA-Z_0-9]*",name.strip()) and not(self.check(name.strip())):
                        csvwriter.writerow(['Identifer',datatype+"Array",name.strip(),'',''])
                        name = ""
                    self.structure += c # Adding '[' into the structure variable.
                    self.flag_array = True # Marking the beginning of dimension.

                # Checking if the declaration is for a function.
                elif c == "(":
                    self.temp = "" # Emptying the string which holds the identifier name since it is a function name and not that of any variable.
                    break

                # Checking if the declaration is marking end of a variable name.
                elif c == ",":
                    flag=0 #after "," it's possible that identifier has digit in it. So, make flag 0 again
                    self.identifiers += self.temp # Adding the name parsed so far into the list of all variables.
                    self.temp = "" # Emptying the string which holds the name of the identifier.
                    if len(name.strip())>0 and re.search(r"[a-zA-Z_][a-zA-Z_0-9]*",name.strip()) and not(self.check(name.strip())):
                        # if(re.search())
                            
                        csvwriter.writerow(['Identifer',datatype,name.strip(),'',''])
                        name = ""
                    continue

                # Checking if the statement has ended.
                elif c == ";":
                    self.identifiers += self.temp # Adding the string parsed so far into the list of identifiers.
                    self.temp = "" # Emptying the string that holds the name of the identifier.
                    if len(name.strip())>0 and re.search(r"[a-zA-Z_][a-zA-Z_0-9]*",name.strip()) and not(self.check(name.strip())):
                        csvwriter.writerow(['Identifer',datatype,name.strip(),'',''])
                        name = ""
                    break

                # Checking for whitespaces within the line.
                elif c == " ":
                    continue
                #Doesn't take values as identifier names
                elif(re.search(r'[0-9]',c)):
                    if(flag == 1): #check if it's value or identifier
                        continue
                    else:
                        self.temp += c
                        name += c

                # If none of the conditions satisfy, then the character is part of the identifier name. Hence adding it to the name string.
                else:
                    self.temp += c
                    name += c
                
                
                

    def identifier_entry(self):
	    """This function is used to look for the identifiers in the program and then making an entry about the identifier into the symbol table."""
	    self.result_code = open("result.c", "r")
	    self.line_array = self.result_code.readlines()
	    self.result_code.close()

	    #self.symbol_table = open("symbol.csv", "w")
	    datatypes = ["int","float","char","double"] #the datatypes
	    '''General Pattern for search and sub function for all datatype '''
	    struct = "&& .*"
	    struct1 = "&& "

	    # Looping over all the lines in the intermediate program.
	    for line in self.line_array:
	        # Checking for integer declarations.
	        for datatype in datatypes:
	            pat = re.sub("&&",datatype,struct)
	            pat1 = re.sub("&&",datatype,struct1)
	            if re.search(pat,line):
	                dec1 = re.split(pat1,line)
                
	                self.process_declaration(dec1[1],datatype)
	    print(self.identifiers)
	    print(self.array_structure)

	    #self.symbol_table.close()

    def op_number(self):
        self.result_code = open("result.c", "r") # Opening the intermediate file in 'read' mode.
        self.line_array = self.result_code.readlines() # Obtaining an array of strings, where each string is a line from the intermediate file.
        self.result_code.close() # Closing the intermediate file.
        num=0
        l=1
        for line in self.line_array:
            c = None
            c = re.findall(r"[+\-\*=/]+",line)
            if len(c)>0:
                print("operators:",len(c),"Line no.: ",l,c)
                num = num + len(c)
            l += 1
        print("num of operators: ",num)


    # def declaration_values(self):
	#     """look for the identifiers in the program and then
    #      make an entry about the identifier and their value
    #     into the symbol table."""

	#     self.result_code = open("result.c", "r")
	#     self.line_array = self.result_code.readlines()
	#     self.result_code.close()
    #     datatypes = ["int","float","double","long","char"]

    #     for line in self.line_array:
    #         for d in datatypes:
    #             if(re.search(d,line)):



if __name__ == '__main__':
    la = lexical_analyser() # Creating object for the class.
    la.remove_comment_lines()
    la.remove_empty_lines()
    la.remove_tab_space()
    la.op_number()
    la.identifier_entry()
