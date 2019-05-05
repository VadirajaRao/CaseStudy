# Program to generate first and follow set given a grammar.

import re

class first_and_follow:
    """This class contains all the necessary methods required for generating first and follow set."""
    def __init__(self):
        #self.grammar = ['S -> ABC', 'A -> a | @', 'B -> b | @', 'C -> c | @']
        #self.grammar = ['E->TA', 'A->+TA|@', 'T->FG', 'G->*FG|@', 'F->(E)|a']
        self.grammar = ['S->aT', 'T->SPT|@', 'P->+|*']
        #self.grammar = ['S->(L)|a', 'L->SP', 'P->,SP|@']
        #self.grammar = ['S->P', 'P->(S)SP|@']
        self.rules = {} # To store the modified grammar.
        self.first = {} # To store the first set of the non-terminals.
        self.follow = {} # To store the follow set of the non-terminals.
        self.base_rule = {} # To store the base rule to handle `@`.
        self.fol = dict()
        self.extend_lst = dict()
        self.starting_NT=(self.grammar[0])[0] #takes the first rule's lhs nonterminal as starting symbol

    def simplify_rules(self):
        """This method is used to convert the grammar which is given as a list into a dictionary for further processing."""
        for rule in self.grammar:
            if re.search(r'->', rule):
                temp = re.split(r'->', rule)
                if len(temp[1].strip()) == 0:
                    print("Invalid rule. The rule does not have the RHS.")
                    return

                lhs = temp[0]
                rhs = temp[1]
                temp = []

                if re.search(r'\|', rhs):
                    temp = re.split(r'\|', rhs)
                    if len(temp[1].strip()) == 0:
                        print("Invalid rule. Unnecessary use of `|`.")
                        return

                    for i in range(0, len(temp)):
                        temp[i] = temp[i].strip()

                if len(temp) == 0:
                    temp.append(rhs.strip())
                    self.rules[lhs.strip()] = temp
                    temp = []
                else:
                    self.rules[lhs.strip()] = temp

            else:
                print("Invalid rule. The rule is not deriving anything.")
                return

        print("Modified rules : ")
        print(self.rules)

    def duplicate_entry(self):
        for key in self.first:
            self.first[key] = list(dict.fromkeys(self.first[key]))

    def first_of_x(self, rule):
        rhs = self.rules[rule]
        temp_first = []

        for one in rhs:
            if re.search(r'[a-z]|\+|\*|\-|/|\(|\)|,', one):
                temp_first += one[0]
            elif re.search(r'[A-Z]', one):
                for i in range(0, len(one)):
                    if one[i] in self.first:
                        temp = self.first[one[i]]
                    else:
                        temp = self.first_of_x(one[i])

                    if '@' not in temp:
                        temp_first += temp
                        break

                    temp.remove('@')
                    temp_first += temp

            elif one[0] == '@':
                temp_first += one[0]
            else:
                print("Invalid production encountered while computing FIRST of " + str(lhs))

        return temp_first

    def first_set(self):
        for rule in self.rules:
            if rule in self.first:
                continue
            else:
                self.first[rule] = self.first_of_x(rule)


    def follow_set(self):

        for Nonterminal in self.rules:
            self.fol[Nonterminal]=[]
            self.extend_lst[Nonterminal]=[]
        self.fol[self.starting_NT]=['$']

        for Nonterminal in self.rules: #for each nonterminal
            for key in self.rules: #check for each rules lhs
                for rhs in self.rules[key]: #the individual rules rhs  (lhs->rhs)
                    if rhs.find(Nonterminal)!=-1:
                        #this rhs as the NT we want
                        pos_of_NT = rhs.find(Nonterminal)

                        if  pos_of_NT == len(rhs)-1:
                            #(Key)->(terminal)(Nonterminal)::A->aB. The Follow[Key] in Follow[Nonterminal]
                            try:
                                self.extend_lst[Nonterminal].append(key)
                            except:
                                self.extend_lst[Nonterminal]=key

                        elif re.search(r"[a-z]|\+|\-|\/|\*|\(|\)|,",rhs[pos_of_NT+1]):
                            #(key)->(Terminal)(Nonterminal)(Terminal)
                            try:
                                self.fol[Nonterminal].append(rhs[pos_of_NT+1])
                            except:
                                self.fol[Nonterminal]=[rhs[pos_of_NT]]

                        elif re.search(r"[A-Z]",rhs[pos_of_NT+1]):
                            #(key)->(Terminal)(Nonterminal)(Nonterminal1|Terminal1)+
                            #key->terminalNonterminalNonterminal
                            while rhs[pos_of_NT+1]!='\0':
                                #if the first(the next nonterminal) as an @. Then we need to continue the iteration.
                                #Till the end of the string or till a terminal.
                                #print("RHS:",rhs[pos_of_NT+1])
                                if re.search(r"[A-Z]",rhs[pos_of_NT+1]):
                                    if '@' in self.first[rhs[pos_of_NT+1]]:
                                        for ele in self.first[rhs[pos_of_NT+1]]:
                                            if '@' != ele:
                                                self.fol[Nonterminal].append(ele)
                                        pos_of_NT += 1
                                    elif re.search(r"[A-Z]",rhs[pos_of_NT+1]):
                                        self.fol[Nonterminal].extend(self.first[rhs[pos_of_NT+1]])
                                        break
                                else:
                                    if re.search(r"[a-z]|\+|\-|\/|\*|\(|\)|,",rhs[pos_of_NT+1]):
                                        self.fol[Nonterminal].append(rhs[pos_of_NT+1])
                                        break

                                if pos_of_NT==len(rhs)-1:
                                    #meaning: we have reached end of string and epilson was in previous.
                                    self.extend_lst[Nonterminal].append(key)
                                    # print("Index position:",pos_of_NT,"is reached for rhs",rhs[pos_of_NT])
                                    break

        #adding follow[key] in follow[Nonterminal]
        for Nonterminal in self.extend_lst:
            for ele in self.extend_lst[Nonterminal]:
                if ele != Nonterminal:
                    try:
                        self.fol[Nonterminal].extend(self.fol[ele])
                    except:
                        self.fol[Nonterminal]=self.fol[ele]

        #removing repeated entry and sorting
        for key in self.fol:
            self.fol[key]=list(dict.fromkeys(self.fol[key]))
            self.fol[key].sort()

if __name__ == '__main__':
    print("Running")
    ff = first_and_follow()
    #Un-comment these lines to allow terminal input of the grammar(ctrl+/)
    # n = int(input("First and Follow Set for grammar having no LR, no LF\nEnter the number of rules(Eg:1. A->a|Ba 2. B->c|d): "))
    #
    # for i in range(n):
    #     ff.grammar.append(input("Enter the rule-%d: "%i))

    print("_________________________________________________________________________________________")
    print("_____________________------------------LOG START-------------------______________________")

    ff.simplify_rules()
    ff.first_set()
    ff.duplicate_entry()
    ff.follow_set()
    #ff.duplicate_enrty2()
    print("_____________________------------------LOG END-------------------______________________")
    print("---------------------------------------------------------------------------------------")
    print("___________________----------------Output Started-----------------____________________")
    print("The rule dictionary::")
    print(ff.rules)
    print("\n")

    print("The first set::")
    print(ff.first)
    print("\n")

    print("The Follow Set::")
    print(ff.fol)
    print("\n")

    print("___________________-----------------Output Ended------------------____________________")
    print("---------------------------------------------------------------------------------------")
