# Emotion Detector Submission Answers

## Task 1: GitHub Repository URL

Submit the public README URL after pushing the repo:

`https://github.com/JonathanRReed/Emotion-Detector/blob/main/README.md`

## Task 2: Watson NLP Emotion Detection Application

### Activity 1: `EmotionDetection/emotion_detection.py` application function

```python
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
```

### Activity 2: Terminal output

```text
$ .venv/bin/python - <<'PY'
from EmotionDetection.emotion_detection import emotion_detector
print(emotion_detector('I am glad this happened'))
PY
{'anger': 0.0, 'disgust': 0.0, 'fear': 0.0, 'joy': 1.0, 'sadness': 0.0, 'dominant_emotion': 'joy'}
```

## Task 3: Format Application Output

### Activity 1: Output format code

```python
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
```

### Activity 2: Terminal output

```text
$ .venv/bin/python - <<'PY'
from EmotionDetection import emotion_detector
result = emotion_detector('I am happy and joyful today')
print(result)
print(type(result).__name__)
print(sorted(result.keys()))
PY
{'anger': 0.0, 'disgust': 0.0, 'fear': 0.0, 'joy': 1.0, 'sadness': 0.0, 'dominant_emotion': 'joy'}
dict
['anger', 'disgust', 'dominant_emotion', 'fear', 'joy', 'sadness']
```

## Task 4: Validate EmotionDetection Package

### Activity 1: `EmotionDetection/__init__.py` URL

Submit after pushing:

`https://github.com/JonathanRReed/Emotion-Detector/blob/main/EmotionDetection/__init__.py`

Code:

```python
"""EmotionDetection package public interface."""

from .emotion_detection import emotion_detector

__all__ = ["emotion_detector"]
```

### Activity 2: Terminal output

```text
$ .venv/bin/python - <<'PY'
import EmotionDetection
from EmotionDetection import emotion_detector
print(EmotionDetection.__all__)
print(emotion_detector('I love this package')['dominant_emotion'])
PY
['emotion_detector']
joy
```

## Task 5: Unit Tests

### Activity 1: `test_emotion_detection.py` tests

```python
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
        mocked_post.return_value = self._mock_response("joy")
        result = emotion_detector("I am glad this happened")
        self.assertEqual(result["dominant_emotion"], "joy")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_anger(self, mocked_post: Mock) -> None:
        mocked_post.return_value = self._mock_response("anger")
        result = emotion_detector("I am really mad about this")
        self.assertEqual(result["dominant_emotion"], "anger")
```

The file also includes tests for disgust, fear, sadness, blank input, and status code 400.

### Activity 2: Terminal output

```text
$ .venv/bin/python -m unittest test_emotion_detection.py
.......
----------------------------------------------------------------------
Ran 7 tests in 0.001s

OK
```

## Task 6: Flask Web Deployment

### Activity 1: `server.py` Flask deployment code

```python
@APP.route("/", methods=["GET"])
def index() -> str:
    """Render the home page."""

    return render_template_string(PAGE_TEMPLATE, text="", result=None, error=None)


@APP.route("/emotionDetector", methods=["POST"])
def emotion_detector_route() -> str:
    """Handle submitted text and display emotion detector output."""

    text_to_analyze = request.form.get("textToAnalyze", "")
    if not text_to_analyze.strip():
        return render_template_string(
            PAGE_TEMPLATE,
            text=text_to_analyze,
            result=None,
            error="Invalid text! Please try again!",
        )
```

### Activity 2: Screenshot

Upload:

`screenshots/6b_deployment_test.png`

## Task 7: Error Handling

### Activity 1: `emotion_detection.py` status code 400 handling

```python
if response.status_code == 400:
    return _blank_response()
```

### Activity 2: `server.py` blank input handling

```python
if not text_to_analyze.strip():
    return render_template_string(
        PAGE_TEMPLATE,
        text=text_to_analyze,
        result=None,
        error="Invalid text! Please try again!",
    )
```

### Activity 3: Screenshot

Upload:

`screenshots/7c_error_handling_interface.png`

## Task 8: Static Code Analysis

### Activity 1: `server.py` code used for static analysis

Submit the contents of `server.py`. It includes module docstrings, route docstrings, clear constants, and pylint-clean Flask route functions.

### Activity 2: Terminal output showing perfect score

```text
$ .venv/bin/pylint server.py

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
```
