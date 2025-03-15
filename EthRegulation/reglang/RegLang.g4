/* RegLang: A Domain Specific Language for Rule-based Regulation on Blockchain.
 * Author: Jianbo Gao (gaojianbo@pku.edu.cn)
 */

grammar RegLang;

prog
    : (knowledgebaseBlock|ruleBlock)*
    ;

knowledgebaseBlock
    : 'knowledgebase' ID knowledgeDecl+ 'end'
    ;

knowledgeDecl
    : 'knowledge' ID '=' arithExpr ';'                  # KnowledgeAssign
    | ID '.' op=('add'|'del') '(' arithExpr ')' ';'     # KnowledgeFunc
    ;

ruleBlock
    : 'rule' ID regScopeStmt regRuleStmt* 'end'  
    ;

regScopeStmt
    : 'reg' logicExpr ':'
    ;

regRuleStmt
    : 'require' logicExpr ';'                      # RequireReg
    | 'prohibit' logicExpr ';'                     # ProhibitReg
    ;

logicExpr
    : arithExpr 'in' 'knowledgebase' '(' ID ')' '.' ID          # InternalFunctionIn
    | func=('at_least'|'at_most') '('arithExpr ',' logicExpr')'  #FuncLeastMost
    | func=('any_item'|'all_items') '(' logicExpr')'             #FuncAnyAllItem
    | arithExpr op=('=='|'!='|'<'|'<='|'>'|'>=') arithExpr      # TwoArithExprComparison
    | logicExpr op=('and'|'or') logicExpr                       # TwoCalcLogicExprLogicOperation
    | '(' logicExpr ')'                                         # ParentheseLogicExprAsLogicExpr
    | op=('true'|'false')                                       # BoolExprAsLogicExpr
    ;


arithExpr
    : 'length' '(' arithExpr ')'                    # FuncArrayLength
    | 'count' '(' logicExpr (',' logicExpr)* ')'    # FuncCountBool
    | <assoc=right> arithExpr POW arithExpr         # CalcPow
    | arithExpr op=('*'|'/'|'%') arithExpr          # CalcMulDivMod
    | arithExpr op=('+'|'-') arithExpr              # CalcAddSub
    | '(' arithExpr ')'                             # ParentheseArithExprAsArithExpr
    | array                                         # ConstantArray
    | varSymbol                                     # VariableAsArithExpr
    | number                                        # NumberAsArithExpr
    | STRING                                        # StringAsArithExpr
    ;

varSymbol
    : 'tx' '.' info=('from'|'to'|'function')                                # TxBasicInfo
    | 'tx' '.' info=('readset'|'writeset') '(' arithExpr ')' '.' varSymbol  # TxReadWriteSets
    | 'tx' '.' 'args' . varSymbol                                           # TxArgs
    | 'contract' '(' arithExpr ')' '.' info=('name'|'owner')                # ContractInfo
    | 'contract' '(' arithExpr ')' '.' 'state' '.' varSymbol                # ContractState
    | 'knowledgebase' '(' ID ')' '.' ID                                     # KnowledgeVar
    | varSymbol '[' arithExpr ']'                                           # ArrayItem
    | '[' arithExpr ']'                                                     # BracketArithExprToVarSymbol
    | '(' arithExpr ')'                                                     # ParentheseArithExprAsVarSymbol
    | '(' varSymbol ')'                                                     # ParentheseVarSymbolAsVarSymbol
    | ID                                                                    # IdAsVarSymbol
    ;

number
    : INT
    ;

array       // only support constant array 
    : '[' number (',' number)* ']'      # NumberArray
    | '[' STRING (',' STRING)* ']'      # StringArray
    ;

comparisonOp
    : EQ
    | NOTEQ
    | LESS
    | LESSEQ
    | GREATER
    | GREATEREQ
    ;

logicOp
    : AND
    | OR
    ;

boolExpr
    : TRUE
    | FALSE
    ;

// Arithmetic Operators
ADD     : '+' ;
SUB     : '-' ;
MUL     : '*' ;
DIV     : '/' ;
MOD     : '%'  ;
POW     : '^' ;

// Comparison Operators
EQ          : '==' ;
NOTEQ       : '!=' ;
LESSEQ      : '<=' ;
GREATEREQ   : '>=' ;
LESS        : '<' ;
GREATER     : '>' ;


// Logic Operators
AND     : 'and' ;
OR      : 'or' ;

TRUE : 'true';
FALSE :'false';

// Skip Tokens
LINE_COMMENT    : '//' .*? '\n' -> skip ;
COMMENT         : '/*' .*? '*/' -> skip ;
WS              : [ \t\r\n]+ -> skip ;

// Common Tokens
INT         : DIGIT+ ;
DIGIT       : [0-9] ;
ID          : ID_LETTER (ID_LETTER|DIGIT)* ;
ID_LETTER   : [a-zA-Z_] ;
STRING      : '"' .*? '"';
