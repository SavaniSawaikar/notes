
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
        return self.fmla.startswith('A') and self.fmla[1] in ['x', 'y', 'z', 'w'] and FirstOrderLogic(self.fmla[2:]).is_fmla()

    def is_existentially_quantified(self):
        return self.fmla.startswith('E') and self.fmla[1] in ['x', 'y', 'z', 'w'] and FirstOrderLogic(self.fmla[2:]).is_fmla()

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

def expanded(fmla):
    pass

def contradict(fmla):
    pass

def is_non_literal(fmla):
    pass

dict_fmla_types = {
    'alpha' : 
}

def sat(tableau):
    tab = theory(tableau)
    while tab:
        sigma = tab.pop(0)
        if expanded(sigma) and not contradict(sigma):
            return 1
        else:
            for k in sigma:
                if is_non_literal(k):
                    switch(k):





with open('input.txt', 'r') as f:
    for line in f:
        print(lhs(line) + "   " + con(line) + "   " + rhs(line))

# fol = FirstOrderLogic("(AxAyEz(P(x,z)/\P(z,y))/\ExP(x,x))")
# print(fol.parse())