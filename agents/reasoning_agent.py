import anthropic
from config import ANTHROPIC_API_KEY


class ReasoningAgent:

    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=ANTHROPIC_API_KEY
        )

    def guess_location(self, clues):

        prompt = f"""
        You are a GeoGuessr expert.

        Based on these clues extracted from a street view image:

        {clues}

        Deduce the most likely country.

        Explain reasoning briefly.
        """

        message = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

        return message.content[0].text