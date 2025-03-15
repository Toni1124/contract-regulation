// Generated from RegLang.g4 by ANTLR 4.9.2
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link RegLangParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface RegLangVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link RegLangParser#prog}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProg(RegLangParser.ProgContext ctx);
	/**
	 * Visit a parse tree produced by {@link RegLangParser#knowledgebaseBlock}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitKnowledgebaseBlock(RegLangParser.KnowledgebaseBlockContext ctx);
	/**
	 * Visit a parse tree produced by the {@code KnowledgeAssign}
	 * labeled alternative in {@link RegLangParser#knowledgeDecl}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitKnowledgeAssign(RegLangParser.KnowledgeAssignContext ctx);
	/**
	 * Visit a parse tree produced by the {@code KnowledgeFunc}
	 * labeled alternative in {@link RegLangParser#knowledgeDecl}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitKnowledgeFunc(RegLangParser.KnowledgeFuncContext ctx);
	/**
	 * Visit a parse tree produced by {@link RegLangParser#ruleBlock}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRuleBlock(RegLangParser.RuleBlockContext ctx);
	/**
	 * Visit a parse tree produced by {@link RegLangParser#regScopeStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRegScopeStmt(RegLangParser.RegScopeStmtContext ctx);
	/**
	 * Visit a parse tree produced by the {@code RequireReg}
	 * labeled alternative in {@link RegLangParser#regRuleStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRequireReg(RegLangParser.RequireRegContext ctx);
	/**
	 * Visit a parse tree produced by the {@code ProhibitReg}
	 * labeled alternative in {@link RegLangParser#regRuleStmt}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProhibitReg(RegLangParser.ProhibitRegContext ctx);
	/**
	 * Visit a parse tree produced by the {@code FuncLeastMost}
	 * labeled alternative in {@link RegLangParser#logicExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFuncLeastMost(RegLangParser.FuncLeastMostContext ctx);
	/**
	 * Visit a parse tree produced by the {@code FuncAnyAllItem}
	 * labeled alternative in {@link RegLangParser#logicExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFuncAnyAllItem(RegLangParser.FuncAnyAllItemContext ctx);
	/**
	 * Visit a parse tree produced by the {@code InternalFunctionIn}
	 * labeled alternative in {@link RegLangParser#logicExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInternalFunctionIn(RegLangParser.InternalFunctionInContext ctx);
	/**
	 * Visit a parse tree produced by the {@code ParentheseLogicExprAsLogicExpr}
	 * labeled alternative in {@link RegLangParser#logicExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParentheseLogicExprAsLogicExpr(RegLangParser.ParentheseLogicExprAsLogicExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code TwoArithExprComparison}
	 * labeled alternative in {@link RegLangParser#logicExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTwoArithExprComparison(RegLangParser.TwoArithExprComparisonContext ctx);
	/**
	 * Visit a parse tree produced by the {@code TwoCalcLogicExprLogicOperation}
	 * labeled alternative in {@link RegLangParser#logicExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTwoCalcLogicExprLogicOperation(RegLangParser.TwoCalcLogicExprLogicOperationContext ctx);
	/**
	 * Visit a parse tree produced by the {@code BoolExprAsLogicExpr}
	 * labeled alternative in {@link RegLangParser#logicExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBoolExprAsLogicExpr(RegLangParser.BoolExprAsLogicExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code StringAsArithExpr}
	 * labeled alternative in {@link RegLangParser#arithExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStringAsArithExpr(RegLangParser.StringAsArithExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code ConstantArray}
	 * labeled alternative in {@link RegLangParser#arithExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConstantArray(RegLangParser.ConstantArrayContext ctx);
	/**
	 * Visit a parse tree produced by the {@code CalcPow}
	 * labeled alternative in {@link RegLangParser#arithExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCalcPow(RegLangParser.CalcPowContext ctx);
	/**
	 * Visit a parse tree produced by the {@code CalcMulDivMod}
	 * labeled alternative in {@link RegLangParser#arithExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCalcMulDivMod(RegLangParser.CalcMulDivModContext ctx);
	/**
	 * Visit a parse tree produced by the {@code ParentheseArithExprAsArithExpr}
	 * labeled alternative in {@link RegLangParser#arithExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParentheseArithExprAsArithExpr(RegLangParser.ParentheseArithExprAsArithExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code VariableAsArithExpr}
	 * labeled alternative in {@link RegLangParser#arithExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVariableAsArithExpr(RegLangParser.VariableAsArithExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code FuncArrayLength}
	 * labeled alternative in {@link RegLangParser#arithExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFuncArrayLength(RegLangParser.FuncArrayLengthContext ctx);
	/**
	 * Visit a parse tree produced by the {@code NumberAsArithExpr}
	 * labeled alternative in {@link RegLangParser#arithExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNumberAsArithExpr(RegLangParser.NumberAsArithExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code CalcAddSub}
	 * labeled alternative in {@link RegLangParser#arithExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCalcAddSub(RegLangParser.CalcAddSubContext ctx);
	/**
	 * Visit a parse tree produced by the {@code FuncCountBool}
	 * labeled alternative in {@link RegLangParser#arithExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFuncCountBool(RegLangParser.FuncCountBoolContext ctx);
	/**
	 * Visit a parse tree produced by the {@code TxArgs}
	 * labeled alternative in {@link RegLangParser#varSymbol}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTxArgs(RegLangParser.TxArgsContext ctx);
	/**
	 * Visit a parse tree produced by the {@code ContractInfo}
	 * labeled alternative in {@link RegLangParser#varSymbol}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitContractInfo(RegLangParser.ContractInfoContext ctx);
	/**
	 * Visit a parse tree produced by the {@code KnowledgeVar}
	 * labeled alternative in {@link RegLangParser#varSymbol}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitKnowledgeVar(RegLangParser.KnowledgeVarContext ctx);
	/**
	 * Visit a parse tree produced by the {@code ArrayItem}
	 * labeled alternative in {@link RegLangParser#varSymbol}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArrayItem(RegLangParser.ArrayItemContext ctx);
	/**
	 * Visit a parse tree produced by the {@code BracketArithExprToVarSymbol}
	 * labeled alternative in {@link RegLangParser#varSymbol}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBracketArithExprToVarSymbol(RegLangParser.BracketArithExprToVarSymbolContext ctx);
	/**
	 * Visit a parse tree produced by the {@code ContractState}
	 * labeled alternative in {@link RegLangParser#varSymbol}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitContractState(RegLangParser.ContractStateContext ctx);
	/**
	 * Visit a parse tree produced by the {@code TxBasicInfo}
	 * labeled alternative in {@link RegLangParser#varSymbol}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTxBasicInfo(RegLangParser.TxBasicInfoContext ctx);
	/**
	 * Visit a parse tree produced by the {@code ParentheseArithExprAsVarSymbol}
	 * labeled alternative in {@link RegLangParser#varSymbol}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParentheseArithExprAsVarSymbol(RegLangParser.ParentheseArithExprAsVarSymbolContext ctx);
	/**
	 * Visit a parse tree produced by the {@code IdAsVarSymbol}
	 * labeled alternative in {@link RegLangParser#varSymbol}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIdAsVarSymbol(RegLangParser.IdAsVarSymbolContext ctx);
	/**
	 * Visit a parse tree produced by the {@code ParentheseVarSymbolAsVarSymbol}
	 * labeled alternative in {@link RegLangParser#varSymbol}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParentheseVarSymbolAsVarSymbol(RegLangParser.ParentheseVarSymbolAsVarSymbolContext ctx);
	/**
	 * Visit a parse tree produced by the {@code TxReadWriteSets}
	 * labeled alternative in {@link RegLangParser#varSymbol}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTxReadWriteSets(RegLangParser.TxReadWriteSetsContext ctx);
	/**
	 * Visit a parse tree produced by {@link RegLangParser#number}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNumber(RegLangParser.NumberContext ctx);
	/**
	 * Visit a parse tree produced by the {@code NumberArray}
	 * labeled alternative in {@link RegLangParser#array}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNumberArray(RegLangParser.NumberArrayContext ctx);
	/**
	 * Visit a parse tree produced by the {@code StringArray}
	 * labeled alternative in {@link RegLangParser#array}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStringArray(RegLangParser.StringArrayContext ctx);
	/**
	 * Visit a parse tree produced by {@link RegLangParser#comparisonOp}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComparisonOp(RegLangParser.ComparisonOpContext ctx);
	/**
	 * Visit a parse tree produced by {@link RegLangParser#logicOp}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLogicOp(RegLangParser.LogicOpContext ctx);
	/**
	 * Visit a parse tree produced by {@link RegLangParser#boolExpr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBoolExpr(RegLangParser.BoolExprContext ctx);
}