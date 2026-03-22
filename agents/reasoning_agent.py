import anthropic
from config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL


class ReasoningAgent:

    def __init__(self):
        if not ANTHROPIC_API_KEY:
            raise ValueError("Missing Anthropic API key. Set ANTHROPIC_API_KEY.")

        self.client = anthropic.Anthropic(
            api_key=ANTHROPIC_API_KEY
        )
        self.model_name = ANTHROPIC_MODEL

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

        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
        except anthropic.NotFoundError as exc:
            available_models = ", ".join(
                model.id for model in self.client.models.list(limit=20).data
            )
            raise ValueError(
                f"Anthropic model '{self.model_name}' is not available for this account. "
                f"Available models: {available_models}"
            ) from exc

        return response.content[0].text
