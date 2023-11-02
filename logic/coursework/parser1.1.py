class Parser:

    final_output = []

    parse_outputs = ['not a formula',
                'an atom',
                '',
                
                
                'a binary connective first order formula',
                'a proposition',
                'a negation of a propositional formula',
                'a binary connective propositional formula']
    
    parse_outputs = {
        "~": "a negation of a first order logic formula",
        "A": "a universally quantified formula",
        "E": "an existentially quantified formula",
        
    }

    def __init__(self, input_string):
        self.input_string = input_string

    def read_string(self):
        for character in self.input_string:
            self.formula_parser(character)

    def formula_parser(self):
        

    