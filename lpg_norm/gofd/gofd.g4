grammar gnfd ;

AMPERSAND : '&' ;
COLON : ':' ;
COMMA : ',' ;
DASH : '-' ;
DETERMINES : '=>' ;
DOT : '.' ;
IDENTIFIER : [a-zA-Z] ([a-zA-Z0-9] | '_')* ;
LANGLE: '<' ;
LBRACK : '[' ;
LPAR : '(' ;
RANGLE : '>' ;
RBRACK : ']' ;
RPAR : ')' ;

dependency : pattern COLON COLON left DETERMINES right EOF ;

left : reference (COMMA reference)* ;

right : reference (COMMA reference)* ;

reference : varName | property ;

property : varName DOT propertyKey ;

pattern: nodePattern
        | pattern LANGLE DASH LBRACK varName? ((labelList propertyList?) | (COLON propertyList))? RBRACK DASH pattern
        | pattern DASH LBRACK varName? ((labelList propertyList?) | (COLON propertyList))? RBRACK DASH RANGLE pattern
        | pattern COMMA pattern ;

labelList : COLON label (AMPERSAND label)* ;

propertyList : COLON propertyKey (AMPERSAND propertyKey)* ;

label : IDENTIFIER ;

varName : IDENTIFIER ;

propertyKey : IDENTIFIER ;

nodePattern : LPAR varName? ((labelList propertyList?) | (COLON propertyList))? RPAR ;
