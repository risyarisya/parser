#ifndef DRIVER_H
#define DRIVER_H

#include <string>
#include "expression.h"


namespace PSU {
class Driver
{
 public:
  Driver();
  bool trace_scanning;
  bool trace_parsing;
  ExprNode* tree;
  ~Driver();
  std::string streamname;
  bool parse_stream(std::istream& in,
  		    const std::string& sname);

  bool parse_string(const std::string& input,
	    const std::string& sname);
  
  bool parse_file(const std::string& filename);
  bool parse_file();

  void error(const class location& l, const std::string& m);
  void error(const std::string& m);

  class Scanner* lexer;
};
}

#endif
