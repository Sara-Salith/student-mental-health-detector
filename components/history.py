import pandas as pd

from components.auth import get_supabase


# ----------------------------------------
# SAVE ASSESSMENT
# ----------------------------------------

def save_assessment(
    username,
    prediction,
    risk_score,
    student_data
):

    supabase = get_supabase()

    try:

        new_record = {
            "username": username,
            "prediction": prediction,
            "risk_score": float(risk_score),

            "gender": student_data.get("Gender"),

            "age": student_data.get("Age"),
            "academic_pressure": student_data.get("Academic Pressure"),
            "work_pressure": student_data.get("Work Pressure"),

            "cgpa": student_data.get("CGPA"),

            "study_satisfaction": student_data.get("Study Satisfaction"),
            "job_satisfaction": student_data.get("Job Satisfaction"),

            "sleep_duration": student_data.get("Sleep Duration"),
            "dietary_habits": student_data.get("Dietary Habits"),
            "suicidal_thoughts": student_data.get("Suicidal Thoughts"),

            "work_study_hours": student_data.get("Work/Study Hours"),

            "financial_stress": student_data.get("Financial Stress"),
            "family_history": student_data.get("Family History")
        }

        # DEBUG: Show exactly what is being sent
        print("\nASSESSMENT DATA BEING SENT:")
        for key, value in new_record.items():
            print(f"{key}: {value} | type: {type(value)}")

        supabase.table(
            "assessment_history"
        ).insert(
            new_record
        ).execute()

        return True

    except Exception as e:

        print("Error saving assessment:", e)

        return False


# ----------------------------------------
# GET USER HISTORY
# ----------------------------------------

def get_user_history(username):

    supabase = get_supabase()

    try:

        response = (
            supabase
            .table("assessment_history")
            .select("*")
            .eq("username", username)
            .order("timestamp", desc=True)
            .execute()
        )

        return pd.DataFrame(response.data)

    except Exception as e:

        print("Error loading history:", e)

        return pd.DataFrame()