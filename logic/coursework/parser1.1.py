class Parser:

    final_output = []
    
    parse_outputs = {
        "~"   : "a negation of a formula",
        "\/" : "Or",
        "/\r" : "And",
        "=>"  : "Implies",
        "A"   : "a universally quantified formula",
        "E"   : "an existentially quantified formula",
        "*"   : "binary connective"
    }

    propositions = ['p', 'q', 'r']

    def __init__(self, input_string):
        self.input_string = input_string

    def read_string(self):
        for character in self.input_string:
            self.formula_parser(character)
        print(self.final_output)

    def formula_parser(self, character):
        if character in self.parse_outputs:
            self.final_output.append(self.parse_outputs[character])

phrase = Parser("p\/q").read_string()