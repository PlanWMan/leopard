class Class1:
    def m(self):
        print("In Class1")


class Class2(Class1):
    def m(self):
        print("In Class2")


class Class3(Class1):
    def m(self):
        print("In Class3")


class Class4(Class2, Class3):
    def __init__(self):
        super(Class2, self).m()
        # super(Class2, self).m()
        # super(Class3, self).m()


obj = Class4()