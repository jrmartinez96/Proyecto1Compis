from PyDecaf import MethodSymbolTableItem, VarSymbolTableItem
from typing import List
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