# -*- coding: utf-8 -*-
import json


# ==========================================================
# שאלה 1 – קריאת קובץ JSON
# ==========================================================
def q1_read_json(student_id):
    """
    Q1: Read JSON file.
    """
    filename = "data_%s.json" % student_id

    users = []

    # TODO: open/read JSON file
    return users


# ==========================================================
# שאלה 2 – כתיבת קובץ פלט JSON
# ==========================================================
def q2_write_output(output_data, filename):
    """
    Q2: Write processed JSON file.
    """
    # TODO: open/write JSON file
    pass


# ==========================================================
# שאלה 3 – בדיקת תקינות כתובות אימייל
# ==========================================================
def q3_check_emails(users):
    valid_emails = []
    invalid_emails = []

    # TODO
    return valid_emails, invalid_emails


# ==========================================================
# שאלה 4 – בדיקת תקינות שמות משתמשים
# ==========================================================
def q4_check_names(users):
    valid_names = []
    invalid_names = []

    # TODO
    return valid_names, invalid_names


# ==========================================================
# שאלה 5 – סטטיסטיקות כלליות
# ==========================================================
def q5_general_stats(users):
    result = {
        "usersCount": 0,
        "averageAge": 0.0,
        "oldestUser": None,
        "youngestUser": None,
        "usersWithoutPurchasesCount": 0
    }

    # TODO
    return result


# ==========================================================
# שאלה 6 – ניתוח רכישות
# ==========================================================
def q6_purchases_analysis(users):
    result = {
        "purchaseStats": {
            "totalPurchaseEvents": 0,
            "totalMoneySpent": 0.0,
            "highestSinglePurchase": {
                "userId": None,
                "name": None,
                "amount": 0.0
            },
            "top3Spenders": []
        },
        "moreThanThreePurchasesCount": 0
    }

    # TODO
    return result


# ==========================================================
# שאלה 7 – פילוח גילאים
# ==========================================================
def q7_age_groups(users):
    groups = {
        "Young": [],
        "Adult": [],
        "Senior": [],
        "Elder": []
    }

    # TODO
    return groups


# ==========================================================
# שאלה 8 – רשימת משתמשים ללא רכישות
# ==========================================================
def q8_users_without_purchases(users):
    res = []

    # TODO
    return res


# ==========================================================
# MAIN – בניית קובץ הפלט סופי
# ==========================================================
def main():
    print("=== HW1 – JSON Analysis (Python Template) ===")
    student_id = input("Enter your student ID (same used in generate_dataset): ").strip()

    if not student_id:
        print("Error: student ID cannot be empty.")
        return

    # Q1
    users = q1_read_json(student_id)
    if not users:
        print("Error: no users loaded.")
        return

    # Q3
    emails_valid, emails_invalid = q3_check_emails(users)

    # Q4
    names_valid, names_invalid = q4_check_names(users)

    # Q5
    general_stats = q5_general_stats(users)

    # Q6
    purchases_info = q6_purchases_analysis(users)

    # Q7
    age_groups = q7_age_groups(users)

    # Q8
    users_no_purchases = q8_users_without_purchases(users)

    # Build final JSON structure
    output_data = {
        "emails": {
            "valid": emails_valid,
            "invalid": emails_invalid
        },
        "names": {
            "valid": names_valid,
            "invalid": names_invalid
        },
        "usersCount": general_stats.get("usersCount", 0),
        "moreThanThreePurchasesCount": purchases_info.get("moreThanThreePurchasesCount", 0),
        "basicStats": {
            "averageAge": general_stats.get("averageAge", 0.0),
            "oldestUser": general_stats.get("oldestUser"),
            "youngestUser": general_stats.get("youngestUser"),
            "usersWithoutPurchasesCount": general_stats.get("usersWithoutPurchasesCount", 0)
        },
        "purchaseStats": purchases_info.get("purchaseStats", {}),
        "ageGroups": age_groups,
        "usersWithoutPurchases": users_no_purchases
    }

    # Q2
    q2_write_output(output_data, "output_analysis.json")
    print("Saved to output_analysis.json")


if __name__ == "__main__":
    main()
