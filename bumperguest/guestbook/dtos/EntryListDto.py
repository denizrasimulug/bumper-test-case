

class EntryListDTO:
    def __init__(self, entry):
        self.subject = entry.subject
        self.message = entry.message
        self.user = entry.guest.name
    
    def to_dict(self):
        return {
            "id": self.id,
            "subject": self.subject,
            "message": self.message,
            "guest": self.guest_name,
            "created_date": self.created_date
        }