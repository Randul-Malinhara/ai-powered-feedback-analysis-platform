from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from config import AZURE_ENDPOINT, AZURE_KEY

def analyze_feedback(text: str) -> dict:
    """
    Analyze sentiment and key phrases using Azure Cognitive Services.
    """
    client = TextAnalyticsClient(endpoint=AZURE_ENDPOINT, credential=AzureKeyCredential(AZURE_KEY))
    sentiment_response = client.analyze_sentiment([text])[0]
    key_phrase_response = client.extract_key_phrases([text])[0]

    return {
        "sentiment": sentiment_response.sentiment,
        "confidence_scores": sentiment_response.confidence_scores._asdict(),  # converting NamedTuple to dict
        "key_phrases": key_phrase_response.key_phrases
    }
