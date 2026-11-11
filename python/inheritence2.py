class student:
    def __init__(self, name):
        self.name = name
    
    def disp_name(self):
        print(self.name)

class course(student):
    def __init__(self, name, course, couname):
        super().__init__(name)
        self.course = course
        self.couname = couname

    def print_name(self):
        print(self.name)

a = course("Raghu", "THis", "hi")
a.print_name()
