import requests
from dotenv import load_dotenv
import os
from datetime import datetime
load_dotenv()

APP_ID = os.getenv("NUTRITIONX_APP_ID")
APP_KEY = os.getenv("NUTRITIONX_APP_KEY")
SHEETS_AUTH = os.getenv("SHEETS_AUTH")

user = input("What exercise did you do today?: ")

HEADERS = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
}

nutritionx_params = {
    "query": user,
    "gender":"female",
    "weight_kg":72.5,
    "height_cm":167.64,
    "age":30
}

response = requests.post(url="https://trackapi.nutritionix.com/v2/natural/exercise", json=nutritionx_params, headers=HEADERS)
result = response.json()

date_now = datetime.now().strftime("%d/%m/%Y")
time_now = datetime.now().time().strftime("%H:%M:%S")

sheets_header = {
    "Authorization": SHEETS_AUTH,
}

for exercise in result["exercises"]:
    sheets_json = {
        "workout": {
            "date": date_now,
            "time": time_now,
            "exercise": exercise['name'],
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories'],
        }
    }
    sheets_response = requests.post(url="https://api.sheety.co/81312712f1055f1b9d9d988ada86af9b/myWorkoutsPython/workouts", json=sheets_json, headers=sheets_header)