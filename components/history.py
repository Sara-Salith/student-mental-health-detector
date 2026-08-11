import pandas as pd
import os
from datetime import datetime


HISTORY_FILE = "assessment_history.csv"


def load_history():

    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE)

    return pd.DataFrame(columns=[
        "username",
        "timestamp",
        "prediction",
        "risk_score",
        "Gender",
        "Age",
        "Academic Pressure",
        "Work Pressure",
        "CGPA",
        "Study Satisfaction",
        "Job Satisfaction",
        "Sleep Duration",
        "Dietary Habits",
        "Suicidal Thoughts",
        "Work/Study Hours",
        "Financial Stress",
        "Family History"
    ])


def save_assessment(username, prediction, risk_score, student_data):

    history = load_history()

    new_record = {
        "username": username,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prediction": prediction,
        "risk_score": risk_score
    }

    # Add student's assessment responses
    new_record.update(student_data)

    new_record_df = pd.DataFrame([new_record])

    history = pd.concat(
        [history, new_record_df],
        ignore_index=True
    )

    history.to_csv(
        HISTORY_FILE,
        index=False
    )


def get_user_history(username):

    history = load_history()

    if history.empty:
        return history

    return history[
        history["username"] == username
    ].copy()