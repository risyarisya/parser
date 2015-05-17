%{
#include "scanner.h"

typedef PSU::Parser::token token;
typedef PSU::Parser::token_type token_type;

#define yyterminate() return token::END
#define YY_NO_UNISTD_H

%}

%option c++
%option prefix="PSU"

%option debug
%option yywrap nounput

%option stack

%{
#define YY_USER_ACTION yylloc->columns(yyleng);
%}

%%

%{
    yylloc->step();
%}


"(" { return Parser::token::LPAREN; }
")" { return Parser::token::RPAREN; }
"{" { return Parser::token::LBRACE; }
"}" { return Parser::token::RBRACE; }
"=" { return Parser::token::EQUAL; }
";" { return Parser::token::SEMICOLON; }
"struct" { return Parser::token::STRUCT; }


[1-9][0-9]* {
  yylval->integerVal = atoi(yytext);
  return token::INTEGER;
}

"0x"[0-9]* {
  yylval->hexVal = new std::string(yytext, yyleng);
  return token::HEXVAL;
}

"cpca"[A-Z_]* {
  yylval->stringVal = new std::string(yytext, yyleng);
  return token::TYPEDEF_NAME;
}

[a-zA-Z_][0-9a-zA-Z_-]* {
  yylval->stringVal = new std::string(yytext, yyleng);
  return token::IDENTIFIER;
}

[" "\t\r]+ {
}

"\n" { 
    yylloc->lines(yyleng);
}

. {
  return static_cast<token_type>(*yytext);
}


%%

namespace PSU {
Scanner::Scanner(std::istream* in, std::ostream* out) : PSUFlexLexer(in, out)
{
}

Scanner::~Scanner()
{
}

void Scanner::set_debug(bool b)
{
    yy_flex_debug = b;
}

}

#ifdef yylex
#undef yylex
#endif

int PSUFlexLexer::yylex()
{
    std::cerr << "in ExampleFlexLexer::yylex()!" << std::endl;
    return 0;
}

int PSUFlexLexer::yywrap()
{
    return 1;
}
