from transformers import pipeline
from typing import List

# load once when app starts (cache in memory)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# example category labels - replace/add as needed
DEFAULT_CATEGORIES = [
    "Billing",
    "Service outage",
    "Harassment",
    "Facility maintenance",
    "Policy dispute",
    "Refund",
    "Other"
]

def predict_category(text: str, candidate_labels: List[str] = None):
    labels = candidate_labels or DEFAULT_CATEGORIES
    res = classifier(text, labels)
    # choose highest scoring label
    label = res["labels"][0]
    score = res["scores"][0]
    return label, float(score)
