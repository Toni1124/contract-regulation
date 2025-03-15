# Generated from d:\OneDrive\OneDrive - pku.edu.cn\Papers\RegLangInterpreter\reglang\RegLang.g4 by ANTLR 4.8
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .RegLangParser import RegLangParser
else:
    from RegLangParser import RegLangParser


# This class defines a complete generic visitor for a parse tree produced by RegLangParser.

class RegLangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by RegLangParser#prog.
    def visitProg(self, ctx: RegLangParser.ProgContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#knowledgebaseBlock.
    def visitKnowledgebaseBlock(self, ctx: RegLangParser.KnowledgebaseBlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#KnowledgeAssign.
    def visitKnowledgeAssign(self, ctx: RegLangParser.KnowledgeAssignContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#KnowledgeFunc.
    def visitKnowledgeFunc(self, ctx: RegLangParser.KnowledgeFuncContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#ruleBlock.
    def visitRuleBlock(self, ctx: RegLangParser.RuleBlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#regScopeStmt.
    def visitRegScopeStmt(self, ctx: RegLangParser.RegScopeStmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#RequireReg.
    def visitRequireReg(self, ctx: RegLangParser.RequireRegContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#ProhibitReg.
    def visitProhibitReg(self, ctx: RegLangParser.ProhibitRegContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#FuncLeastMost.
    def visitFuncLeastMost(self, ctx: RegLangParser.FuncLeastMostContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#FuncAnyAllItem.
    def visitFuncAnyAllItem(self, ctx: RegLangParser.FuncAnyAllItemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#InternalFunctionIn.
    def visitInternalFunctionIn(self, ctx: RegLangParser.InternalFunctionInContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#ParentheseLogicExprAsLogicExpr.
    def visitParentheseLogicExprAsLogicExpr(self, ctx: RegLangParser.ParentheseLogicExprAsLogicExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#TwoArithExprComparison.
    def visitTwoArithExprComparison(self, ctx: RegLangParser.TwoArithExprComparisonContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#TwoCalcLogicExprLogicOperation.
    def visitTwoCalcLogicExprLogicOperation(self, ctx: RegLangParser.TwoCalcLogicExprLogicOperationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#BoolExprAsLogicExpr.
    def visitBoolExprAsLogicExpr(self, ctx: RegLangParser.BoolExprAsLogicExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#StringAsArithExpr.
    def visitStringAsArithExpr(self, ctx: RegLangParser.StringAsArithExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#ConstantArray.
    def visitConstantArray(self, ctx: RegLangParser.ConstantArrayContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#CalcPow.
    def visitCalcPow(self, ctx: RegLangParser.CalcPowContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#CalcMulDivMod.
    def visitCalcMulDivMod(self, ctx: RegLangParser.CalcMulDivModContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#ParentheseArithExprAsArithExpr.
    def visitParentheseArithExprAsArithExpr(self, ctx: RegLangParser.ParentheseArithExprAsArithExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#VariableAsArithExpr.
    def visitVariableAsArithExpr(self, ctx: RegLangParser.VariableAsArithExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#FuncArrayLength.
    def visitFuncArrayLength(self, ctx: RegLangParser.FuncArrayLengthContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#NumberAsArithExpr.
    def visitNumberAsArithExpr(self, ctx: RegLangParser.NumberAsArithExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#CalcAddSub.
    def visitCalcAddSub(self, ctx: RegLangParser.CalcAddSubContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#FuncCountBool.
    def visitFuncCountBool(self, ctx: RegLangParser.FuncCountBoolContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#TxArgs.
    def visitTxArgs(self, ctx: RegLangParser.TxArgsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#ContractInfo.
    def visitContractInfo(self, ctx: RegLangParser.ContractInfoContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#KnowledgeVar.
    def visitKnowledgeVar(self, ctx: RegLangParser.KnowledgeVarContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#ArrayItem.
    def visitArrayItem(self, ctx: RegLangParser.ArrayItemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#BracketArithExprToVarSymbol.
    def visitBracketArithExprToVarSymbol(self, ctx: RegLangParser.BracketArithExprToVarSymbolContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#ContractState.
    def visitContractState(self, ctx: RegLangParser.ContractStateContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#TxBasicInfo.
    def visitTxBasicInfo(self, ctx: RegLangParser.TxBasicInfoContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#ParentheseArithExprAsVarSymbol.
    def visitParentheseArithExprAsVarSymbol(self, ctx: RegLangParser.ParentheseArithExprAsVarSymbolContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#IdAsVarSymbol.
    def visitIdAsVarSymbol(self, ctx: RegLangParser.IdAsVarSymbolContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#ParentheseVarSymbolAsVarSymbol.
    def visitParentheseVarSymbolAsVarSymbol(self, ctx: RegLangParser.ParentheseVarSymbolAsVarSymbolContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#TxReadWriteSets.
    def visitTxReadWriteSets(self, ctx: RegLangParser.TxReadWriteSetsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#number.
    def visitNumber(self, ctx: RegLangParser.NumberContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#NumberArray.
    def visitNumberArray(self, ctx: RegLangParser.NumberArrayContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#StringArray.
    def visitStringArray(self, ctx: RegLangParser.StringArrayContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#comparisonOp.
    def visitComparisonOp(self, ctx: RegLangParser.ComparisonOpContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#logicOp.
    def visitLogicOp(self, ctx: RegLangParser.LogicOpContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by RegLangParser#boolExpr.
    def visitBoolExpr(self, ctx: RegLangParser.BoolExprContext):
        return self.visitChildren(ctx)


del RegLangParser
