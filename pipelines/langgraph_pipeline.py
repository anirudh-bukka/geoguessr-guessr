from langgraph.graph import StateGraph
from agents.perception_agent import PerceptionAgent
from agents.reasoning_agent import ReasoningAgent
from agents.reflection_agent import ReflectionAgent
from embeddings.clip_encoder import ClipEncoder
from retrieval.vector_store import VectorStore


class GeoGuessrPipeline:

    def __init__(self):

        self.perception = PerceptionAgent()
        self.reasoning = ReasoningAgent()
        self.reflection = ReflectionAgent()

        self.encoder = ClipEncoder()

        self.store = VectorStore()
        self.store.load()

    def run(self, image_path):

        emb = self.encoder.encode(image_path)

        retrieved = self.store.search(emb)

        clues = self.perception.analyze(image_path)

        reasoning = self.reasoning.infer_location(clues, retrieved)

        final = self.reflection.reflect(reasoning)

        return final