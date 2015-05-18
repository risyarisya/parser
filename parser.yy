%{

#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <fstream>
#include "expression.h"

%}

%require "2.3"
%debug

%defines

%name-prefix="PSU"

%define "parser_class_name" "Parser"
%defines /* output a header file */
%skeleton "lalr1.cc"

%locations
%initial-action
{
  @$.begin.filename = @$.end.filename = &driver.streamname;
};

%parse-param { class Driver& driver }

%error-verbose

%union {
  int integerVal;
  std::string* hexVal;
  std::string* stringVal;
  ExprNode* exprnode;
  StructDeclarationList* defs;
}

%token LPAREN RPAREN EQUAL LBRACE RBRACE STRUCT UNION SEMICOLON
%token <integerVal> INTEGER
%token <stringVal> IDENTIFIER
%token <stringVal> TYPEDEF_NAME
%token <stringVal> STRING_LITERAL
%token <hexVal> HEXVAL
%token END 0 "end of file"
%token EOL "end of line"


%type <exprnode> expr 
%type <exprnode> struct_specifier direct_declarator
%type <exprnode> struct_declaration struct_declarator
%type <defs> struct_declaration_list
%destructor { delete $$; } IDENTIFIER
%destructor { delete $$; } expr struct_declaration struct_specifier struct_declarator

%{
  #include "driver.h"
  #include "scanner.h"

#undef yylex
#define yylex driver.lexer->lex
%}

%%
input
: line { }
| input line { }
;

line
: struct_specifier {
  driver.tree = $1; 
//  $1->print(std::cout, 0); 
}
;

expr 
: INTEGER { $$ = new IntegerNode($1); }
| HEXVAL { $$ = new HexNode(*$1); }
| STRING_LITERAL { $$ = new StringNode(*$1); }
;

struct_specifier
: STRUCT IDENTIFIER LBRACE struct_declaration_list RBRACE { 
  $$ = new StructNode(*$2, $4); }
;

struct_declaration_list
: struct_declaration { $$ = new StructDeclarationList($1); }
| struct_declaration_list struct_declaration { 
  $1->add($2);
  $$ = $1;
 }
;

struct_declaration
: struct_specifier SEMICOLON { $$ = $1 } /* struct */
| struct_declarator SEMICOLON { $$ = $1 }
;

direct_declarator
: '*' IDENTIFIER { $$ = new DirectDeclaration(*$2, true); }
| IDENTIFIER { $$ = new DirectDeclaration(*$1, false); }
| IDENTIFIER '[' INTEGER ']' { $$ = new ArrayNode(*$1, $3); }
;

struct_declarator
: TYPEDEF_NAME direct_declarator EQUAL expr { 
  $$ = new AssignNode(*$1, $2, $4); 
}
;


%%

void PSU::Parser::error(const Parser::location_type& l, const std::string &m) {

}

int main(int argc, char *arvg[]) {

    PSU::Driver driver;
    
    bool result = driver.parse_file("test.cmn");
    driver.tree->print(std::cout, 0);
    return 0;
}
