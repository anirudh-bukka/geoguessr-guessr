import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from config import CLIP_MODEL


class ClipEncoder:

    def __init__(self):

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = CLIPModel.from_pretrained(CLIP_MODEL).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(CLIP_MODEL)

    def encode(self, image_path):

        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(images=image, return_tensors="pt").to(self.device)

        with torch.no_grad():
            features = self.model.get_image_features(**inputs)

        return features.cpu().numpy()[0]