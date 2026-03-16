import anthropic
from config import ANTHROPIC_API_KEY


class ReasoningAgent:

    def __init__(self):

        self.client = anthropic.Anthropic(
            api_key=ANTHROPIC_API_KEY
        )

    def infer_location(self, clues, retrieved):

        prompt = f"""
You are a GeoGuessr expert.

Clues:
{clues}

Similar locations from database:
{retrieved}

Infer the most likely country.
Explain reasoning.
"""

        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text