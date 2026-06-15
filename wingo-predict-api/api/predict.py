from http.server import BaseHTTPRequestHandler
import json
import requests

def calculate_prediction(period):
    period = str(period)

    short_period = int(period[-5:])

    result = (short_period * 2 + 5 * short_period + 5) % 10

    prediction = "SMALL" if result <= 4 else "BIG"

    return prediction, result


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

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

            result = {
                "period": period,
                "prediction": prediction,
                "predictedNumber": predicted_number,
                "actual": actual,
                "actualNumber": actual_number,
                "status": status,
                "icon": icon
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(result).encode())

        except Exception as e:

            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())
