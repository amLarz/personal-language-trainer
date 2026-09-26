class ActionRefactorTest:
    
    def __init__(self, name=None, age=None, email=None):
        self.name = name
        self.age = age
        self.email = email
    
    def clean_inputs(self): # TODO: filters null values and returns a dictionary of the remaining key-value pairs
        values = {k: v for k, v in vars(self).items() if v is not None}
        
        if 
        print(values)
        print(values["age"])
        return values

ActionRefactorTest(name="Alice", age=30).clean_inputs()

    
KS