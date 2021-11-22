
from DecafParser import DecafParser
from DecafListener import DecafListener
import DecafErrors
import utils

class AssignationInstruction():
    def __init__(self, assignTo: str = '', operand1: str = '', operator: str = '', operand2: str = '', goToLabel: str = ''):
        self.assignTo = assignTo
        self.operand1 = operand1
        self.operator = operator
        self.operand2 = operand2
        self.goToLabel = goToLabel

class CopyAssignationInstruction():
    def __init__(self, assignTo: str, operand1: str, goToLabel: str = ''):
        self.assignTo = assignTo
        self.operand1 = operand1
        self.goToLabel = goToLabel

class CopyAssignationIndexInstruction():
    def __init__(self, assignTo: str, operand1: str, index: str, isAssignToItem: bool = False, goToLabel: str = ''):
        self.assignTo = assignTo
        self.operand1 = operand1
        self.index = index
        self.isAssignToItem = isAssignToItem
        self.goToLabel = goToLabel

class UnaryAssignationInstruction():
    def __init__(self, assignTo: str, operand1: str, operator: str, goToLabel: str = ''):
        self.assignTo = assignTo
        self.operand1 = operand1
        self.operator = operator
        self.goToLabel = goToLabel

class InconditionalJumpInstruction():
    def __init__(self, label: str, goToLabel: str = ''):
        self.label = label
        self.goToLabel = goToLabel

class ConditionalJumpInstruction():
    def __init__(self, label: str, condition: str, isIfFalse: bool = False, goToLabel: str = ''):
        self.label = label
        self.isIfFalse = isIfFalse
        self.condition = condition
        self.goToLabel = goToLabel
        
class ConditionalRelopJumpInstruction():
    def __init__(self, label: str, operand1: str, operand2: str, relop: str, goToLabel: str = ''):
        self.label = label
        self.operand1 = operand1
        self.operand2 = operand2
        self.relop = relop
        self.goToLabel = goToLabel

class ProcedureParamInstrunction():
    def __init__(self, param: str = '', base: int = 0, goToLabel: str = ''):
        self.param = param
        self.goToLabel = goToLabel
        self.base = base
        

class ProcedureInstruction():
    def __init__(self, procedure: str, params: list, goToLabel: str = ''):
        self.procedure = procedure
        self.params = params
        self.goToLabel = goToLabel

class LabelInstruction():
    def __init__(self, label:str):
        self.label = label

class FuncDeclarationBeginInstruction():
    def __init__(self, name:str):
        self.name = name

class FuncDeclarationEndInstruction():
    def __init__(self):
        pass

class FuncReturnInstruction():
    def __init__(self, variable:str = ''):
        self.variable = variable

class ThreeAddressInstruction():
    def __init__(self,
                 # Instrucciones de asignacion
                 assignationInstruction: AssignationInstruction = None, 
                 copyAssignationInstruction: CopyAssignationInstruction = None,
                 copyAssignationIndexInstruction: CopyAssignationIndexInstruction = None,
                 unaryAssignationInstruction: UnaryAssignationInstruction = None,
                 # Instrucciones de saltos
                 inconditionalJumpInstruction: InconditionalJumpInstruction = None,
                 conditionalJumpInstruction: ConditionalJumpInstruction = None,
                 conditionalRelopJumpInstruction: ConditionalRelopJumpInstruction = None,
                 # Instrucciones de procedures
                 paramInstrunction: ProcedureParamInstrunction = None,
                 procedureInstruction: ProcedureInstruction = None,
                 # Instruccion de label
                 labelInstruction: LabelInstruction = None,
                 # Func declaration
                 funcDeclarationBeginInstruction: FuncDeclarationBeginInstruction = None,
                 funcDeclarationEndInstruction: FuncDeclarationEndInstruction = None,
                 funcReturnInstruction: FuncReturnInstruction = None
                 ):
        self.assignationInstruction = assignationInstruction
        self.copyAssignationInstruction = copyAssignationInstruction
        self.copyAssignationIndexInstruction = copyAssignationIndexInstruction
        self.unaryAssignationInstruction = unaryAssignationInstruction
        self.inconditionalJumpInstruction = inconditionalJumpInstruction
        self.conditionalJumpInstruction = conditionalJumpInstruction
        self.conditionalRelopJumpInstruction = conditionalRelopJumpInstruction
        self.paramInstrunction = paramInstrunction
        self.procedureInstruction = procedureInstruction
        self.labelInstruction = labelInstruction
        self.funcDeclarationBeginInstruction = funcDeclarationBeginInstruction
        self.funcDeclarationEndInstruction = funcDeclarationEndInstruction
        self.funcReturnInstruction = funcReturnInstruction
    
    def toString(self):
        line = ''
        if self.assignationInstruction != None:
            a = self.assignationInstruction
            line = "%s = %s %s %s" % (a.assignTo, a.operand1, a.operator, a.operand2)
            if a.goToLabel != '':
                line = '%s: ' % (a.goToLabel) + line
            else:
                line = "\t" + line
        
        elif self.copyAssignationInstruction != None:
            a = self.copyAssignationInstruction
            line = "%s = %s" % (a.assignTo, a.operand1)
            if a.goToLabel != '':
                line = '%s: ' % (a.goToLabel) + line
            else:
                line = "\t" + line
            
        elif self.copyAssignationIndexInstruction != None:
            a = self.copyAssignationIndexInstruction
            line = ''
            if a.isAssignToItem:
                line = "%s[%s] = %s" % (a.assignTo, str(a.index), a.operand1)
            else:
                line = "%s = %s[%s]" % (a.assignTo, a.operand1, str(a.index))

            if a.goToLabel != '':
                line = '%s: ' % (a.goToLabel) + line
            else:
                line = "\t" + line
            
        elif self.unaryAssignationInstruction != None:
            a = self.unaryAssignationInstruction
            line = "%s = %s%s" % (a.assignTo, a.operator, a.operand1)
            if a.goToLabel != '':
                line = '%s: ' % (a.goToLabel) + line
            else:
                line = "\t" + line
            
        elif self.inconditionalJumpInstruction != None:
            a = self.inconditionalJumpInstruction
            line = "goto %s" % (a.label)
            if a.goToLabel != '':
                line = '%s: ' % (a.goToLabel) + line
            else:
                line = "\t" + line
            
        elif self.conditionalJumpInstruction != None:
            a = self.conditionalJumpInstruction
            line = ''
            if not a.isIfFalse:
                line = "if %s goto %s" % (a.condition, a.label)
            else:
                line = "ifFalse %s goto %s" % (a.condition, a.label)
            
            if a.goToLabel != '':
                line = '%s: ' % (a.goToLabel) + line
            else:
                line = "\t" + line
            
        elif self.conditionalRelopJumpInstruction != None:
            a = self.conditionalRelopJumpInstruction
            line = "if %s %s %s goto %s" % (a.operand1, a.relop, a.operand2, a.label) 
            if a.goToLabel != '':
                line = '%s: ' % (a.goToLabel) + line
            else:
                line = "\t" + line
            
        elif self.paramInstrunction != None:
            a = self.paramInstrunction
            line = "param %s" % (a.param)
            if a.goToLabel != '':
                line = '%s: ' % (a.goToLabel) + line
            else:
                line = "\t" + line
        elif self.procedureInstruction != None:
            a = self.procedureInstruction
            line = "call %s, %s" % (a.procedure, str(len(a.params))) 
            if a.goToLabel != '':
                line = '%s: ' % (a.goToLabel) + line
            else:
                line = "\t" + line
            
        elif self.labelInstruction != None:
            a = self.labelInstruction
            line = "%s:" % (a.label)
        
        elif self.funcDeclarationBeginInstruction != None:
            a = self.funcDeclarationBeginInstruction
            line = "func begin %s" % (a.name)
        
        elif self.funcDeclarationEndInstruction != None:
            line = "func end"
        
        elif self.funcReturnInstruction != None:
            a = self.funcReturnInstruction
            line = "\treturn %s" % (a.variable)
    
        return line
        


#---------------------------------------------------------------------------------------------------

class IntermediateCode(DecafListener):
    def __init__(self, varSymbolTable, methodSymbolTable, structSymbolTable):
        # Scopes
        self.scopes = []
        self.ifCount = 0
        self.elseCount = 0
        self.whileCount = 0

        # labels
        self.temps = []
        self.temps_to_release = []
        self.last_temp = -1
        self.label_number = 0
        self.last_location_variable = ''
        self.las_location_variable_index = -1

        # Symbol table related
        self.varSymbolTable = varSymbolTable
        self.methodSymbolTable = methodSymbolTable
        self.structSymbolTable = structSymbolTable

        # Intermediate code
        self.lines = []

        super().__init__()

    def returnErrorList(self):
        return self.errorList
    
    # Enter a parse tree produced by DecafParser#program.
    def enterProgram(self, ctx:DecafParser.ProgramContext):
        self.enterScope('global')
    
    def exitProgram(self, ctx:DecafParser.ProgramContext):
        self.exitScope()

    def enterVarDeclaration(self, ctx: DecafParser.VarDeclarationContext):
        pass

    def enterMethodDeclaration(self, ctx: DecafParser.MethodDeclarationContext):
        method_name = ctx.ID().getText()
        a = ThreeAddressInstruction(funcDeclarationBeginInstruction=FuncDeclarationBeginInstruction(method_name))
        self.lines.append(a)
        self.enterScope(method_name)
        block_code = self.get_block_code(ctx.block())
        self.add_lines(block_code)

    # Exit a parse tree produced by DecafParser#methodDeclaration.
    def exitMethodDeclaration(self, ctx:DecafParser.MethodDeclarationContext):
        a = ThreeAddressInstruction(funcDeclarationEndInstruction=FuncDeclarationEndInstruction())
        self.lines.append(a)
        self.exitScope()
    
    # Enter a parse tree produced by DecafParser#parameter.
    def enterParameter(self, ctx:DecafParser.ParameterContext):
        pass

    def enterBlock(self, ctx: DecafParser.BlockContext):
        pass

    def enterStatement(self, ctx: DecafParser.StatementContext):
        pass
    
    def exitStatement(self, ctx: DecafParser.StatementContext):
        pass

        
    # Enter a parse tree produced by DecafParser#ifStatement.
    def enterIfStatement(self, ctx:DecafParser.IfStatementContext):
        pass
        
    # Exit a parse tree produced by DecafParser#ifStatement.
    def exitIfStatement(self, ctx:DecafParser.IfStatementContext):
        pass
    
    # Enter a parse tree produced by DecafParser#elseStatement.
    def enterElseStatement(self, ctx:DecafParser.ElseStatementContext):
        pass

    # Exit a parse tree produced by DecafParser#elseStatement.
    def exitElseStatement(self, ctx:DecafParser.ElseStatementContext):
        pass

    # Enter a parse tree produced by DecafParser#whileStatement.
    def enterWhileStatement(self, ctx:DecafParser.WhileStatementContext):
        pass
        
    # Exit a parse tree produced by DecafParser#whileStatement.
    def exitWhileStatement(self, ctx:DecafParser.WhileStatementContext):
        pass

    # Enter a parse tree produced by DecafParser#location.
    def enterLocation(self, ctx:DecafParser.LocationContext):
        pass
        
    # Enter a parse tree produced by DecafParser#expression.
    def enterExpression(self, ctx:DecafParser.ExpressionContext):
        pass
    # Enter a parse tree produced by DecafParser#methodCall.
    def enterMethodCall(self, ctx:DecafParser.MethodCallContext):
        pass

    # --------------------------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------#
    # --------------------------------------------------------------------------------------------------#
    # Gen Code
    def get_block_code(self, ctx:DecafParser.BlockContext):
        lines = []

        for child in ctx.children:
            if str(type(child)) == "<class 'DecafParser.DecafParser.StatementContext'>":
                statement_code = self.get_statement_code(child)
                lines = lines + statement_code

        return lines
    
    def get_statement_code(self, ctx:DecafParser.StatementContext):
        lines = []
        if ctx.location() != None:

            expression_code = self.get_expression_code(ctx.expression())
            lines = lines + expression_code
            last_expression_temp = self.get_last_temp()
            self.release_temps()

            location_code = self.get_location_code(ctx.location(), isLeftSide=True)
            lines = lines + location_code

            if self.las_location_variable_index != -1:
                lines.append(self.copy_assignation_index(self.last_location_variable, last_expression_temp, self.las_location_variable_index, isAssignToItem=True))
                self.las_location_variable_index = -1
            else: 
                lines.append(self.copy_assignation(self.last_location_variable, last_expression_temp))
        elif ctx.expression() != None:
            expression_code = self.get_expression_code(ctx.expression())
            lines = lines + expression_code
        elif ctx.methodCall() != None:
            method_call_code = self.get_method_call_code(ctx.methodCall())
            lines = lines + method_call_code
        elif ctx.whileStatement() != None:
            while_code = self.get_while_statement_code(ctx.whileStatement())
            lines = lines + while_code
        elif ctx.ifStatement() != None:
            ifCtx = ctx.ifStatement()
            elseCtx = ctx.elseStatement()
            if_else_code = self.get_if_else_statement_code(ifCtx, elseCtx)
            lines = lines + if_else_code
        elif ctx.block() != None:
            block_code = self.get_block_code(ctx.block())
            lines = lines + block_code
        elif ctx.expressionOom() != None:
            expressionOm_code = self.get_expressionOom_code(ctx.expressionOom())

            if len(expressionOm_code) == 0:
                a = ThreeAddressInstruction(funcReturnInstruction=FuncReturnInstruction())
                lines.append(a)
            else:
                lines = lines + expressionOm_code
                last_expressionOm_temp = self.get_last_temp()
                self.release_temps()
                a = ThreeAddressInstruction(funcReturnInstruction=FuncReturnInstruction(variable=last_expressionOm_temp))
                lines.append(a)
        
        return lines
    
    def get_while_statement_code(self, ctx:DecafParser.WhileStatementContext):
        lines = []

        start_label = self.new_label()
        end_label = self.new_label()

        lines.append(self.add_label(start_label))
        expression_code = self.get_expression_code(ctx.expression())
        last_expression_temp = self.get_last_temp()
        self.release_temps()

        lines = lines + expression_code
        lines.append(self.conditional_jump(end_label, last_expression_temp, isIfFalse=True))


        self.enterScope("while" + str(self.whileCount))
        self.whileCount = self.whileCount + 1

        block_code = self.get_block_code(ctx.block())
        lines = lines + block_code

        self.exitScope()

        lines.append(self.inconditional_jump(start_label))
        lines.append(self.add_label(end_label))

        return lines
    
    def get_if_else_statement_code(self, ifCtx: DecafParser.IfStatementContext, elseCtx: DecafParser.ElseStatementContext):
        lines = []

        if elseCtx == None:
            end_label = self.new_label()
            
            # Expression del if
            expression_code = self.get_expression_code(ifCtx.expression())
            last_expression_temp = self.get_last_temp()
            self.release_temps()

            lines = lines + expression_code

            # Codicional del if
            lines.append(self.conditional_jump(end_label, last_expression_temp, isIfFalse=True))

            # Block del code
            self.enterScope("if" + str(self.ifCount))
            self.ifCount = self.ifCount + 1

            block_code = self.get_block_code(ifCtx.block())
            lines = lines + block_code

            self.exitScope()

            # Label del end
            lines.append(self.add_label(end_label))
        else:
            else_label = self.new_label()
            end_label = self.new_label()

            # Expression de la condicional
            expression_code = self.get_expression_code(ifCtx.expression())
            last_expression_temp = self.get_last_temp()
            self.release_temps()

            lines = lines + expression_code

            lines.append(self.conditional_jump(else_label, last_expression_temp, isIfFalse=True))

            # Block del if
            self.enterScope("if" + str(self.ifCount))
            self.ifCount = self.ifCount + 1

            if_block_code = self.get_block_code(ifCtx.block())
            lines = lines + if_block_code
            lines.append(self.inconditional_jump(end_label))

            self.exitScope()

            # Label del else
            lines.append(self.add_label(else_label))

            # Block del else
            self.enterScope("else" + str(self.elseCount))
            self.elseCount = self.elseCount + 1

            else_block_code = self.get_block_code(elseCtx.block())
            lines = lines + else_block_code

            self.exitScope()

            # Label del end
            lines.append(self.add_label(end_label))
        return lines
    
    def get_expressionOom_code(self, ctx:DecafParser.ExpressionOomContext):
        lines = []

        if ctx.expression() != None:
            expression_code = self.get_expression_code(ctx.expression())
            lines = lines + expression_code

        return lines

    def get_expression_code(self, ctx:DecafParser.ExpressionContext):
        lines = []
        if ctx.literal() != None:
            temp = self.new_temp()
            lines.append(self.copy_assignation(temp, ctx.literal().getText()))
        elif ctx.location() != None:
            location_code = self.get_location_code(ctx.location())
            lines = lines + location_code
        elif ctx.methodCall() != None:
            method_call_code = self.get_method_call_code(ctx.methodCall())
            lines = lines + method_call_code
        elif ctx.children[0].getText() == '-':
            expression_code = self.get_expression_code(ctx.expression())
            lines = lines + expression_code
            last_temp = self.get_last_temp()
            self.release_temps()
            temp_unary = self.new_temp()
            lines.append(self.unary_assignation(temp_unary, last_temp, "-"))
        elif ctx.children[0].getText() == '!':
            expression_code = self.get_expression_code(ctx.expression())
            lines = lines + expression_code
            last_temp = self.get_last_temp()
            self.release_temps()
            temp_unary = self.new_temp()
            lines.append(self.unary_assignation(temp_unary, last_temp, "!"))
        elif ctx.arith_op_first() != None:
            expression1 = ctx.children[0]
            expression2 = ctx.children[2]

            expression1_code = self.get_expression_code(expression1)
            last_temp1 = self.get_last_temp()
            self.release_temps()
            expression2_code = self.get_expression_code(expression2)
            last_temp2 = self.get_last_temp()
            self.release_temps()

            temp = self.new_temp()

            lines = lines + expression1_code + expression2_code
            lines.append(self.assignation(temp, last_temp1, last_temp2, '||'))
        elif ctx.arith_op_second() != None:
            expression1 = ctx.children[0]
            expression2 = ctx.children[2]

            expression1_code = self.get_expression_code(expression1)
            last_temp1 = self.get_last_temp()
            self.release_temps()
            expression2_code = self.get_expression_code(expression2)
            last_temp2 = self.get_last_temp()
            self.release_temps()

            temp = self.new_temp()

            lines = lines + expression1_code + expression2_code
            lines.append(self.assignation(temp, last_temp1, last_temp2, '&&'))
        elif ctx.arith_op_third() != None:
            expression1 = ctx.children[0]
            expression2 = ctx.children[2]

            expression1_code = self.get_expression_code(expression1)
            last_temp1 = self.get_last_temp()
            self.release_temps()
            expression2_code = self.get_expression_code(expression2)
            last_temp2 = self.get_last_temp()
            self.release_temps()

            temp = self.new_temp()

            lines = lines + expression1_code + expression2_code
            relop = ctx.children[1].getText()
            lines.append(self.assignation(temp, last_temp1, last_temp2, relop))
        elif ctx.arith_op_fourth() != None:
            expression1 = ctx.children[0]
            expression2 = ctx.children[2]

            expression1_code = self.get_expression_code(expression1)
            last_temp1 = self.get_last_temp()
            self.release_temps()
            expression2_code = self.get_expression_code(expression2)
            last_temp2 = self.get_last_temp()
            self.release_temps()

            temp = self.new_temp()

            lines = lines + expression1_code + expression2_code
            arith = ctx.children[1].getText()
            lines.append(self.assignation(temp, last_temp1, last_temp2, arith))
        elif ctx.arith_op_fifth() != None:
            if ctx.children[1].getText() == '*':
                expression1 = ctx.children[0]
                expression2 = ctx.children[2]
                
                expression1_code = self.get_expression_code(expression1)
                last_temp1 = self.get_last_temp()
                self.release_temps()
                expression2_code = self.get_expression_code(expression2)
                last_temp2 = self.get_last_temp()
                self.release_temps()
                lines = lines + expression1_code + expression2_code

                temp_count = self.new_temp()
                temp_addition = self.new_temp()
                temp_temp_count = self.new_temp()
                temp_temp_addition = self.new_temp()

                label = self.new_label()
                
                lines.append(self.copy_assignation(temp_count, '0'))
                lines.append(self.copy_assignation(temp_addition, '0'))
                lines.append(self.add_label(label))
                lines.append(self.assignation(temp_temp_addition, temp_addition, last_temp1, '+'))
                lines.append(self.copy_assignation(temp_addition, temp_temp_addition))
                lines.append(self.assignation(temp_temp_count, temp_count, '1', '+'))
                lines.append(self.copy_assignation(temp_count, temp_temp_count))
                lines.append(self.conditional_jump_relop(label, temp_count, last_temp2, '<'))
                temp_result = self.new_temp()
                lines.append(self.copy_assignation(temp_result, temp_addition))
            # TODO: Division y Modulo

        else:
            expression_code = self.get_expression_code(ctx.expression())
            lines = lines + expression_code
        
        return lines
    
    def get_location_code(self, ctx: DecafParser.LocationContext, parent_varType: str = None, isLeftSide: bool = False):
        lines = []

        parentCtx = ctx.parentCtx
        if str(type(parentCtx)) == "<class 'DecafParser.DecafParser.LocationContext'>":
            id = ctx.ID().getText()

            parent_varType = parent_varType.replace("struct", '')
            
            struct_items = utils.getStructItemsFromStructId(self.structSymbolTable, parent_varType)
            offset = 0
            struct_item = None
            for item in struct_items:
                if item.varId == id:
                    struct_item = item
                    break
                offset += item.size
            
            # Asignacion del offset
            temp = self.new_temp()
            lines.append(self.copy_assignation(temp, "%d" % (offset)))

            # Si hay array y location
            if ctx.expression() != None and ctx.location() != None:
                # Array
                expression_code = self.get_expression_code(ctx.expression())
                lines = lines + expression_code
                last_temp_expression = self.get_last_temp()
                self.release_temps()

                vss_temp = self.new_temp()
                var_singular_size = '%d' % (struct_item.size)
                lines.append(self.copy_assignation(vss_temp, var_singular_size))
                
                index_temp = self.new_temp()
                lines.append(self.assignation(index_temp, last_temp_expression, vss_temp, '*'))

                array_offset_temp = self.new_temp()
                lines.append(self.assignation(array_offset_temp, temp, index_temp, '+'))

                # Location
                location_code = self.get_location_code(ctx.location(), struct_item.varType)
                lines = lines + location_code
                last_temp_location = self.get_last_temp()
                self.release_temps()

                array_location_offset = self.new_temp()
                lines.append(self.assignation(array_location_offset, array_offset_temp, last_temp_location, '+'))
            
            # Si solo es array
            elif ctx.expression() != None:
                expression_code = self.get_expression_code(ctx.expression())
                lines = lines + expression_code
                last_temp_expression = self.get_last_temp()
                self.release_temps()

                vss_temp = self.new_temp()
                var_singular_size = '%d' % (struct_item.size)
                lines.append(self.copy_assignation(vss_temp, var_singular_size))
                
                index_temp = self.new_temp()
                lines.append(self.assignation(index_temp, last_temp_expression, vss_temp, '*'))

                array_offset_temp = self.new_temp()
                lines.append(self.assignation(array_offset_temp, temp, index_temp, '+'))
            
            # Si solo hay location
            elif ctx.location() != None:
                location_code = self.get_location_code(ctx.location(), struct_item.varType)
                lines = lines + location_code
                last_temp_location = self.get_last_temp()
                self.release_temps()

                final_offset = self.new_temp()
                lines.append(self.assignation(final_offset, offset, last_temp_location, '+'))
                
        else:
            id = ctx.ID().getText()

            item = utils.getVarItemInScopes(self.varSymbolTable, id, self.getScopes())

            id = "estatica[%d]" % (item.base)


            last_temp_expression = ''
            if ctx.expression() != None:
                expression_code = self.get_expression_code(ctx.expression())
                lines = lines + expression_code
                last_temp_expression = self.get_last_temp()
                # self.release_temps()
            
            last_temp_location = ''
            if ctx.location() != None:

                varItem = utils.getVarItemInScopes(self.varSymbolTable, id, self.getScopes())
                location_code = self.get_location_code(ctx.location(), varItem.varType)
                lines = lines + location_code
                last_temp_location = self.get_last_temp()
                self.release_temps()
            
            if last_temp_location != '' or last_temp_expression != '':
                if last_temp_expression != '' and last_temp_location != '':
                    vss_temp = self.new_temp()
                    var_singular_size = utils.getSingularVarSize(self.varSymbolTable, self.structSymbolTable, id, self.getScopes())
                    
                    lines.append(self.copy_assignation(vss_temp, '8'))
                    index_temp = self.new_temp()
                    lines.append(self.assignation(index_temp, last_temp_expression, vss_temp, '*'))

                    expression_location_temp = self.new_temp()
                    lines.append(self.assignation(expression_location_temp, index_temp, last_temp_location, '+'))

                    if isLeftSide:
                        self.last_location_variable = "%s" % (id)
                        if id.find('estatica[') != -1:
                            self.las_location_variable_index = expression_location_temp
                    else:
                        temp = self.new_temp()
                        lines.append(self.copy_assignation_index(temp, id, expression_location_temp))
                elif last_temp_expression != '':
                    vss_temp = self.new_temp()
                    var_singular_size = utils.getSingularVarSize(self.varSymbolTable, self.structSymbolTable, id, self.getScopes())
                    lines.append(self.copy_assignation(vss_temp, '8'))
                    
                    index_temp = self.new_temp()
                    lines.append(self.assignation(index_temp, last_temp_expression, vss_temp, '*'))
                    
                    if isLeftSide:
                        self.last_location_variable = "%s" % (id)
                        if id.find('estatica[') != -1:
                            self.las_location_variable_index = index_temp
                    else:
                        temp = self.new_temp()
                        lines.append(self.copy_assignation_index(temp, id, index_temp))
                elif last_temp_location != '':
                    if isLeftSide:
                        self.last_location_variable = "%s" % (id)
                        if id.find('estatica[') != -1:
                            self.las_location_variable_index = last_temp_location
                    else:
                        temp = self.new_temp()
                        lines.append(self.copy_assignation_index(temp, id, last_temp_location))
            else:
                if isLeftSide:
                    self.last_location_variable = "%s" % (id)
                else:
                    temp = self.new_temp()
                    lines.append(self.copy_assignation(temp, id))

        return lines
    
    def get_method_call_code(self, ctx: DecafParser.MethodCallContext):
        lines = []

        # Method
        id = ctx.ID().getText()
        params = []

        arg1 = ctx.arg1()
        if arg1 != None:
            arg2 = arg1.arg2()
            if arg2 != None:
                arg2_children = arg2.children
                for child in arg2_children:
                    if child.getText() != ',':
                        child_lines = self.get_expression_code(child.expression())
                        last_temp = self.get_last_temp()
                        self.release_temps()
                        lines = lines + child_lines
                        params.append(last_temp)
        
        methodParams = utils.getMethodParams(self.varSymbolTable, id)
        
        for i in range(len(params)):
            param = params[i]
            varSymbolItem = methodParams[i]
            base = varSymbolItem.base
            lines.append(self.procedure_param(param, base))

        lines.append(self.procedure(id, params))
        result_temp = self.new_temp()
        lines.append(self.copy_assignation(result_temp, 'result'))
        return lines
        
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

    def new_temp(self):
        isTempsFull = True
        free_index = -1
        
        for index in range(len(self.temps)):
            temp = self.temps[index]
            if temp == 0:
                isTempsFull = False
                free_index = index
                break
        
        temp_id = 0
        if isTempsFull:
            self.temps.append(1)
            temp_id = len(self.temps) - 1
        else:
            self.temps[free_index] = 1
            temp_id = free_index
        
        self.last_temp = temp_id
        self.temps_to_release.append(temp_id)
        return self.get_last_temp()
    
    def release_temps(self):
        temps = self.temps_to_release
        for temp_id in temps:
            for i in range(len(self.temps)):
                if i == temp_id and i != self.last_temp:
                    self.temps[i] = 0
                    
        # Vaciar temps del scope
        self.temps_to_release = [self.last_temp]
    
    def new_label(self):
        label_name = "L%d" % (self.label_number)
        self.label_number = self.label_number + 1
        return label_name
    
    def get_last_temp(self):
        return 't%d' %(self.last_temp)

    def add_lines(self, lines: list):
        for line in lines:
            self.lines.append(line)
    
    def assignation(self, result: str, arg1: str, arg2: str, op: str, gotoLabel: str = ''):
        a = AssignationInstruction(result, arg1, op, arg2, gotoLabel)
        line = ThreeAddressInstruction(assignationInstruction=a)
        return line
    
    def unary_assignation(self, result: str, arg1: str, op: str, gotoLabel: str = ''):
        a = UnaryAssignationInstruction(result, arg1, op, gotoLabel)
        line = ThreeAddressInstruction(unaryAssignationInstruction=a)
        return line
    
    def copy_assignation(self, result: str, arg1: str, gotoLabel: str = ''):
        a = CopyAssignationInstruction(result, arg1, gotoLabel)
        line = ThreeAddressInstruction(copyAssignationInstruction=a)
        return line
    
    def inconditional_jump(self, label: str, gotoLabel: str = ''):
        a = InconditionalJumpInstruction(label, gotoLabel)
        line = ThreeAddressInstruction(inconditionalJumpInstruction=a)
        return line
    
    def conditional_jump(self, label: str, x: str, isIfFalse: bool = False, gotoLabel: str = ''):
        a = ConditionalJumpInstruction(label, x, isIfFalse, gotoLabel)
        line = ThreeAddressInstruction(conditionalJumpInstruction=a)

        return line

    def conditional_jump_relop(self, label: str, x: str, y: str, relop: str, gotoLabel: str = ''):
        a = ConditionalRelopJumpInstruction(label, x, y, relop, gotoLabel)
        line = ThreeAddressInstruction(conditionalRelopJumpInstruction=a)
        return line

    def procedure_param(self, param: str, base: int, gotoLabel: str = ''):
        a = ProcedureParamInstrunction(param, base, gotoLabel)
        line = ThreeAddressInstruction(paramInstrunction=a)
        return line

    def procedure(self, procedure: str, params: list, gotoLabel: str = ''):
        a = ProcedureInstruction(procedure, params, gotoLabel)
        line = ThreeAddressInstruction(procedureInstruction=a)
        return line

    def copy_assignation_index(self, result: str, x: str, index: str, isAssignToItem: bool = False, gotoLabel: str = ''):
        a = CopyAssignationIndexInstruction(result, x, index, isAssignToItem, gotoLabel)
        line = ThreeAddressInstruction(copyAssignationIndexInstruction=a)
        return line
    
    def add_label(self, label:str):
        a = LabelInstruction(label)
        line = ThreeAddressInstruction(labelInstruction=a)
        return line
    
    


