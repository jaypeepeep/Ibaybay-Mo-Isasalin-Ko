vowels_lower = "aeiou"
vowels_upper = vowels_lower.upper()

consonants_lower = "bcdfghjklmnpqrstvwxyz"
consonants_upper = consonants_lower.upper()

consonants_for_digraph = "n"
consonants_for_digraph_upper = consonants_for_digraph.upper()

second_consonants_for_digraph_lower = "g"
second_consonants_for_digraph_upper = second_consonants_for_digraph_lower.upper()

class LatinToBaybayin:
    def __init__(self):
        self.stack = []
        self.state = "start"
        self.digraph = False

    # Process the input string
    def process_input(self, input_str):
        for char in input_str:
            self.transition(char)
        return ''.join(self.stack)  # Convert the stack content to a string and return as the result

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
        if a is not None:
            self.push(a)

    # Transition 
    def transition(self, char):
        # Start State
        if self.state == "start":
            if char.lower() in vowels_lower or char.upper() in vowels_upper:
                self.state = "vowel"
                self.transition_function(char)
            elif char.lower() in consonants_lower or char.upper() in consonants_upper:
                if char.lower() == consonants_for_digraph or char.upper() == consonants_for_digraph_upper:
                    self.state = "consonant"
                    self.transition_function(char)
                    self.digraph = True
                else:
                    self.state = "consonant"
                    self.transition_function(char)
            elif char.isspace():
                self.state = "start"
                self.transition_function("||")
            else:
                self.stack = ["Invalid Output"]
                
        # Vowel State
        elif self.state == "vowel":
            if char.lower() in vowels_lower or char.upper() in vowels_upper:
                self.state = "vowel"
                self.transition_function(char)
            elif char.lower() in consonants_lower or char.upper() in consonants_upper:
                if char.lower() == consonants_for_digraph or char.upper() == consonants_for_digraph_upper:
                    self.state = "consonant"
                    self.transition_function(char)
                    self.digraph = True
                else:
                    self.state = "consonant"
                    self.transition_function(char)
            elif char.isspace():
                self.state = "space"
                self.transition_function("||")
            else:
                self.stack = ["Invalid Output"]
                
        elif self.state == "consonant":
            if char.lower() in vowels_lower or char.upper() in vowels_upper:
                self.state = "syllable"
                self.transition_function(char)
            elif char.lower() in consonants_lower or char.upper() in consonants_upper:
                if char.lower() in second_consonants_for_digraph_lower or char.upper() in second_consonants_for_digraph_upper and self.digraph == True:
                    self.state = "digraph"
                    self.transition_function("NG", consonants_for_digraph)
                else:
                    self.state = "dead"
                    self.transition_function(char)
            elif char.isspace():
                self.state = "dead"
                self.transition_function("||")
            else:
                self.stack = ["Invalid Output"]  
        
        elif self.state == "syllable":
            if char.lower() in vowels_lower or char.upper() in vowels_upper:
                self.state = "vowel"
                self.transition_function(char)
            elif char.lower() in consonants_lower or char.upper() in consonants_upper:
                if char.lower() in consonants_for_digraph or char.upper() in consonants_for_digraph_upper:
                    self.state = "final_consonant"
                    self.transition_function(char)
                    self.digraph = True
                else:
                    self.state = "final_consonant"
                    self.transition_function(char)
            elif char.isspace():
                self.state = "space"
                self.transition_function("||")
            else:
                self.stack = ["Invalid Output"]  
        
        elif self.state == "digraph":
            # Input is a vowel
            if char.lower() in vowels_lower or char.upper() in vowels_upper:
                self.state = "syllable"
                self.digraph = False
                self.transition_function(char)
            # Input is a consonant
            elif char.lower() in consonants_lower or char.upper() in consonants_upper:
                self.state = "dead"
                self.transition_function(char)
            # Input is a space
            elif char.isspace():
                self.state = "dead"
                self.transition_function(char)
            elif char.isspace():
                self.state = "dead"
                self.transition_function("||")
            else:
                self.stack = ["Invalid Output"]  

        elif self.state == "final_consonant":
            # Input is a vowel
            if char.lower() in vowels_lower or char.upper() in vowels_upper:
                self.state = "syllable"
                self.transition_function(char)
            # Input is a consonant
            elif char.lower() in consonants_lower or char.upper() in consonants_upper:
                # Consonant can form a digraph
                if char.lower() in second_consonants_for_digraph_lower or char.upper() in second_consonants_for_digraph_upper and self.digraph == True:
                    self.state = "final_digraph"
                    self.transition_function("NG", consonants_for_digraph)
                elif char.lower() in consonants_for_digraph or char.upper() in consonants_for_digraph_upper:
                    self.state = "consonant"
                    self.digraph = True
                    self.transition_function(char, "consonant")
                else:
                    self.state = "consonant"
                    self.transition_function(char, "consonant")
            elif char.isspace():
                self.state = "space"
                self.transition_function("||", "final consonant")
            else:
                self.stack = ["Invalid Output"]  

        elif self.state == "final_digraph":
            # Input is a vowel
            if char.lower() in vowels_lower or char.upper() in vowels_upper:
                self.state = "syllable"
                self.digraph = False
                self.transition_function(char)
            # Input is a consonant
            elif char.lower() in consonants_lower or char.upper() in consonants_upper:
                # Consonant can form a digraph
                if char.lower() in consonants_for_digraph or char.upper() in consonants_for_digraph_upper:
                    self.state = "consonant"
                    self.digraph = True
                    self.transition_function(char, "final_digraph")

                else:
                    self.state = "consonant"
                    self.transition_function(char, "final_digraph")
            elif char.isspace():
                self.state = "space"
                self.transition_function("||", "final_digraph")
            else:
                self.stack = ["Invalid Output"]  
                
        elif self.state == "space":
            if char.lower() in vowels_lower or char.upper() in vowels_upper:
                self.state = "vowel"
                self.transition_function(char)
            # Input is a consonant
            elif char.lower() in consonants_lower or char.upper() in consonants_upper:
                if char.lower() in consonants_for_digraph or char.upper() in consonants_for_digraph_upper:
                    self.state = "consonant"
                    self.digraph = True
                    self.transition_function(char)
                else:
                    self.state = "consonant"
                    self.transition_function(char)
            # Input is a space
            elif char.isspace():
                self.state = "space"
                self.transition_function("||")
            else:
                self.result = "Invalid input"

        elif self.state == "dead":
            # Input is a vowel
            if char.lower() in vowels_lower or char.upper() in vowels_upper:
                self.state = "dead"
                self.transition_function(char)
            # Input is a consonant
            elif char.lower() in consonants_lower or char.upper() in consonants_upper:
                self.state = "dead"
                self.transition_function(char)
            # Input is a space
            elif char.isspace():
                self.state = "dead"
                self.transition_function(char)
            else:
                self.result = "Invalid input"
                
if __name__ == "__main__":
    while True:
        pda = LatinToBaybayin()
        input_str = input("Enter a Latin string: ")
        result = pda.process_input(input_str)
        
        if pda.state == "start": # If input is only in a start state
            result = "Enter a character"
        elif pda.state == pda.state == "dead" or pda.state == "consonant" or pda.state == "digraph": # If last input is not in a final state
            result = "Input not available in Baybayin"
            
        elif pda.state == "final_consonant": # If last input is a final consonant
            result = result[:-1]
        elif pda.state == "final_digraph": # If last input is a final digraph
            result = result[:-2]
        
        print("Baybayin output:", result)
