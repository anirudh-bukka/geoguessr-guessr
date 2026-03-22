import os

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

from pipelines.langgraph_pipeline import GeoGuessrPipeline


def main():

    pipeline = GeoGuessrPipeline()

    image = "/Users/anirbukk/Documents/utilities/personal-github-repos/geoguessr-guessr/image9.png"
    # image = "dataset/geoguessr/India/canvas_1629934825.jpg"

    result = pipeline.run(image)

    print(result)


if __name__ == "__main__":
    main()









# from agents.perception_agent import PerceptionAgent
# from agents.reasoning_agent import ReasoningAgent


# def main():

#     image_path = "images/test_image.jpg"

#     perception = PerceptionAgent()
#     reasoning = ReasoningAgent()

#     print("\n🔎 Analyzing image...\n")

#     clues = perception.analyze(image_path)

#     print("CLUES:")
#     print(clues)

#     print("\n🧠 Reasoning...\n")

#     guess = reasoning.guess_location(clues)

#     print("FINAL GUESS:")
#     print(guess)


# if __name__ == "__main__":
#     main()








# # from pipelines.geoguessr_pipeline import GeoGuessrPipeline


# # def main():

# #     image_path = "images/test_image.jpg"

# #     pipeline = GeoGuessrPipeline()

# #     result = pipeline.run(image_path)

# #     print("\n--- CLUES ---\n")
# #     print(result["clues"])


# # if __name__ == "__main__":
# #     main()
