from flask import Flask, jsonify
import requests

app = Flask(__name__)

def calculate_prediction(period):
    period = str(period)

    try:
        short_period = int(period[-5:])
        result = (short_period * 2 + 5 * short_period + 5) % 10

        prediction = "SMALL" if result <= 4 else "BIG"

        return prediction, result

    except:
        return "ERROR", 0


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Prediction API Running"
    })


@app.route("/api/predict")
def predict():

    try:
        url = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

        response = requests.get(url, timeout=10)
        data = response.json()

        latest = data["data"]["list"][0]

        period = latest["issueNumber"]
        actual_number = int(latest["number"])

        actual = "SMALL" if actual_number <= 4 else "BIG"

        prediction, predicted_number = calculate_prediction(period)

        status = "WIN" if prediction == actual else "LOSS"

        icon = "✅" if status == "WIN" else "❌"

        return jsonify({
            "period": period,
            "prediction": prediction,
            "predictedNumber": predicted_number,
            "actual": actual,
            "actualNumber": actual_number,
            "status": status,
            "icon": icon
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# Required by Vercel
app = app
