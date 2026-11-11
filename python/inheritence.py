class student:
    def __init__(self, name, roll=0):
        self.name = name
        self.roll = roll
    
    def print_details(self):
        print(self.name)
    

class coursedetails:
    def __init__(self, name, roll, course, code):
        self.course = course
        self.code = code
        student.__init__(self, name, roll)

    def print_details(self):
        print(f"{self.name}, {self.roll}, {self.course}, {self.code}")

    
a = student("Rahu")
a.print_details()
student("Raghu").print_details()
b = coursedetails(a, "com", "read")
b.print_details()
