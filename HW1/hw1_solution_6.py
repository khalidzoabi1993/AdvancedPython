# -*- coding: utf-8 -*-
import json
import re


# ==========================================================
#  Helpers – עם באגים לוגיים בכוונה
# ==========================================================

def is_valid_email(email):
    """
    BUG:
    - בודק אימייל עם Regex קשוח מדי:
      דורש בדיוק אותיות/מספרים לפני ואחרי @
      ודורש בדיוק .com / .net / .org (שוכח .co, .io)
    - לא חופף למה שהבודק האוטומטי מצפה.
    """
    if not isinstance(email, str):
        return False
    email = email.strip()
    pattern = re.compile(r'^[A-Za-z0-9._]+@[A-Za-z0-9]+\.(com|net|org)$')
    return pattern.match(email) is not None


def is_valid_name(name):
    """
    BUG:
    - רק בודק שהשם לא ריק ושהאות הראשונה גדולה.
    - לא בודק שאין מספרים/תווים מיוחדים.
    - לא בודק מינימום 3 תווים.
    """
    if not isinstance(name, str):
        return False
    name = name.strip()
    if not name:
        return False
    return name[0].isupper()


# ==========================================================
# שאלה 1 – קריאת קובץ JSON
# ==========================================================
def q1_read_json(student_id):
    """
    Q1: Read JSON file data_<student_id>.json
    """
    filename = "data_%s.json" % student_id
    try:
        f = open(filename, "r", encoding="utf-8")
        data = json.load(f)
        f.close()
        # BUG קטן: לא מוודא שהשורש באמת list
        return data
    except Exception as e:
        print("Error reading file:", e)
        return []


# ==========================================================
# שאלה 2 – כתיבת קובץ פלט JSON
# ==========================================================
def q2_write_output(output_data, filename):
    """
    Q2: Write processed JSON file.
    """
    try:
        # BUG קטן: אין ensure_ascii=False (עברית תצא ב- \u05xx )
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)
    except Exception as e:
        print("Error writing output:", e)


# ==========================================================
# שאלה 3 – בדיקת תקינות כתובות אימייל
# ==========================================================
def q3_check_emails(users):
    """
    BUG לוגי:
    - משתמש ב-is_valid_email הבעייתי.
    - לא מסיר כפילויות, לא ממיין (זה לא קריטי לבודק, אבל פחות יפה).
    """
    valid_emails = []
    invalid_emails = []

    for u in users:
        email = u.get("email", "")
        if is_valid_email(email):
            valid_emails.append(email)
        else:
            invalid_emails.append(email)

    return valid_emails, invalid_emails


# ==========================================================
# שאלה 4 – בדיקת תקינות שמות משתמשים
# ==========================================================
def q4_check_names(users):
    """
    BUG:
    - משתמש ב-is_valid_name הרופף, יכניס הרבה שמות "מלוכלכים" כתקינים.
    """
    valid_names = []
    invalid_names = []

    for u in users:
        name = u.get("name", "")
        if is_valid_name(name):
            valid_names.append(name)
        else:
            invalid_names.append(name)

    # בלי הסרת כפילויות / מיון – פחות נקי
    return valid_names, invalid_names


# ==========================================================
# שאלה 5 – סטטיסטיקות כלליות
# ==========================================================
def q5_general_stats(users):
    """
    BUGים:
    - averageAge מחושב כ-int(...) (חותך את השבר, לא תואם round(,2))
    - usersWithoutPurchasesCount בודק רק purchases is None,
      מתעלם מ-[].
    """
    result = {
        "usersCount": 0,
        "averageAge": 0.0,
        "oldestUser": None,
        "youngestUser": None,
        "usersWithoutPurchasesCount": 0
    }

    if not users:
        return result

    result["usersCount"] = len(users)

    ages = []
    for u in users:
        age = u.get("age")
        if isinstance(age, (int, float)):
            ages.append(age)

    if ages:
        # BUG: שימוש ב-int במקום round ל-2 ספרות
        avg = int(sum(ages) / len(ages))
        result["averageAge"] = avg

        max_age = max(ages)
        min_age = min(ages)

        oldest = None
        youngest = None
        for u in users:
            a = u.get("age")
            if a == max_age and oldest is None:
                oldest = {
                    "id": u.get("id"),
                    "name": u.get("name"),
                    "age": a
                }
            if a == min_age and youngest is None:
                youngest = {
                    "id": u.get("id"),
                    "name": u.get("name"),
                    "age": a
                }

        result["oldestUser"] = oldest
        result["youngestUser"] = youngest

    count_no_purchases = 0
    for u in users:
        purchases = u.get("purchases", [])
        # BUG: אם purchases == [] זה לא נספר!
        if purchases is None:
            count_no_purchases += 1

    result["usersWithoutPurchasesCount"] = count_no_purchases
    return result


# ==========================================================
# שאלה 6 – ניתוח רכישות
# ==========================================================
def q6_purchases_analysis(users):
    """
    BUGים:
    - moreThanThreePurchasesCount משתמש ב- >= 3 במקום > 3.
    - top3Spenders נבחרים לפי הסכום הכי קטן (סדר עולה),
      במקום הסכום הכי גבוה.
    """
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

    total_events = 0
    total_money = 0.0
    highest = {
        "userId": None,
        "name": None,
        "amount": 0.0
    }
    per_user_totals = []
    more_than_three = 0

    for u in users:
        purchases = u.get("purchases", [])
        if not isinstance(purchases, list):
            purchases = []

        num_p = len(purchases)
        total_events += num_p

        user_sum = 0.0
        for p in purchases:
            try:
                amount = float(p)
            except Exception:
                continue
            user_sum += amount
            total_money += amount
            if amount > highest["amount"]:
                highest["amount"] = amount
                highest["userId"] = u.get("id")
                highest["name"] = u.get("name")

        if user_sum > 0:
            per_user_totals.append((user_sum, u))

        # BUG: צריך להיות > 3 ולא >= 3
        if num_p >= 3:
            more_than_three += 1

    # BUG: ממיין בסדר עולה – בוחר את *הכי בזבזנים* הפוכים
    per_user_totals.sort(key=lambda t: t[0])
    top3 = []
    for total, u in per_user_totals[:3]:
        top3.append({
            "id": u.get("id"),
            "name": u.get("name"),
            "total": round(total, 2)
        })

    result["purchaseStats"]["totalPurchaseEvents"] = total_events
    result["purchaseStats"]["totalMoneySpent"] = round(total_money, 2)
    result["purchaseStats"]["highestSinglePurchase"] = highest
    result["purchaseStats"]["top3Spenders"] = top3
    result["moreThanThreePurchasesCount"] = more_than_three

    return result


# ==========================================================
# שאלה 7 – פילוח גילאים
# ==========================================================
def q7_age_groups(users):
    """
    BUG:
    - גבולות גילאים לא תואמים את ההגדרה המדויקת:
      Young: age < 25 (במקום <= 25)
      Adult: 25–40 (כולל 25 במקום מ-26)
    """
    groups = {
        "Young": [],
        "Adult": [],
        "Senior": [],
        "Elder": []
    }

    for u in users:
        age = u.get("age")
        if not isinstance(age, (int, float)):
            continue

        info = {
            "id": u.get("id"),
            "name": u.get("name"),
            "age": age
        }

        # BUGים בגבולות:
        if age < 25:                      # צריך להיות age <= 25
            groups["Young"].append(info)
        elif 25 <= age <= 40:             # צריך להיות 26–40
            groups["Adult"].append(info)
        elif 41 <= age <= 60:
            groups["Senior"].append(info)
        else:
            groups["Elder"].append(info)

    return groups


# ==========================================================
# שאלה 8 – רשימת משתמשים ללא רכישות
# ==========================================================
def q8_users_without_purchases(users):
    """
    BUG:
    - בודק רק purchases is None, מי שיש לו [] לא נחשב ללא רכישות.
    """
    res = []

    for u in users:
        purchases = u.get("purchases", [])
        if purchases is None:
            res.append({
                "id": u.get("id"),
                "name": u.get("name")
            })

    return res


# ==========================================================
# MAIN – בניית קובץ הפלט סופי
# ==========================================================
def main():
    print("=== HW1 – JSON Analysis (Bad Solution Example) ===")
    student_id = input(
        "Enter your student ID (or student_id1_student_id2 if in pair): "
    ).strip()

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

    q2_write_output(output_data, "output_analysis.json")
    print("Saved to output_analysis.json (BAD example)")


if __name__ == "__main__":
    main()
