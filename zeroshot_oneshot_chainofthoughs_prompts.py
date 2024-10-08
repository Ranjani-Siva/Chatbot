# -*- coding: utf-8 -*-
"""prompts data from hugging.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1P1-Hvb3GqH9GrhI3EXW_KZBZiSKKkSua
"""

!huggingface-cli login

import pandas as pd


df = pd.read_csv("hf://datasets/fka/awesome-chatgpt-prompts/prompts.csv")

df.head()

df.shape

#Zero shot prompts
from transformers import pipeline

# Initialize the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define the text dataset
texts = df.values.tolist()

# Define candidate labels
candidate_labels = ["positive", "negative", "neutral"]

# Classify each text in the dataset
for text in texts:
    result = classifier(text, candidate_labels)
    label = result['labels'][0]
    score = result['scores'][0]
    print(f"Text: '{text}'")
    print(f"Predicted Label: {label} (Score: {score:.2f})\n")

# One shot Prompts
from transformers import pipeline

# Initialize the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define the text dataset
texts = df.values.tolist()

# Define candidate labels
candidate_labels = ["positive", "negative", "neutral"]

# Provide a one-shot example
one_shot_example = {
    "text": "The weather was great and the scenery was beautiful during our hike.",
    "label": "positive"
}

# Classify each text in the dataset using the one-shot example as context
for text in texts:
    # Combine the one-shot example with the target text
    combined_text = f"Example: {one_shot_example['text']} (Label: {one_shot_example['label']})\n\nTarget Text: {text}"

    # Perform classification
    result = classifier(combined_text, candidate_labels)
    label = result['labels'][0]
    score = result['scores'][0]

    print(f"Text: '{text}'")
    print(f"Predicted Label: {label} (Score: {score:.2f})\n")

#Chain of throughts prompts
from transformers import pipeline

# Initialize the text generation pipeline with a model suitable for CoT reasoning
generator = pipeline("text-generation", model="openai-community/gpt2")

# Define the text dataset
texts = df.values.tolist()

# Chain of thought prompt for reasoning
cot_prompt_template = (
    "Text: {text}\n"
)
# Generate reasoning for each text in the dataset
for text in texts:
    # Create a chain of thought prompt using the template
    cot_prompt = cot_prompt_template.format(text=text)

    # Generate the response using the text-generation model
    result = generator(cot_prompt, max_length=200, num_return_sequences=1)

    # Extract the generated text
    generated_text = result[0]['generated_text']

    print(f"Original Text: {text}\n")
    print(f"Chain of Thought Reasoning:\n{generated_text}\n")
    print("-" * 80 + "\n")