class ActionRefactorTest:
    def __init__(self, name=None, age=None, email=None):
        self.name = name
        self.age = age
        self.email = email

    def clean_inputs(
        self,
    ):  # TODO: filters null values and returns a dictionary of the remaining key-value pairs
        values = {k: v for k, v in vars(self).items() if v is not None}

        header_table = {
            "name": "users",
            "age": "users",
            "email": "users",
        }

        for key in values:
            if key in header_table:
                print(f"{header_table[key]} SET {key} = ? WHERE {key} = ?")

        return values


#ActionRefactorTest(name="Alice", age=30).clean_inputs()


words_table_cols = {
    "id": "INTEGER PRIMARY KEY",
    "hanzi": "TEXT",
    "pinyin": "TEXT",
    "word": "TEXT NOT NULL UNIQUE",
    "lemma": "TEXT NOT NULL",
    "frequency_score": "INTEGER DEFAULT 0",
    "specificity_score": "INTEGER DEFAULT 0",
    "total_count": "INTEGER DEFAULT 0",
}
col_headers = ", ".join(f"{col} {config}" for col, config in words_table_cols.items())

print(col_headers)