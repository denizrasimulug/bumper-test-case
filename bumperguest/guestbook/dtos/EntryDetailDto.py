

class EntryDetailDTO:
    def __init__(self, entry):
        self.id = entry.id
        self.subject = entry.subject
        self.message = entry.message
        self.guest_name = entry.guest.name
        self.created_date = entry.created_date
    
    def to_dict(self):
        return {
            "id": self.id,
            "subject": self.subject,
            "message": self.message,
            "guest": self.guest_name,
            "created_date": self.created_date
        }