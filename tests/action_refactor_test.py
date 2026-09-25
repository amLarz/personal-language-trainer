class ActionRefactorTest:
    def clean_inputs(self): # TODO: filters null values and returns a dictionary of the remaining key-value pairs
        return {k: v for k, v in vars(self).items() if v is not None}
    
