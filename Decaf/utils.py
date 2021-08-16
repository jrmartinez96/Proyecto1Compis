from PyDecaf import MethodSymbolTableItem, VarSymbolTableItem
import DecafParser
from typing import List
# Solicita una variable a partir de su id
def getVarItem(varSymbolTable: List[VarSymbolTableItem], varId: str):
    returnItem = None

    for item in varSymbolTable:
        if item.varId == varId:
            returnItem = item
    
    return returnItem

# Solicita un metodo a partir de su id
def getMethodItem(methodSymbolTable: List[MethodSymbolTableItem], methodId: str):
    returnItem = None

    for item in methodSymbolTable:
        if item.methodId == methodId:
            returnItem = item
    
    return returnItem

# Solicita los parametros de un metido, Retorna una lista de tipo VarSymbolTableItem
def getMethodParams(varSymbolTable: List[VarSymbolTableItem], methodId: str):
    params = []

    for item in varSymbolTable:
        if item.scope == methodId and item.isParam:
            params.append(item)
    
    return params

# Solicita si existe el metido en la tabla de simbolos
def doesMethodExists(methodSymbolTable: List[MethodSymbolTableItem], methodId: str):
    exists = False

    for item in methodSymbolTable:
        if item.methodId == methodId:
            exists = True
    
    return exists

# Solicita el tipo de una expresion
def getExpressionType(ctx: DecafParser.DecafParser.ExpressionContext, varSymbolTable: List[VarSymbolTableItem], methodSymbolTable: List[MethodSymbolTableItem]):
    
    expressionChild = ctx.getChild(0)
    expressionChildType = str(type(expressionChild))

    if expressionChildType == "<class 'DecafParser.DecafParser.LocationContext'>":
        return getLocationType(expressionChild, varSymbolTable)
    elif expressionChildType == "<class 'DecafParser.DecafParser.MethodCallContext'>":
        return getMethodCallType(expressionChild, methodSymbolTable)
    elif expressionChildType == "<class 'DecafParser.DecafParser.LiteralContext'>":
        return getLiteralType(expressionChild)
    elif expressionChildType == "<class 'DecafParser.DecafParser.ExpressionContext'>":
        return getExpressionType(expressionChild, varSymbolTable, methodSymbolTable)
    else:
        expressionChild = ctx.getChild(1)
        return getExpressionType(expressionChild, varSymbolTable, methodSymbolTable)

# Solicita el tipo de una location
def getLocationType(ctx: DecafParser.DecafParser.LocationContext, varSymbolTable: List[VarSymbolTableItem]):
    varId = ctx.getChild(0).getText()

    varItem = getVarItem(varSymbolTable, varId)
    if varItem != None:
        return varItem.varType
    
    return None

# Solicita el tipo de un method call
def getMethodCallType(ctx: DecafParser.DecafParser.MethodCallContext, methodSymbolTable: List[MethodSymbolTableItem]):
    methodId = ctx.getChild(0).getText()

    methodItem = getMethodItem(methodSymbolTable, methodId)
    if methodItem != None:
        return methodItem.methodType
    
    return None

# Solicita el tipo de un literal
def getLiteralType(ctx: DecafParser.DecafParser.LiteralContext):
    literalChild = ctx.getChild(0)
    literalChildType = str(type(literalChild))

    if literalChildType == "<class 'DecafParser.DecafParser.Int_literalContext'>":
        return 'int'
    elif literalChildType == "<class 'DecafParser.DecafParser.Char_literalContext'>":
        return 'char'
    elif literalChildType == "<class 'DecafParser.DecafParser.Bool_literalContext'>":
        return 'bool'
    
    return None
    