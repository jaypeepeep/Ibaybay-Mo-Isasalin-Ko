def execute_main_code(center_canvas_symbol, top_canvas_symbol, bottom_canvas_symbol):
    # Define allowed syllabic and vowel symbols
    syllabic = ["BA", "CA", "DA", "FA", "GA", "HA", "JA", "KA", "LA", "MA", "NA", "NGA", "PA", "QA", "RA", "SA", "TA", "VA", "WA", "XA", "YA", "ZA"]
    vowel = ["A", "O or U", "E or I"]

    # Initialize the Pushdown Automaton
    automata = BaybayinRecognizer(syllabic, vowel)
    # Process input for center canvas
    automata.process_input("centerCanvas", center_canvas_symbol)
    # Process input for top canvas
    automata.process_input("topCanvas", top_canvas_symbol)
    # Process input for bottom canvas
    automata.process_input("bottomCanvas", bottom_canvas_symbol)
    result = automata.get_result()
    state = automata.get_state()

    return result, state

# Define a custom exception class for invalid input configurations
class InvalidInputConfiguration:
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"Error: {self.message}"

# Define a class for the Pushdown Automaton
class BaybayinRecognizer:
    def __init__(self, syllabic, vowel):
        # Initialize the stack and the allowed syllabic and vowel symbols
        self.stack = []
        self.syllabic = syllabic
        self.vowel = vowel
        self.state = "centerCanvas"  # Initialize the state to the center canvas
        self.result = ""

    # Process input based on canvas ID and symbol
    def process_input(self, canvas_id, symbol):
        # Delegate processing based on the canvas ID
        if canvas_id == "centerCanvas":
            self.process_center_canvas(symbol)
        elif canvas_id == "topCanvas":
            self.process_top_canvas(symbol)
        elif canvas_id == "bottomCanvas":
            self.process_bottom_canvas(symbol)

    # Process symbols when in the center canvas state
    def process_center_canvas(self, symbol):
        if symbol == "∈":
            self.result = "No Input"
            #self.state = "End State"
            return
        elif symbol in self.syllabic:
            # Handle each syllabic character separately
            for char in symbol:
                self.stack.append(char)
                self.state = "topCanvas"
        elif symbol in self.vowel:
            # Check if both top and bottom canvases have empty values (ε)
            print("symboltest" + symbol)
            if self.stack == [""] and self.state == "topCanvas":
                self.stack.append(symbol)
                self.result = "".join(self.stack)
                self.stack.pop()
                return
            elif self.stack == [""] and self.state == "bottomCanvas":
                self.stack.append(symbol)
                self.result = "".join(self.stack)
                self.stack.pop()
                return
            elif not self.stack:
                # If center canvas is a vowel and both top and bottom are ε, output the center canvas
                self.stack.append(symbol)
                self.result = "".join(self.stack)
                self.stack.pop()
                return
            
    # Process symbols when in the top canvas state
    def process_top_canvas(self, symbol):
        if len(self.stack) == 0:
            if symbol == "i" or symbol == "e":
                self.result = "Invalid input"
                return
        if symbol == "i" and self.stack and self.stack[-1] == "A":
            # Pop the last character and append "i"
            self.stack.pop()
            self.stack.append("I")
            self.result = "".join(self.stack)
            self.state = "bottomCanvas"
        elif symbol == "e" and self.stack and self.stack[-1] == "A":
            # Pop the last character and append "E"
            self.stack.pop()
            self.stack.append("E")
            self.result = "".join(self.stack)
            self.state = "bottomCanvas"
        elif symbol == "∈":
            self.state = "bottomCanvas"

    # Process symbols when in the bottom canvas state
    def process_bottom_canvas(self, symbol):
        if len(self.stack) == 0:
            if symbol == "o" or symbol == "u":
                self.result = "Invalid input"
                return
        elif self.stack[-1] == "E" or self.stack[-1] == "I":
            if symbol == "o" or symbol == "u":
                self.result = "Invalid input configuration"
                self.stack.pop()
                #self.state = "End State"
                self.stack.pop()
                return self.result
        elif symbol == "o" and self.stack and self.stack[-1] == "A":
            # Pop the last character and append "i"
            self.stack.pop()
            self.stack.append("O")
            self.result = "".join(self.stack)
            self.stack.pop()
            #self.state = "End State"
            return
        elif symbol == "u" and self.stack and self.stack[-1] == "A":
            # Pop the last character and append "E"
            self.stack.pop()
            self.stack.append("U")
            self.result = "".join(self.stack)
            self.stack.pop()
            #self.state = "End State"
            self.stack.pop()
            return
        elif symbol == "∈":
            self.result = "".join(self.stack)
            self.stack.pop()
            #self.state = "End State"
            self.stack.pop()

    # Get the result based on the current state
    def get_result(self):
        return self.result
    
    def get_state(self):
        return self.state


# Example usage
if __name__ == "__main__":
    # Define allowed syllabic and vowel symbols
    syllabic = ["BA", "CA", "DA", "FA", "GA", "HA", "JA", "KA", "LA", "MA", "NA", "NGA", "PA", "QA", "RA", "SA", "TA", "VA", "WA", "XA", "YA", "ZA"]
    vowel = ["A", "E", "I", "O", "U"]

    # Initialize the Pushdown Automaton
    automata = BaybayinRecognizer(syllabic, vowel)

    # Example 1∈
    automata.process_input("centerCanvas", "KA")
    automata.process_input("topCanvas", "e")
    automata.process_input("bottomCanvas", "∈")
    result = automata.get_result()
    print(f"Output: {result}")