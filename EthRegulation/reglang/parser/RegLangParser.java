// Generated from RegLang.g4 by ANTLR 4.9.2
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class RegLangParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.9.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, T__12=13, T__13=14, T__14=15, T__15=16, T__16=17, 
		T__17=18, T__18=19, T__19=20, T__20=21, T__21=22, T__22=23, T__23=24, 
		T__24=25, T__25=26, T__26=27, T__27=28, T__28=29, T__29=30, T__30=31, 
		T__31=32, T__32=33, T__33=34, T__34=35, T__35=36, ADD=37, SUB=38, MUL=39, 
		DIV=40, MOD=41, POW=42, EQ=43, NOTEQ=44, LESSEQ=45, GREATEREQ=46, LESS=47, 
		GREATER=48, AND=49, OR=50, TRUE=51, FALSE=52, LINE_COMMENT=53, COMMENT=54, 
		WS=55, INT=56, DIGIT=57, ID=58, ID_LETTER=59, STRING=60;
	public static final int
		RULE_prog = 0, RULE_knowledgebaseBlock = 1, RULE_knowledgeDecl = 2, RULE_ruleBlock = 3, 
		RULE_regScopeStmt = 4, RULE_regRuleStmt = 5, RULE_logicExpr = 6, RULE_arithExpr = 7, 
		RULE_varSymbol = 8, RULE_number = 9, RULE_array = 10, RULE_comparisonOp = 11, 
		RULE_logicOp = 12, RULE_boolExpr = 13;
	private static String[] makeRuleNames() {
		return new String[] {
			"prog", "knowledgebaseBlock", "knowledgeDecl", "ruleBlock", "regScopeStmt", 
			"regRuleStmt", "logicExpr", "arithExpr", "varSymbol", "number", "array", 
			"comparisonOp", "logicOp", "boolExpr"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'knowledgebase'", "'end'", "'knowledge'", "'='", "';'", "'.'", 
			"'add'", "'del'", "'('", "')'", "'rule'", "'reg'", "':'", "'require'", 
			"'prohibit'", "'in'", "'at_least'", "'at_most'", "','", "'any_item'", 
			"'all_items'", "'length'", "'count'", "'tx'", "'from'", "'to'", "'function'", 
			"'readset'", "'writeset'", "'args'", "'contract'", "'name'", "'owner'", 
			"'state'", "'['", "']'", "'+'", "'-'", "'*'", "'/'", "'%'", "'^'", "'=='", 
			"'!='", "'<='", "'>='", "'<'", "'>'", "'and'", "'or'", "'true'", "'false'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, "ADD", "SUB", "MUL", "DIV", "MOD", "POW", "EQ", "NOTEQ", "LESSEQ", 
			"GREATEREQ", "LESS", "GREATER", "AND", "OR", "TRUE", "FALSE", "LINE_COMMENT", 
			"COMMENT", "WS", "INT", "DIGIT", "ID", "ID_LETTER", "STRING"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "RegLang.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public RegLangParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	public static class ProgContext extends ParserRuleContext {
		public List<KnowledgebaseBlockContext> knowledgebaseBlock() {
			return getRuleContexts(KnowledgebaseBlockContext.class);
		}
		public KnowledgebaseBlockContext knowledgebaseBlock(int i) {
			return getRuleContext(KnowledgebaseBlockContext.class,i);
		}
		public List<RuleBlockContext> ruleBlock() {
			return getRuleContexts(RuleBlockContext.class);
		}
		public RuleBlockContext ruleBlock(int i) {
			return getRuleContext(RuleBlockContext.class,i);
		}
		public ProgContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_prog; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitProg(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ProgContext prog() throws RecognitionException {
		ProgContext _localctx = new ProgContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_prog);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(32);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__0 || _la==T__10) {
				{
				setState(30);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case T__0:
					{
					setState(28);
					knowledgebaseBlock();
					}
					break;
				case T__10:
					{
					setState(29);
					ruleBlock();
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				}
				setState(34);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class KnowledgebaseBlockContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(RegLangParser.ID, 0); }
		public List<KnowledgeDeclContext> knowledgeDecl() {
			return getRuleContexts(KnowledgeDeclContext.class);
		}
		public KnowledgeDeclContext knowledgeDecl(int i) {
			return getRuleContext(KnowledgeDeclContext.class,i);
		}
		public KnowledgebaseBlockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_knowledgebaseBlock; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitKnowledgebaseBlock(this);
			else return visitor.visitChildren(this);
		}
	}

	public final KnowledgebaseBlockContext knowledgebaseBlock() throws RecognitionException {
		KnowledgebaseBlockContext _localctx = new KnowledgebaseBlockContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_knowledgebaseBlock);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(35);
			match(T__0);
			setState(36);
			match(ID);
			setState(38); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(37);
				knowledgeDecl();
				}
				}
				setState(40); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==T__2 || _la==ID );
			setState(42);
			match(T__1);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class KnowledgeDeclContext extends ParserRuleContext {
		public KnowledgeDeclContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_knowledgeDecl; }
	 
		public KnowledgeDeclContext() { }
		public void copyFrom(KnowledgeDeclContext ctx) {
			super.copyFrom(ctx);
		}
	}
	public static class KnowledgeAssignContext extends KnowledgeDeclContext {
		public TerminalNode ID() { return getToken(RegLangParser.ID, 0); }
		public ArithExprContext arithExpr() {
			return getRuleContext(ArithExprContext.class,0);
		}
		public KnowledgeAssignContext(KnowledgeDeclContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitKnowledgeAssign(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class KnowledgeFuncContext extends KnowledgeDeclContext {
		public Token op;
		public TerminalNode ID() { return getToken(RegLangParser.ID, 0); }
		public ArithExprContext arithExpr() {
			return getRuleContext(ArithExprContext.class,0);
		}
		public KnowledgeFuncContext(KnowledgeDeclContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitKnowledgeFunc(this);
			else return visitor.visitChildren(this);
		}
	}

	public final KnowledgeDeclContext knowledgeDecl() throws RecognitionException {
		KnowledgeDeclContext _localctx = new KnowledgeDeclContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_knowledgeDecl);
		int _la;
		try {
			setState(58);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__2:
				_localctx = new KnowledgeAssignContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(44);
				match(T__2);
				setState(45);
				match(ID);
				setState(46);
				match(T__3);
				setState(47);
				arithExpr(0);
				setState(48);
				match(T__4);
				}
				break;
			case ID:
				_localctx = new KnowledgeFuncContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(50);
				match(ID);
				setState(51);
				match(T__5);
				setState(52);
				((KnowledgeFuncContext)_localctx).op = _input.LT(1);
				_la = _input.LA(1);
				if ( !(_la==T__6 || _la==T__7) ) {
					((KnowledgeFuncContext)_localctx).op = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(53);
				match(T__8);
				setState(54);
				arithExpr(0);
				setState(55);
				match(T__9);
				setState(56);
				match(T__4);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class RuleBlockContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(RegLangParser.ID, 0); }
		public RegScopeStmtContext regScopeStmt() {
			return getRuleContext(RegScopeStmtContext.class,0);
		}
		public List<RegRuleStmtContext> regRuleStmt() {
			return getRuleContexts(RegRuleStmtContext.class);
		}
		public RegRuleStmtContext regRuleStmt(int i) {
			return getRuleContext(RegRuleStmtContext.class,i);
		}
		public RuleBlockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ruleBlock; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitRuleBlock(this);
			else return visitor.visitChildren(this);
		}
	}

	public final RuleBlockContext ruleBlock() throws RecognitionException {
		RuleBlockContext _localctx = new RuleBlockContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_ruleBlock);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(60);
			match(T__10);
			setState(61);
			match(ID);
			setState(62);
			regScopeStmt();
			setState(66);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__13 || _la==T__14) {
				{
				{
				setState(63);
				regRuleStmt();
				}
				}
				setState(68);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(69);
			match(T__1);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class RegScopeStmtContext extends ParserRuleContext {
		public LogicExprContext logicExpr() {
			return getRuleContext(LogicExprContext.class,0);
		}
		public RegScopeStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_regScopeStmt; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitRegScopeStmt(this);
			else return visitor.visitChildren(this);
		}
	}

	public final RegScopeStmtContext regScopeStmt() throws RecognitionException {
		RegScopeStmtContext _localctx = new RegScopeStmtContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_regScopeStmt);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(71);
			match(T__11);
			setState(72);
			logicExpr(0);
			setState(73);
			match(T__12);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class RegRuleStmtContext extends ParserRuleContext {
		public RegRuleStmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_regRuleStmt; }
	 
		public RegRuleStmtContext() { }
		public void copyFrom(RegRuleStmtContext ctx) {
			super.copyFrom(ctx);
		}
	}
	public static class RequireRegContext extends RegRuleStmtContext {
		public LogicExprContext logicExpr() {
			return getRuleContext(LogicExprContext.class,0);
		}
		public RequireRegContext(RegRuleStmtContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitRequireReg(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class ProhibitRegContext extends RegRuleStmtContext {
		public LogicExprContext logicExpr() {
			return getRuleContext(LogicExprContext.class,0);
		}
		public ProhibitRegContext(RegRuleStmtContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitProhibitReg(this);
			else return visitor.visitChildren(this);
		}
	}

	public final RegRuleStmtContext regRuleStmt() throws RecognitionException {
		RegRuleStmtContext _localctx = new RegRuleStmtContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_regRuleStmt);
		try {
			setState(83);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__13:
				_localctx = new RequireRegContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(75);
				match(T__13);
				setState(76);
				logicExpr(0);
				setState(77);
				match(T__4);
				}
				break;
			case T__14:
				_localctx = new ProhibitRegContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(79);
				match(T__14);
				setState(80);
				logicExpr(0);
				setState(81);
				match(T__4);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class LogicExprContext extends ParserRuleContext {
		public LogicExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_logicExpr; }
	 
		public LogicExprContext() { }
		public void copyFrom(LogicExprContext ctx) {
			super.copyFrom(ctx);
		}
	}
	public static class FuncLeastMostContext extends LogicExprContext {
		public Token func;
		public ArithExprContext arithExpr() {
			return getRuleContext(ArithExprContext.class,0);
		}
		public LogicExprContext logicExpr() {
			return getRuleContext(LogicExprContext.class,0);
		}
		public FuncLeastMostContext(LogicExprContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitFuncLeastMost(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class FuncAnyAllItemContext extends LogicExprContext {
		public Token func;
		public LogicExprContext logicExpr() {
			return getRuleContext(LogicExprContext.class,0);
		}
		public FuncAnyAllItemContext(LogicExprContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitFuncAnyAllItem(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class InternalFunctionInContext extends LogicExprContext {
		public ArithExprContext arithExpr() {
			return getRuleContext(ArithExprContext.class,0);
		}
		public List<TerminalNode> ID() { return getTokens(RegLangParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(RegLangParser.ID, i);
		}
		public InternalFunctionInContext(LogicExprContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitInternalFunctionIn(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class ParentheseLogicExprAsLogicExprContext extends LogicExprContext {
		public LogicExprContext logicExpr() {
			return getRuleContext(LogicExprContext.class,0);
		}
		public ParentheseLogicExprAsLogicExprContext(LogicExprContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitParentheseLogicExprAsLogicExpr(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class TwoArithExprComparisonContext extends LogicExprContext {
		public Token op;
		public List<ArithExprContext> arithExpr() {
			return getRuleContexts(ArithExprContext.class);
		}
		public ArithExprContext arithExpr(int i) {
			return getRuleContext(ArithExprContext.class,i);
		}
		public TerminalNode EQ() { return getToken(RegLangParser.EQ, 0); }
		public TerminalNode NOTEQ() { return getToken(RegLangParser.NOTEQ, 0); }
		public TerminalNode LESS() { return getToken(RegLangParser.LESS, 0); }
		public TerminalNode LESSEQ() { return getToken(RegLangParser.LESSEQ, 0); }
		public TerminalNode GREATER() { return getToken(RegLangParser.GREATER, 0); }
		public TerminalNode GREATEREQ() { return getToken(RegLangParser.GREATEREQ, 0); }
		public TwoArithExprComparisonContext(LogicExprContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitTwoArithExprComparison(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class TwoCalcLogicExprLogicOperationContext extends LogicExprContext {
		public Token op;
		public List<LogicExprContext> logicExpr() {
			return getRuleContexts(LogicExprContext.class);
		}
		public LogicExprContext logicExpr(int i) {
			return getRuleContext(LogicExprContext.class,i);
		}
		public TerminalNode AND() { return getToken(RegLangParser.AND, 0); }
		public TerminalNode OR() { return getToken(RegLangParser.OR, 0); }
		public TwoCalcLogicExprLogicOperationContext(LogicExprContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitTwoCalcLogicExprLogicOperation(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class BoolExprAsLogicExprContext extends LogicExprContext {
		public Token op;
		public TerminalNode TRUE() { return getToken(RegLangParser.TRUE, 0); }
		public TerminalNode FALSE() { return getToken(RegLangParser.FALSE, 0); }
		public BoolExprAsLogicExprContext(LogicExprContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitBoolExprAsLogicExpr(this);
			else return visitor.visitChildren(this);
		}
	}

	public final LogicExprContext logicExpr() throws RecognitionException {
		return logicExpr(0);
	}

	private LogicExprContext logicExpr(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		LogicExprContext _localctx = new LogicExprContext(_ctx, _parentState);
		LogicExprContext _prevctx = _localctx;
		int _startState = 12;
		enterRecursionRule(_localctx, 12, RULE_logicExpr, _p);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(116);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,6,_ctx) ) {
			case 1:
				{
				_localctx = new InternalFunctionInContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(86);
				arithExpr(0);
				setState(87);
				match(T__15);
				setState(88);
				match(T__0);
				setState(89);
				match(T__8);
				setState(90);
				match(ID);
				setState(91);
				match(T__9);
				setState(92);
				match(T__5);
				setState(93);
				match(ID);
				}
				break;
			case 2:
				{
				_localctx = new FuncLeastMostContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(95);
				((FuncLeastMostContext)_localctx).func = _input.LT(1);
				_la = _input.LA(1);
				if ( !(_la==T__16 || _la==T__17) ) {
					((FuncLeastMostContext)_localctx).func = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(96);
				match(T__8);
				setState(97);
				arithExpr(0);
				setState(98);
				match(T__18);
				setState(99);
				logicExpr(0);
				setState(100);
				match(T__9);
				}
				break;
			case 3:
				{
				_localctx = new FuncAnyAllItemContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(102);
				((FuncAnyAllItemContext)_localctx).func = _input.LT(1);
				_la = _input.LA(1);
				if ( !(_la==T__19 || _la==T__20) ) {
					((FuncAnyAllItemContext)_localctx).func = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(103);
				match(T__8);
				setState(104);
				logicExpr(0);
				setState(105);
				match(T__9);
				}
				break;
			case 4:
				{
				_localctx = new TwoArithExprComparisonContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(107);
				arithExpr(0);
				setState(108);
				((TwoArithExprComparisonContext)_localctx).op = _input.LT(1);
				_la = _input.LA(1);
				if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << EQ) | (1L << NOTEQ) | (1L << LESSEQ) | (1L << GREATEREQ) | (1L << LESS) | (1L << GREATER))) != 0)) ) {
					((TwoArithExprComparisonContext)_localctx).op = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(109);
				arithExpr(0);
				}
				break;
			case 5:
				{
				_localctx = new ParentheseLogicExprAsLogicExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(111);
				match(T__8);
				setState(112);
				logicExpr(0);
				setState(113);
				match(T__9);
				}
				break;
			case 6:
				{
				_localctx = new BoolExprAsLogicExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(115);
				((BoolExprAsLogicExprContext)_localctx).op = _input.LT(1);
				_la = _input.LA(1);
				if ( !(_la==TRUE || _la==FALSE) ) {
					((BoolExprAsLogicExprContext)_localctx).op = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				}
				break;
			}
			_ctx.stop = _input.LT(-1);
			setState(123);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,7,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new TwoCalcLogicExprLogicOperationContext(new LogicExprContext(_parentctx, _parentState));
					pushNewRecursionContext(_localctx, _startState, RULE_logicExpr);
					setState(118);
					if (!(precpred(_ctx, 3))) throw new FailedPredicateException(this, "precpred(_ctx, 3)");
					setState(119);
					((TwoCalcLogicExprLogicOperationContext)_localctx).op = _input.LT(1);
					_la = _input.LA(1);
					if ( !(_la==AND || _la==OR) ) {
						((TwoCalcLogicExprLogicOperationContext)_localctx).op = (Token)_errHandler.recoverInline(this);
					}
					else {
						if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
						_errHandler.reportMatch(this);
						consume();
					}
					setState(120);
					logicExpr(4);
					}
					} 
				}
				setState(125);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,7,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	public static class ArithExprContext extends ParserRuleContext {
		public ArithExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_arithExpr; }
	 
		public ArithExprContext() { }
		public void copyFrom(ArithExprContext ctx) {
			super.copyFrom(ctx);
		}
	}
	public static class StringAsArithExprContext extends ArithExprContext {
		public TerminalNode STRING() { return getToken(RegLangParser.STRING, 0); }
		public StringAsArithExprContext(ArithExprContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitStringAsArithExpr(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class ConstantArrayContext extends ArithExprContext {
		public ArrayContext array() {
			return getRuleContext(ArrayContext.class,0);
		}
		public ConstantArrayContext(ArithExprContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitConstantArray(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class CalcPowContext extends ArithExprContext {
		public List<ArithExprContext> arithExpr() {
			return getRuleContexts(ArithExprContext.class);
		}
		public ArithExprContext arithExpr(int i) {
			return getRuleContext(ArithExprContext.class,i);
		}
		public TerminalNode POW() { return getToken(RegLangParser.POW, 0); }
		public CalcPowContext(ArithExprContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitCalcPow(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class CalcMulDivModContext extends ArithExprContext {
		public Token op;
		public List<ArithExprContext> arithExpr() {
			return getRuleContexts(ArithExprContext.class);
		}
		public ArithExprContext arithExpr(int i) {
			return getRuleContext(ArithExprContext.class,i);
		}
		public TerminalNode MUL() { return getToken(RegLangParser.MUL, 0); }
		public TerminalNode DIV() { return getToken(RegLangParser.DIV, 0); }
		public TerminalNode MOD() { return getToken(RegLangParser.MOD, 0); }
		public CalcMulDivModContext(ArithExprContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitCalcMulDivMod(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class ParentheseArithExprAsArithExprContext extends ArithExprContext {
		public ArithExprContext arithExpr() {
			return getRuleContext(ArithExprContext.class,0);
		}
		public ParentheseArithExprAsArithExprContext(ArithExprContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitParentheseArithExprAsArithExpr(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class VariableAsArithExprContext extends ArithExprContext {
		public VarSymbolContext varSymbol() {
			return getRuleContext(VarSymbolContext.class,0);
		}
		public VariableAsArithExprContext(ArithExprContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitVariableAsArithExpr(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class FuncArrayLengthContext extends ArithExprContext {
		public ArithExprContext arithExpr() {
			return getRuleContext(ArithExprContext.class,0);
		}
		public FuncArrayLengthContext(ArithExprContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitFuncArrayLength(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class NumberAsArithExprContext extends ArithExprContext {
		public NumberContext number() {
			return getRuleContext(NumberContext.class,0);
		}
		public NumberAsArithExprContext(ArithExprContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitNumberAsArithExpr(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class CalcAddSubContext extends ArithExprContext {
		public Token op;
		public List<ArithExprContext> arithExpr() {
			return getRuleContexts(ArithExprContext.class);
		}
		public ArithExprContext arithExpr(int i) {
			return getRuleContext(ArithExprContext.class,i);
		}
		public TerminalNode ADD() { return getToken(RegLangParser.ADD, 0); }
		public TerminalNode SUB() { return getToken(RegLangParser.SUB, 0); }
		public CalcAddSubContext(ArithExprContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitCalcAddSub(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class FuncCountBoolContext extends ArithExprContext {
		public List<LogicExprContext> logicExpr() {
			return getRuleContexts(LogicExprContext.class);
		}
		public LogicExprContext logicExpr(int i) {
			return getRuleContext(LogicExprContext.class,i);
		}
		public FuncCountBoolContext(ArithExprContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitFuncCountBool(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ArithExprContext arithExpr() throws RecognitionException {
		return arithExpr(0);
	}

	private ArithExprContext arithExpr(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		ArithExprContext _localctx = new ArithExprContext(_ctx, _parentState);
		ArithExprContext _prevctx = _localctx;
		int _startState = 14;
		enterRecursionRule(_localctx, 14, RULE_arithExpr, _p);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(152);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,9,_ctx) ) {
			case 1:
				{
				_localctx = new FuncArrayLengthContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(127);
				match(T__21);
				setState(128);
				match(T__8);
				setState(129);
				arithExpr(0);
				setState(130);
				match(T__9);
				}
				break;
			case 2:
				{
				_localctx = new FuncCountBoolContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(132);
				match(T__22);
				setState(133);
				match(T__8);
				setState(134);
				logicExpr(0);
				setState(139);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__18) {
					{
					{
					setState(135);
					match(T__18);
					setState(136);
					logicExpr(0);
					}
					}
					setState(141);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(142);
				match(T__9);
				}
				break;
			case 3:
				{
				_localctx = new ParentheseArithExprAsArithExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(144);
				match(T__8);
				setState(145);
				arithExpr(0);
				setState(146);
				match(T__9);
				}
				break;
			case 4:
				{
				_localctx = new ConstantArrayContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(148);
				array();
				}
				break;
			case 5:
				{
				_localctx = new VariableAsArithExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(149);
				varSymbol(0);
				}
				break;
			case 6:
				{
				_localctx = new NumberAsArithExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(150);
				number();
				}
				break;
			case 7:
				{
				_localctx = new StringAsArithExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(151);
				match(STRING);
				}
				break;
			}
			_ctx.stop = _input.LT(-1);
			setState(165);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,11,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(163);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,10,_ctx) ) {
					case 1:
						{
						_localctx = new CalcPowContext(new ArithExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_arithExpr);
						setState(154);
						if (!(precpred(_ctx, 8))) throw new FailedPredicateException(this, "precpred(_ctx, 8)");
						setState(155);
						match(POW);
						setState(156);
						arithExpr(8);
						}
						break;
					case 2:
						{
						_localctx = new CalcMulDivModContext(new ArithExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_arithExpr);
						setState(157);
						if (!(precpred(_ctx, 7))) throw new FailedPredicateException(this, "precpred(_ctx, 7)");
						setState(158);
						((CalcMulDivModContext)_localctx).op = _input.LT(1);
						_la = _input.LA(1);
						if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << MUL) | (1L << DIV) | (1L << MOD))) != 0)) ) {
							((CalcMulDivModContext)_localctx).op = (Token)_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(159);
						arithExpr(8);
						}
						break;
					case 3:
						{
						_localctx = new CalcAddSubContext(new ArithExprContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_arithExpr);
						setState(160);
						if (!(precpred(_ctx, 6))) throw new FailedPredicateException(this, "precpred(_ctx, 6)");
						setState(161);
						((CalcAddSubContext)_localctx).op = _input.LT(1);
						_la = _input.LA(1);
						if ( !(_la==ADD || _la==SUB) ) {
							((CalcAddSubContext)_localctx).op = (Token)_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(162);
						arithExpr(7);
						}
						break;
					}
					} 
				}
				setState(167);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,11,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	public static class VarSymbolContext extends ParserRuleContext {
		public VarSymbolContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_varSymbol; }
	 
		public VarSymbolContext() { }
		public void copyFrom(VarSymbolContext ctx) {
			super.copyFrom(ctx);
		}
	}
	public static class TxArgsContext extends VarSymbolContext {
		public VarSymbolContext varSymbol() {
			return getRuleContext(VarSymbolContext.class,0);
		}
		public TxArgsContext(VarSymbolContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitTxArgs(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class ContractInfoContext extends VarSymbolContext {
		public Token info;
		public ArithExprContext arithExpr() {
			return getRuleContext(ArithExprContext.class,0);
		}
		public ContractInfoContext(VarSymbolContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitContractInfo(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class KnowledgeVarContext extends VarSymbolContext {
		public List<TerminalNode> ID() { return getTokens(RegLangParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(RegLangParser.ID, i);
		}
		public KnowledgeVarContext(VarSymbolContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitKnowledgeVar(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class ArrayItemContext extends VarSymbolContext {
		public VarSymbolContext varSymbol() {
			return getRuleContext(VarSymbolContext.class,0);
		}
		public ArithExprContext arithExpr() {
			return getRuleContext(ArithExprContext.class,0);
		}
		public ArrayItemContext(VarSymbolContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitArrayItem(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class BracketArithExprToVarSymbolContext extends VarSymbolContext {
		public ArithExprContext arithExpr() {
			return getRuleContext(ArithExprContext.class,0);
		}
		public BracketArithExprToVarSymbolContext(VarSymbolContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitBracketArithExprToVarSymbol(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class ContractStateContext extends VarSymbolContext {
		public ArithExprContext arithExpr() {
			return getRuleContext(ArithExprContext.class,0);
		}
		public VarSymbolContext varSymbol() {
			return getRuleContext(VarSymbolContext.class,0);
		}
		public ContractStateContext(VarSymbolContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitContractState(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class TxBasicInfoContext extends VarSymbolContext {
		public Token info;
		public TxBasicInfoContext(VarSymbolContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitTxBasicInfo(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class ParentheseArithExprAsVarSymbolContext extends VarSymbolContext {
		public ArithExprContext arithExpr() {
			return getRuleContext(ArithExprContext.class,0);
		}
		public ParentheseArithExprAsVarSymbolContext(VarSymbolContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitParentheseArithExprAsVarSymbol(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class IdAsVarSymbolContext extends VarSymbolContext {
		public TerminalNode ID() { return getToken(RegLangParser.ID, 0); }
		public IdAsVarSymbolContext(VarSymbolContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitIdAsVarSymbol(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class ParentheseVarSymbolAsVarSymbolContext extends VarSymbolContext {
		public VarSymbolContext varSymbol() {
			return getRuleContext(VarSymbolContext.class,0);
		}
		public ParentheseVarSymbolAsVarSymbolContext(VarSymbolContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitParentheseVarSymbolAsVarSymbol(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class TxReadWriteSetsContext extends VarSymbolContext {
		public Token info;
		public ArithExprContext arithExpr() {
			return getRuleContext(ArithExprContext.class,0);
		}
		public VarSymbolContext varSymbol() {
			return getRuleContext(VarSymbolContext.class,0);
		}
		public TxReadWriteSetsContext(VarSymbolContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitTxReadWriteSets(this);
			else return visitor.visitChildren(this);
		}
	}

	public final VarSymbolContext varSymbol() throws RecognitionException {
		return varSymbol(0);
	}

	private VarSymbolContext varSymbol(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		VarSymbolContext _localctx = new VarSymbolContext(_ctx, _parentState);
		VarSymbolContext _prevctx = _localctx;
		int _startState = 16;
		enterRecursionRule(_localctx, 16, RULE_varSymbol, _p);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(221);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,12,_ctx) ) {
			case 1:
				{
				_localctx = new TxBasicInfoContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(169);
				match(T__23);
				setState(170);
				match(T__5);
				setState(171);
				((TxBasicInfoContext)_localctx).info = _input.LT(1);
				_la = _input.LA(1);
				if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__24) | (1L << T__25) | (1L << T__26))) != 0)) ) {
					((TxBasicInfoContext)_localctx).info = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				}
				break;
			case 2:
				{
				_localctx = new TxReadWriteSetsContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(172);
				match(T__23);
				setState(173);
				match(T__5);
				setState(174);
				((TxReadWriteSetsContext)_localctx).info = _input.LT(1);
				_la = _input.LA(1);
				if ( !(_la==T__27 || _la==T__28) ) {
					((TxReadWriteSetsContext)_localctx).info = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(175);
				match(T__8);
				setState(176);
				arithExpr(0);
				setState(177);
				match(T__9);
				setState(178);
				match(T__5);
				setState(179);
				varSymbol(10);
				}
				break;
			case 3:
				{
				_localctx = new TxArgsContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(181);
				match(T__23);
				setState(182);
				match(T__5);
				setState(183);
				match(T__29);
				setState(184);
				matchWildcard();
				setState(185);
				varSymbol(9);
				}
				break;
			case 4:
				{
				_localctx = new ContractInfoContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(186);
				match(T__30);
				setState(187);
				match(T__8);
				setState(188);
				arithExpr(0);
				setState(189);
				match(T__9);
				setState(190);
				match(T__5);
				setState(191);
				((ContractInfoContext)_localctx).info = _input.LT(1);
				_la = _input.LA(1);
				if ( !(_la==T__31 || _la==T__32) ) {
					((ContractInfoContext)_localctx).info = (Token)_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				}
				break;
			case 5:
				{
				_localctx = new ContractStateContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(193);
				match(T__30);
				setState(194);
				match(T__8);
				setState(195);
				arithExpr(0);
				setState(196);
				match(T__9);
				setState(197);
				match(T__5);
				setState(198);
				match(T__33);
				setState(199);
				match(T__5);
				setState(200);
				varSymbol(7);
				}
				break;
			case 6:
				{
				_localctx = new KnowledgeVarContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(202);
				match(T__0);
				setState(203);
				match(T__8);
				setState(204);
				match(ID);
				setState(205);
				match(T__9);
				setState(206);
				match(T__5);
				setState(207);
				match(ID);
				}
				break;
			case 7:
				{
				_localctx = new BracketArithExprToVarSymbolContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(208);
				match(T__34);
				setState(209);
				arithExpr(0);
				setState(210);
				match(T__35);
				}
				break;
			case 8:
				{
				_localctx = new ParentheseArithExprAsVarSymbolContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(212);
				match(T__8);
				setState(213);
				arithExpr(0);
				setState(214);
				match(T__9);
				}
				break;
			case 9:
				{
				_localctx = new ParentheseVarSymbolAsVarSymbolContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(216);
				match(T__8);
				setState(217);
				varSymbol(0);
				setState(218);
				match(T__9);
				}
				break;
			case 10:
				{
				_localctx = new IdAsVarSymbolContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(220);
				match(ID);
				}
				break;
			}
			_ctx.stop = _input.LT(-1);
			setState(230);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,13,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new ArrayItemContext(new VarSymbolContext(_parentctx, _parentState));
					pushNewRecursionContext(_localctx, _startState, RULE_varSymbol);
					setState(223);
					if (!(precpred(_ctx, 5))) throw new FailedPredicateException(this, "precpred(_ctx, 5)");
					setState(224);
					match(T__34);
					setState(225);
					arithExpr(0);
					setState(226);
					match(T__35);
					}
					} 
				}
				setState(232);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,13,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	public static class NumberContext extends ParserRuleContext {
		public TerminalNode INT() { return getToken(RegLangParser.INT, 0); }
		public NumberContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_number; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitNumber(this);
			else return visitor.visitChildren(this);
		}
	}

	public final NumberContext number() throws RecognitionException {
		NumberContext _localctx = new NumberContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_number);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(233);
			match(INT);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ArrayContext extends ParserRuleContext {
		public ArrayContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_array; }
	 
		public ArrayContext() { }
		public void copyFrom(ArrayContext ctx) {
			super.copyFrom(ctx);
		}
	}
	public static class StringArrayContext extends ArrayContext {
		public List<TerminalNode> STRING() { return getTokens(RegLangParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(RegLangParser.STRING, i);
		}
		public StringArrayContext(ArrayContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitStringArray(this);
			else return visitor.visitChildren(this);
		}
	}
	public static class NumberArrayContext extends ArrayContext {
		public List<NumberContext> number() {
			return getRuleContexts(NumberContext.class);
		}
		public NumberContext number(int i) {
			return getRuleContext(NumberContext.class,i);
		}
		public NumberArrayContext(ArrayContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitNumberArray(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ArrayContext array() throws RecognitionException {
		ArrayContext _localctx = new ArrayContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_array);
		int _la;
		try {
			setState(256);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,16,_ctx) ) {
			case 1:
				_localctx = new NumberArrayContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(235);
				match(T__34);
				setState(236);
				number();
				setState(241);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__18) {
					{
					{
					setState(237);
					match(T__18);
					setState(238);
					number();
					}
					}
					setState(243);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(244);
				match(T__35);
				}
				break;
			case 2:
				_localctx = new StringArrayContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(246);
				match(T__34);
				setState(247);
				match(STRING);
				setState(252);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__18) {
					{
					{
					setState(248);
					match(T__18);
					setState(249);
					match(STRING);
					}
					}
					setState(254);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(255);
				match(T__35);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ComparisonOpContext extends ParserRuleContext {
		public TerminalNode EQ() { return getToken(RegLangParser.EQ, 0); }
		public TerminalNode NOTEQ() { return getToken(RegLangParser.NOTEQ, 0); }
		public TerminalNode LESS() { return getToken(RegLangParser.LESS, 0); }
		public TerminalNode LESSEQ() { return getToken(RegLangParser.LESSEQ, 0); }
		public TerminalNode GREATER() { return getToken(RegLangParser.GREATER, 0); }
		public TerminalNode GREATEREQ() { return getToken(RegLangParser.GREATEREQ, 0); }
		public ComparisonOpContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_comparisonOp; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitComparisonOp(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ComparisonOpContext comparisonOp() throws RecognitionException {
		ComparisonOpContext _localctx = new ComparisonOpContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_comparisonOp);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(258);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << EQ) | (1L << NOTEQ) | (1L << LESSEQ) | (1L << GREATEREQ) | (1L << LESS) | (1L << GREATER))) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class LogicOpContext extends ParserRuleContext {
		public TerminalNode AND() { return getToken(RegLangParser.AND, 0); }
		public TerminalNode OR() { return getToken(RegLangParser.OR, 0); }
		public LogicOpContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_logicOp; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitLogicOp(this);
			else return visitor.visitChildren(this);
		}
	}

	public final LogicOpContext logicOp() throws RecognitionException {
		LogicOpContext _localctx = new LogicOpContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_logicOp);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(260);
			_la = _input.LA(1);
			if ( !(_la==AND || _la==OR) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class BoolExprContext extends ParserRuleContext {
		public TerminalNode TRUE() { return getToken(RegLangParser.TRUE, 0); }
		public TerminalNode FALSE() { return getToken(RegLangParser.FALSE, 0); }
		public BoolExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_boolExpr; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof RegLangVisitor ) return ((RegLangVisitor<? extends T>)visitor).visitBoolExpr(this);
			else return visitor.visitChildren(this);
		}
	}

	public final BoolExprContext boolExpr() throws RecognitionException {
		BoolExprContext _localctx = new BoolExprContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_boolExpr);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(262);
			_la = _input.LA(1);
			if ( !(_la==TRUE || _la==FALSE) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public boolean sempred(RuleContext _localctx, int ruleIndex, int predIndex) {
		switch (ruleIndex) {
		case 6:
			return logicExpr_sempred((LogicExprContext)_localctx, predIndex);
		case 7:
			return arithExpr_sempred((ArithExprContext)_localctx, predIndex);
		case 8:
			return varSymbol_sempred((VarSymbolContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean logicExpr_sempred(LogicExprContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return precpred(_ctx, 3);
		}
		return true;
	}
	private boolean arithExpr_sempred(ArithExprContext _localctx, int predIndex) {
		switch (predIndex) {
		case 1:
			return precpred(_ctx, 8);
		case 2:
			return precpred(_ctx, 7);
		case 3:
			return precpred(_ctx, 6);
		}
		return true;
	}
	private boolean varSymbol_sempred(VarSymbolContext _localctx, int predIndex) {
		switch (predIndex) {
		case 4:
			return precpred(_ctx, 5);
		}
		return true;
	}

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3>\u010b\4\2\t\2\4"+
		"\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t"+
		"\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\3\2\3\2\7\2!\n\2\f\2\16\2$\13"+
		"\2\3\3\3\3\3\3\6\3)\n\3\r\3\16\3*\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4"+
		"\3\4\3\4\3\4\3\4\3\4\3\4\3\4\5\4=\n\4\3\5\3\5\3\5\3\5\7\5C\n\5\f\5\16"+
		"\5F\13\5\3\5\3\5\3\6\3\6\3\6\3\6\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\7\5\7V"+
		"\n\7\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3"+
		"\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\3\b\5\bw\n\b\3"+
		"\b\3\b\3\b\7\b|\n\b\f\b\16\b\177\13\b\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t"+
		"\3\t\3\t\3\t\7\t\u008c\n\t\f\t\16\t\u008f\13\t\3\t\3\t\3\t\3\t\3\t\3\t"+
		"\3\t\3\t\3\t\3\t\5\t\u009b\n\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\3\t\7\t"+
		"\u00a6\n\t\f\t\16\t\u00a9\13\t\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n"+
		"\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3"+
		"\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n"+
		"\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\5\n\u00e0\n\n\3\n\3\n\3\n\3\n\3\n\7\n"+
		"\u00e7\n\n\f\n\16\n\u00ea\13\n\3\13\3\13\3\f\3\f\3\f\3\f\7\f\u00f2\n\f"+
		"\f\f\16\f\u00f5\13\f\3\f\3\f\3\f\3\f\3\f\3\f\7\f\u00fd\n\f\f\f\16\f\u0100"+
		"\13\f\3\f\5\f\u0103\n\f\3\r\3\r\3\16\3\16\3\17\3\17\3\17\2\5\16\20\22"+
		"\20\2\4\6\b\n\f\16\20\22\24\26\30\32\34\2\r\3\2\t\n\3\2\23\24\3\2\26\27"+
		"\3\2-\62\3\2\65\66\3\2\63\64\3\2)+\3\2\'(\3\2\33\35\3\2\36\37\3\2\"#\2"+
		"\u011f\2\"\3\2\2\2\4%\3\2\2\2\6<\3\2\2\2\b>\3\2\2\2\nI\3\2\2\2\fU\3\2"+
		"\2\2\16v\3\2\2\2\20\u009a\3\2\2\2\22\u00df\3\2\2\2\24\u00eb\3\2\2\2\26"+
		"\u0102\3\2\2\2\30\u0104\3\2\2\2\32\u0106\3\2\2\2\34\u0108\3\2\2\2\36!"+
		"\5\4\3\2\37!\5\b\5\2 \36\3\2\2\2 \37\3\2\2\2!$\3\2\2\2\" \3\2\2\2\"#\3"+
		"\2\2\2#\3\3\2\2\2$\"\3\2\2\2%&\7\3\2\2&(\7<\2\2\')\5\6\4\2(\'\3\2\2\2"+
		")*\3\2\2\2*(\3\2\2\2*+\3\2\2\2+,\3\2\2\2,-\7\4\2\2-\5\3\2\2\2./\7\5\2"+
		"\2/\60\7<\2\2\60\61\7\6\2\2\61\62\5\20\t\2\62\63\7\7\2\2\63=\3\2\2\2\64"+
		"\65\7<\2\2\65\66\7\b\2\2\66\67\t\2\2\2\678\7\13\2\289\5\20\t\29:\7\f\2"+
		"\2:;\7\7\2\2;=\3\2\2\2<.\3\2\2\2<\64\3\2\2\2=\7\3\2\2\2>?\7\r\2\2?@\7"+
		"<\2\2@D\5\n\6\2AC\5\f\7\2BA\3\2\2\2CF\3\2\2\2DB\3\2\2\2DE\3\2\2\2EG\3"+
		"\2\2\2FD\3\2\2\2GH\7\4\2\2H\t\3\2\2\2IJ\7\16\2\2JK\5\16\b\2KL\7\17\2\2"+
		"L\13\3\2\2\2MN\7\20\2\2NO\5\16\b\2OP\7\7\2\2PV\3\2\2\2QR\7\21\2\2RS\5"+
		"\16\b\2ST\7\7\2\2TV\3\2\2\2UM\3\2\2\2UQ\3\2\2\2V\r\3\2\2\2WX\b\b\1\2X"+
		"Y\5\20\t\2YZ\7\22\2\2Z[\7\3\2\2[\\\7\13\2\2\\]\7<\2\2]^\7\f\2\2^_\7\b"+
		"\2\2_`\7<\2\2`w\3\2\2\2ab\t\3\2\2bc\7\13\2\2cd\5\20\t\2de\7\25\2\2ef\5"+
		"\16\b\2fg\7\f\2\2gw\3\2\2\2hi\t\4\2\2ij\7\13\2\2jk\5\16\b\2kl\7\f\2\2"+
		"lw\3\2\2\2mn\5\20\t\2no\t\5\2\2op\5\20\t\2pw\3\2\2\2qr\7\13\2\2rs\5\16"+
		"\b\2st\7\f\2\2tw\3\2\2\2uw\t\6\2\2vW\3\2\2\2va\3\2\2\2vh\3\2\2\2vm\3\2"+
		"\2\2vq\3\2\2\2vu\3\2\2\2w}\3\2\2\2xy\f\5\2\2yz\t\7\2\2z|\5\16\b\6{x\3"+
		"\2\2\2|\177\3\2\2\2}{\3\2\2\2}~\3\2\2\2~\17\3\2\2\2\177}\3\2\2\2\u0080"+
		"\u0081\b\t\1\2\u0081\u0082\7\30\2\2\u0082\u0083\7\13\2\2\u0083\u0084\5"+
		"\20\t\2\u0084\u0085\7\f\2\2\u0085\u009b\3\2\2\2\u0086\u0087\7\31\2\2\u0087"+
		"\u0088\7\13\2\2\u0088\u008d\5\16\b\2\u0089\u008a\7\25\2\2\u008a\u008c"+
		"\5\16\b\2\u008b\u0089\3\2\2\2\u008c\u008f\3\2\2\2\u008d\u008b\3\2\2\2"+
		"\u008d\u008e\3\2\2\2\u008e\u0090\3\2\2\2\u008f\u008d\3\2\2\2\u0090\u0091"+
		"\7\f\2\2\u0091\u009b\3\2\2\2\u0092\u0093\7\13\2\2\u0093\u0094\5\20\t\2"+
		"\u0094\u0095\7\f\2\2\u0095\u009b\3\2\2\2\u0096\u009b\5\26\f\2\u0097\u009b"+
		"\5\22\n\2\u0098\u009b\5\24\13\2\u0099\u009b\7>\2\2\u009a\u0080\3\2\2\2"+
		"\u009a\u0086\3\2\2\2\u009a\u0092\3\2\2\2\u009a\u0096\3\2\2\2\u009a\u0097"+
		"\3\2\2\2\u009a\u0098\3\2\2\2\u009a\u0099\3\2\2\2\u009b\u00a7\3\2\2\2\u009c"+
		"\u009d\f\n\2\2\u009d\u009e\7,\2\2\u009e\u00a6\5\20\t\n\u009f\u00a0\f\t"+
		"\2\2\u00a0\u00a1\t\b\2\2\u00a1\u00a6\5\20\t\n\u00a2\u00a3\f\b\2\2\u00a3"+
		"\u00a4\t\t\2\2\u00a4\u00a6\5\20\t\t\u00a5\u009c\3\2\2\2\u00a5\u009f\3"+
		"\2\2\2\u00a5\u00a2\3\2\2\2\u00a6\u00a9\3\2\2\2\u00a7\u00a5\3\2\2\2\u00a7"+
		"\u00a8\3\2\2\2\u00a8\21\3\2\2\2\u00a9\u00a7\3\2\2\2\u00aa\u00ab\b\n\1"+
		"\2\u00ab\u00ac\7\32\2\2\u00ac\u00ad\7\b\2\2\u00ad\u00e0\t\n\2\2\u00ae"+
		"\u00af\7\32\2\2\u00af\u00b0\7\b\2\2\u00b0\u00b1\t\13\2\2\u00b1\u00b2\7"+
		"\13\2\2\u00b2\u00b3\5\20\t\2\u00b3\u00b4\7\f\2\2\u00b4\u00b5\7\b\2\2\u00b5"+
		"\u00b6\5\22\n\f\u00b6\u00e0\3\2\2\2\u00b7\u00b8\7\32\2\2\u00b8\u00b9\7"+
		"\b\2\2\u00b9\u00ba\7 \2\2\u00ba\u00bb\13\2\2\2\u00bb\u00e0\5\22\n\13\u00bc"+
		"\u00bd\7!\2\2\u00bd\u00be\7\13\2\2\u00be\u00bf\5\20\t\2\u00bf\u00c0\7"+
		"\f\2\2\u00c0\u00c1\7\b\2\2\u00c1\u00c2\t\f\2\2\u00c2\u00e0\3\2\2\2\u00c3"+
		"\u00c4\7!\2\2\u00c4\u00c5\7\13\2\2\u00c5\u00c6\5\20\t\2\u00c6\u00c7\7"+
		"\f\2\2\u00c7\u00c8\7\b\2\2\u00c8\u00c9\7$\2\2\u00c9\u00ca\7\b\2\2\u00ca"+
		"\u00cb\5\22\n\t\u00cb\u00e0\3\2\2\2\u00cc\u00cd\7\3\2\2\u00cd\u00ce\7"+
		"\13\2\2\u00ce\u00cf\7<\2\2\u00cf\u00d0\7\f\2\2\u00d0\u00d1\7\b\2\2\u00d1"+
		"\u00e0\7<\2\2\u00d2\u00d3\7%\2\2\u00d3\u00d4\5\20\t\2\u00d4\u00d5\7&\2"+
		"\2\u00d5\u00e0\3\2\2\2\u00d6\u00d7\7\13\2\2\u00d7\u00d8\5\20\t\2\u00d8"+
		"\u00d9\7\f\2\2\u00d9\u00e0\3\2\2\2\u00da\u00db\7\13\2\2\u00db\u00dc\5"+
		"\22\n\2\u00dc\u00dd\7\f\2\2\u00dd\u00e0\3\2\2\2\u00de\u00e0\7<\2\2\u00df"+
		"\u00aa\3\2\2\2\u00df\u00ae\3\2\2\2\u00df\u00b7\3\2\2\2\u00df\u00bc\3\2"+
		"\2\2\u00df\u00c3\3\2\2\2\u00df\u00cc\3\2\2\2\u00df\u00d2\3\2\2\2\u00df"+
		"\u00d6\3\2\2\2\u00df\u00da\3\2\2\2\u00df\u00de\3\2\2\2\u00e0\u00e8\3\2"+
		"\2\2\u00e1\u00e2\f\7\2\2\u00e2\u00e3\7%\2\2\u00e3\u00e4\5\20\t\2\u00e4"+
		"\u00e5\7&\2\2\u00e5\u00e7\3\2\2\2\u00e6\u00e1\3\2\2\2\u00e7\u00ea\3\2"+
		"\2\2\u00e8\u00e6\3\2\2\2\u00e8\u00e9\3\2\2\2\u00e9\23\3\2\2\2\u00ea\u00e8"+
		"\3\2\2\2\u00eb\u00ec\7:\2\2\u00ec\25\3\2\2\2\u00ed\u00ee\7%\2\2\u00ee"+
		"\u00f3\5\24\13\2\u00ef\u00f0\7\25\2\2\u00f0\u00f2\5\24\13\2\u00f1\u00ef"+
		"\3\2\2\2\u00f2\u00f5\3\2\2\2\u00f3\u00f1\3\2\2\2\u00f3\u00f4\3\2\2\2\u00f4"+
		"\u00f6\3\2\2\2\u00f5\u00f3\3\2\2\2\u00f6\u00f7\7&\2\2\u00f7\u0103\3\2"+
		"\2\2\u00f8\u00f9\7%\2\2\u00f9\u00fe\7>\2\2\u00fa\u00fb\7\25\2\2\u00fb"+
		"\u00fd\7>\2\2\u00fc\u00fa\3\2\2\2\u00fd\u0100\3\2\2\2\u00fe\u00fc\3\2"+
		"\2\2\u00fe\u00ff\3\2\2\2\u00ff\u0101\3\2\2\2\u0100\u00fe\3\2\2\2\u0101"+
		"\u0103\7&\2\2\u0102\u00ed\3\2\2\2\u0102\u00f8\3\2\2\2\u0103\27\3\2\2\2"+
		"\u0104\u0105\t\5\2\2\u0105\31\3\2\2\2\u0106\u0107\t\7\2\2\u0107\33\3\2"+
		"\2\2\u0108\u0109\t\6\2\2\u0109\35\3\2\2\2\23 \"*<DUv}\u008d\u009a\u00a5"+
		"\u00a7\u00df\u00e8\u00f3\u00fe\u0102";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}