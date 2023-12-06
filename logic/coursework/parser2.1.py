
MAX_LIMIT = 10


class PropositionalStatement:


   def __init__(self, expression):
       self.expression = expression.strip()


   def is_simple_statement(self):
       return self.expression in  ['p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
  
   def check_negation(self):
       if self.expression.startswith('~'):
           if self.expression[1:].startswith('(') and self.expression[-1] == ')':
               if PropositionalStatement(self.expression[2:-1]).is_simple_statement():
                   return False
           return True
       return False


   def is_alpha(self):
       connector = con(self.expression)
       return connector in ['/\\']


   def is_beta(self):
       connector = con(self.expression)
       return connector in ['\/', '=>']


   def check_connective(self):
       operators = ['=>', '/\\', '\\/']
       if not (self.expression.startswith('(') and self.expression.endswith(')')):
           return None


       count_brackets = 0
       for idx in range(1, len(self.expression) - 1):
           if self.expression[idx] == '(':
               count_brackets += 1
           elif self.expression[idx] == ')':
               count_brackets -= 1
           elif count_brackets == 0:
               for op in operators:
                   if self.expression[idx:idx+len(op)] == op:
                       left_part = self.expression[1:idx]
                       right_part = self.expression[idx+len(op):-1]
                       return left_part, op, right_part
       return None
  
   def validate_expression(self):
       if ' ' in self.expression or not validate_brackets(self.expression):
           return False
       if self.is_simple_statement() or self.check_negation() or self.check_connective():
           return True
       return False
  


   def analyze(self):
       if not self.validate_expression():
           return 0
       if self.check_negation():
           return 7
       elif self.check_connective():
           return 8
       elif self.is_simple_statement():
           return 6

class PredicateStatement:
   def __init__(self, expression):
       self.expression = expression.strip()


   def is_var(self):
       return self.expression in ['x', 'y', 'z', 'w']


   def is_predicate(self):
       predicates = ['P', 'Q', 'R', 'S']
       if len(self.expression) > 4 and self.expression[0] in predicates and self.expression[1] == '(' and self.expression[-1] == ')' and ',' in self.expression:
           variables = self.expression[2:-1].split(',')
           return len(variables) == 2 and all(var in ['x', 'y', 'z', 'w']  for var in variables)
       return False


   def check_negation(self):
       return self.expression.startswith('~') and PredicateStatement(self.expression[1:]).validate_expression()


   def is_universal(self):
       return self.expression.startswith('A') and self.expression[1] in ['x', 'y', 'z', 'w'] and PredicateStatement(self.expression[2:]).validate_expression()


   def is_existential(self):
       return self.expression.startswith('E') and self.expression[1] in ['x', 'y', 'z', 'w']  and PredicateStatement(self.expression[2:]).validate_expression()


   def check_connective(self):
       if not (self.expression.startswith('(') and self.expression.endswith(')')):
           return None


       count_brackets = 0
       for idx in range(1, len(self.expression) - 1):
           if self.expression[idx] == '(':
               count_brackets += 1
           elif self.expression[idx] == ')':
               count_brackets -= 1
           elif count_brackets == 0:
               for op in ['=>', '/\\', '\\/']:
                   if self.expression[idx:idx+len(op)] == op:
                       left_part = self.expression[1:idx]
                       right_part = self.expression[idx+len(op):-1]
                       if PredicateStatement(left_part).validate_expression() and PredicateStatement(right_part).validate_expression():
                           return left_part, op, right_part
       return None


   def validate_expression(self):
       if ' ' in self.expression or not validate_brackets(self.expression):
           return False       
       return self.is_predicate() or self.check_negation() or self.is_universal() or self.is_existential() or self.check_connective()


   def analyze(self):
       if not self.validate_expression():
           return 0
       if self.is_predicate():
           return 1
       if self.check_negation():
           return 2
       if self.is_universal():
           return 3
       if self.is_existential():
           return 4
       if self.check_connective():
           return 5
      
def validate_brackets(expression):
   stack = []
   for char in expression:
       if char == '(':
           stack.append(char)
       elif char == ')':
           if not stack:
               return False
           stack.pop()
   return len(stack) == 0


def parse(expression):
   if PredicateStatement(expression).validate_expression():
       return PredicateStatement(expression).analyze()
   elif PropositionalStatement(expression).validate_expression():
       return PropositionalStatement(expression).analyze()
   else:
       return 0


def lhs_clean(expression):
   return clean_negations(lhs(expression))
def rhs_clean(expression):
   return clean_negations(rhs(expression))


def lhs(expression):
   if PredicateStatement(expression).validate_expression():
       result = PredicateStatement(expression).check_connective()
       if result:
           return result[0]
   elif PropositionalStatement(expression).validate_expression():
       result = PropositionalStatement(expression).check_connective()
       if result:
           return result[0]
   return ''


def con(expression):
   if PredicateStatement(expression).validate_expression():
       result = PredicateStatement(expression).check_connective()
       if result:
           return result[1]
   elif PropositionalStatement(expression).validate_expression():
       result = PropositionalStatement(expression).check_connective()
       if result:
           return result[1]
   return ''


def rhs(expression):
   if PredicateStatement(expression).validate_expression():
       result = PredicateStatement(expression).check_connective()
       if result:
           return result[2]
   elif PropositionalStatement(expression).validate_expression():
       result = PropositionalStatement(expression).check_connective()
       if result:
           return result[2]
   return ''


def theory(expression):
   return [expression]


class Node:
   def __init__(self, expression, parent=None):
       self.expression = expression
       self.parent = parent
       self.children = []


   def add_child(self, expression):
       child = Node(expression, self)
       self.children.append(child)
       return child


def find_leaf_nodes(node):
   if not node.children:
       return [node]
   else:
       return [leaf for child in node.children for leaf in find_leaf_nodes(child)]


def clean_negations(expression):
   # if there are an odd number of negations leave only 1. if there are even remove them all
   count = 0
   for char in expression:
       if char == '~':
           count += 1
       else:
           break
   if count % 2 == 0:
       return expression[count:]
   else:
       return '~' + expression[count:]
  
def expand_node(node):
   expr = node.expression
   expr = clean_negations(expr)
   parsed = parse(expr)

   if parsed == 7:  # Negated proposition
       child_expr = expr[1:]
       child_expr = clean_negations(child_expr)   
       if PropositionalStatement(child_expr).is_simple_statement():
           return []
       elif PropositionalStatement(child_expr).check_connective():
           lhs_expr, con_expr, rhs_expr = lhs_clean(child_expr), con(child_expr), rhs_clean(child_expr)
           if con_expr == '/\\':  # Conjunction
               leaf_nodes = find_leaf_nodes(node)
               added_nodes = []
               for leaf in leaf_nodes:
                   new_node = leaf.add_child(clean_negations(f'~{lhs_expr}'))
                   other_node = leaf.add_child(clean_negations(f'~{rhs_expr}'))
                   added_nodes.append(new_node)
                   added_nodes.append(other_node)
               return added_nodes
           elif con_expr == '\\/':  # Disjunction
               leaf_nodes = find_leaf_nodes(node)
               added_nodes = []
               for leaf in leaf_nodes:
                   new_node = leaf.add_child(clean_negations(f'~{lhs_expr}'))
                   other_node = new_node.add_child(clean_negations(f'~{rhs_expr}'))
                   added_nodes.append(new_node)
                   added_nodes.append(other_node)
               return added_nodes
           elif con_expr == '=>':  # Implication
               leaf_nodes = find_leaf_nodes(node)
               added_nodes = []
               for leaf in leaf_nodes:
                   new_node = leaf.add_child(lhs_expr)
                   other_node = new_node.add_child(clean_negations(f'~{rhs_expr}'))
                   added_nodes.append(new_node)
                   added_nodes.append(other_node)
               return added_nodes


   if parsed == 8:  # Binary connective propositional formula
       lhs_expr, con_expr, rhs_expr = lhs_clean(expr), con(expr), rhs_clean(expr)
       if con_expr == '/\\':  # Conjunction
           leaf_nodes = find_leaf_nodes(node)
           added_nodes = []
           for leaf in leaf_nodes:
               new_node = leaf.add_child(lhs_expr)
               other_node = new_node.add_child(rhs_expr)
               added_nodes.append(new_node)
               added_nodes.append(other_node)
           return added_nodes
       elif con_expr == '\\/':  # Disjunction or implication
           leaf_nodes = find_leaf_nodes(node)
           added_nodes = []
           for leaf in leaf_nodes:
               new_node = leaf.add_child(lhs_expr)
               other_node = leaf.add_child(rhs_expr)
               added_nodes.append(new_node)
               added_nodes.append(other_node)
           return added_nodes
       elif con_expr == '=>':  # Implication
           leaf_nodes = find_leaf_nodes(node)
           added_nodes = []
           for leaf in leaf_nodes:
               new_node = leaf.add_child(clean_negations(f'~{lhs_expr}'))
               other_node = leaf.add_child(rhs_expr)
               added_nodes.append(new_node)
               added_nodes.append(other_node)
           return added_nodes


   # Similar handling for first-order logic statements would go here...
   return []




def build_tableau(root):
   nodes_to_expand = [root]
   while nodes_to_expand:
       current_node = nodes_to_expand.pop()
       children = expand_node(current_node)
       # print(current_node.expression, [child.expression for child in children])
       nodes_to_expand.extend(children)


def print_tree(node, indent=''):
   if node is None:
       return
   print(f'{indent}{node.expression}')
   for child in node.children:
       print_tree(child, indent + '  ')
  
  
def check_root_closed(node):
   def dfs(node, seen):
       if node is None:
           return True
       if node.expression.startswith('~') and node.expression[1:] in seen:
           return True
       if not node.expression.startswith('~') and '~' + node.expression in seen:
           return True
       seen = seen.copy()
       seen.add(node.expression)
       if not node.children:  # If the node is a leaf
           return False 
       return all(dfs(child, seen) for child in node.children)


   return dfs(node, set())
  


def sat(tableau):
   expression = tableau[0][0]
   root = Node(expression)
   build_tableau(root)
   # print tree from root to leaves
   print_tree(root)
   return not check_root_closed(root)




f = open('input.txt')


parseOutputs = ['not a formula',
               'an atom',
               'a negation of a first order logic formula',
               'a universally quantified formula',
               'an existentially quantified formula',
               'a binary connective first order formula',
               'a proposition',
               'a negation of a propositional formula',
               'a binary connective propositional formula']


satOutput = ['is not satisfiable', 'is satisfiable', 'may or may not be satisfiable']


firstline = f.readline()


PARSE = False
if 'PARSE' in firstline:
   PARSE = True


SAT = False
if 'SAT' in firstline:
   SAT = True
for line in f:
   if line[-1] == '\n':
       line = line[:-1]
   parsed = parse(line)


   if PARSE:
       output = "%s is %s." % (line, parseOutputs[parsed])
       if parsed in [5,8]:
           output += " Its left hand side is %s, its connective is %s, and its right hand side is %s." % (lhs(line), con(line) ,rhs(line))
       print(output)


   if SAT:
       if parsed:
           tableau = [theory(line)]
           print('%s %s.' % (line, satOutput[sat(tableau)]))
       else:
           print('%s is not a formula.' % line)

