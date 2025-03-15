from antlr4 import *
from reglang.RegLangLexer import RegLangLexer
from reglang.RegLangParser import RegLangParser
from reglang.RegLangVisitor import RegLangVisitor
from reglang.logger import logger
from reglang.RegLangTypes import *

class Visitor(RegLangVisitor):
    def __init__(self, tx):
        # global regulation result
        self.rejected = False
        # all knowlegebases
        self.knowledgebases = {}
        self.current_knowledgebase = ""
        # current transaction
        self.tx = tx
        # mark whether the visitor is visiting `varSymbol '[' arithExpr ']'`
        self.arrayFlag = False
        # mark whether the visitor is visiting `logicExpr: func=('at_least'|'at_most') '('arithExpr ',' logicExpr')'`
        self.funcLeastMostFlag = False
        # mark whether the visitor is visiting `logicExpr: func=('any_item'|'all_items') '(' logicExpr')'`
        self.funcAnyItemFlag = False
        self.funcAllItemFlag = False

        super().__init__()

    def _stringToInt(self, s):
        if isinstance(s, str) and s.startswith("0x"):
            return int(s, 16)
        return int(s)

    def visitProg(self, ctx:RegLangParser.ProgContext):
        # # Add knowledgebase first
        # knowledgebaseBlocks = ctx.knowledgebaseBlock()
        # for knowledgebaseBlock in knowledgebaseBlocks:
        #     self.visit(knowledgebaseBlock)

        # # Checking rules sequentially
        # ruleBlocks = ctx.ruleBlock()
        # for ruleBlock in ruleBlocks:
        #     self.visit(ruleBlock)
        self.visitChildren(ctx)

        # Final result
        all_rules_passed = True
        if self.rejected:
            logger.debug("Some rules not satisfied. See log for detail.")
            all_rules_passed = False
            return all_rules_passed
        else:
            logger.debug("All rules passed.")
            return all_rules_passed

    def visitKnowledgebaseBlock(self, ctx:RegLangParser.KnowledgebaseBlockContext):
        knowledgebaseName = ctx.ID().getText()
        logger.debug("Adding Knowledgebase: %s"%knowledgebaseName)
        self.current_knowledgebase = knowledgebaseName
        if not knowledgebaseName in self.knowledgebases.keys():
            self.knowledgebases[knowledgebaseName] = {}
        knowledgeDecls = ctx.knowledgeDecl()
        for knowledgeDecl in knowledgeDecls:
            self.visit(knowledgeDecl)
        logger.debug("Build knowledgebase :%s"%self.knowledgebases[knowledgebaseName])

    # visits `knowledgeDecl : 'knowledge' ID '=' arithExpr ';'`
    def visitKnowledgeAssign(self, ctx:RegLangParser.KnowledgeAssignContext):
        knowledgeName = ctx.ID().getText()
        knowledgeValue = self.visit(ctx.arithExpr())
        self.knowledgebases[self.current_knowledgebase][knowledgeName] = knowledgeValue
        logger.debug("Adding knowledge %s = %s" % (knowledgeName, knowledgeValue))

    # visits `knowledgeDecl : ID '.' op=('add'|'del') '(' arithExpr ')' ';'`
    def visitKnowledgeFunc(self, ctx:RegLangParser.KnowledgeFuncContext):
        knowledgeName = ctx.ID().getText()
        if knowledgeName not in self.knowledgebases[self.current_knowledgebase].keys():
            raise Exception("knowledge %s does not exist" % knowledgeName)
        op = ctx.op.text
        knowledgeValue = self.visit(ctx.arithExpr())
        if op == "add":
            if isinstance(knowledgeValue, list):
                for v in knowledgeValue:
                    if v not in self.knowledgebases[self.current_knowledgebase][knowledgeName]:
                        self.knowledgebases[self.current_knowledgebase][knowledgeName].append(v)
                        logger.debug("Adding knowledge %s value %s"%(knowledgeName, v))
                    else:
                        logger.debug("Duplicate knowledge %s value %s"%(knowledgeName, v))
            else:
                if knowledgeValue not in self.knowledgebases[self.current_knowledgebase][knowledgeName]:
                    self.knowledgebases[self.current_knowledgebase][knowledgeName].append(knowledgeValue)
                    logger.debug("Adding knowledge %s value %s"%(knowledgeName, knowledgeValue))
                else:
                    logger.debug("Duplicate knowledge %s value %s"%(knowledgeName, knowledgeValue))
        elif op == "del":
            if isinstance(knowledgeValue, list):
                for v in knowledgeValue:
                    if v in self.knowledgebases[self.current_knowledgebase][knowledgeName]:
                        self.knowledgebases[self.current_knowledgebase][knowledgeName].remove(v)
                        logger.debug("Deleting knowledge %s value %s"%(knowledgeName, v))
                    else:
                        logger.debug("Knowledge %s value %s does not exist"%(knowledgeName, v))
            else:
                if knowledgeValue in self.knowledgebases[self.current_knowledgebase][knowledgeName]:
                    self.knowledgebases[self.current_knowledgebase][knowledgeName].remove(knowledgeValue)
                    logger.debug("Deleting knowledge %s value %s"%(knowledgeName, knowledgeValue))
                else:
                    logger.debug("Knowledge %s value %s does not exist"%(knowledgeName, knowledgeValue))
        else:
            logger.warning("parse error: KnowledgeFunc")

    def visitRuleBlock(self, ctx:RegLangParser.RuleBlockContext):
        if not self.rejected:
            ruleName = ctx.ID()
            logger.debug("Checking Rule: %s" % ruleName)

            # visit regScopeStme
            inScope = self.visit(ctx.regScopeStmt())
            if inScope:
                logger.debug("In Rule %s's scope" % ruleName)
            else:
                logger.debug("NOT In Rule %s's scope" % ruleName)
                # do not need to check reg rules due to out of scope
                return
            # visit all regRuleStmt one by one
            regRuleStmts = ctx.regRuleStmt()
            i = 0
            for regRuleStmt in regRuleStmts:
                if not self.rejected:
                    logger.debug("Calculating RegRuleStmt No. %d" % i)
                    self.visit(regRuleStmt) 
                    if self.rejected:
                        logger.debug("Rule rejected at Rule %s condition %d"%(ruleName,i))
                    i += 1
    
    def visitRegScopeStmt(self, ctx: RegLangParser.RegScopeStmtContext):
        logger.debug("Entering Reg Scope")
        if self.visit(ctx.logicExpr()):
            return True
        return False

    def visitRequireReg(self, ctx: RegLangParser.RequireRegContext):
        # require means the condition must be true, otherwise the tx will be rejected
        try:
            if not self.visit(ctx.logicExpr()):
                logger.debug("Rejected!")
                self.rejected = True
            else:
                logger.debug("Passed..")
        except Exception as e:
            logger.warning("Skipped..(error: %s)"%e)
    
    def visitProhibitReg(self, ctx: RegLangParser.ProhibitRegContext):
        # prohibit means the condition can not be true, otherwise the tx will be rejected
        try:
            if self.visit(ctx.logicExpr()):
                logger.debug("Rejected!")
                self.rejected = True
            else:
                logger.debug("Passed..")
        except Exception as e:
            logger.warning("Skipped..(error: %s)"%e)

    def __checkValInKnowledge(self, val, knowledge, knowledgebaseName, knowledgeName):
        logger.debug("val: %s"%val)
        logger.debug("knowledge: %s"%knowledge)
        if val in knowledge or str(val).lower() in knowledge:
            logger.debug("Check Val in knowledgebase(%s).%s: True"%(knowledgebaseName,knowledgeName))
            return True
        else:
            try:
                if self._stringToInt(val) in knowledge:
                    logger.debug("Check Val in knowledgebase(%s).%s: True"%(knowledgebaseName,knowledgeName))
                    return True
                else:
                    logger.debug("Check Val in knowledgebase(%s).%s: False"%(knowledgebaseName,knowledgeName))
                    return False
            except:
                logger.debug("Check Val in knowledgebase(%s).%s: False"%(knowledgebaseName,knowledgeName))
                return False

    # visits `logicExpr: arithExpr 'in' 'knowledgebase' '(' ID ')' '.' ID`
    def visitInternalFunctionIn(self, ctx:RegLangParser.InternalFunctionInContext):
        knowledgebaseName = ctx.ID(0).getText()
        knowledgeName = ctx.ID(1).getText()
        knowledge = self.knowledgebases[knowledgebaseName][knowledgeName]
        val = self.visit(ctx.arithExpr())
        if self.funcLeastMostFlag:
            self.funcLeastMostFlag = False
            count = 0
            if isinstance(val, list):
                for item in val:
                    if self.__checkValInKnowledge(item, knowledge, knowledgebaseName, knowledgeName):
                        count += 1
                logger.debug("Arg result in at_least/at_most: %d"%count)
                return count
            else:
                logger.warning("Left side of Arg1 in at_least/at_most is not array.")
        elif self.funcAnyItemFlag:
            self.funcAnyItemFlag = False
            if isinstance(val, list):
                for item in val:
                    if self.__checkValInKnowledge(item, knowledge, knowledgebaseName, knowledgeName):
                        logger.debug("Comparing result in any_item: True")
                        return True
                logger.debug("Arg result in any_item: False")
                return False
            else:
                logger.warning("Left side of Arg1 in any_item is not array.")
        elif self.funcAllItemFlag:
            self.funcAllItemFlag = False
            if isinstance(val, list):
                for item in val:
                    if not self.__checkValInKnowledge(item, knowledge, knowledgebaseName, knowledgeName):
                        logger.debug("Comparing result in all_items: False")
                        return False
                logger.debug("Arg result in all_items: True")
                return True
            else:
                logger.warning("Left side of Arg1 in all_items is not array.")
        else:
            return self.__checkValInKnowledge(val, knowledge, knowledgebaseName, knowledgeName)

    # visits `logicExpr: func=('at_least'|'at_most') '('arithExpr ',' logicExpr')'`
    def visitFuncLeastMost(self, ctx:RegLangParser.FuncLeastMostContext):
        funcname = ctx.func.text
        num = self.visit(ctx.arithExpr())
        self.funcLeastMostFlag = True
        count = self.visit(ctx.logicExpr())
        if funcname == "at_least":
            logger.debug("Function at_least requires at least: %d"%num)
            return count >= num
        elif funcname == "at_most":
            logger.debug("Function at_most requires at most: %d"%num)
            return count <= num
        else:
            logger.warning("parse error: FuncLeastMost")

    # visits `logicExpr: func=('any_item'|'all_items') '(' logicExpr')'`
    def visitFuncAnyAllItem(self, ctx:RegLangParser.FuncAnyAllItemContext):
        funcname = ctx.func.text
        if funcname == "any_item":
            self.funcAnyItemFlag = True
            return self.visit(ctx.logicExpr())
        elif funcname == "all_items":
            self.funcAllItemFlag = True
            return self.visit(ctx.logicExpr())
        else:
            logger.warning("parse error: FuncAnyAllItem")

    def __compareTwoArithExpr(self, op, opText, left, right):
        result = None
        if op == RegLangParser.EQ:
            try:
                result = ( self._stringToInt(left) == self._stringToInt(right) or left == right or str(left).lower() == str(right).lower() )
            except:
                result = ( left == right or str(left).lower() == str(right).lower() )
        elif op == RegLangParser.NOTEQ:
            try:
                result = ( self._stringToInt(left) != self._stringToInt(right) and left != right and str(left).lower() != str(right).lower() )
            except:
                result = ( left != right and str(left).lower() != str(right).lower() )
        elif op == RegLangParser.LESS:
            try:
                result = ( self._stringToInt(left) < self._stringToInt(right) )
            except:
                result = ( left < right )
        elif op == RegLangParser.LESSEQ:
            try:
                result = ( self._stringToInt(left) <= self._stringToInt(right) )
            except:
                result = ( left <= right )
        elif op == RegLangParser.GREATER:
            try:
                result = ( self._stringToInt(left) > self._stringToInt(right) )
            except:
                result = ( left > right )
        elif op == RegLangParser.GREATEREQ:
            try:
                result = ( self._stringToInt(left) >= self._stringToInt(right) )
            except:
                result = ( left >= right )
        else:
            logger.warning("parse error: TwoArithExprComparison")
        logger.debug("Calculating logic expr: %s %s %s (%s)"%(left, opText, right, result))
        return result

    # visits `logicExpr: arithExpr op=('=='|'!='|'<'|'<='|'>'|'>=') arithExpr`
    def visitTwoArithExprComparison(self, ctx: RegLangParser.TwoArithExprComparisonContext):
        left = self.visit(ctx.arithExpr(0))
        right = self.visit(ctx.arithExpr(1))
        op = ctx.op.type
        opText = ctx.op.text
        # logger.debug('left: %s, type: %s' % (str(left), type(left)))
        # logger.debug('right: %s, type: %s' % (str(right), type(right)))
        if self.funcLeastMostFlag:
            self.funcLeastMostFlag = False
            if isinstance(left, list):
                count = 0
                for item in left:
                    if self.__compareTwoArithExpr(op, opText, item, right):
                        count += 1
                logger.debug("Arg result in at_least/at_most: %d"%count)
                return count
            else:
                logger.warning("Left side of Arg1 in at_least/at_most is not array.")
        elif self.funcAnyItemFlag:
            self.funcAnyItemFlag = False
            if isinstance(left, list):
                for item in left:
                    if self.__compareTwoArithExpr(op, opText, item, right):
                        logger.debug("Arg result in any_item: True")
                        return True
                logger.debug("Arg result in any_item: False")
                return False
            else:
                logger.warning("Left side of Arg1 in any_item is not array.")
        elif self.funcAllItemFlag:
            self.funcAllItemFlag = False
            if isinstance(left, list):
                for item in left:
                    if not self.__compareTwoArithExpr(op, opText, item, right):
                        logger.debug("Comparing result in all_items: False")
                        return False
                logger.debug("Comparing result in all_items: True")
                return True
            else:
                logger.warning("Left side of Arg1 in all_items is not array.")
        else:
            return self.__compareTwoArithExpr(op, opText, left, right)

    # visits `logicExpr: logicExpr op=('and'|'or') logicExpr`
    def visitTwoCalcLogicExprLogicOperation(self, ctx: RegLangParser.TwoCalcLogicExprLogicOperationContext):
        if self.funcLeastMostFlag or self.funcAnyItemFlag or self.funcAllItemFlag:
            logger.warning("Internal functions at_least(), at_most(), any_item(), all_items() do not support and/or in logic expression.")
            return
        left = self.visit(ctx.logicExpr(0))
        right = self.visit(ctx.logicExpr(1))
        op = ctx.op.type
        if op == RegLangParser.AND:
            return left and right
        elif op == RegLangParser.OR:
            return left or right
        else:
            logger.warning("parse error: TwoCalcLogicExprLogicOperation")

    # visits `logicExpr: '(' logicExpr ')'`
    def visitParentheseLogicExprAsLogicExpr(self, ctx: RegLangParser.ParentheseLogicExprAsLogicExprContext):
        return self.visit(ctx.logicExpr())

    # visits `logicExpr: boolExpr`
    def visitBoolExprAsLogicExpr(self, ctx: RegLangParser.BoolExprAsLogicExprContext):
        op = ctx.op.type
        if op == RegLangParser.TRUE:
            return True
        elif op == RegLangParser.FALSE:
            return False
        else:
            logger.warning("parse error: BoolExprAsLogicExpr")

    # visits `arithExpr: 'length' '(' arithExpr ')'`
    def visitFuncArrayLength(self, ctx:RegLangParser.FuncArrayLengthContext):
        arg = self.visit(ctx.arithExpr())
        if isinstance(arg, list):
            arg_len = len(arg)
            logger.debug("Calculating Array (%s) Length %d"%(arg, arg_len))
            return arg_len
        else:
            logger.warning("Argument in length() is not array. (%s)"%arg)

    # visits `arithExpr: 'count' '(' logicExpr (',' logicExpr)* ')'`
    def visitFuncCountBool(self, ctx:RegLangParser.FuncCountBoolContext):
        count = 0
        for expr in ctx.logicExpr():
            if self.visit(expr):
                count += 1
        logger.debug("Calculating count() result: %d"%count)
        return count

    # visits `arithExpr: <assoc=right> arithExpr POW arithExpr`
    def visitCalcPow(self, ctx: RegLangParser.CalcPowContext):
        left = self._stringToInt(self.visit(ctx.arithExpr(0)))
        right = self._stringToInt(self.visit(ctx.arithExpr(1)))
        return left ** right

    # visits `arithExpr: arithExpr op=('*'|'/'|'%') arithExpr`
    def visitCalcMulDivMod(self, ctx: RegLangParser.CalcMulDivModContext):
        left = self._stringToInt(self.visit(ctx.arithExpr(0)))
        right = self._stringToInt(self.visit(ctx.arithExpr(1)))
        op = ctx.op.type
        if op == RegLangParser.MUL:
            return left * right
        elif op == RegLangParser.DIV:
            return left // right
        elif op == RegLangParser.MOD:
            return left % right
        else:
            logger.warning("parse error: CalcMulDivMod")

    # visits `arithExpr: arithExpr op=('+'|'-') arithExpr`
    def visitCalcAddSub(self, ctx: RegLangParser.CalcAddSubContext):
        left = self._stringToInt(self.visit(ctx.arithExpr(0)))
        right = self._stringToInt(self.visit(ctx.arithExpr(1)))
        op = ctx.op.type
        if op == RegLangParser.ADD:
            return left + right
        elif op == RegLangParser.SUB:
            result = left - right
            if result < 0:
                return 0
            else:
                return result
        else:
            logger.warning("parse error: CalcAddSub")

    # visits `arithExpr: '(' arithExpr ')'`
    def visitParentheseArithExprAsArithExpr(self, ctx: RegLangParser.ParentheseArithExprAsArithExprContext):
        return self.visit(ctx.arithExpr())

    # visits `arithExpr: varSymbol`
    def visitVariableAsArithExpr(self, ctx: RegLangParser.VariableAsArithExprContext):
        return self.visit(ctx.varSymbol())

    # visits `array: '[' number (',' number)* ']'`
    def visitNumberArray(self, ctx:RegLangParser.NumberArrayContext):
        numberArray = []
        numbers = ctx.number()
        for number in numbers:
            numberArray.append(self.visit(number))
        return numberArray

    # visits `array: '[' STRING (',' STRING)* ']'`
    def visitStringArray(self, ctx:RegLangParser.StringArrayContext):
        stringArray = []
        strings = ctx.STRING()
        for string in strings:
            stringArray.append(string.getText()[1:-1].lower())
        logger.debug("Parse array: %s"%stringArray)
        return stringArray

    # visits `arithExpr: STRING`
    def visitStringAsArithExpr(self, ctx: RegLangParser.StringAsArithExprContext):
        string = ctx.STRING().getText()[1:-1].lower()
        logger.debug("Parse string: %s"%string)
        return string

    # visits `number: INT`
    def visitNumber(self, ctx: RegLangParser.NumberContext):
        number =self._stringToInt(ctx.INT().getText())
        logger.debug("Parse number: %d"%number)
        return number

    # visits `varSymbol : 'tx' '.' info=('from'|'to'|'function')`
    def visitTxBasicInfo(self, ctx:RegLangParser.TxBasicInfoContext):
        info = ctx.info.text
        if info == 'from':
            logger.debug('Fetch tx.from: %s' % self.tx.fromAddr)
            return self.tx.fromAddr
        elif info == 'to':
            logger.debug('Fetch tx.to: %s' % self.tx.toAddr)
            return self.tx.toAddr
        elif info == 'function':
            logger.debug('Fetch tx.function: %s' % self.tx.function)
            return self.tx.function
        else:
            logger.warning("parse error: TxBasicInfo")

    # visits  `varSymbol : 'tx' '.' info=('readset'|'writeset') '(' arithExpr ')' '.' varSymbol`
    def visitTxReadWriteSets(self, ctx:RegLangParser.TxReadWriteSetsContext):
        addr = self.visit(ctx.arithExpr())
        setType = ctx.info.text
        if setType == 'readset':
            var = ReadSetVar(self.tx, addr, ctx.varSymbol().getText())
            if self.arrayFlag:
                return var
            else: 
                logger.debug("Fetch readset value: %s" % var.getValue())
                return var.getValue()
        elif setType == 'writeset':
            var = WriteSetVar(self.tx, addr, ctx.varSymbol().getText())
            if self.arrayFlag:
                return var
            else: 
                logger.debug("Fetch writeset value: %s" % var.getValue())
                return var.getValue()
        else:
            logger.warning("parse error: TxReadWriteSets")

    # visits `varSymbol : 'tx' '.' 'args' . varSymbol`
    def visitTxArgs(self, ctx:RegLangParser.TxArgsContext):
        # logger.debug(ctx.varSymbol().getText())
        # logger.debug(self.tx.args[ctx.varSymbol().getText()])
        return(self.tx.args[ctx.varSymbol().getText()])

    # visits `varSymbol : varSymbol '[' arithExpr ']'`
    def visitArrayItem(self, ctx:RegLangParser.ArrayItemContext):
        self.arrayFlag = True
        array = self.visit(ctx.varSymbol())
        index = self.visit(ctx.arithExpr())
        self.arrayFlag = False
        if isinstance(array, list):
            return array[index]
        elif isinstance(array, ReadSetVar) or isinstance(array, WriteSetVar):
            # logger.debug("Fetch readset/writeset value: %s" % array.getValue(index))
            return array.getValue(index)
        elif isinstance(array, ContractStateVar):
            # logger.debug("Fetch contract state value: %s" % array.getValue(index))
            return array.getValue(index)
        else:
            logger.warning("parse error: ArrayItem")

    # visits `varSymbol: 'contract' '(' arithExpr ')' '.' info=('name'|'owner')`
    def visitContractInfo(self, ctx:RegLangParser.ContractInfoContext):
        contractAddr = self.visit(ctx.arithExpr())
        infoType = ctx.info.text
        contract = self.tx.contracts.get_contract(contractAddr)
        if infoType == "name":
            # logger.debug("Fetch contract(%s).name: %s"%(contractAddr,contract.contractName))
            return contract.contractName
        elif infoType == "owner":
            # logger.debug("Fetch contract(%s).owner: %s"%(contractAddr,contract.contractOwner))
            return contract.contractOwner
        else:
            logger.warning("parse error: ContractInfo")

    # visits `varSymbol: 'contract' '(' arithExpr ')' '.' 'state' '.' varSymbol`
    def visitContractState(self, ctx:RegLangParser.ContractStateContext):
        contractAddr = self.visit(ctx.arithExpr())
        var = ContractStateVar(self.tx, contractAddr, ctx.varSymbol().getText())
        if self.arrayFlag:
            return var
        else: 
            # logger.debug("Fetch contract state value: %s" % var.getValue())
            return var.getValue()
    
    # visits `varSymbol: 'knowledgebase' '(' ID ')' '.' ID `
    def visitKnowledgeVar(self, ctx:RegLangParser.KnowledgeVarContext):
        knowledgebaseName = ctx.ID(0).getText()
        knoledgeName = ctx.ID(1).getText()
        return self.knowledgebases[knowledgebaseName][knoledgeName]

class RegLang:
    def __init__(self, rules, tx):
        logger.debug("Welcome to RegLang %s" % config.VERSION)
        lexer = RegLangLexer(InputStream(rules))
        stream = CommonTokenStream(lexer)
        parser = RegLangParser(stream)
        self.tree = parser.prog()
        print(self.tree.depth())
        self.v = Visitor(tx)
    
    def regulate(self):
        return self.v.visit(self.tree)


