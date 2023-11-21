
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

        open_brackets = 0
        for i in range(1, len(self.fmla) - 1):
            if self.fmla[i] == '(':
                open_brackets += 1
            elif self.fmla[i] == ')':
                open_brackets -= 1
            elif open_brackets == 0:  # Potential binary connective at top level
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
            return self.fmla + " is " + parseOutputs[0]
        if self.is_negation():
            return self.fmla + " is " +  parseOutputs[7]
        elif self.is_binary_connective():
            return self.fmla + " is " + parseOutputs[8]
        elif self.is_proposition():
            return self.fmla + " is " + parseOutputs[6]
    
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
        if len(self.fmla) > 2 and self.fmla.startswith('A') and self.fmla[1] in ['x', 'y', 'z', 'w']:
            return FirstOrderLogic(self.fmla[2:]).is_fmla()
        return False

    def is_existentially_quantified(self):
        if len(self.fmla) > 2 and self.fmla.startswith('E') and self.fmla[1] in ['x', 'y', 'z', 'w']:
            return FirstOrderLogic(self.fmla[2:]).is_fmla()
        return False

    def is_binary_connective(self):
        if not (self.fmla.startswith('(') and self.fmla.endswith(')')):
            return None

        open_brackets = 0
        for i in range(1, len(self.fmla) - 1):
            if self.fmla[i] == '(':
                open_brackets += 1
            elif self.fmla[i] == ')':
                open_brackets -= 1
            elif open_brackets == 0:
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
            return self.fmla + " is " + parseOutputs[0]
        if self.is_predicate():
            return self.fmla + " is " + parseOutputs[1]
        if self.is_negation():
            return self.fmla + " is " + parseOutputs[2]
        if self.is_universally_quantified():
            return self.fmla + " is " + parseOutputs[3]
        if self.is_existentially_quantified():
            return self.fmla + " is " + parseOutputs[4]
        if self.is_binary_connective():
            return self.fmla + " is " + parseOutputs[5]
    
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
    if Proposition(fmla).is_fmla():
        return Proposition(fmla).parse()
    elif FirstOrderLogic(fmla).is_fmla():
        return FirstOrderLogic(fmla).parse()
    else:
        return fmla + " is " + parseOutputs[0]
    

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
    for char in 'abcdefghijklmnopqrstuvwxyz':
        if char not in existing_constants:
            return char
    raise Exception("Exhausted all possible constants")

def is_closed(tableau):
    for branch in tableau:
        for fmla in branch:
            if contradict(fmla, branch):
                return True
    return False

def expanded(tableau):
    print(tableau)
    for branch in tableau:
        for fmla in branch:
            if is_non_literal(fmla):
                return False
    return True

def contradict(fmla, branch):
    negation = '~' + fmla if not fmla.startswith('~') else fmla[1:]
    return negation in branch

def is_non_literal(fmla):
    prop = Proposition(fmla)
    fol = FirstOrderLogic(fmla)

    return (prop.is_binary_connective() is not None) or \
           fol.is_binary_connective() or \
           fol.is_universally_quantified() or \
           fol.is_existentially_quantified()

def sat(tableau):
    print(tableau)
    while tableau:
        sigma = tableau.pop(0)
        constant_count = 0

        if expanded(sigma) and not is_closed(sigma):
            return 1  # satisfiable

        for phi in sigma:
            if is_non_literal(phi):
                # Apply the correct expansion rule
                fmla_type = determine_fmla_type(phi)
                if fmla_type == 'alpha':
                    FmlaTypes.alpha(phi, sigma)
                elif fmla_type == 'beta':
                    FmlaTypes.beta(phi, sigma)
                elif fmla_type == 'gamma':
                    FmlaTypes.gamma(phi, sigma, constants)
                elif fmla_type == 'delta':
                    constant_count, constants = FmlaTypes.delta(phi, sigma, constant_count, constants)

            if constant_count > MAX_CONSTANTS:
                return 2  # undetermined

    return 0  # not satisfiable

def determine_fmla_type(fmla):
    prop = Proposition(fmla)
    fol = FirstOrderLogic(fmla)

    if prop.is_binary_connective() or fol.is_binary_connective():
        return 'alpha' if con(fmla) == '/\\' else 'beta'
    elif fol.is_universally_quantified():
        return 'gamma'
    elif fol.is_existentially_quantified():
        return 'delta'

# with open('input.txt', 'r') as f:
#     for line in f:
#         print(line + "     " + satOutput[sat(theory(line))])

# fol = FirstOrderLogic("(AxAyEz(P(x,z)/\P(z,y))/\ExP(x,x))")
# print(fol.parse())

print(parse('(~p=>p)'), "  " , satOutput[sat(theory('(~p=>p)'))])