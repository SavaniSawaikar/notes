
MAX_CONSTANTS = 10

class Proposition:

    def __init__(self, fmla):
        self.fmla = fmla.strip()

    def is_proposition(self):
        return self.fmla in ['p', 'q', 'r', 's']
    
    def is_negation(self):
        if self.fmla.startswith('~'):
            if self.fmla[1:].startswith('(') and self.fmla[1:].endswith(')'):
                if Proposition(self.fmla[2:-1]).is_proposition():
                    return False
            return True
        return False
    
    def is_binary_connective(self):
        connectives = ['=>', '/\\', '\\/']
        if not (self.fmla.startswith('(') and self.fmla.endswith(')')):
            return None

        brackets = 0
        for i in range(1, len(self.fmla) - 1):
            if self.fmla[i] == '(':
                brackets += 1
            elif self.fmla[i] == ')':
                brackets -= 1
            elif brackets == 0:  # Potential binary connective at top level
                for conn in connectives:
                    if self.fmla[i:i+len(conn)] == conn:
                        left = self.fmla[1:i]
                        right = self.fmla[i+len(conn):-1]
                        return left, conn, right
        return None
    
    def is_fmla(self):
        if ' ' in self.fmla or not check_matching_brackets(self.fmla):
            return False
        if self.is_proposition():
            return True
        elif self.is_negation():
            return True
        elif bool(self.is_binary_connective()):
            return True
        return False
    
    def parse(self):
        # Check if it is actually a formula
        if not self.is_fmla():
            return 0
        if self.is_negation():
            return 7
        elif self.is_binary_connective():
            return 8
        elif self.is_proposition():
            return 6

class FirstOrderLogic:
    def __init__(self, fmla):
        self.fmla = fmla.strip()

    def is_variable(self):
        return self.fmla in ['x', 'y', 'z', 'w']

    def is_predicate(self):
        predicates = ['P', 'Q', 'R', 'S']
        if len(self.fmla) > 4 and self.fmla[0] in predicates and self.fmla[1] == '(' and self.fmla[-1] == ')' and ',' in self.fmla:
            vars = self.fmla[2:-1].split(',')
            return len(vars) == 2 and all(var in ['x', 'y', 'z', 'w'] for var in vars)
        return False

    def is_negation(self):
        return self.fmla.startswith('~') and FirstOrderLogic(self.fmla[1:]).is_fmla()

    def is_universally_quantified(self):
        return self.fmla.startswith('A') and self.fmla[1] in ['x', 'y', 'z', 'w'] and FirstOrderLogic(self.fmla[2:]).is_fmla()

    def is_existentially_quantified(self):
        return self.fmla.startswith('E') and self.fmla[1] in ['x', 'y', 'z', 'w'] and FirstOrderLogic(self.fmla[2:]).is_fmla()

    def is_binary_connective(self):
        if not (self.fmla.startswith('(') and self.fmla.endswith(')')):
            return None

        brackets = 0
        for i in range(1, len(self.fmla) - 1):
            if self.fmla[i] == '(':
                brackets += 1
            elif self.fmla[i] == ')':
                brackets -= 1
            elif brackets == 0:
                for conn in ['=>', '/\\', '\\/']:
                    if self.fmla[i:i+len(conn)] == conn:
                        left = self.fmla[1:i]
                        right = self.fmla[i+len(conn):-1]
                        if FirstOrderLogic(left).is_fmla() and FirstOrderLogic(right).is_fmla():
                            return left, conn, right
        return None

    def is_fmla(self):
        if ' ' in self.fmla or not check_matching_brackets(self.fmla):
            return False
        return self.is_predicate() or self.is_negation() or self.is_universally_quantified() or self.is_existentially_quantified() or bool(self.is_binary_connective())

    def parse(self):
        if not self.is_fmla():
            return 0
        if self.is_predicate():
            return 1
        if self.is_negation():
            return 2
        if self.is_universally_quantified():
            return 3
        if self.is_existentially_quantified():
            return 4
        if self.is_binary_connective():
            return 5
    
# Check if a formula has matching brackets
def check_matching_brackets(fmla):
    stack = []
    for elem in fmla:
        if elem == '(':
            stack.append(elem)
        elif elem == ')':
            if len(stack) == 0:
                return False
            stack.pop()
    if len(stack) == 0:
        return True
    return False

# Parse a formula, consult parseOutputs for return values.
def parse(fmla):
    if FirstOrderLogic(fmla).is_fmla():
        return FirstOrderLogic(fmla).parse()
    elif Proposition(fmla).is_fmla():
        return Proposition(fmla).parse()
    else:
        return 0

# Return the LHS of a binary connective formula
def lhs(fmla):
    if FirstOrderLogic(fmla).is_fmla():
        if FirstOrderLogic(fmla).is_binary_connective():
            return FirstOrderLogic(fmla).is_binary_connective()[0]
        else:
            return ''
    elif Proposition(fmla).is_fmla():
        if Proposition(fmla).is_binary_connective():
            return Proposition(fmla).is_binary_connective()[0]
        else:
            return ''
    else:
        return ''

# Return the connective symbol of a binary connective formula
def con(fmla):
    if FirstOrderLogic(fmla).is_fmla():
        if FirstOrderLogic(fmla).is_binary_connective():
            return FirstOrderLogic(fmla).is_binary_connective()[1]
        else:
            return ''
    elif Proposition(fmla).is_fmla():
        if Proposition(fmla).is_binary_connective():
            return Proposition(fmla).is_binary_connective()[1]
        else:
            return ''
    return ''

# Return the RHS symbol of a binary connective formula
def rhs(fmla):
    if FirstOrderLogic(fmla).is_fmla():
        if FirstOrderLogic(fmla).is_binary_connective():
            return FirstOrderLogic(fmla).is_binary_connective()[2]
        else:
            return ''
    elif Proposition(fmla).is_fmla():
        if Proposition(fmla).is_binary_connective():
            return Proposition(fmla).is_binary_connective()[2]
        else:
            return ''
    return '' 

# You may choose to represent a theory as a set or a list
def theory(fmla):#initialise a theory with a single formula in it
    return [fmla]

class FmlaTypes:

    @staticmethod
    def alpha(fmla, tableau):
        # Alpha expansion: Adding two formulas to the current branch
        new_elems = [lhs(fmla), rhs(fmla)]
        tableau.append([*tableau.pop(), *new_elems])

    @staticmethod
    def beta(fmla, tableau):
        # Beta expansion: Creating two new branches
        left_branch = [*tableau.pop(), lhs(fmla)]
        right_branch = [*tableau.pop(), rhs(fmla)]
        tableau.extend([left_branch, right_branch])

    @staticmethod
    def gamma(fmla, tableau, constants):
        # Gamma expansion: For universally quantified formulas
        if fmla.startswith('A'):
            variable = fmla[1]
            for constant in constants:
                new_fmla = fmla[2:].replace(variable, constant)
                if new_fmla not in tableau:
                    tableau.append(new_fmla)

    @staticmethod
    def delta(fmla, tableau, constant_count, constants):
        # Delta expansion: For existentially quantified formulas
        if fmla.startswith('E'):
            variable = fmla[1]
            new_constant = get_new_constant(constants)
            new_fmla = fmla[2:].replace(variable, new_constant)
            if new_fmla not in tableau:
                tableau.append(new_fmla)
                constants.append(new_constant)
                constant_count += 1
        return constant_count, constants
    
def get_new_constant(existing_constants):
    for char in 'abcdefghijklmnotuv':
        if char not in existing_constants:
            return char
    raise Exception("Exhausted all possible constants")


def is_non_literal(fmla):
    prop = Proposition(fmla)
    fol = FirstOrderLogic(fmla)

    return (prop.is_binary_connective() is not None) or \
           fol.is_binary_connective() or \
           fol.is_universally_quantified() or \
           fol.is_existentially_quantified()

def is_closed(tableau):
    for branch in tableau:
        for fmla in branch:
            if contradict(fmla, branch):
                return True
    return False

def expanded(tableau):
    for branch in tableau:
        for fmla in branch:
            if is_non_literal(fmla):
                return False
    return True

def contradict(fmla, branch):
    negation = '~' + fmla if not fmla.startswith('~') else fmla[1:]
    return negation in branch

global constants
constants = ['a', 'b', 'c']

def sat(tableau):
    while tableau:
        new_tableau = []
        for branch in tableau:
            if is_closed(branch) or expanded(branch):
                new_tableau.append(branch)
                continue

            for phi in branch:
                if is_non_literal(phi):
                    branch.remove(phi)
                    fmla_type = determine_fmla_type(phi)
                    if fmla_type == 'alpha':
                        branch.extend([lhs(phi), rhs(phi)])
                    elif fmla_type == 'beta':
                        new_tableau.append(branch + [lhs(phi)])
                        new_tableau.append(branch + [rhs(phi)])
                        break
                    elif fmla_type == 'gamma':
                        for constant in constants:
                            new_formula = replace_variable(phi, constant)
                            if new_formula not in branch:
                                branch.append(new_formula)
                    elif fmla_type == 'delta':
                        new_constant = get_new_constant(constants)
                        new_formula = replace_variable(phi, new_constant)
                        if new_formula not in branch:
                            branch.append(new_formula)
                            constants.append(new_constant)
                            if len(constants) > MAX_CONSTANTS:
                                return 2  # undetermined
                    break
            else:
                new_tableau.append(branch)

        if not new_tableau:
            return 0  # not satisfiable

        tableau = new_tableau

    for branch in tableau:
        if not is_closed(branch):
            return 1  # satisfiable

    return 0  # not satisfiable


def replace_variable(fmla, constant):
    if fmla.startswith('A') or fmla.startswith('E'):
        variable = fmla[1]
        scope = fmla[2:]  # Extract the scope of the quantifier

        # Replace only within the scope
        new_scope = scope.replace(variable, constant)
        new_fmla = fmla[0:2] + new_scope
        return new_fmla

    return fmla

def determine_fmla_type(fmla):
    prop = Proposition(fmla)
    fol = FirstOrderLogic(fmla)

    if prop.is_binary_connective() or fol.is_binary_connective():
        return 'alpha' if con(fmla) == '/\\' else 'beta'
    elif fol.is_universally_quantified():
        return 'gamma'
    elif fol.is_existentially_quantified():
        return 'delta'

#DO NOT MODIFY THE CODE BELOW
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