syllabic = ["BA", "CA", "DA", "FA", "GA", "HA", "JA", "KA", "LA", "MA", "NA", "NGA","PA", "QA", "RA", "SA", "TA", "VA", "WA", "XA", "YA", "ZA"]
vowel = "AEIOU "
kudlit = "eiou"


class BaybayinToLatin:  
    def __init__(self):
        self.stack = []
        self.state = "start"
        self.digraph = False
        self.consonant = ""

    # Process the input string
    def process_input(self, input_str, inSyllabic):
        i = 0
        while i < len(input_str):
            if i + 1 < len(input_str):
                trigram = input_str[i:i + 3]
                if trigram in inSyllabic:
                    self.transition(trigram)
                    i += 3
                else:
                    bigram = input_str[i:i + 2]
                    if bigram in inSyllabic:
                        self.transition(bigram)
                        i += 2
                    else:
                        self.transition(input_str[i])
                        i += 1
            else:
                self.transition(input_str[i])
                i += 1
        return ''.join(self.stack)
  # Convert the stack content to a string and return as the result

    # Adding items into the stack
    def push(self, item):
        self.stack.append(item)

    # Removing an element from the stack
    def pop(self):
        if self.stack:
            return self.stack.pop()
        else:
            return None  # Return None if the stack is empty

    # Graphical Notation of Transition in PDA
    def transition_function(self, a, b=None):
        if b is not None:
            self.pop()
            # Process popped_value if needed
        self.push(a)

    # Transition 
    def transition(self, string):
        # Start State
        if self.state == "start":
            if len(string) == 1:
                if string in vowel:
                    self.state = "vowel"
                    self.transition_function(string)
                elif string in kudlit:
                    self.state = "start"
                    self.transition_function(string)
                elif string.isspace():
                    self.state = "start"
                    self.transition_function(string)      
                else:
                    self.stack = ["Invalid Output"] 
            else:
                if string in syllabic:
                    if len(string) == 3:
                        self.state = "syllable"
                        self.consonant = string[:2]
                        self.transition_function(string)                          
                    else:
                        self.state = "syllable"
                        self.consonant = string[:1]
                        self.transition_function(string)   
                else:
                    self.stack = ["Invalid Output"] 

        # Vowel State
        elif self.state == "vowel":
            if len(string) == 1:
                if string in vowel:
                    self.state = "vowel"
                    self.transition_function(string)
                elif string in kudlit:
                    self.state = "dead"
                    self.transition_function(string)
                elif string.isspace():
                    self.state = "space"
                    self.transition_function(string)      
                else:
                    self.stack = ["Invalid Output"] 
            else:
                if string in syllabic:
                    if len(string) == 3:
                        self.state = "syllable"
                        self.consonant = string[:2]
                        self.transition_function(string)                          
                    else:
                        self.state = "syllable"
                        self.consonant = string[:1]
                        self.transition_function(string)   
                else:
                    self.stack = ["Invalid Output"] 

        # Syllable State
        elif self.state == "syllable":
            if len(string) == 1:
                if string in vowel:
                    self.state = "vowel"
                    self.transition_function(string)
                elif string in kudlit:
                    self.state = "kudlit"
                    self.transition_function(self.consonant + string.upper(), "syllabic")
                elif string.isspace():
                    self.state = "space"
                    self.transition_function(string)      
                else:
                    self.stack = ["Invalid Output"] 
            else:
                if string in syllabic:
                    if len(string) == 3:
                        self.state = "syllable"
                        self.consonant = string[:2]
                        self.transition_function(string)                          
                    else:
                        self.state = "syllable"
                        self.consonant = string[:1]
                        self.transition_function(string)   
                else:
                    self.stack = ["Invalid Output"] 

        # Space State        
        elif self.state == "space":
            if len(string) == 1:
                if string in vowel:
                    self.state = "vowel"
                    self.transition_function(string)
                elif string in kudlit:
                    self.state = "space"
                    self.transition_function(string)
                elif string.isspace():
                    self.state = "space"
                    self.transition_function(string)      
                else:
                    self.stack = ["Invalid Output"] 
            else:
                if string in syllabic:
                    if len(string) == 3:
                        self.state = "syllable"
                        self.consonant = string[:2]
                        self.transition_function(string)                          
                    else:
                        self.state = "syllable"
                        self.consonant = string[:1]
                        self.transition_function(string)   
                else:
                    self.stack = ["Invalid Output"] 

        # Kudlit State
        elif self.state == "kudlit":
            if len(string) == 1:
                if string in vowel:
                    self.state = "vowel"
                    self.transition_function(string)
                elif string in kudlit:
                    self.state = "dead"
                    self.transition_function(string)
                elif string.isspace():
                    self.state = "space"
                    self.transition_function(string)      
                else:
                    self.stack = ["Invalid Output"] 
            else:
                if string in syllabic:
                    if len(string) == 3:
                        self.state = "syllable"
                        self.consonant = string[:2]
                        self.transition_function(string)                          
                    else:
                        self.state = "syllable"
                        self.consonant = string[:1]
                        self.transition_function(string)   
                else:
                    self.stack = ["Invalid Output"]  

        # Dead State
        elif self.state == "dead":
            if len(string) == 1:
                if string in vowel:
                    self.state = "dead"
                    self.transition_function(string)
                elif string in kudlit:
                    self.state = "dead"
                    self.transition_function(string)
                elif string.isspace():
                    self.state = "dead"
                    self.transition_function(string)      
                else:
                    self.stack = ["Invalid Output"] 
            else:
                if string in syllabic:
                    if len(string) == 3:
                        self.state = "syllable"
                        self.consonant = string[:2]
                        self.transition_function(string)                          
                    else:
                        self.state = "syllable"
                        self.consonant = string[:1]
                        self.transition_function(string)   
                else:
                    self.stack = ["Invalid Output"] 
                
if __name__ == "__main__":
        pda = BaybayinToLatin()
        input_str = input("Enter a Baybayin string: ")
        result = pda.process_input(input_str, syllabic)
        
        if pda.state == "start": # If input is only in a start state
            result = "Enter a character"
        elif pda.state == "dead": # If last input is not in a final state
            result = "Input not available in Baybayin"
            
        print("Latin output:", result)
