from google import genai
from PIL import Image
from config import GEMINI_MODEL, GOOGLE_API_KEY


class PerceptionAgent:

    def __init__(self):
        if not GOOGLE_API_KEY:
            raise ValueError(
                "Missing Gemini API key. Set GEMINI_API_KEY or GOOGLE_API_KEY."
            )

        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.model_name = GEMINI_MODEL

    def analyze(self, image_path):

        image = Image.open(image_path)

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[
                "Analyze this GeoGuessr image. Extract location clues like language, road signs, vegetation, architecture, etc.",
                image
            ]
        )

        return response.text








# from google import genai
# from config import GOOGLE_API_KEY


# class PerceptionAgent:

#     def __init__(self):

#         self.client = genai.Client(api_key=GOOGLE_API_KEY)

#     def analyze(self, image_path):

#         response = self.client.models.generate_content(
#             model="gemini-2.0-flash",
#             contents=[
#                 "Analyze this GeoGuessr image. Extract clues like language, road markings, vegetation, architecture, and driving side.",
#                 genai.types.Part.from_file(image_path)
#             ]
#         )

#         return response.text
