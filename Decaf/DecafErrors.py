from antlr4.error.ErrorListener import ErrorListener

class MyErrorListener( ErrorListener ):
    
    def __init__(self):
        self.errorsList = []
        super(MyErrorListener, self).__init__()
    
    def addErrorList(self, line, column, msg):
        self.errorsList.append("line %d:%d %s" % (line, column, msg))

    def getErrorsList(self):
        return self.errorsList

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.addErrorList(line, column, msg)

class Error(Exception):
    """Base class for other exceptions"""
    pass

class ArraySizeError(Error):
    pass

class VoidReturnError(Error):
    pass

class ReturnEmpty(Error):
    pass

class ReturnNotEmpty(Error):
    pass

class ReturnMissing(Error):
    pass

class ReturnType(Error):
    pass

class ExistingItem(Error):
    pass

class MainNotFound(Error):
    pass

class MainHasParameters(Error):
    pass

class MethodNotDeclared(Error):
    pass

class MethodCallArgumentsDoesNotMatchDeclaration(Error):
    pass

class MethodCallArgumentTypeError(Error):
    pass

class IfExpressionIsNotBoolean(Error):
    pass

class WhileExpressionIsNotBoolean(Error):
    pass

class VariableNotDeclared(Error):
    pass

class ExpressionDoesNotExist(Error):
    pass

class AssignmentType(Error):
    pass

class ExpressionMustBeType(Error):
    pass

class EqualOpType(Error):
    pass

class ExpressionIsNotBoolean(Error):
    pass

class ExpressionIsNotInt(Error):
    pass

class VarIsNotArray(Error):
    pass