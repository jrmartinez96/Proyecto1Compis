
import sys
from antlr4 import *
from antlr4.tree.Trees import  TerminalNode
from source_code import SourceCode
from analize_semantic import Semantic, DecafParser, DecafErrors
from DecafLexer import DecafLexer
from intermediate_code import IntermediateCode

def main(argv):
    try:
        input_stream = FileStream(argv[1])
        lexer = DecafLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = DecafParser(stream)
        myErrorListener = DecafErrors.MyErrorListener()
        parser.addErrorListener(myErrorListener)
        tree = parser.program()  
        printer = Semantic()
        walker = ParseTreeWalker()
        walker.walk(printer, tree)

        semantic_errors = printer.errorList + myErrorListener.getErrorsList()

        if len(semantic_errors) == 0:
            varSymbolTable = printer.varSymbolTable
            methodSymbolTable = printer.methodSymbolTable
            structSymbolTable = printer.structSymbolTable
            intermediate_printer = IntermediateCode(varSymbolTable, methodSymbolTable, structSymbolTable)
            intemediate_walker = ParseTreeWalker()
            intemediate_walker.walk(intermediate_printer, tree)

            with open('Decaf/test_files/intermediate.txt', "w") as output_file:
                text = ''
                for line in intermediate_printer.lines:
                    text = text + line.toString() + '\n'
                output_file.write(text)
            
            sourceCode = SourceCode(intermediate_printer.lines, varSymbolTable, structSymbolTable)
            sourceCode.generate()

        for error in myErrorListener.getErrorsList():
            print(error)
        
    except AttributeError as e:
        print(e)
    except Exception as e:
        print(e)
    

def compile_file(filePath):
    try:
        input_stream = FileStream(filePath)
        lexer = DecafLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = DecafParser(stream)
        myErrorListener = DecafErrors.MyErrorListener()
        parser.addErrorListener(myErrorListener)
        tree = parser.program()  
        printer = Semantic()
        walker = ParseTreeWalker()
        walker.walk(printer, tree)

        semantic_errors = printer.errorList + myErrorListener.getErrorsList()

        if len(semantic_errors) == 0:
            varSymbolTable = printer.varSymbolTable
            methodSymbolTable = printer.methodSymbolTable
            structSymbolTable = printer.structSymbolTable
            intermediate_printer = IntermediateCode(varSymbolTable, methodSymbolTable, structSymbolTable)
            intemediate_walker = ParseTreeWalker()
            intemediate_walker.walk(intermediate_printer, tree)

            with open('Decaf/test_files/intermediate.txt', "w") as output_file:
                text = ''
                for line in intermediate_printer.lines:
                    text = text + line.toString() + '\n'
                output_file.write(text)
            
            sourceCode = SourceCode(intermediate_printer.lines, varSymbolTable, structSymbolTable)
            sourceCode.generate()
        
        return semantic_errors
    except AttributeError as e:
        print(e)
    except Exception as e:
        print(e)

def traverse(tree, rule_names, indent = 0):
    if tree.getText() == "<EOF>":
        return
    elif isinstance(tree, TerminalNode):
        print("{0}T='{1}'".format("  " * indent, tree.getText()))
    else:
        print("{0}R='{1}'".format("  " * indent, rule_names[tree.getRuleIndex()]))
        if (tree.children != None):
            for child in tree.children:
                traverse(child, rule_names, indent + 1)

if __name__ == '__main__':
    main(sys.argv)

