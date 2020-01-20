import sys

class Parser:

        #Global variables
        lexlist = []
        Filename = ""
        nextlex = 0
        nexttoken = 0
        position = 0

        #Tokens
        INT_LIT = 10
        IDENT = 12
        ASSIGN_OP = 20
        ADD_OP = 21
        SUB_OP = 22
        MULT_OP = 23
        DIV_OP = 24
        LEFT_PAREN = 25
        RIGHT_PAREN = 26
        UNKNOWN = 99

        def __init__(self, filename):
                try:
                        self.Filename = filename
                        with open(filename, 'r') as textfile:
                                temp = textfile.readlines()
                                self.clean(temp)
                                self.stmnt()
                        textfile.close()
                except OSError:
                        print("Error in opening file")
        
        #Cleans the given lexeme/token pair text file. It basically
        #filters out all the unneeded characters, spaces and commas,
        #into a new list. Within the new list, it removes the
        #unneeded newline character and passes the result to the
        #global lexeme/token list.
        def clean(self, string):
                size = len(string)
                templist = []
                newlist = []

                for i in range(size):
                        lex = string[i]
                        lexsize = len(lex)
                        j = 0
                        while j < lexsize:
                                if lex[j].isalnum() or lex[j] == ".":
                                        tempString = []
                                        while lex[j].isalnum() or lex[j] == ".":
                                                tempString.append(lex[j])
                                                j += 1
                                                if j >= lexsize:
                                                        break
                                        templist.append("".join(tempString))
                                elif lex[j] != " " and lex[j] != ",":
                                        templist.append(lex[j])
                                        j += 1
                                else:
                                        j += 1

                self.lexlist = list(filter(lambda i: i != "\n", templist))

                for i in range(len(self.lexlist)):
                        if self.lexlist[i].isnumeric():
                                newlist.append(int(self.lexlist[i]))
                        else:
                                newlist.append(self.lexlist[i])

                self.lexlist = newlist

        #It gets and sets the next lexeme and token to be
        #analyzed. It then prints out the lexeme/token.
        def get_next(self):
                self.nextlex = self.lexlist[self.position]
                self.position += 1
                self.nexttoken = self.lexlist[self.position]
                self.position += 1
                print("Next token is: {token} Next lexeme is {lex}".format(token = self.nexttoken, lex = self.nextlex))

        #The statement checker determines if a new statement
        #needs to be called after a expression has been
        #anazlyed. If an expression does, it will call the
        #stmnt method with the new expression.
        def stmnt_checker(self):
                if self.nexttoken == self.IDENT and self.lexlist[self.position + 1] == self.IDENT:
                        print("Exit <stmnt>")
                        self.stmnt()
                elif self.nexttoken == self.INT_LIT and self.lexlist[self.position + 1] == self.IDENT:
                        print("Exit <stmnt>")
                        self.stmnt()
                elif self.nexttoken == self.INT_LIT and self.lexlist[self.position + 1] == self.INT_LIT:
                        print("Exit <stmnt>")
                        self.stmnt()
                elif self.nexttoken == self.IDENT and self.lexlist[self.position + 1] == self.INT_LIT:
                        print("Exit <stmnt>")
                        self.stmnt()
                elif self.nexttoken == self.RIGHT_PAREN and self.lexlist[self.position + 1] == self.INT_LIT:
                        print("Exit <stmnt>")
                        self.stmnt()
                elif self.nexttoken == self.RIGHT_PAREN and self.lexlist[self.position + 1] == self.IDENT:
                        print("Exit <stmnt>")
                        self.stmnt()
                elif self.nexttoken == self.IDENT and self.lexlist[self.position + 1] == self.UNKNOWN:
                        print("Exit <stmnt>")
                        self.stmnt()
                elif self.nexttoken == self.INT_LIT and self.lexlist[self.position + 1] == self.UNKNOWN:
                        print("Exit <stmnt>")
                        self.stmnt()

        #The stmnt method introduces the new expression
        #that needs to be analyzed. Its main goal is to
        #determine if the next operator is either an
        #assignment or any other. They will each go to
        #their respective methods.
        def stmnt(self):
                print("Enter <stmnt>")
                if self.lexlist[self.position + 1] == self.IDENT:
                        self.get_next()
                else:
                        self.get_next()
                        print("Syntax error: The following lexeme does not exist: {lex}".format(lex = self.nextlex))

                if self.lexlist[self.position + 1] == self.ASSIGN_OP:
                        while(self.lexlist[self.position + 1] == self.ASSIGN_OP):
                                self.get_next()
                                self.expr()
                        self.get_next()
                        self.expr()
                else:
                        self.expr()

        #In this method, it determines if the next operator
        #is either add or sub. If neither, it will parse the
        #LHS of the expression. If it is add or sub, it will
        #get the next lexeme/token and then parse the LHS of
        #that and then the RHS.
        def expr(self):
                print("Enter <expr>")
                if self.lexlist[self.position + 1] != self.ADD_OP and self.lexlist[self.position + 1] != self.SUB_OP:
                        self.term()
                else:
                        while(self.lexlist[self.position + 1] == self.ADD_OP or self.lexlist[self.position + 1] == self.SUB_OP):
                                self.get_next()
                                self.term()
                print("Exit <expr>")

        #Similar to the expr method. If the next op is not
        #either mult nor div, it will parse the LHS. If it is,
        #it will get the next lexeme/token pair and parse the
        #LHS and then the RHS.
        def term(self):
                print("Enter <term>")
                if self.lexlist[self.position + 1] != self.MULT_OP and self.lexlist[self.position + 1] != self.DIV_OP:
                        self.factor()
                else:
                        while(self.lexlist[self.position + 1] == self.MULT_OP or self.lexlist[self.position + 1] == self.DIV_OP):
                                self.get_next()
                                self.factor()
                print("Exit <term>")

        #The factor method analyzes the lexeme that it is handed.
        #If it is not an operator, it will get the next lexeme/
        #token to be analyzed. If the current lexeme/token is 
        #a left paren however, it will go back to the expr method
        #to determine the next parsing of the expression with its
        #operator. Once a right paren is found, it will get the
        #next lexeme/token to be analyzed. From this point, if
        #there is another operator being used, it will go to its
        #respective method for parsing. As for the errors, if
        #any of the lexemes found is not part of the grammar, it
        #will be thrown as a "syntax error" output and will
        #continue with the parsing. After everything is checked,
        #the method will see if the entire lexeme/token list is
        #completely analyzed and if so, it will exit the program.
        #If not, it will use the statement checker method to
        #check if the next lexeme/token pair is a new statement
        #of expressions and will pass it to the stmnt method for
        #parsing.
        def factor(self):
                print("Enter <factor>")
                if self.lexlist[self.position + 1] == self.IDENT or self.lexlist[self.position + 1] == self.INT_LIT:
                        self.get_next()
                elif self.lexlist[self.position + 1] == self.LEFT_PAREN:
                        while(self.lexlist[self.position + 1] != self.RIGHT_PAREN):
                                self.get_next()
                                self.expr()
                        self.get_next()
                        if self.lexlist[self.position + 1] == self.ADD_OP or self.lexlist[self.position + 1] == self.SUB_OP:
                                self.expr()
                        elif self.lexlist[self.position + 1] == self.MULT_OP or self.lexlist[self.position + 1] == self.DIV_OP:
                                self.term()
                elif self.lexlist[self.position + 1] == self.UNKNOWN:
                        self.get_next()
                        print("Syntax error: The following lexeme does not exist: {lex}".format(lex = self.nextlex))
                else:
                        self.get_next()
                        print("Syntax error: The following lexeme does not exist: {lex}".format(lex = self.nextlex))
                print("Exit <factor>")

                if self.position >= len(self.lexlist):
                        print("Exit <stmnt>")
                        sys.exit()

                self.stmnt_checker()

if __name__ == '__main__':
        Parser(sys.argv[1])
        
#Citation #1: The link provided has few examples of what the filter function can do. In my code,
#             it uses the lambda within the filter function to take out the unnecessary "\n" found
#             in the lexeme/token list. In by doing so, a new list is obtained that has all the
#             lexeme and token pairs without the newline character.
#             (Link: https://www.geeksforgeeks.org/filter-in-python/)

#Citation #2: From user godidier, it was shown how to exit out of a program using the sys library.
#             This was used in the code so the program will exit if the bounds within the
#             lexeme/token list is out of bounds as to not make repeated recursive calls.
#             (Link: https://stackoverflow.com/questions/14639077/how-to-use-sys-exit-in-python)

#Citation #3: In the textbook, pages 175 - 178, it gives the code excerpt for recursive-descent parsing.
#             My code uses parts of the code that was shown but my code accounts for little bit more tweaking.
#             Since it is legal to not have an assignment operator, it needs to determine if the next
#             operator is under <expr> or under <term>. Another difference is that under <factor>,
#             after the right paren, the code checks if another operator is in use. If so, it goes
#             to the correct method. And, the last couple of things, the program will terminate when
#             the index is out of bounds as to not recursive call itself and run into memory leak and
#             the code uses a statement checker. The statement checker determines if the next expression
#             should start a new statement, if so, it will go to the <stmnt> method and run through the new
#             expression.
