grammar spgds;
import GQL;

// COLON ':' is imported from GQL
// COMMA ',' is imported from GQL
DETERMINES: '->' | '-->' | '→';
// LEFT_BRACKET '[' is imported from GQL
// MATCH is imported from GQL
// PERIOD '.' is imported from GQL
// RIGHT_BRACKET ']' is imported from GQL

dependency : pathPatternList COLON left DETERMINES right EOF;

left : reference (COMMA reference)* ;

right : reference ;

reference : elementVariable (PERIOD propertyName)? ;

