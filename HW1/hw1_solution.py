# -*- coding: utf-8 -*-
import json


# ==========================================================
# עזר: בדיקת תקינות אימייל ושם – תואם לאוטוגריידר
# ==========================================================

def is_valid_email(email):
    """
    אימייל תקין אם:
    - הוא מחרוזת
    - מכיל '@'
    - מסתיים באחת הסיומות: .com, .net, .org, .co, .io
    """
    if not isinstance(email, str):
        return False
    e = email.strip().lower()
    if "@" not in e:
        return False
    endings = (".com", ".net", ".org", ".co", ".io")
    return e.endswith(endings)


def is_valid_name(name):
    """
    שם תקין אם:
    - מחרוזת
    - לפחות 3 תווים
    - האות הראשונה גדולה באנגלית
    - כל התווים אותיות בלבד
    """
    if not isinstance(name, str):
        return False
    name = name.strip()
    if len(name) < 3:
        return False
    if not name[0].isupper():
        return False
    if not name.isalpha():
        return False
    return True


# ==========================================================
# שאלה 1 – קריאת קובץ JSON
# ==========================================================
def q1_read_json(student_id):
    """
    Q1: Read JSON file data_<student_id>.json and return list of users.
    """
    filename = "data_%s.json" % student_id
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            print("Error: JSON root is not a list.")
            return []
        return data
    except FileNotFoundError:
        print("Error: file '%s' not found." % filename)
    except json.JSONDecodeError as e:
        print("Error: JSON decode error: %s" % e)
    except Exception as e:
        print("Unexpected error while reading JSON: %s" % e)
    return []


# ==========================================================
# שאלה 2 – כתיבת קובץ פלט JSON
# ==========================================================
def q2_write_output(output_data, filename):
    """
    Q2: Write processed JSON file to output_analysis.json.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)
        print("Output saved to '%s'" % filename)
    except Exception as e:
        print("Error while writing JSON: %s" % e)


# ==========================================================
# שאלה 3 – בדיקת תקינות כתובות אימייל
# ==========================================================
def q3_check_emails(users):
    """
    מחזירה שתי רשימות:
    - valid_emails: כל כתובות האימייל התקינות (ללא כפילויות, ממוינות)
    - invalid_emails: כל כתובות האימייל הלא תקינות (ללא כפילויות, ממוינות)
    """
    valid_emails = []
    invalid_emails = []

    for u in users:
        email = u.get("email", "")
        if is_valid_email(email):
            valid_emails.append(email)
        else:
            invalid_emails.append(email)

    # הסרת כפילויות + מיון (תואם לבודק)
    valid_emails = sorted(set(valid_emails))
    invalid_emails = sorted(set(invalid_emails))

    return valid_emails, invalid_emails


# ==========================================================
# שאלה 4 – בדיקת תקינות שמות משתמשים
# ==========================================================
def q4_check_names(users):
    """
    מחזירה שתי רשימות:
    - valid_names: שמות תקינים
    - invalid_names: שמות לא תקינים
    לפי הכללים:
      * מתחיל באות גדולה באנגלית
      * ללא מספרים או תווים מיוחדים
      * לפחות 3 תווים
    """
    valid_names = []
    invalid_names = []

    for u in users:
        name = u.get("name", "")
        if is_valid_name(name):
            valid_names.append(name)
        else:
            invalid_names.append(name)

    valid_names = sorted(set(valid_names))
    invalid_names = sorted(set(invalid_names))

    return valid_names, invalid_names


# ==========================================================
# שאלה 5 – סטטיסטיקות כלליות
# ==========================================================
def q5_general_stats(users):
    """
    מחזירה מילון:
    {
        "usersCount": מספר משתמשים,
        "averageAge": ממוצע גיל (2 ספרות אחרי הנקודה),
        "oldestUser": {id,name,age} או None,
        "youngestUser": {id,name,age} או None,
        "usersWithoutPurchasesCount": מספר משתמשים בלי רכישות
    }
    """
    result = {
        "usersCount": 0,
        "averageAge": 0.0,
        "oldestUser": None,
        "youngestUser": None,
        "usersWithoutPurchasesCount": 0
    }

    if not isinstance(users, list) or not users:
        return result

    # מספר משתמשים
    result["usersCount"] = len(users)

    # רשימת גילאים תקינים
    ages = []
    for u in users:
        age = u.get("age")
        if isinstance(age, (int, float)):
            ages.append(age)

    if ages:
        avg = sum(ages) / float(len(ages))
        result["averageAge"] = round(avg, 2)

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

    # ספירת משתמשים ללא רכישות
    count_no_purchases = 0
    for u in users:
        purchases = u.get("purchases", [])
        if not purchases:  # ריק / None / []
            count_no_purchases += 1
    result["usersWithoutPurchasesCount"] = count_no_purchases

    return result


# ==========================================================
# שאלה 6 – ניתוח רכישות
# ==========================================================
def q6_purchases_analysis(users):
    """
    מחזירה:
    {
        "purchaseStats": {
            "totalPurchaseEvents": ...,
            "totalMoneySpent": ...,
            "highestSinglePurchase": {userId,name,amount},
            "top3Spenders": [ {id,name,total}, ... ]
        },
        "moreThanThreePurchasesCount": ...
    }
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

        if num_p > 3:
            more_than_three += 1

    per_user_totals.sort(key=lambda t: t[0], reverse=True)
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
    פילוח גילאים:
    Young  : age <= 25
    Adult  : 26–40
    Senior : 41–60
    Elder  : 61+
    מחזיר:
    {
       "Young":  [ {id,name,age}, ... ],
       "Adult":  [...],
       "Senior": [...],
       "Elder":  [...]
    }
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

        if age <= 25:
            groups["Young"].append(info)
        elif 26 <= age <= 40:
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
    מחזירה רשימה:
    [
      {"id": ..., "name": "..."},
      ...
    ]
    של כל המשתמשים ללא רכישות.
    """
    res = []

    for u in users:
        purchases = u.get("purchases", [])
        if not purchases:
            res.append({
                "id": u.get("id"),
                "name": u.get("name")
            })

    return res


# ==========================================================
# MAIN – בניית קובץ הפלט סופי
# ==========================================================
def main():
    print("=== HW1 – JSON Analysis (Python Template) ===")
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

    # Q2
    q2_write_output(output_data, "output_analysis.json")
    print("Saved to output_analysis.json")


if __name__ == "__main__":
    main()
