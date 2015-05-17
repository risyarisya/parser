#ifndef EXAMPLE_SCANNER_H
#define EXAMPLE_SCANNER_H

#ifndef YY_DECL
#define YY_DECL \
  PSU::Parser::token_type			\
  PSU::Scanner::lex(				\
		    PSU::Parser::semantic_type* yylval,	\
		    PSU::Parser::location_type* yylloc	\
						)
#endif

#ifndef __FLEX_LEXER_H
#define yyFlexLexer PSUFlexLexer
#include "FlexLexer.h"
#undef yyFlexLexer
#endif

#include "parser.hpp"

namespace PSU {
  class Scanner : public PSUFlexLexer
  {
  public:
    Scanner(std::istream* arg_yyin = 0, std::ostream* arg_yyout = 0);
    virtual ~Scanner();
    virtual Parser::token_type lex(
				   Parser::semantic_type* yylval,
				   Parser::location_type* yylloc
				   );
    void set_debug(bool b);
  };
}

#endif
