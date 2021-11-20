

class BasicBlock():
    def __init__(self, name:str):
        self.intermediateCode = []
        self.name = name


class SourceCode():
    def __init__(self, intermediateCode: list, varSymbolTable: list):
        self.intermediateCode = intermediateCode
        self.varSymbolTable = varSymbolTable
        
        self.basicBlocks = []
        self.mainBlock = ''
        self.labelBlockMap = {'L-1' : 'block-1'}
        self.tempsAddresses = {}
        
        self.registersToUse = ["X2", "X3", "X4", "X5", "X6", "X7", "X8", "X9", "X10",]
        self.tempsToUse = ['t0', 't1', 't2', 't3', 't4', 't5']
        self.registryDescriptor = {}
        self.addressDescriptor = {}
        
        self.sourceCodeLines = []
        
        self.labelNumber = 0
        self.registerForAddress = 'X15'
    
    def generate(self):
        # Agrega las variables en el desriptor de direcciones
        self.setUpDescriptors()
        
        # Separa los bloques basicos
        self.separateToBasicBlocks()
        self.changeBasicBlocksLabelNames()
        self.printBasicBlocks()
        
        # Genera el codigo de maquina
        self.generateCode()
        self.printSourceCode() 
        
    # Agrega las variables en el desriptor de direcciones
    def setUpDescriptors(self):
        tempsAddressBase = 0
        for varSymbolItem in self.varSymbolTable:
            varName = 'estatica[%d]' % (varSymbolItem.base)
            self.addressDescriptor[varName] = {'registry': '', 'var': varName}
            tempsAddressBase = varSymbolItem.base + varSymbolItem.size
        
        for tempToUse in self.tempsToUse:
            self.addressDescriptor[tempToUse] = {'registry': '', 'var': ''}
            self.tempsAddresses[tempToUse] = '%d' % tempsAddressBase
            tempsAddressBase = tempsAddressBase + 8
        
        for registerToUse in self.registersToUse:
            self.registryDescriptor[registerToUse] = []
    
    # Separa los bloques basicos
    def separateToBasicBlocks(self):
        lines = []
        for i in range(len(self.intermediateCode)):
            threeAddressInstruction = self.intermediateCode[i]
            if i == 0:
                lines.append(threeAddressInstruction)
                if threeAddressInstruction.funcDeclarationBeginInstruction.name == 'main':
                    self.mainBlock = 'block0'
            elif i == len(self.intermediateCode) - 1:
                lines.append(threeAddressInstruction)
                basicBlock = BasicBlock('block%s' % (len(self.basicBlocks)))
                basicBlock.intermediateCode = lines.copy()
                self.basicBlocks.append(basicBlock)
            else:
                previousInstruction = self.intermediateCode[i - 1]

                # Si se declara una funcion
                if threeAddressInstruction.funcDeclarationBeginInstruction != None:
                    basicBlock = BasicBlock('block%s' % (len(self.basicBlocks)))
                    basicBlock.intermediateCode = lines.copy()
                    self.basicBlocks.append(basicBlock)
                    
                    lines = [threeAddressInstruction]
                    
                    if threeAddressInstruction.funcDeclarationBeginInstruction.name == 'main':
                        self.mainBlock = 'block%s' % (len(self.basicBlocks) + 1)
                
                # si es una label instruction
                elif threeAddressInstruction.labelInstruction != None: 
                    basicBlock = BasicBlock('block%s' % (len(self.basicBlocks)))
                    basicBlock.intermediateCode = lines.copy()
                    self.basicBlocks.append(basicBlock)
                    
                    
                    bbName = 'block%s' % (len(self.basicBlocks))
                    labelName = threeAddressInstruction.labelInstruction.label
                    
                    self.labelBlockMap[labelName] = bbName
                    
                    lines = []
                    
                # Si la instruccion PREVIA es una salto incondicional o condicional
                elif previousInstruction.inconditionalJumpInstruction != None or previousInstruction.conditionalJumpInstruction != None or previousInstruction.conditionalRelopJumpInstruction != None:
                    basicBlock = BasicBlock('block%s' % (len(self.basicBlocks)))
                    basicBlock.intermediateCode = lines.copy()
                    self.basicBlocks.append(basicBlock)
                    
                    lines = [threeAddressInstruction]
                    
                # Si es el return de una funcion
                elif threeAddressInstruction.funcReturnInstruction != None:
                    lines.append(threeAddressInstruction)
                    basicBlock = BasicBlock('block%s' % (len(self.basicBlocks)))
                    basicBlock.intermediateCode = lines.copy()
                    self.basicBlocks.append(basicBlock)
                    
                    lines = []
                    
                # Todo lo demas
                else:
                    lines.append(threeAddressInstruction)
    
    # Cambia los labels en los saltos condicionales con los nombres de lo bloques basicos
    def changeBasicBlocksLabelNames(self):
        for bb in self.basicBlocks:
            for threeAddressInstruction in bb.intermediateCode:
                # Si la instruccion es una salto incondicional
                if threeAddressInstruction.inconditionalJumpInstruction != None:
                    goToLabel = threeAddressInstruction.inconditionalJumpInstruction.label
                    
                    bbLabel = self.labelBlockMap.get(goToLabel)
                    threeAddressInstruction.inconditionalJumpInstruction.label = bbLabel
                
                # Si la instruccion es una salto condicional
                elif threeAddressInstruction.conditionalJumpInstruction != None:
                    goToLabel = threeAddressInstruction.conditionalJumpInstruction.label
                    
                    bbLabel = self.labelBlockMap.get(goToLabel)
                    threeAddressInstruction.conditionalJumpInstruction.label = bbLabel
                
                # Si la instruccion es una salto condicional relop
                elif threeAddressInstruction.conditionalRelopJumpInstruction != None:
                    goToLabel = threeAddressInstruction.conditionalRelopJumpInstruction.label
                    
                    bbLabel = self.labelBlockMap.get(goToLabel)
                    threeAddressInstruction.conditionalRelopJumpInstruction.label = bbLabel
    
    # Imprime todos los bloques basicos
    def printBasicBlocks(self):
        for bb in self.basicBlocks:
            print(bb.name)
            for line in bb.intermediateCode:
                print(line.toString())
    
    # Funcion para obtener un registro para asignarle a una variable
    def getReg(self, varName: str, isOperand: bool = False, assignableVar: str = '', otherOperand: str = '', registriesInLine = []):
        registrySelected = None
        registryNames = self.registryDescriptor.keys()
        
        # Caso 1: si ya existe un registro con el nombre de la variable
        for r in registryNames:
            if varName in self.registryDescriptor[r]:
                registrySelected = r
                break
        
        if registrySelected != None:
            return registrySelected
        
        # Caso 2: si no hay registro con la variable, pero si hay uno vacio
        for r in registryNames:
            if len(self.registryDescriptor[r]) == 0:
                registrySelected = r
                break
        
        if registrySelected != None:
            return registrySelected
        
        # Caso 3.1
        for r in registryNames:
            for rv in self.registryDescriptor[r]:
                addDesVar = self.addressDescriptor[rv]['var']
                if addDesVar == rv:
                    registrySelected = r
                    break
            if registrySelected != None:
                break
        
        if registrySelected != None:
            return registrySelected
        
        # Caso 3.2
        if isOperand:
            for r in registryNames:
                if assignableVar in self.registryDescriptor[r] and assignableVar != otherOperand:
                    registrySelected = r
                    break
        
        if registrySelected != None:
            return registrySelected
        
        # Caso 3.3 TODO: 'Si v no se utiliza mas adelante'
        
        # Caso 3.4 Spill
        for r in registryNames:
            if r not in registriesInLine:
                registrySelected = r
                
                for v in self.registryDescriptor[r]:
                    if v.find('estatica') != -1:
                        v = '[%s]' % self.getAddressFromEstatica(v)
                    
                    line = 'STR %s, %s' % (v, r)
                    self.sourceCodeLines.append(line)
                    
                break
        
        if registrySelected != None:
            return registrySelected
    
    # Obtiene el numero de direccion de una estatica
    def getAddressFromEstatica(self, estatica: str):
        first = estatica.find('[') + 1
        last = estatica.find(']')
        
        return estatica[first:last]

    def generateCode(self):
        for basicBlock in self.basicBlocks:
            self.generateCodeFromBasicBlock(basicBlock)

    def generateCodeFromBasicBlock(self, basicBlock: BasicBlock):
        varNames = self.addressDescriptor.keys()
        self.sourceCodeLines.append('%s:' % basicBlock.name)
        
        for threeAddressLine in basicBlock.intermediateCode:
            if threeAddressLine.copyAssignationInstruction != None:
                assignTo = threeAddressLine.copyAssignationInstruction.assignTo
                operand1 = threeAddressLine.copyAssignationInstruction.operand1
                
                assignToRegister = ''
                
                assignToRegister = self.getReg(assignTo)
                
                if operand1 in varNames:
                    varRegister = self.getReg(operand1)
                    self.addLoadInstruction(varRegister, operand1)
                    self.addMoveInstruction(assignToRegister, varRegister)
                else:
                    operand = '#%s' % operand1
                    self.addMoveInstruction(assignToRegister, operand)
                
                # Guardar valor en memoria
                self.addStoreInstruction(assignTo, assignToRegister)
            
            elif threeAddressLine.assignationInstruction != None:
                assignationInstruction = threeAddressLine.assignationInstruction  
                result = assignationInstruction.assignTo
                firstOperand = assignationInstruction.operand1
                secondOperand = assignationInstruction.operand2
                
                resultRegister = ''
                
                # Si es una suma
                if assignationInstruction.operator == '+' or assignationInstruction.operator == '-' or assignationInstruction.operator == '*':
                    operation = ''
                    if assignationInstruction.operator == '+':
                        operation = 'ADD'
                    if assignationInstruction.operator == '-':
                        operation = 'SUB'
                    if assignationInstruction.operator == '*':
                        operation = 'MUL'
                    
                    resultRegister = self.getReg(result)
                    
                    firstOperandRegister = self.getReg(firstOperand, isOperand=True, assignableVar='result', otherOperand=secondOperand, registriesInLine=[resultRegister])
                    secondOperandRegister = self.getReg(secondOperand, isOperand=True, assignableVar='result', otherOperand=firstOperand, registriesInLine=[firstOperandRegister])
                    
                    self.addLoadInstruction(firstOperandRegister, firstOperand)
                    self.addLoadInstruction(secondOperandRegister, secondOperand)
                    
                    line = '%s %s, %s, %s' % (operation, resultRegister, firstOperandRegister, secondOperandRegister)
                    self.sourceCodeLines.append(line)
                    
                    self.addStoreInstruction(result, resultRegister)
                    
                
                # Si es una operacion booleana
                if assignationInstruction.operator == '<' or assignationInstruction.operator == '>' or assignationInstruction.operator == '<=' or assignationInstruction.operator == '>=' or assignationInstruction.operator == '==' or assignationInstruction.operator =='!=':
                    compareFlag = ''
                    if assignationInstruction.operator == '<':
                        compareFlag = 'LT'
                    if assignationInstruction.operator == '>':
                        compareFlag = 'GT'
                    if assignationInstruction.operator == '<=':
                        compareFlag = 'LE'
                    if assignationInstruction.operator == '>=':
                        compareFlag = 'GE'
                    if assignationInstruction.operator == '==':
                        compareFlag = 'EQ'
                    if assignationInstruction.operator == '!=':
                        compareFlag = 'NE'
                    
                    firstOperandRegister = self.getReg(firstOperand)
                    secondOperandRegister = self.getReg(secondOperand)
                    
                    self.addLoadInstruction(firstOperandRegister, firstOperand)
                    self.addLoadInstruction(secondOperandRegister, secondOperand)
                    
                    label1 = self.getNewLabel()
                    label2 = self.getNewLabel()
                    
                    line = 'CMP %s, %s' % (firstOperandRegister, secondOperandRegister)
                    self.sourceCodeLines.append(line)
                    line = 'B.%s %s' % (compareFlag, label1)
                    self.sourceCodeLines.append(line)
                    
                    resultRegister = self.getReg(result)
                    self.addMoveInstruction(resultRegister, '#0')
                    line = 'B %s' % label2
                    self.sourceCodeLines.append(line)
                    
                    self.addLabelInstruction(label1)
                    self.addMoveInstruction(resultRegister, '#1')
                    
                    self.addLabelInstruction(label2)
                    self.addStoreInstruction(result, resultRegister)
                
                
                if result.find('estatica') != -1:
                    # Modificar el descriptor de registro para Rx, de manera que sólo contenga a x.
                    self.registryDescriptor[resultRegister] = [result]
                    
                    # Modificar el descriptor de dirección para x, de manera que su única ubicación sea Rx. 
                    # Observe que la ubicación de memoria para x no se encuentra ahora en el descriptor de dirección para x.
                    self.addressDescriptor[result]['var'] = ''
                    self.addressDescriptor[result]['registry'] = resultRegister
                    
                    # Eliminar Rx del descriptor de dirección de cualquier variable distinta de x.
                    for varName in self.addressDescriptor.keys():
                        if varName != result:
                            self.addressDescriptor[varName]['registry'] = ''
            
            elif threeAddressLine.conditionalJumpInstruction != None:
                conditionalJumpInstruction = threeAddressLine.conditionalJumpInstruction
                condition = conditionalJumpInstruction.condition
                
                conditionRegister = self.getReg(condition)
                
                self.addLoadInstruction(conditionRegister, condition)
                
                compareRegister = 'X1'
                
                if conditionalJumpInstruction.isIfFalse:  
                    self.addMoveInstruction(compareRegister, '#0')
                else:  
                    self.addMoveInstruction(compareRegister, '#1')
                    
                line = 'CMP %s, %s' % (compareRegister, conditionRegister)
                self.sourceCodeLines.append(line)
                line = 'B.EQ %s' % (conditionalJumpInstruction.label)
                self.sourceCodeLines.append(line)

            elif threeAddressLine.inconditionalJumpInstruction != None:
                line = 'B %s' % threeAddressLine.inconditionalJumpInstruction.label
                self.sourceCodeLines.append(line)
                
    def addStoreInstruction(self, varName: str, register: str):
        var = varName
        if varName.find('estatica') != -1:
            line = 'MOV %s, #%s' % (self.registerForAddress, self.getAddressFromEstatica(varName))
            self.sourceCodeLines.append(line)
            var = '[%s]' % self.registerForAddress
            # Cambiar el descriptor de direcciones
            self.addressDescriptor[varName]['var'] = varName
        else:
            tempAddress = '#%s' % self.tempsAddresses[var]
            line = 'MOV %s, %s' % (self.registerForAddress, tempAddress)
            self.sourceCodeLines.append(line)
            var = '[%s]' % self.registerForAddress
            
        # Asegura que el descriptor de registros tenga el valor de la variable
        self.registryDescriptor[register] = [varName]

        line = 'STR %s, %s' % (register, var)
            
        self.sourceCodeLines.append(line)
    
    def addMoveInstruction(self, r1, r2):
        line = 'MOV %s, %s' %(r1, r2)
        self.sourceCodeLines.append(line)
        
        if r1 != 'X0' and r1 != 'X1':
            varNamesInR1 = self.registryDescriptor[r1].copy()
            for varNameR1 in varNamesInR1:
                if r2.find('X') != -1:
                    self.registryDescriptor[r2].append(varNameR1)
                    self.addressDescriptor[varNameR1]['var'] = ''
                    self.addressDescriptor[varNameR1]['registry'] = r2
    
    def addLoadInstruction(self, register: str, varName: str):
        # Ejecuta la funcion de LD para la variable y el registro
        v = varName
        if v.find('estatica') != -1:
            line = 'MOV %s, #%s' % (self.registerForAddress, self.getAddressFromEstatica(v))
            self.sourceCodeLines.append(line)
            v = '[%s]' % self.registerForAddress
        else:
            tempAddress = '#%s' % self.tempsAddresses[v]
            line = 'MOV %s, %s' % (self.registerForAddress, tempAddress)
            self.sourceCodeLines.append(line)
            v = '[%s]' % self.registerForAddress
        line = 'LDR %s, %s' % (register, v)
        self.sourceCodeLines.append(line)
        
        if register != 'X0' and register != 'X1':
            # Modifica los descriptores de registro y de direcciones
            self.registryDescriptor[register] = [varName]
            self.addressDescriptor[varName]['registry'] = register

    def addLabelInstruction(self, label:str):
        line = '%s:' % (label)
        self.sourceCodeLines.append(line)
 
    def getNewLabel(self):
        label = 'l%d' % self.labelNumber
        self.labelNumber = self.labelNumber + 1
        
        return label

    # Print generated code
    def printSourceCode(self):
        with open('Decaf/test_files/result/source.s', "w") as output_file:
            output_file.write('.global _main \n\n_main:\n\n')
            for line in self.sourceCodeLines:
                text = ''
                if len(line) < 4 or (line.find('block') != -1 and line.find(':') != -1):
                    print(line)
                    text = '%s\n' % line
                else:
                    print('\t%s' % line)
                    text = '\t%s\n' % line
                output_file.write(text)