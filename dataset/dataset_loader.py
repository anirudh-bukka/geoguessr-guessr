"""
This file converts the dataset into a list of samples, 
where each sample is a dictionary containing the path to the image and the corresponding country label. 
The output format is as follows:
[
 {path: ".../france/img1.jpg", country:"france"},
 {path: ".../india/img22.jpg", country:"india"}
]
"""

import os
from config import DATASET_PATH


def load_dataset():

    samples = []

    for country in os.listdir(DATASET_PATH):

        country_path = os.path.join(DATASET_PATH, country)

        if not os.path.isdir(country_path):
            continue

        for img in os.listdir(country_path):

            if img.endswith(".jpg"):

                samples.append({
                    "path": os.path.join(country_path, img),
                    "country": country
                })

    return samples