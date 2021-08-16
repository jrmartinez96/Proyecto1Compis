import sys
from antlr4 import *
from antlr4.tree.Trees import  TerminalNode
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.ErrorStrategy import ErrorStrategy, DefaultErrorStrategy
from antlr4.error.Errors import *
from DecafLexer import DecafLexer
from DecafParser import DecafParser
from DecafListener import DecafListener
from DecafErrors import *
import utils

class VarSymbolTableItem():
    def __init__(self, varId, varType, isParam, scope):
        self.varId = varId
        self.varType = varType
        self.scope = scope
        self.isParam = isParam
        self.offset = 0

class MethodSymbolTableItem():
    def __init__(self, methodId, methodType):
        self.methodId = methodId
        self.methodType = methodType

class StructSymbolTableItem():
    def __init__(self, varId, varType, structId):
        self.varId = varId
        self.varType = varType
        self.structId = structId

# Maybe a class to check struct?

#---------------------------------------------------------------------------------------------------

class DecafPrinter(DecafListener):
    def __init__(self) -> None:
        # Flags or misc
        self.errorList = []
        self.mainFound = False
        self.currentMethodVoid = False
        self.scopes = []

        # Symbol table related
        self.varSymbolTable = []
        self.methodSymbolTable = []
        self.structSymbolTable = []
        super().__init__()

    def returnErrorList(self):
        return self.errorList
    
    # Enter a parse tree produced by DecafParser#program.
    def enterProgram(self, ctx:DecafParser.ProgramContext):
        self.enterScope('global')
        return super().enterProgram(ctx)
    
    def exitProgram(self, ctx:DecafParser.ProgramContext):
        try:
            if not self.mainFound:
                raise MainNotFound
        except MainNotFound:
            print("MainNotFound at line %d: Main method not found" % ctx.start.line)
        
        self.exitScope()

        return super().exitProgram(ctx)

    def enterVarDeclaration(self, ctx: DecafParser.VarDeclarationContext):
        try:
            if (ctx.NUM() != None):
                value = ctx.getChild(3).getText()
                if (int(value) <= 0):
                    raise ArraySizeError
                else:
                    varType = ctx.getChild(0).getText()
                    varId = ctx.getChild(1).getText()
                    # Add to symbol table
                    newVarStEntry = VarSymbolTableItem(varType=varType, varId=varId, scope=self.getCurrentScope(), isParam=False)

                    self.addVarToSymbolTable(item=newVarStEntry)
            else:
                varType = ctx.varType().getText()
                varId = ctx.ID()
                newVarStEntry = VarSymbolTableItem(varType=varType, varId=varId, scope=self.getCurrentScope(), isParam=False)
                self.addVarToSymbolTable(item=newVarStEntry)     
        except ArraySizeError:
            print("ArraySizeError at line %d: Array size must be bigger than 0" % ctx.start.line)
        
        return super().enterVarDeclaration(ctx)

    def enterMethodDeclaration(self, ctx: DecafParser.MethodDeclarationContext):
        # Se obtienen valores de declaracion de method
        methodType = ctx.getChild(0).getText()
        methodName = ctx.getChild(1).getText()

        # Se ingresa el nuevo scope
        self.enterScope(methodName)

        if (methodType == 'void'):
            self.currentMethodVoid = True
        
        if (methodName == 'main'):
            self.mainFound = True
            try:
                if ctx.getChild(3).getText() != 'void':
                    raise MainHasParameters
            except MainHasParameters:
                print("MainHasParameters at line %d: Method main is declared with parameters" % ctx.start.line)

        # Switch scope to method
        self.enterScope(methodName)

        # Add to method symbol table
        newMethodStEntry = MethodSymbolTableItem(methodName, methodType)

        self.addToMethodSymbolTable(item=newMethodStEntry)

        # Add params to symbol table

        return super().enterMethodDeclaration(ctx)

    # Exit a parse tree produced by DecafParser#methodDeclaration.
    def exitMethodDeclaration(self, ctx:DecafParser.MethodDeclarationContext):
        self.exitScope()
        return super().exitMethodDeclaration(ctx)
    
    # Enter a parse tree produced by DecafParser#parameter.
    def enterParameter(self, ctx:DecafParser.ParameterContext):
        methodId = ctx.parentCtx.getChild(1).getText()
        parameterType = ctx.getChild(0).getText()

        if parameterType != 'void':
            varId = ctx.getChild(1).getText()
            varSymbolTableItem = VarSymbolTableItem(varId=varId, varType=parameterType, isParam=True, scope=methodId)
            self.addVarToSymbolTable(varSymbolTableItem)
        
        return super().enterParameter(ctx)

    def enterBlock(self, ctx: DecafParser.BlockContext):
        return super().enterBlock(ctx)

    def enterStatement(self, ctx: DecafParser.StatementContext):
        try:
            # Children structure
            # 0: Return
            # 1: Value
            # 2: ;
            currentMethodItem = utils.getMethodItem(self.methodSymbolTable, self.getCurrentScope())
            methodType = currentMethodItem.methodType
            returnType = ''

            # Si el statement empieza con return
            if ctx.getChild(0).getText() == 'return':
                if methodType == 'void':
                    if ctx.getChild(1).getText() != '':
                        raise ReturnNotEmpty
                else:
                    expressionCtx = ctx.getChild(1).getChild(0)
                    if expressionCtx == None:
                        returnType = 'void'
                        raise ReturnType
                    
                    expressionType = utils.getExpressionType(expressionCtx, self.varSymbolTable, self.methodSymbolTable)
                    returnType = expressionType
                    if expressionType != methodType:
                        raise ReturnType

            self.currentMethodVoid = False

            return super().enterStatement(ctx)

        except ReturnMissing:
            print("Expected return statement on method")
        except ReturnEmpty:
            print("Missing return value on non-void method")
        except ReturnNotEmpty:
            print("ReturnNotEmpty at line %d: Void type method should have an empty return" % ctx.start.line)
        except ReturnType:
            print("ReturnType at line %d: Cannot return expression of type %s when method type is %s" % (ctx.start.line, returnType, methodType))
    
    # Enter a parse tree produced by DecafParser#methodCall.
    def enterMethodCall(self, ctx:DecafParser.MethodCallContext):
        methodId = ctx.getChild(0).getText()
        try:
            exists = utils.doesMethodExists(methodSymbolTable=self.methodSymbolTable, methodId=methodId)
            if not exists:
                raise MethodNotDeclared
        except MethodNotDeclared:
            print("MethodNotDeclared at line %d: Method '%s' is not declared" % (ctx.start.line, methodId))
        return super().enterMethodCall(ctx)
    
    # --------------------------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------#
    # Funciones de cambio de estado
    def enterScope(self, scope):
        self.scopes.append(scope)
    
    def exitScope(self):
        self.scopes.pop()
    
    def getCurrentScope(self):
        if len(self.scopes) > 0:
            return self.scopes[len(self.scopes) - 1]

    def addVarToSymbolTable(self, item: VarSymbolTableItem):
        try:
            if self.varSymbolTable.count == 0:
                self.varSymbolTable.append(item)
            else:
                exists = False
                for i in self.varSymbolTable:
                    if (item.varId == i.varId and item.scope == i.scope):
                        exists = True

                if not exists:
                    self.varSymbolTable.append(item)
                else:
                    raise ExistingItem
        except ExistingItem:
            print("Variable %s is already declared.", item.varId)

    def addToMethodSymbolTable(self, item: MethodSymbolTableItem):
        try:
            if self.methodSymbolTable.count == 0:
                self.methodSymbolTable.append(item)
            else:
                exists = False
                for i in self.methodSymbolTable:
                    if item.methodId == i.methodId:
                        exists = True

                if not exists:
                    self.methodSymbolTable.append(item)
                else:
                    raise ExistingItem
                    
        except ExistingItem:
            print("Method %s is already declared.", item.methodId)

    def addToStructSymbolTable(self, item: StructSymbolTableItem):
        try:
            if self.structSymbolTable.count == 0:
                self.structSymbolTable.append(item)
            else:
                exists = False
                for i in self.structSymbolTable:
                    if item.structId == i.structId:
                        exists = True

                if not exists:
                    self.structSymbolTable.append(item)
                else:
                    raise ExistingItem
                    
        except ExistingItem:
            print("Struct %s is already declared.", item.structId)

#---------------------------------------------------------------------------------------------------

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = DecafLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = DecafParser(stream)
    tree = parser.program()  
    printer = DecafPrinter()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

    #traverse(tree, parser.ruleNames)

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

