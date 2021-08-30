
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

class VarSymbolTableItem():
    def __init__(self, varId, varType, isParam, scope, isArray=False):
        self.varId = varId
        self.varType = varType
        self.scope = scope
        self.isParam = isParam
        self.isArray = isArray
        self.offset = 0

class MethodSymbolTableItem():
    def __init__(self, methodId, methodType):
        self.methodId = methodId
        self.methodType = methodType

class StructSymbolTableItem():
    def __init__(self, varId, varType, structId, isArray=False):
        self.varId = varId
        self.varType = varType
        self.structId = structId
        self.isArray = isArray


import utils

#---------------------------------------------------------------------------------------------------

class DecafPrinter(DecafListener):
    def __init__(self) -> None:
        # Flags or misc
        self.errorList = []
        self.mainFound = False
        self.currentMethodVoid = False
        self.currentMethod = ''
        self.scopes = []
        self.ifCount = 0
        self.elseCount = 0
        self.whileCount = 0

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
            self.errorList.append("MainNotFound at line %d: Main method not found" % ctx.start.line)
            print("MainNotFound at line %d: Main method not found" % ctx.start.line)
        
        self.exitScope()

        return super().exitProgram(ctx)

    def enterVarDeclaration(self, ctx: DecafParser.VarDeclarationContext):
        parentCtx = ctx.parentCtx
        isParentStruct = False
        structId = ''
        isArray = False

        if str(type(parentCtx)) == "<class 'DecafParser.DecafParser.StructDeclarationContext'>":
            isParentStruct = True
            structId = parentCtx.ID().getText()

        try:
            varType = ctx.varType().getText()
            varId = ctx.ID().getText()

            if (ctx.NUM() != None):
                value = ctx.getChild(3).getText()
                isArray = True
                if (int(value) <= 0):
                    raise ArraySizeError
            
            if isParentStruct:
                newStructEntry = StructSymbolTableItem(varId=varId, varType=varType, structId=structId, isArray=isArray)
                self.addToStructSymbolTable(item=newStructEntry)
            else:
                newVarStEntry = VarSymbolTableItem(varType=varType, varId=varId, scope=self.getCurrentScope(), isParam=False, isArray=isArray)
                self.addVarToSymbolTable(item=newVarStEntry)    
        except ArraySizeError:
            self.errorList.append("ArraySizeError at line %d:%d Array size must be bigger than 0" % (ctx.start.line, ctx.start.column))
            print("ArraySizeError at line %d:%d Array size must be bigger than 0" % (ctx.start.line, ctx.start.column))
        
        return super().enterVarDeclaration(ctx)

    def enterMethodDeclaration(self, ctx: DecafParser.MethodDeclarationContext):
        # Se obtienen valores de declaracion de method
        methodType = ctx.getChild(0).getText()
        methodName = ctx.getChild(1).getText()

        # Se ingresa el nuevo scope
        self.enterScope(methodName)
        self.currentMethod = methodName

        if (methodType == 'void'):
            self.currentMethodVoid = True
        
        if (methodName == 'main'):
            self.mainFound = True
            try:
                if ctx.getChild(3).getText() != 'void':
                    raise MainHasParameters
            except MainHasParameters:
                self.errorList.append("MainHasParameters at line %d:%d Method main is declared with parameters" % (ctx.start.line, ctx.start.column))
                print("MainHasParameters at line %d:%d Method main is declared with parameters" % (ctx.start.line, ctx.start.column))

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

            currentMethodItem = utils.getMethodItem(self.methodSymbolTable, self.currentMethod)
            methodType = currentMethodItem.methodType
            returnType = ''

            # Errores de asignacion
            locationType = ''
            expressionType = ''

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
                    
                    expressionType = utils.getExpressionType(expressionCtx, self.varSymbolTable, self.methodSymbolTable, self.structSymbolTable, self.getScopes())
                    returnType = expressionType
                    if expressionType != methodType:
                        if expressionType == None:
                            raise ExpressionDoesNotExist
                        else:
                            raise ReturnType

            self.currentMethodVoid = False
            
            # Si es una asignacion
            if ctx.location() != None:
                locationCtx = ctx.location()
                expressionCtx = ctx.expression()

                locationType = utils.getLocationType(locationCtx, self.varSymbolTable, self.structSymbolTable, self.getScopes(), False, '')
                expressionType = utils.getExpressionType(expressionCtx, self.varSymbolTable, self.methodSymbolTable, self.structSymbolTable, self.getScopes())

                if locationType == None:
                    raise VariableNotDeclared
                if expressionType == None:
                    raise ExpressionDoesNotExist
                
                if locationType != expressionType:
                    raise AssignmentType

        except ReturnMissing:
            self.errorList.append("Expected return statement on method")
            print("Expected return statement on method")
        except ReturnEmpty:
            self.errorList.append("Missing return value on non-void method")
            print("Missing return value on non-void method")
        except ReturnNotEmpty:
            self.errorList.append("ReturnNotEmpty at line %d:%d Void type method should have an empty return" % (ctx.start.line, ctx.start.column))
            print("ReturnNotEmpty at line %d:%d Void type method should have an empty return" % (ctx.start.line, ctx.start.column))
        except ExpressionDoesNotExist:
            self.errorList.append("ExpressionDoesNotExist at line %d:%d Something in the expression does not exist in the local context" % (ctx.start.line, ctx.start.column))
            print("ExpressionDoesNotExist at line %d:%d Something in the expression does not exist in the local context" % (ctx.start.line, ctx.start.column))
        except VariableNotDeclared:
            self.errorList.append("VariableNotDeclared at line %d:%d Variable is not declared." % (ctx.start.line, ctx.start.column))
            print("VariableNotDeclared at line %d:%d Variable is not declared." % (ctx.start.line, ctx.start.column))
        except ReturnType:
            self.errorList.append("ReturnType at line %d:%d Cannot return expression of type %s when method type is %s" % (ctx.start.line, ctx.start.column, returnType, methodType))
            print("ReturnType at line %d:%d Cannot return expression of type %s when method type is %s" % (ctx.start.line, ctx.start.column, returnType, methodType))
        except AssignmentType:
            self.errorList.append("AssignmentType at line %d:%d '%s' type cannot be assign to '%s' type" % (ctx.start.line, ctx.start.column, expressionType, locationType))
            print("AssignmentType at line %d:%d '%s' type cannot be assign to '%s' type" % (ctx.start.line, ctx.start.column, expressionType, locationType))
    
    # Enter a parse tree produced by DecafParser#ifStatement.
    def enterIfStatement(self, ctx:DecafParser.IfStatementContext):
        try:
            expressionCtx = ctx.expression()
            expressionType = utils.getExpressionType(expressionCtx, self.varSymbolTable, self.methodSymbolTable, self.structSymbolTable, self.getScopes())
            self.enterScope("if" + str(self.ifCount))
            self.ifCount = self.ifCount + 1
            if expressionType != 'boolean':
                raise IfExpressionIsNotBoolean
        except IfExpressionIsNotBoolean:
            self.errorList.append("IfExpressionIsNotBoolean at line %d:%d If expression is not of type boolean" % (ctx.start.line, ctx.start.column))
            print("IfExpressionIsNotBoolean at line %d:%d If expression is not of type boolean" % (ctx.start.line, ctx.start.column))
    
    # Exit a parse tree produced by DecafParser#ifStatement.
    def exitIfStatement(self, ctx:DecafParser.IfStatementContext):
        self.exitScope()
    
    # Enter a parse tree produced by DecafParser#elseStatement.
    def enterElseStatement(self, ctx:DecafParser.ElseStatementContext):
        self.enterScope("else" + str(self.elseCount))
        self.elseCount = self.elseCount + 1

    # Exit a parse tree produced by DecafParser#elseStatement.
    def exitElseStatement(self, ctx:DecafParser.ElseStatementContext):
        self.exitScope()

    # Enter a parse tree produced by DecafParser#whileStatement.
    def enterWhileStatement(self, ctx:DecafParser.WhileStatementContext):
        try:
            expressionCtx = ctx.expression()
            expressionType = utils.getExpressionType(expressionCtx, self.varSymbolTable, self.methodSymbolTable, self.structSymbolTable, self.getScopes())
            self.enterScope("while" + str(self.whileCount))
            self.whileCount = self.whileCount + 1
            if expressionType != 'boolean':
                raise WhileExpressionIsNotBoolean
        except WhileExpressionIsNotBoolean:
            self.errorList.append("WhileExpressionIsNotBoolean at line %d:%d While expression is not of type boolean" % (ctx.start.line, ctx.start.column))
            print("WhileExpressionIsNotBoolean at line %d:%d While expression is not of type boolean" % (ctx.start.line, ctx.start.column))
    
    # Exit a parse tree produced by DecafParser#whileStatement.
    def exitWhileStatement(self, ctx:DecafParser.WhileStatementContext):
        self.exitScope()

    # Enter a parse tree produced by DecafParser#location.
    def enterLocation(self, ctx:DecafParser.LocationContext):
        scopes = self.getScopes()
        try:
            parentCtx = ctx.parentCtx
            idCtx = ctx.ID()
            expressionCtx = ctx.expression()
            if expressionCtx != None:
                # Verifica si el ID es de tipo array
                varId = idCtx.getText()
                if str(type(parentCtx)) == "<class 'DecafParser.DecafParser.LocationContext'>": # Si el padre es un struct
                    parentVarId = parentCtx.ID().getText()
                    parentVarItem = None
                    for i in reversed(range(0, len(scopes))):
                        scope = scopes[i]
                        parentVarItem = utils.getVarItemInScope(self.varSymbolTable, parentVarId, scope)
                        if parentVarItem != None:
                            break
                    
                    if parentVarItem == None:
                        raise VariableNotDeclared
                    
                    structId = parentVarItem.varType.replace('struct', '', 1)
                    
                    structItem = utils.getStructItem(self.structSymbolTable, structId, varId)

                    if structItem == None:
                        raise VariableNotDeclared
                    
                    if not structItem.isArray:
                        raise VarIsNotArray

                else: # Si es una variable
                    varItem = None
                    for i in reversed(range(0, len(scopes))):
                        scope = scopes[i]
                        varItem = utils.getVarItemInScope(self.varSymbolTable, varId, scope)
                        if varItem != None:
                            break
                    
                    if varItem == None:
                        raise VariableNotDeclared
                    
                    if not varItem.isArray:
                        raise VarIsNotArray
                
                # Verifica si la expression es de tipo int
                expressionType = utils.getExpressionType(expressionCtx, self.varSymbolTable, self.methodSymbolTable, self.structSymbolTable, self.getScopes())
                
                if expressionType != 'int':
                    raise ExpressionIsNotInt

        except VarIsNotArray:
            self.errorList.append("VarIsNotArray at line %d:%d Variable is not declared as an array" % (ctx.start.line, ctx.start.column))
            print("VarIsNotArray at line %d:%d Variable is not declared as an array" % (ctx.start.line, ctx.start.column))
        except VariableNotDeclared:
            self.errorList.append("VariableNotDeclared at line %d:%d Variable is not declared." % (ctx.start.line, ctx.start.column))
            print("VariableNotDeclared at line %d:%d Variable is not declared." % (ctx.start.line, ctx.start.column))
        except ExpressionIsNotInt:
            self.errorList.append("ExpressionIsNotInt at line %d:%d Expression inside '[' ']' is not of type int." % (ctx.start.line, ctx.start.column))
            print("ExpressionIsNotInt at line %d:%d Expression inside '[' ']' is not of type int." % (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by DecafParser#expression.
    def enterExpression(self, ctx:DecafParser.ExpressionContext):
        expressionNumberError = 1
        try:
            # Si se tiene un arith_op_third
            if ctx.arith_op_third() != None:
                # Si es operando == o !=
                if ctx.arith_op_third().getText() == '==' or ctx.arith_op_third().getText() == '!=':
                    expression1 = ctx.getChild(0)
                    expression2 = ctx.getChild(2)

                    expression1Type = utils.getExpressionType(expression1, self.varSymbolTable, self.methodSymbolTable, self.structSymbolTable, self.getScopes())
                    expression2Type = utils.getExpressionType(expression2, self.varSymbolTable, self.methodSymbolTable, self.structSymbolTable, self.getScopes())

                    if expression1Type == None:
                        expressionNumberError = 1
                        raise ExpressionDoesNotExist
                    if expression2Type == None:
                        expressionNumberError = 2
                        raise ExpressionDoesNotExist
                    
                    if expression1Type != 'boolean' and expression1Type != 'char' and expression1Type != 'int':
                        expressionNumberError = 1
                        raise ExpressionMustBeType
                    if expression2Type != 'boolean' and expression1Type != 'char' and expression1Type != 'int':
                        expressionNumberError = 2
                        raise ExpressionMustBeType
                    
                    if expression1Type != expression2Type:
                        raise EqualOpType
                # Si el operando es < <= > >=
                else:
                    expression1 = ctx.getChild(0)
                    expression2 = ctx.getChild(2)

                    expression1Type = utils.getExpressionType(expression1, self.varSymbolTable, self.methodSymbolTable, self.structSymbolTable, self.getScopes())
                    expression2Type = utils.getExpressionType(expression2, self.varSymbolTable, self.methodSymbolTable, self.structSymbolTable, self.getScopes())

                    if expression1Type == None:
                        expressionNumberError = 1
                        raise ExpressionDoesNotExist
                    if expression2Type == None:
                        expressionNumberError = 2
                        raise ExpressionDoesNotExist
                    
                    if expression1Type != 'int':
                        raise ExpressionIsNotInt
                    if expression1Type != 'int':
                        raise ExpressionIsNotInt


            
            # Si operando es !
            if ctx.getChild(0).getText() == '!':
                expressionCtx = ctx.expression()
                expressionType = utils.getExpressionType(expressionCtx, self.varSymbolTable, self.methodSymbolTable, self.structSymbolTable, self.getScopes())

                if expressionType != 'boolean':
                    raise ExpressionIsNotBoolean

            # Si operandos son && o ||
            if ctx.arith_op_second() != None or ctx.arith_op_first() != None:
                expression1 = ctx.getChild(0)
                expression2 = ctx.getChild(2)

                expression1Type = utils.getExpressionType(expression1, self.varSymbolTable, self.methodSymbolTable, self.structSymbolTable, self.getScopes())
                expression2Type = utils.getExpressionType(expression2, self.varSymbolTable, self.methodSymbolTable, self.structSymbolTable, self.getScopes())

                if expression1Type == None:
                    expressionNumberError = 1
                    raise ExpressionDoesNotExist
                if expression2Type == None:
                    expressionNumberError = 2
                    raise ExpressionDoesNotExist
                
                if expression1Type != 'boolean':
                    raise ExpressionIsNotBoolean
                if expression2Type != 'boolean':
                    raise ExpressionIsNotBoolean
            
            # Si operando es -
            if ctx.getChild(0).getText() == '-':
                expressionCtx = ctx.expression()
                expressionType = utils.getExpressionType(expressionCtx, self.varSymbolTable, self.methodSymbolTable, self.structSymbolTable, self.getScopes())

                if expressionType != 'int':
                    raise ExpressionIsNotInt

            # Si operandos son + o -
            if ctx.arith_op_fourth() != None:
                expression1 = ctx.getChild(0)
                expression2 = ctx.getChild(2)

                expression1Type = utils.getExpressionType(expression1, self.varSymbolTable, self.methodSymbolTable, self.structSymbolTable, self.getScopes())
                expression2Type = utils.getExpressionType(expression2, self.varSymbolTable, self.methodSymbolTable, self.structSymbolTable, self.getScopes())

                if expression1Type == None:
                    expressionNumberError = 1
                    raise ExpressionDoesNotExist
                if expression2Type == None:
                    expressionNumberError = 2
                    raise ExpressionDoesNotExist
                
                if expression1Type != 'int':
                    raise ExpressionIsNotInt
                if expression2Type != 'int':
                    raise ExpressionIsNotInt
                
        except ExpressionDoesNotExist:
            self.errorList.append("ExpressionDoesNotExist at line %d:%d Something in the expression %d does not exist in the local context" % (ctx.start.line, ctx.start.column, expressionNumberError))
            print("ExpressionDoesNotExist at line %d:%d Something in the expression %d does not exist in the local context" % (ctx.start.line, ctx.start.column, expressionNumberError))
        except ExpressionMustBeType:
            self.errorList.append("ExpressionMustBeType at line %d:%d Expression %d must be 'char', 'int' or 'boolean'" % (ctx.start.line, ctx.start.column, expressionNumberError))
            print("ExpressionMustBeType at line %d:%d Expression %d must be 'char', 'int' or 'boolean'" % (ctx.start.line, ctx.start.column, expressionNumberError))
        except EqualOpType:
            self.errorList.append("EqualOpType at line %d:%d Expressions types are not the same in equal operand" % (ctx.start.line, ctx.start.column))
            print("EqualOpType at line %d:%d Expressions types are not the same in equal operand" % (ctx.start.line, ctx.start.column))
        except ExpressionIsNotBoolean:
            self.errorList.append("ExpressionIsNotBoolean at line %d:%d Expression must be boolean" % (ctx.start.line, ctx.start.column))
            print("ExpressionIsNotBoolean at line %d:%d Expression must be boolean" % (ctx.start.line, ctx.start.column))
        except ExpressionIsNotInt:
            self.errorList.append("ExpressionIsNotInt at line %d:%d Expression must be int" % (ctx.start.line, ctx.start.column))
            print("ExpressionIsNotInt at line %d:%d Expression must be int" % (ctx.start.line, ctx.start.column))

    # Enter a parse tree produced by DecafParser#methodCall.
    def enterMethodCall(self, ctx:DecafParser.MethodCallContext):
        methodId = ctx.ID().getText()
        argNameError = ''
        argTypeError = ''
        paramTypeError = ''
        try:
            # Valida si el metodo existe en la tabla de simbolos
            exists = utils.doesMethodExists(methodSymbolTable=self.methodSymbolTable, methodId=methodId)
            if not exists:
                raise MethodNotDeclared
            
            # Obtiene los tipos de los argumentos del metodo llamado
            methodParams = utils.getMethodParams(self.varSymbolTable, methodId)
            methodArguments = utils.getMethodCallArgumentsTypes(ctx, self.varSymbolTable, self.methodSymbolTable, self.structSymbolTable, self.getScopes())

            if len(methodParams) != len(methodArguments):
                raise MethodCallArgumentsDoesNotMatchDeclaration
            
            for i in range(len(methodParams)):
                methodParam = methodParams[i]
                methodArgument = methodArguments[i]

                if methodParam.varType != methodArgument['argType']:
                    argNameError = methodArgument['argId']
                    argTypeError = methodArgument['argType']
                    paramTypeError = methodParam.varType
                    raise MethodCallArgumentTypeError


        except MethodNotDeclared:
            self.errorList.append("MethodNotDeclared at line %d:%d Method '%s' is not declared" % (ctx.start.line, ctx.start.column, methodId))
            print("MethodNotDeclared at line %d:%d Method '%s' is not declared" % (ctx.start.line, ctx.start.column, methodId))
        except MethodCallArgumentsDoesNotMatchDeclaration:
            self.errorList.append("MethodCallArgumentsDoesNotMatchDeclaration at line %d:%d Method call '%s' does not have the correct amount of arguments" % (ctx.start.line, ctx.start.column, methodId))
            print("MethodCallArgumentsDoesNotMatchDeclaration at line %d:%d Method call '%s' does not have the correct amount of arguments" % (ctx.start.line, ctx.start.column, methodId))
        except MethodCallArgumentTypeError:
            self.errorList.append("MethodCallArgumentTypeError at line %d:%d Method call argument '%s' type is '%s', and the method declaration '%s' positioned parameter is of type '%s'" % (ctx.start.line, ctx.start.column, argNameError, argTypeError, methodId, paramTypeError))
            print("MethodCallArgumentTypeError at line %d:%d Method call argument '%s' type is '%s', and the method declaration '%s' positioned parameter is of type '%s'" % (ctx.start.line, ctx.start.column, argNameError, argTypeError, methodId, paramTypeError))
        
        return super().enterMethodCall(ctx)
    
    # --------------------------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------#
    # Funciones de cambio de estado
    def getScopes(self):
        scopes = self.scopes
        return scopes

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
            self.errorList.append("Variable %s is already declared." % item.varId)
            print("Variable %s is already declared." % item.varId)

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
            self.errorList.append("Method %s is already declared." % item.methodId)
            print("Method %s is already declared." % item.methodId)

    def addToStructSymbolTable(self, item: StructSymbolTableItem):
        try:
            if self.structSymbolTable.count == 0:
                self.structSymbolTable.append(item)
            else:
                exists = False
                for i in self.structSymbolTable:
                    if item.structId == i.structId and item.varId == i.varId:
                        exists = True

                if not exists:
                    self.structSymbolTable.append(item)
                else:
                    raise ExistingItem
                    
        except ExistingItem:
            self.errorList.append("Struct var %s is already declared." % item.structId)
            print("Struct var %s is already declared." % item.structId)

#---------------------------------------------------------------------------------------------------

def main(argv):
    try:
        input_stream = FileStream(argv[1])
        lexer = DecafLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = DecafParser(stream)
        myErrorListener = MyErrorListener()
        parser.addErrorListener(myErrorListener)
        tree = parser.program()  
        printer = DecafPrinter()
        walker = ParseTreeWalker()
        walker.walk(printer, tree)
    except AttributeError as e:
        print(e)
    except Exception as e:
        print(e)
    
    for error in myErrorListener.getErrorsList():
        print(error)

def compile_file(filePath):
    try:
        input_stream = FileStream(filePath)
        lexer = DecafLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = DecafParser(stream)
        myErrorListener = MyErrorListener()
        parser.addErrorListener(myErrorListener)
        tree = parser.program()  
        printer = DecafPrinter()
        walker = ParseTreeWalker()
        walker.walk(printer, tree)
        return printer.errorList + myErrorListener.getErrorsList()
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

