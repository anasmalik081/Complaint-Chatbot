import uuid

def generate_complaint_id():
    return str(uuid.uuid4())[:8].upper()
