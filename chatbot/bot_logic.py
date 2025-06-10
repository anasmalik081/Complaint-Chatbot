import re
import requests

REQUIRED_FIELDS = ["name", "phone_number", "email", "complaint_details"]

class ChatSession:
    def __init__(self, api_base_url="http://localhost:8000"):
        self.state = {}
        self.api_base_url = api_base_url
        self.collecting_complaint = False

    def reset(self):
        self.state = {}
        self.collecting_complaint = False

    def is_filing_complaint(self, user_input: str):
        return any(word in user_input.lower() for word in ["file a complaint", "want to complain", "register complaint", "raise an issue", "delayed delivery", "problem", "issue"])

    def is_querying_complaint(self, user_input: str):
        return bool(re.search(r"\bcomplaint\s*(id)?\s*[:\-]?\s*(\w+)", user_input.lower()))

    def extract_complaint_id(self, user_input: str):
        match = re.search(r"\bcomplaint\s*(id)?\s*[:\-]?\s*(\w+)", user_input.lower())
        return match.group(2).upper() if match else None

    def collect_field(self, user_input: str):
        for field in REQUIRED_FIELDS:
            if field not in self.state:
                self.state[field] = user_input.strip()
                break

    def get_missing_field_prompt(self):
        for field in REQUIRED_FIELDS:
            if field not in self.state:
                return {
                    "name": "Please provide your name.",
                    "phone_number": "What is your phone number?",
                    "email": "Can you share your email address?",
                    "complaint_details": "Please describe your complaint in detail."
                }[field]
        return None

    def is_complete(self):
        return all(field in self.state for field in REQUIRED_FIELDS)

    def submit_complaint(self):
        response = requests.post(
            f"{self.api_base_url}/complaints",
            json=self.state
        )
        if response.status_code == 200:
            complaint_id = response.json().get("complaint_id")
            self.reset()
            return f"Your complaint has been registered with ID: {complaint_id}. You'll hear back soon."
        return "There was an error while submitting your complaint."

    def fetch_complaint(self, complaint_id):
        response = requests.get(f"{self.api_base_url}/complaints/{complaint_id}")
        if response.status_code == 200:
            c = response.json()
            return (
                f"Complaint ID: {c['complaint_id']}\n"
                f"Name: {c['name']}\n"
                f"Phone: {c['phone_number']}\n"
                f"Email: {c['email']}\n"
                f"Details: {c['complaint_details']}\n"
                f"Created At: {c['created_at']}"
            )
        return "Sorry, no complaint found with that ID."

    def handle_input(self, user_input, rag_chain=None):
        # CASE 1: Already in complaint flow
        if self.collecting_complaint:
            self.collect_field(user_input)
            if self.is_complete():
                return self.submit_complaint()
            else:
                return self.get_missing_field_prompt()

        # CASE 2: Starting complaint flow
        if self.is_filing_complaint(user_input):
            self.collecting_complaint = True
            return "I'm sorry to hear that. Please provide your name."

        # CASE 3: Fetch complaint details
        if self.is_querying_complaint(user_input):
            complaint_id = self.extract_complaint_id(user_input)
            return self.fetch_complaint(complaint_id)

        # CASE 4: General fallback to knowledge base
        if rag_chain:
            return rag_chain.invoke({"query": user_input})["result"]

        return "I'm not sure how to help with that."
