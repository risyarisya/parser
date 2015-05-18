#ifndef EXPRESSION_H
#define EXPRESSION_H

#include <map>
#include <vector>
#include <ostream>
#include <stdexcept>
class ExprNode
{
 public:
  virtual ~ExprNode() {}

  virtual void print(std::ostream &os, unsigned int depth=0) const = 0;
  static inline std::string indent(unsigned int d) {
    return std::string(d*2, ' ');
  }
};

class StructDeclarationList : public ExprNode
{
 private:
  std::vector<ExprNode*> defs;
 public:
  StructDeclarationList(ExprNode* _def) 
    : ExprNode() {
    defs.clear();
    defs.push_back(_def);
  }
  virtual ~StructDeclarationList() {
    for (unsigned int i=0; i<defs.size(); ++i) {
      delete defs[i];
    }
    defs.clear();
  }
  void add(ExprNode* def) {
    defs.push_back(def);
  }
  virtual void print(std::ostream &os, unsigned int depth) const {
    for (unsigned int i=0; i<defs.size(); ++i) {
      defs[i]->print(os, depth+1);
      os << std::endl;
    }
  }
};

class StructNode : public ExprNode
{
 private:
  std::string name;
  StructDeclarationList* defs;

 public:  
  explicit StructNode(std::string _name, StructDeclarationList*  _defs) 
    : ExprNode(), name(_name), defs(_defs) {
  }

  virtual ~StructNode() {
    delete defs;
  }

  virtual void print(std::ostream &os, unsigned int depth) const
  {
    os << indent(depth) << "struct " << name << " {" << std::endl;
    defs->print(os, depth+1);
    os << indent(depth) << "};" << std::endl;
  }
};

  
class IntegerNode : public ExprNode {
 private:
  int value;

 public:
  explicit IntegerNode(int _value) 
    : ExprNode(), value(_value) {
  }

  virtual ~IntegerNode() {
  }

  virtual void print(std::ostream &os, unsigned int depth) const {
    os << value; 
  }
};

class HexNode : public ExprNode {
 private:
  std::string value;
 public:
  explicit HexNode(std::string _name) 
    : ExprNode(), value(_name) {
  }
  
  virtual ~HexNode() {}

  virtual void print(std::ostream &os, unsigned int depth) const {
    os << value;
  }
};

class StringNode : public ExprNode {
 private:
  std::string value;
 public:
  StringNode(std::string _value) 
    :ExprNode(), value(_value) { }
  virtual void print(std::ostream &os, unsigned int depth) const {
    os << '"' << value << '"';
  }
};

class DirectDeclaration : public ExprNode {
 private:
  std::string name;
  bool isPointer;
 public:
  explicit DirectDeclaration(std::string _name, bool _isPointer)
    : ExprNode(), name(_name), isPointer(_isPointer) {}
  virtual void print(std::ostream &os, unsigned int depth) const {
    os << ((isPointer) ? "*" : "") << name;
  }
};

class ArrayNode : public ExprNode {
 private:
  int cnt;
  std::string name;
 public:
  explicit ArrayNode(std::string _name, int _cnt)
    : ExprNode(), name(_name), cnt(_cnt) {}
  virtual void print(std::ostream &os, unsigned int depth) const {
    os << name << "[" << cnt << "]";
  }
};

class AssignNode : public ExprNode {
 private:
  ExprNode* dec;
  std::string type;
  ExprNode* def;
 public:
  explicit AssignNode(std::string _type, ExprNode* _dec, ExprNode* _def) 
    : ExprNode(), type(_type), dec(_dec), def(_def) {}
  
  virtual void print(std::ostream &os, unsigned int depth) const {
    os << indent(depth) << type << " ";
    dec->print(os, depth);
    os << " = ";
    def->print(os, depth);
    os << ";";
  }
};

#endif
