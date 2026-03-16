from google import genai
from config import GOOGLE_API_KEY


class PerceptionAgent:

    def __init__(self):

        self.client = genai.Client(api_key=GOOGLE_API_KEY)

    def analyze(self, image_path):

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                "Analyze this GeoGuessr image. Extract clues like language, road markings, vegetation, architecture, and driving side.",
                genai.types.Part.from_file(image_path)
            ]
        )

        return response.text