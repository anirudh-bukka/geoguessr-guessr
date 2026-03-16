from pipelines.langgraph_pipeline import GeoGuessrPipeline
from dataset.dataset_loader import load_dataset


pipeline = GeoGuessrPipeline()

samples = load_dataset()[:100]

correct = 0

for s in samples:

    pred = pipeline.run(s["path"])

    if s["country"].lower() in pred.lower():
        correct += 1

print("Accuracy:", correct / len(samples))