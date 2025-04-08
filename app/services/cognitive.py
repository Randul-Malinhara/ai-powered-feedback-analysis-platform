import logging
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from config.config import config

logger = logging.getLogger(__name__)
_client = TextAnalyticsClient(endpoint=config.AZURE_ENDPOINT, credential=AzureKeyCredential(config.AZURE_KEY))

def analyze_feedback(text: str) -> dict:
    """
    Analyze sentiment and extract key phrases using Azure Cognitive Services.
    """
    try:
        sentiment_response = _client.analyze_sentiment([text])[0]
        key_phrase_response = _client.extract_key_phrases([text])[0]
        return {
            "sentiment": sentiment_response.sentiment,
            "confidence_scores": sentiment_response.confidence_scores._asdict(),
            "key_phrases": key_phrase_response.key_phrases
        }
    except Exception as e:
        logger.error(f"Error during cognitive analysis: {e}")
        raise
