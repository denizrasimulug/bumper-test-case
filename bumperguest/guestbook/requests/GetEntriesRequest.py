class GetEntriesRequest:
    def __init__(self, page_number, max_page):
        self.errors = []
        try:
            self.page = int(page_number)
        except TypeError:
            self.errors.append("Invalid page number, should be an integer.")

        self.validate(max_page)

    def validate(self, max_page):
        if self.page < 1 or self.page > max_page:
            self.errors.append("Invalid page number, must be between 1 and {max_page}")

    def is_valid(self):
        return not self.errors
