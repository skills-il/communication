# Sending an interactive list message

Interactive messages are non-template messages, so they can only be sent inside an open customer service window. From 1 October 2026 they count as billable service messages after the monthly free tier.

```python
import requests

def send_interactive_list(phone_number_id: str, access_token: str,
                          to: str, body_text: str, sections: list):
    """Send an interactive list message in Hebrew."""
    url = f"https://graph.facebook.com/v26.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {"text": body_text},
            "action": {"button": "בחר אפשרות", "sections": sections},
        },
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
```
