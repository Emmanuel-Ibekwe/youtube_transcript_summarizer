import re
import spacy
import pandas as pd

input_file = "../data/youtube_links_with_transcripts.csv"
output_file = "../data/youtube_links_with_cleaned_transcripts.csv"

# Cleaning of text
def basic_clean_transcript(text):
    # Remove speaker tags 'Speaker 1':', 'John:', etc.
    text = re.sub(r'(Speaker \d+:|[A-Z][a-z]+:)', '', text)
    
    # Remove common disfluencies/fillers (case-insensitive)
    fillers = r"\b(uh|um|you know|like|i mean|you see|sort of|kind of|you guys|okay|right|actually|basically|literally)\b"
    text = re.sub(fillers, "", text, flags=re.IGNORECASE)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.rstrip()

def remove_repetitions(text):
    # Remove repeated short phrases like: "so so", "I I", "we we"
    text = re.sub(r'\b(\w+)( \1\b)+', r'\1', text)
    return text

nlp = spacy.load('en_core_web_sm')

def advanced_clean(text):
    doc = nlp(text)
    cleaned_sentences = []
    for sent in doc.sents:
        tokens = [token.text for token in sent if token.pos_ not in ["INTJ"]]
        cleaned_sentences.append(" ".join(tokens))
    return " ".join(cleaned_sentences)

def clean_transcript_with_index(row):
    index = row.name
    transcript = row['transcript']
    text = basic_clean_transcript(transcript)
    text = remove_repetitions(text)
    text = advanced_clean(text)
    print(f"Transcript {index} cleaned.")
    return text

df = pd.read_csv(input_file)
df["transcript"] = df.apply(clean_transcript_with_index, axis=1)
df.to_csv(output_file, index=False)