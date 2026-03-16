class ReflectionAgent:

    def reflect(self, reasoning):

        prompt = f"""
Review the reasoning below.

Identify mistakes and improve the final prediction.

{reasoning}
"""

        return prompt