
from DecafParser import DecafParser
from DecafListener import DecafListener
import DecafErrors
import utils

#---------------------------------------------------------------------------------------------------

class IntermediateCode(DecafListener):
    def __init__(self, varSymbolTable, methodSymbolTable, structSymbolTable):
        # Scopes
        self.scopes = []
        self.ifCount = 0
        self.elseCount = 0
        self.whileCount = 0

        # Flags or misc
        self.temp_number = 0
        self.label_number = 0
        self.last_location_variable = ''

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
        self.lines.append("func begin %s" % (method_name))
        self.enterScope(method_name)
        block_code = self.get_block_code(ctx.block())
        self.add_lines(block_code)

    # Exit a parse tree produced by DecafParser#methodDeclaration.
    def exitMethodDeclaration(self, ctx:DecafParser.MethodDeclarationContext):
        self.lines.append("func end")
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
        self.enterScope("if" + str(self.ifCount))
        
    # Exit a parse tree produced by DecafParser#ifStatement.
    def exitIfStatement(self, ctx:DecafParser.IfStatementContext):
        self.exitScope()
    
    # Enter a parse tree produced by DecafParser#elseStatement.
    def enterElseStatement(self, ctx:DecafParser.ElseStatementContext):
        self.enterScope("else" + str(self.elseCount))

    # Exit a parse tree produced by DecafParser#elseStatement.
    def exitElseStatement(self, ctx:DecafParser.ElseStatementContext):
        self.exitScope()

    # Enter a parse tree produced by DecafParser#whileStatement.
    def enterWhileStatement(self, ctx:DecafParser.WhileStatementContext):
        self.enterScope("while" + str(self.whileCount))
        
    # Exit a parse tree produced by DecafParser#whileStatement.
    def exitWhileStatement(self, ctx:DecafParser.WhileStatementContext):
        self.exitScope()

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

            location_code = self.get_location_code(ctx.location(), isLeftSide=True)
            lines = lines + location_code

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
                lines.append('\treturn')
            else:
                lines = lines + expressionOm_code
                last_expressionOm_temp = self.get_last_temp()
                lines.append('\treturn %s' % (last_expressionOm_temp))
        
        return lines
    
    def get_while_statement_code(self, ctx:DecafParser.WhileStatementContext):
        lines = []

        start_label = self.new_label()
        end_label = self.new_label()

        lines.append(self.add_label(start_label))
        expression_code = self.get_expression_code(ctx.expression())
        last_expression_temp = self.get_last_temp()

        lines = lines + expression_code
        lines.append(self.conditional_jump(end_label, last_expression_temp, isIfFalse=True))

        block_code = self.get_block_code(ctx.block())
        lines = lines + block_code

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

            lines = lines + expression_code

            # Codicional del if
            lines.append(self.conditional_jump(end_label, last_expression_temp, isIfFalse=True))

            # Block del code
            block_code = self.get_block_code(ifCtx.block())
            lines = lines + block_code

            # Label del end
            lines.append(self.add_label(end_label))
        else:
            else_label = self.new_label()
            end_label = self.new_label()

            # Expression de la condicional
            expression_code = self.get_expression_code(ifCtx.expression())
            last_expression_temp = self.get_last_temp()

            lines = lines + expression_code

            lines.append(self.conditional_jump(else_label, last_expression_temp, isIfFalse=True))

            # Block del if
            if_block_code = self.get_block_code(ifCtx.block())
            lines = lines + if_block_code
            lines.append(self.inconditional_jump(end_label))

            # Label del else
            lines.append(self.add_label(else_label))

            # Block del else
            else_block_code = self.get_block_code(elseCtx.block())
            lines = lines + else_block_code

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
            temp_unary = self.new_temp()
            lines.append(self.unary_assignation(temp_unary, last_temp, "-"))
        elif ctx.children[0].getText() == '!':
            expression_code = self.get_expression_code(ctx.expression())
            lines = lines + expression_code
            last_temp = self.get_last_temp()
            temp_unary = self.new_temp()
            lines.append(self.unary_assignation(temp_unary, last_temp, "!"))
        elif ctx.arith_op_first() != None:
            expression1 = ctx.children[0]
            expression2 = ctx.children[2]

            expression1_code = self.get_expression_code(expression1)
            last_temp1 = self.get_last_temp()
            expression2_code = self.get_expression_code(expression2)
            last_temp2 = self.get_last_temp()

            temp = self.new_temp()

            lines = lines + expression1_code + expression2_code
            lines.append(self.assignation(temp, last_temp1, last_temp2, '||'))
        elif ctx.arith_op_second() != None:
            expression1 = ctx.children[0]
            expression2 = ctx.children[2]

            expression1_code = self.get_expression_code(expression1)
            last_temp1 = self.get_last_temp()
            expression2_code = self.get_expression_code(expression2)
            last_temp2 = self.get_last_temp()

            temp = self.new_temp()

            lines = lines + expression1_code + expression2_code
            lines.append(self.assignation(temp, last_temp1, last_temp2, '&&'))
        elif ctx.arith_op_third() != None:
            expression1 = ctx.children[0]
            expression2 = ctx.children[2]

            expression1_code = self.get_expression_code(expression1)
            last_temp1 = self.get_last_temp()
            expression2_code = self.get_expression_code(expression2)
            last_temp2 = self.get_last_temp()

            temp = self.new_temp()

            lines = lines + expression1_code + expression2_code
            relop = ctx.children[1].getText()
            lines.append(self.assignation(temp, last_temp1, last_temp2, relop))
        elif ctx.arith_op_fourth() != None:
            expression1 = ctx.children[0]
            expression2 = ctx.children[2]

            expression1_code = self.get_expression_code(expression1)
            last_temp1 = self.get_last_temp()
            expression2_code = self.get_expression_code(expression2)
            last_temp2 = self.get_last_temp()

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
                expression2_code = self.get_expression_code(expression2)
                last_temp2 = self.get_last_temp()
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

                var_singular_size = '%d' % (struct_item.size)
                
                index_temp = self.new_temp()
                lines.append(self.assignation(index_temp, last_temp_expression, var_singular_size, '*'))

                array_offset_temp = self.new_temp()
                lines.append(self.assignation(array_offset_temp, temp, index_temp, '+'))

                # Location
                location_code = self.get_location_code(ctx.location(), struct_item.varType)
                lines = lines + location_code
                last_temp_location = self.get_last_temp()

                array_location_offset = self.new_temp()
                lines.append(self.assignation(array_location_offset, array_offset_temp, last_temp_location, '+'))
            
            # Si solo es array
            elif ctx.expression() != None:
                expression_code = self.get_expression_code(ctx.expression())
                lines = lines + expression_code
                last_temp_expression = self.get_last_temp()

                var_singular_size = '%d' % (struct_item.size)
                
                index_temp = self.new_temp()
                lines.append(self.assignation(index_temp, last_temp_expression, var_singular_size, '*'))

                array_offset_temp = self.new_temp()
                lines.append(self.assignation(array_offset_temp, temp, index_temp, '+'))
            
            # Si solo hay location
            elif ctx.location() != None:
                location_code = self.get_location_code(ctx.location(), struct_item.varType)
                lines = lines + location_code
                last_temp_location = self.get_last_temp()

                final_offset = self.new_temp()
                lines.append(self.assignation(final_offset, offset, last_temp_location, '+'))
                
        else:
            id = ctx.ID().getText()

            last_temp_expression = ''
            if ctx.expression() != None:
                expression_code = self.get_expression_code(ctx.expression())
                lines = lines + expression_code
                last_temp_expression = self.get_last_temp()
            
            last_temp_location = ''
            if ctx.location() != None:

                varItem = utils.getVarItemInScopes(self.varSymbolTable, id, self.getScopes())
                location_code = self.get_location_code(ctx.location(), varItem.varType)
                lines = lines + location_code
                last_temp_location = self.get_last_temp()
            
            if last_temp_location != '' or last_temp_expression != '':
                if last_temp_expression != '' and last_temp_location != '':
                    var_singular_size = utils.getSingularVarSize(self.varSymbolTable, self.structSymbolTable, id, self.getScopes())
                    index_temp = self.new_temp()
                    lines.append(self.assignation(index_temp, last_temp_expression, var_singular_size, '*'))

                    expression_location_temp = self.new_temp()
                    lines.append(self.assignation(expression_location_temp, index_temp, last_temp_location, '+'))

                    if isLeftSide:
                        self.last_location_variable = "%s[%s]" % (id, expression_location_temp)
                    else:
                        temp = self.new_temp()
                        lines.append(self.copy_assignation_index(temp, id, expression_location_temp))
                elif last_temp_expression != '':
                    var_singular_size = utils.getSingularVarSize(self.varSymbolTable, self.structSymbolTable, id, self.getScopes())
                    index_temp = self.new_temp()
                    lines.append(self.assignation(index_temp, last_temp_expression, var_singular_size, '*'))
                    
                    if isLeftSide:
                        self.last_location_variable = "%s[%s]" % (id, index_temp)
                    else:
                        temp = self.new_temp()
                        lines.append(self.copy_assignation_index(temp, id, index_temp))
                elif last_temp_location != '':
                    if isLeftSide:
                        self.last_location_variable = "%s[%s]" % (id, last_temp_location)
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
                        last_temp = "t%d" % (self.temp_number)
                        lines = lines + child_lines
                        params.append(last_temp)
        
        for param in params:
            lines.append(self.procedure_param(param))

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
        self.temp_number = self.temp_number + 1
        temp_name = "t%d" % (self.temp_number)
        return temp_name
    
    def new_label(self):
        label_name = "L%d" % (self.label_number)
        self.label_number = self.label_number + 1
        return label_name
    
    def get_last_temp(self):
        return "t%d" % (self.temp_number)

    def add_lines(self, lines: list):
        for line in lines:
            self.lines.append(line)
    
    def assignation(self, result: str, arg1: str, arg2: str, op: str, gotoLabel: str = ''):
        line = "%s = %s %s %s" % (result, arg1, op, arg2)
        if gotoLabel != '':
            line = '%s: ' % (gotoLabel) + line
        else:
            line = "\t" + line
        return line
    
    def unary_assignation(self, result: str, arg1: str, op: str, gotoLabel: str = ''):
        line = "%s = %s %s" % (result, op, arg1)
        if gotoLabel != '':
            line = '%s: ' % (gotoLabel) + line
        else:
            line = "\t" + line
        return line
    
    def copy_assignation(self, result: str, arg1: str, gotoLabel: str = ''):
        line = "%s = %s" % (result, arg1)
        if gotoLabel != '':
            line = '%s: ' % (gotoLabel) + line
        else:
            line = "\t" + line
        return line
    
    def inconditional_jump(self, label: str, gotoLabel: str = ''):
        line = "goto %s" % (label)
        if gotoLabel != '':
            line = '%s: ' % (gotoLabel) + line
        else:
            line = "\t" + line
        return line
    
    def conditional_jump(self, label: str, x: str, isIfFalse: bool = False, gotoLabel: str = ''):
        line = ''
        if not isIfFalse:
            line = "if %s goto %s" % (x, label)
        else:
            line = "ifFalse %s goto %s" % (x, label)
        
        if gotoLabel != '':
            line = '%s: ' % (gotoLabel) + line
        else:
            line = "\t" + line

        return line

    def conditional_jump_relop(self, label: str, x: str, y: str, relop: str, gotoLabel: str = ''):
        line = "if %s %s %s goto %s" % (x, relop, y, label) 
        if gotoLabel != '':
            line = '%s: ' % (gotoLabel) + line
        else:
            line = "\t" + line
        return line

    def procedure_param(self, param: str, gotoLabel: str = ''):
        line = "param %s" % (param)
        if gotoLabel != '':
            line = '%s: ' % (gotoLabel) + line
        else:
            line = "\t" + line
        return line

    def procedure(self, procedure: str, params: list, gotoLabel: str = ''):
        line = "call %s, %s" % (procedure, str(len(params))) 
        if gotoLabel != '':
            line = '%s: ' % (gotoLabel) + line
        else:
            line = "\t" + line
        return line

    def copy_assignation_index(self, result: str, x: str, index: int, isAssignToItem: bool = False, gotoLabel: str = ''):
        line = ''
        if isAssignToItem:
            line = "%s[%s] = %s" % (result, str(index), x)
        else:
            line = "%s = %s[%s]" % (result, x, str(index))

        if gotoLabel != '':
            line = '%s: ' % (gotoLabel) + line
        else:
            line = "\t" + line
        return line
    
    def add_label(self, label:str):
        line = "%s:" % (label)
        return line

    


