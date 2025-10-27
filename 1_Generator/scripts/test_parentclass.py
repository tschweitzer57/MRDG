class Display():
    def __init__(self):
        self.message = "This is the Display class"
        print(self.message)

    def affiche(self, value):
        print(f"Value: {value}")

class childDisplay(Display):
    def __init__(self):
        super().__init__()
        self.child_message = "This is the Child Display class"
        print(self.child_message)

    # def affiche(self, value):
    #     print(f"Value is: {value}")

if __name__ == "__main__":
    disp = childDisplay()