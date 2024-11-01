

class EntryDetailDTO:
    def __init__(self, entry):
        self.id = entry.id
        self.subject = entry.subject
        self.message = entry.message
        self.guest_name = entry.guest.name
        self.created_at = entry.created_at
    
    def to_dict(self):
        return {
            "id": self.id,
            "subject": self.subject,
            "message": self.message,
            "guest_name": self.guest_name,
            "created_at": self.created_at
        }