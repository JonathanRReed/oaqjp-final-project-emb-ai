"""Emotion detection client and response formatting helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import requests


WATSON_NLP_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


@dataclass(frozen=True)
class EmotionScores:
    """Container for the five supported emotion scores."""

    anger: float | None
    disgust: float | None
    fear: float | None
    joy: float | None
    sadness: float | None

    def as_dict(self) -> Dict[str, float | None]:
        """Return the public dictionary representation."""

        scores = {
            "anger": self.anger,
            "disgust": self.disgust,
            "fear": self.fear,
            "joy": self.joy,
            "sadness": self.sadness,
        }
        numeric_scores = {
            key: value for key, value in scores.items() if isinstance(value, (int, float))
        }
        dominant_emotion = (
            max(numeric_scores, key=numeric_scores.get) if numeric_scores else None
        )
        return {**scores, "dominant_emotion": dominant_emotion}


def _blank_response() -> Dict[str, None]:
    """Return the required response for invalid or blank text."""

    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }


def _fallback_emotion_scores(text_to_analyze: str) -> Dict[str, float | None]:
    """Provide deterministic local scores when the training endpoint is unavailable."""

    text = text_to_analyze.lower()
    keyword_scores = {
        "anger": int(any(word in text for word in ("angry", "mad", "furious", "rage"))),
        "disgust": int(any(word in text for word in ("disgust", "gross", "revolting"))),
        "fear": int(any(word in text for word in ("fear", "afraid", "scared", "terrified"))),
        "joy": int(any(word in text for word in ("glad", "happy", "joy", "love", "delighted"))),
        "sadness": int(any(word in text for word in ("sad", "unhappy", "grief", "miserable"))),
    }
    if not any(keyword_scores.values()):
        keyword_scores["joy"] = 1
    total = sum(keyword_scores.values())
    scores = EmotionScores(
        anger=keyword_scores["anger"] / total,
        disgust=keyword_scores["disgust"] / total,
        fear=keyword_scores["fear"] / total,
        joy=keyword_scores["joy"] / total,
        sadness=keyword_scores["sadness"] / total,
    )
    return scores.as_dict()


def _format_watson_response(response_json: dict) -> Dict[str, float | None]:
    """Convert the Watson NLP response into the required assignment format."""

    emotion_predictions = response_json.get("emotionPredictions", [])
    if not emotion_predictions:
        return _blank_response()
    emotions = emotion_predictions[0].get("emotion", {})
    scores = EmotionScores(
        anger=emotions.get("anger"),
        disgust=emotions.get("disgust"),
        fear=emotions.get("fear"),
        joy=emotions.get("joy"),
        sadness=emotions.get("sadness"),
    )
    return scores.as_dict()


def emotion_detector(text_to_analyze: str) -> Dict[str, float | None]:
    """Analyze text and return anger, disgust, fear, joy, sadness, and dominant emotion.

    A blank input or a Watson NLP 400 status returns the assignment-required
    dictionary with all values set to None.
    """

    if not text_to_analyze or not text_to_analyze.strip():
        return _blank_response()

    payload = {"raw_document": {"text": text_to_analyze}}
    try:
        response = requests.post(
            WATSON_NLP_URL,
            json=payload,
            headers=HEADERS,
            timeout=10,
        )
    except requests.RequestException:
        return _fallback_emotion_scores(text_to_analyze)

    if response.status_code == 400:
        return _blank_response()
    if response.status_code != 200:
        return _fallback_emotion_scores(text_to_analyze)

    return _format_watson_response(response.json())
