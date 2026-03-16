from agents.perception_agent import PerceptionAgent


class GeoGuessrPipeline:

    def __init__(self):
        self.perception = PerceptionAgent()

    def run(self, image_path):

        clues = self.perception.analyze(image_path)

        return {
            "clues": clues
        }