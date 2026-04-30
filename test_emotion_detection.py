"""Unit tests for the EmotionDetection package."""

from unittest import TestCase, main
from unittest.mock import Mock, patch

from EmotionDetection import emotion_detector


class TestEmotionDetector(TestCase):
    """Validate dominant emotion detection and invalid input handling."""

    def _mock_response(self, dominant_emotion: str) -> Mock:
        response = Mock()
        response.status_code = 200
        scores = {
            "anger": 0.0,
            "disgust": 0.0,
            "fear": 0.0,
            "joy": 0.0,
            "sadness": 0.0,
        }
        scores[dominant_emotion] = 0.9
        response.json.return_value = {"emotionPredictions": [{"emotion": scores}]}
        return response

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_joy(self, mocked_post: Mock) -> None:
        """Confirm joy is selected for a joyful statement."""

        mocked_post.return_value = self._mock_response("joy")
        result = emotion_detector("I am glad this happened")
        self.assertEqual(result["dominant_emotion"], "joy")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_anger(self, mocked_post: Mock) -> None:
        """Confirm anger is selected for an angry statement."""

        mocked_post.return_value = self._mock_response("anger")
        result = emotion_detector("I am really mad about this")
        self.assertEqual(result["dominant_emotion"], "anger")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_disgust(self, mocked_post: Mock) -> None:
        """Confirm disgust is selected for a disgusted statement."""

        mocked_post.return_value = self._mock_response("disgust")
        result = emotion_detector("That was disgusting")
        self.assertEqual(result["dominant_emotion"], "disgust")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_fear(self, mocked_post: Mock) -> None:
        """Confirm fear is selected for a fearful statement."""

        mocked_post.return_value = self._mock_response("fear")
        result = emotion_detector("I am afraid of what comes next")
        self.assertEqual(result["dominant_emotion"], "fear")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_sadness(self, mocked_post: Mock) -> None:
        """Confirm sadness is selected for a sad statement."""

        mocked_post.return_value = self._mock_response("sadness")
        result = emotion_detector("I feel sad today")
        self.assertEqual(result["dominant_emotion"], "sadness")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_blank_response(self, mocked_post: Mock) -> None:
        """Confirm blank input returns the required None response."""

        result = emotion_detector("")
        mocked_post.assert_not_called()
        self.assertEqual(
            result,
            {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None,
            },
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_status_code_400(self, mocked_post: Mock) -> None:
        """Confirm Watson NLP status code 400 returns the required None response."""

        response = Mock()
        response.status_code = 400
        mocked_post.return_value = response
        result = emotion_detector("invalid")
        self.assertIsNone(result["dominant_emotion"])


if __name__ == "__main__":
    main()
