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
    os << std::endl;
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


class AssignNode : public ExprNode {
 private:
  std::string name;
  std::string type;
  ExprNode* def;
 public:
  explicit AssignNode(std::string _type, std::string _name, ExprNode* _def) 
    : ExprNode(), type(_type), name(_name), def(_def) {}
  
  virtual void print(std::ostream &os, unsigned int depth) const {
    os << indent(depth) << type << " " << name << " = ";
    def->print(os, depth);
    os << ";";
  }
};

#endif
