"""Flask web server for the Emotion Detector application."""

from __future__ import annotations

from flask import Flask, render_template_string, request

from EmotionDetection import emotion_detector


APP = Flask(__name__)

PAGE_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Emotion Detector</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2rem; max-width: 760px; }
        textarea { width: 100%; min-height: 120px; padding: 0.75rem; }
        button { margin-top: 1rem; padding: 0.7rem 1rem; }
        .result { margin-top: 1.5rem; padding: 1rem; border: 1px solid #cccccc; }
        .error { color: #9b1c1c; font-weight: 700; }
    </style>
</head>
<body>
    <h1>Emotion Detector</h1>
    <form method="post" action="/emotionDetector">
        <label for="textToAnalyze">Text to analyze</label>
        <textarea id="textToAnalyze" name="textToAnalyze">{{ text }}</textarea>
        <button type="submit">Run emotion detection</button>
    </form>
    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}
    {% if result %}
        <div class="result">{{ result }}</div>
    {% endif %}
</body>
</html>
"""


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

    response = emotion_detector(text_to_analyze)
    dominant_emotion = response.get("dominant_emotion")
    if dominant_emotion is None:
        return render_template_string(
            PAGE_TEMPLATE,
            text=text_to_analyze,
            result=None,
            error="Invalid text! Please try again!",
        )

    output = (
        f"For the given statement, the system response is 'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, 'fear': {response['fear']}, "
        f"'joy': {response['joy']} and 'sadness': {response['sadness']}. "
        f"The dominant emotion is {dominant_emotion}."
    )
    return render_template_string(
        PAGE_TEMPLATE,
        text=text_to_analyze,
        result=output,
        error=None,
    )


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=5000, debug=True)
