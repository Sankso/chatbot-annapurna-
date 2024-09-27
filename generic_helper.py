import re

def extract_session_id(session_str: str):
    """
    Extract the session ID from the context name in Dialogflow output contexts.
    Example context: "projects/your-project-id/agent/sessions/session_id/contexts/context_name"
    """
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        return match.group(1)
    return ""

def get_str_from_food_dict(food_dict: dict):
    """
    Convert a dictionary of food items and quantities into a readable string.
    Example: {'pizza': 2, 'samosa': 3} -> '2 pizzas, 3 samosas'
    """
    return ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])

# Test helper functions
if __name__ == "__main__":
    print(get_str_from_food_dict({"samosa": 2, "chhole bhature": 5}))
    print(extract_session_id("projects/annapurna-chatbot-jyap/agent/sessions/f3c835c0-cae0-02e1-4353-07a3b1a43ac2/contexts/ongoing-order"))
