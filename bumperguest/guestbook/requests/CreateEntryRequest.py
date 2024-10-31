class CreateEntryRequest:
    def __init__(self, data):
        self.name = data.get("name")
        self.subject = data.get("subject")
        self.message = data.get("message")
        self.errors = []

        self.validate()

    def validate(self):
        if not self.name:
            self.errors.append("Name is required.")
        if not self.subject:
            self.errors.append("Subject is required.")
        if not self.message:
            self.errors.append("Message is required.")

    def is_valid(self):
        return not self.errors