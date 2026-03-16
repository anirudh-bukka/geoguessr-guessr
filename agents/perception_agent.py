from google import genai
from PIL import Image
from config import GEMINI_API_KEY


class PerceptionAgent:

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def analyze(self, image_path):

        image = Image.open(image_path)

        prompt = """
        You are a professional GeoGuessr player.

        Analyze this street view image and extract:

        - road type
        - road markings
        - visible language
        - vegetation
        - architecture
        - driving side
        - road sign colors
        - climate

        Return bullet points.
        """

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt, image]
        )

        return response.text










# import os
# from PIL import Image
# from dotenv import load_dotenv
# from google import genai

# load_dotenv()


# class PerceptionAgent:

#     def __init__(self):
#         self.client = genai.Client(
#             api_key=os.getenv("GEMINI_API_KEY")
#         )

#     def analyze(self, image_path):

#         image = Image.open(image_path)

#         prompt = """
#         You are a GeoGuessr expert.

#         Analyze this street view image and extract:

#         - road type
#         - road markings
#         - visible language on signs
#         - vegetation
#         - architecture style
#         - driving side
#         - road sign colors
#         - climate type

#         Return structured bullet points.
#         """

#         response = self.client.models.generate_content(
#             model="gemini-2.0-flash",
#             contents=[prompt, image]
#         )

#         return response.text