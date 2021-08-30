from PyDecaf import MethodSymbolTableItem, VarSymbolTableItem, StructSymbolTableItem
import DecafParser
from typing import List
# Solicita una variable a partir de su id
def getVarItemInScope(varSymbolTable: List[VarSymbolTableItem], varId: str, scope: str):
    returnItem = None

    for item in varSymbolTable:
        if item.varId == varId and item.scope == scope:
            returnItem = item
    
    return returnItem

# Solicita un metodo a partir de su id
def getMethodItem(methodSymbolTable: List[MethodSymbolTableItem], methodId: str):
    returnItem = None

    for item in methodSymbolTable:
        if item.methodId == methodId:
            returnItem = item
    
    return returnItem

def getStructItem(structSymbolTable: List[StructSymbolTableItem], structId: str, varId: str):
    returnItem = None

    for item in structSymbolTable:
        if item.structId == structId and item.varId == varId:
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
def getExpressionType(ctx: DecafParser.DecafParser.ExpressionContext, varSymbolTable: List[VarSymbolTableItem], methodSymbolTable: List[MethodSymbolTableItem], structSymbolTable: List[StructSymbolTableItem], scopes: List[str]):
    
    expressionChild = ctx.getChild(0)
    expressionChildType = str(type(expressionChild))

    if ctx.location() != None:
        return getLocationType(expressionChild, varSymbolTable, structSymbolTable, scopes, False, '')
    elif ctx.methodCall() != None:
        return getMethodCallType(expressionChild, methodSymbolTable)
    elif ctx.literal()!=None:
        return getLiteralType(expressionChild)
    elif expressionChildType == "<class 'DecafParser.DecafParser.ExpressionContext'>":
        if ctx.arith_op_third() != None or ctx.arith_op_second() != None or ctx.arith_op_first() != None:
            return 'boolean'
        
        if ctx.arith_op_fifth() != None or ctx.arith_op_fourth() != None:
            return 'int'

        return getExpressionType(expressionChild, varSymbolTable, methodSymbolTable, structSymbolTable, scopes)
    else:
        if expressionChild.getText() == '!':
            return 'boolean'
        
        if expressionChild.getText() == '-':
            return 'int'

        expressionChild = ctx.getChild(1)
        return getExpressionType(expressionChild, varSymbolTable, methodSymbolTable, structSymbolTable, scopes)

# Solicita el tipo de una location
def getLocationType(ctx: DecafParser.DecafParser.LocationContext, varSymbolTable: List[VarSymbolTableItem], structSymbolTable: List[StructSymbolTableItem], scopes: List[str], isParentStruct: bool, structParentId: str):
    varId = ctx.ID().getText()

    if ctx.location() != None:
        structId = ''
        if isParentStruct:
            structItem = getStructItem(structSymbolTable, structParentId, varId)
            if structItem != None:
                structId = structItem.varType.replace('struct', '', 1)
        else:
            for i in reversed(range(0, len(scopes))):
                scope = scopes[i]
                varItem = getVarItemInScope(varSymbolTable, varId, scope)
                if varItem != None:
                    structId = varItem.varType.replace('struct', '', 1)
                    break
        
        return getLocationType(ctx.location(), varSymbolTable, structSymbolTable, scopes, True, structId)
    else:
        if isParentStruct:
            structItem = getStructItem(structSymbolTable, structParentId, varId)
            if structItem != None:
                return structItem.varType
        else:
            for i in reversed(range(0, len(scopes))):
                scope = scopes[i]
                varItem = getVarItemInScope(varSymbolTable, varId, scope)
                if varItem != None:
                    if 'struct' in varItem.varType:
                        return varItem.varType.replace('struct', '', 1)
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
        return 'boolean'
    
    return None
    
# Solicita los tipos de los argumentos de MethodCall, retorna una lista con los tipos de los argumentos
def getMethodCallArgumentsTypes(ctx: DecafParser.DecafParser.MethodCallContext, varSymbolTable: List[VarSymbolTableItem], methodSymbolTable: List[MethodSymbolTableItem], structSymbolTable: List[StructSymbolTableItem], scopes: List[str]):
    argumentsTypes = []
    arg1Ctx = ctx.arg1()

    if arg1Ctx != None:
        argumentsTypes = getArg1ArgumentsTypes(arg1Ctx, varSymbolTable, methodSymbolTable, structSymbolTable, scopes)
    
    return argumentsTypes

# Solicita los tipos de los argumentos de arg1, retorna una lista con los tipos de los argumentos
def getArg1ArgumentsTypes(ctx: DecafParser.DecafParser.Arg1Context, varSymbolTable: List[VarSymbolTableItem], methodSymbolTable: List[MethodSymbolTableItem], structSymbolTable: List[StructSymbolTableItem], scopes: List[str]):
    argumentsTypes = []
    arg2Ctx = ctx.arg2()

    if arg2Ctx != None:
        argumentsTypes = getArg2ArgumentsTypes(arg2Ctx, varSymbolTable, methodSymbolTable, structSymbolTable, scopes)
    
    return argumentsTypes

# Solicita los tipos de los argumentos de arg2, retorna una lista con los tipos de los argumentos
def getArg2ArgumentsTypes(ctx: DecafParser.DecafParser.Arg2Context, varSymbolTable: List[VarSymbolTableItem], methodSymbolTable: List[MethodSymbolTableItem], structSymbolTable: List[StructSymbolTableItem], scopes: List[str]):
    argumentsTypes = []
    children = ctx.children

    for child in children:
        childType = str(type(child))
        if childType == "<class 'DecafParser.DecafParser.ArgContext'>":
            argType = getArgType(child, varSymbolTable, methodSymbolTable, structSymbolTable, scopes)
            argumentsTypes.append({"argId": child.getText(), "argType": argType}) # Si argType es None entonces no existe en la tabla de simbolos

    return argumentsTypes
            
    

# Solicita los tipos de los argumentos de arg, retorna una string con el tipo del argumento
def getArgType(ctx: DecafParser.DecafParser.ArgContext, varSymbolTable: List[VarSymbolTableItem], methodSymbolTable: List[MethodSymbolTableItem], structSymbolTable: List[StructSymbolTableItem], scopes: List[str]):
    expressionContext = ctx.expression()
    if expressionContext != None:
        return getExpressionType(expressionContext, varSymbolTable, methodSymbolTable, structSymbolTable, scopes)
    
    return None
