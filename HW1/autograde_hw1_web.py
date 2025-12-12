# -*- coding: utf-8 -*-
import json
import math
import os

# ==========================================================
#  Helper functions
# ==========================================================

def load_json_file(path):
    """
    Load JSON file safely. Returns (data, error_message_or_None)
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data, None
    except FileNotFoundError:
        return None, "File not found"
    except json.JSONDecodeError as e:
        return None, "JSON decode error: %s" % e
    except Exception as e:
        return None, "Error: %s" % e


def almost_equal(a, b, eps=1e-2):
    """
    Compare two numeric values with tolerance.
    """
    try:
        af = float(a)
        bf = float(b)
        return math.isclose(af, bf, abs_tol=eps)
    except Exception:
        return False


def compare_lists_as_sets(expected_list, student_list):
    """
    Simple set equality on stringified elements.
    """
    return set(map(str, expected_list)) == set(map(str, student_list))


def diff_lists_as_sets(expected_list, student_list):
    """
    Return (ok, missing, extra) for two lists (by stringified values).
    """
    exp_set = set(map(str, expected_list))
    stu_set = set(map(str, student_list))
    missing = sorted(exp_set - stu_set)
    extra = sorted(stu_set - exp_set)
    ok = (len(missing) == 0 and len(extra) == 0)
    return ok, missing, extra


# ==========================================================
#  Reference solution logic (MUST match HW instructions)
# ==========================================================

def is_valid_email(email):
    """
    לפי ההנחיות בעבודה:
    - יש '@'
    - מסתיים באחת הסיומות: .com, .net, .org, .co, .io
    (פשוט, בלי Regex מתוחכם)
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
    לפי ההנחיות:
    - מתחיל באות גדולה באנגלית
    - אינו מכיל מספרים
    - אינו מכיל תווים מיוחדים
    - אורך לפחות 3 תווים
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


def ref_emails(users):
    valid = []
    invalid = []
    for u in users:
        email = u.get("email", "")
        if is_valid_email(email):
            valid.append(email)
        else:
            invalid.append(email)
    valid = sorted(set(valid))
    invalid = sorted(set(invalid))
    return valid, invalid


def ref_names(users):
    valid = []
    invalid = []
    for u in users:
        name = u.get("name", "")
        if is_valid_name(name):
            valid.append(name)
        else:
            invalid.append(name)
    valid = sorted(set(valid))
    invalid = sorted(set(invalid))
    return valid, invalid


def ref_general_stats(users):
    """
    מחזיר:
    {
        "usersCount": ...,
        "averageAge": ...,
        "oldestUser": {...} or None,
        "youngestUser": {...} or None,
        "usersWithoutPurchasesCount": ...
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

    result["usersCount"] = len(users)

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

    # בלי רכישות
    count_no_purchases = 0
    for u in users:
        purchases = u.get("purchases", [])
        if not purchases:
            count_no_purchases += 1
    result["usersWithoutPurchasesCount"] = count_no_purchases

    return result


def ref_purchases_analysis(users):
    """
    מחזיר:
    {
        "purchaseStats": {...},
        "moreThanThreePurchasesCount": ...
    }
    """
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

        total_events += len(purchases)

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

        if len(purchases) > 3:
            more_than_three += 1

    per_user_totals.sort(key=lambda t: t[0], reverse=True)
    top3 = []
    for total, u in per_user_totals[:3]:
        top3.append({
            "id": u.get("id"),
            "name": u.get("name"),
            "total": round(total, 2)
        })

    purchase_stats = {
        "totalPurchaseEvents": total_events,
        "totalMoneySpent": round(total_money, 2),
        "highestSinglePurchase": highest,
        "top3Spenders": top3
    }

    return {
        "purchaseStats": purchase_stats,
        "moreThanThreePurchasesCount": more_than_three
    }


def ref_age_groups(users):
    """
    פילוח:
    Young  : age <= 25
    Adult  : 26–40
    Senior : 41–60
    Elder  : 61+
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


def ref_users_without_purchases(users):
    res = []
    for u in users:
        purchases = u.get("purchases", [])
        if not purchases:
            res.append({
                "id": u.get("id"),
                "name": u.get("name")
            })
    return res


def build_expected_output(users):
    emails_valid, emails_invalid = ref_emails(users)
    names_valid, names_invalid = ref_names(users)
    gen = ref_general_stats(users)
    purch = ref_purchases_analysis(users)
    age_groups = ref_age_groups(users)
    no_pur = ref_users_without_purchases(users)

    expected = {
        "emails": {
            "valid": emails_valid,
            "invalid": emails_invalid
        },
        "names": {
            "valid": names_valid,
            "invalid": names_invalid
        },
        "usersCount": gen["usersCount"],
        "moreThanThreePurchasesCount": purch["moreThanThreePurchasesCount"],
        "basicStats": {
            "averageAge": gen["averageAge"],
            "oldestUser": gen["oldestUser"],
            "youngestUser": gen["youngestUser"],
            "usersWithoutPurchasesCount": gen["usersWithoutPurchasesCount"]
        },
        "purchaseStats": purch["purchaseStats"],
        "ageGroups": age_groups,
        "usersWithoutPurchases": no_pur
    }
    return expected


# ==========================================================
#  Structure checking
# ==========================================================

def check_structure(expected, student):
    """
    בודק את מבנה ה-output_analysis.json:
    האם יש את כל המפתחות והמבנים הנדרשים.
    לא בודק ערכים, רק מבנה.
    מחזיר (ok, list_of_errors)
    """
    errors = []

    # top-level required keys
    required_top = [
        "emails", "names", "usersCount", "moreThanThreePurchasesCount",
        "basicStats", "purchaseStats", "ageGroups", "usersWithoutPurchases"
    ]
    for key in required_top:
        if key not in student:
            errors.append("Missing top-level key: %s" % key)

    # emails
    if "emails" in student:
        e = student["emails"]
        if not isinstance(e, dict):
            errors.append("emails should be an object")
        else:
            for subkey in ["valid", "invalid"]:
                if subkey not in e:
                    errors.append("Missing key: emails.%s" % subkey)

    # names
    if "names" in student:
        n = student["names"]
        if not isinstance(n, dict):
            errors.append("names should be an object")
        else:
            for subkey in ["valid", "invalid"]:
                if subkey not in n:
                    errors.append("Missing key: names.%s" % subkey)

    # basicStats
    if "basicStats" in student:
        b = student["basicStats"]
        if not isinstance(b, dict):
            errors.append("basicStats should be an object")
        else:
            for subkey in ["averageAge", "oldestUser", "youngestUser", "usersWithoutPurchasesCount"]:
                if subkey not in b:
                    errors.append("Missing key: basicStats.%s" % subkey)

    # purchaseStats
    if "purchaseStats" in student:
        p = student["purchaseStats"]
        if not isinstance(p, dict):
            errors.append("purchaseStats should be an object")
        else:
            for subkey in ["totalPurchaseEvents", "totalMoneySpent", "highestSinglePurchase", "top3Spenders"]:
                if subkey not in p:
                    errors.append("Missing key: purchaseStats.%s" % subkey)

            if "highestSinglePurchase" in p and not isinstance(p["highestSinglePurchase"], dict):
                errors.append("purchaseStats.highestSinglePurchase should be an object")

            if "top3Spenders" in p and not isinstance(p["top3Spenders"], list):
                errors.append("purchaseStats.top3Spenders should be a list")

    # ageGroups
    if "ageGroups" in student:
        ag = student["ageGroups"]
        if not isinstance(ag, dict):
            errors.append("ageGroups should be an object")
        else:
            for grp in ["Young", "Adult", "Senior", "Elder"]:
                if grp not in ag:
                    errors.append("Missing key: ageGroups.%s" % grp)

    # usersWithoutPurchases
    if "usersWithoutPurchases" in student and not isinstance(student["usersWithoutPurchases"], list):
        errors.append("usersWithoutPurchases should be a list")

    ok = len(errors) == 0
    return ok, errors


# ==========================================================
#  Main grading function – with detailed feedback
# ==========================================================

def grade_student(student_id, folder_path):
    """
    folder_path – תיקיה שבה נמצאים:
      data_<student_id>.json
      output_analysis.json
    """

    # weights per question (Total = 100)
    weights = {
        "Q1": 5,   # load JSON
        "Q2": 10,  # output structure
        "Q3": 15,  # emails
        "Q4": 10,  # names
        "Q5": 20,  # general stats
        "Q6": 20,  # purchases
        "Q7": 10,  # age groups
        "Q8": 10   # users without purchases
    }

    scores = {k: 0.0 for k in weights}
    remarks = []        # summary line per Q
    details = []        # detailed feedback per Q

    data_filename = "data_%s.json" % student_id
    data_path = os.path.join(folder_path, data_filename)
    out_path = os.path.join(folder_path, "output_analysis.json")

    # ---------- Q1: load JSON ----------
    users, err1 = load_json_file(data_path)
    if err1 is not None:
        remarks.append("Q1 – JSON loading: 0/%d (error: %s)" % (weights["Q1"], err1))
        print("Error loading data file:", err1)
        total_score = 0.0
        print("=" * 60)
        print("Student ID:", student_id)
        print("Folder   :", folder_path)
        print("-" * 60)
        for r in remarks:
            print(r)
        print("-" * 60)
        print("TOTAL: %.1f/100" % total_score)
        print("=" * 60)
        return
    if not isinstance(users, list):
        remarks.append("Q1 – JSON loading: 0/%d (root is not a list)" % weights["Q1"])
        total_score = 0.0
        print("=" * 60)
        print("Student ID:", student_id)
        print("Folder   :", folder_path)
        print("-" * 60)
        for r in remarks:
            print(r)
        print("-" * 60)
        print("TOTAL: %.1f/100" % total_score)
        print("=" * 60)
        return

    scores["Q1"] = float(weights["Q1"])
    remarks.append("Q1 – JSON loading: %.1f/%d" % (scores["Q1"], weights["Q1"]))
    details.append("Q1 details: ✅ JSON file '%s' loaded successfully, root is a list with %d users."
                   % (data_filename, len(users)))

    # Build expected reference
    expected = build_expected_output(users)

    # Load student's output
    student_output, err2 = load_json_file(out_path)
    if err2 is not None:
        remarks.append("Q2–Q8: cannot grade because output_analysis.json has error: %s" % err2)
        total_score = scores["Q1"]
        print("=" * 60)
        print("Student ID:", student_id)
        print("Folder   :", folder_path)
        print("-" * 60)
        for r in remarks:
            print(r)
        print("-" * 60)
        for d in details:
            print(d)
        print("-" * 60)
        print("TOTAL: %.1f/100" % total_score)
        print("=" * 60)
        return

    # ---------- Q2: structure ----------
    ok_struct, struct_errors = check_structure(expected, student_output)
    if ok_struct:
        scores["Q2"] = float(weights["Q2"])
        remarks.append("Q2 – output structure: %.1f/%d" % (scores["Q2"], weights["Q2"]))
        details.append("Q2 details: ✅ All required top-level keys and nested keys exist in output_analysis.json.")
    else:
        scores["Q2"] = 0.0
        remarks.append("Q2 – output structure: 0/%d" % (weights["Q2"]))
        details.append("Q2 details: ❌ Structure problems in output_analysis.json:")
        for e in struct_errors:
            details.append("    - %s" % e)

    # ---------- Q3: emails ----------
    try:
        exp_valid = expected["emails"]["valid"]
        exp_invalid = expected["emails"]["invalid"]
        stu_emails = student_output.get("emails", {})
        stu_valid = stu_emails.get("valid", [])
        stu_invalid = stu_emails.get("invalid", [])

        part = weights["Q3"] / 2.0
        q_score = 0.0
        sub_details = []

        ok_valid, missing_valid, extra_valid = diff_lists_as_sets(exp_valid, stu_valid)
        ok_invalid, missing_invalid, extra_invalid = diff_lists_as_sets(exp_invalid, stu_invalid)

        if ok_valid:
            q_score += part
            sub_details.append("  - Valid emails: ✅ matched (count = %d)." % len(exp_valid))
        else:
            sub_details.append("  - Valid emails: ❌ mismatch.")
            sub_details.append("      Expected count: %d, student count: %d" %
                               (len(exp_valid), len(stu_valid)))
            if missing_valid:
                sub_details.append("      Missing from student's valid: %s" %
                                   (", ".join(missing_valid[:5]) +
                                    (" ..." if len(missing_valid) > 5 else "")))
            if extra_valid:
                sub_details.append("      Extra in student's valid (should not be valid): %s" %
                                   (", ".join(extra_valid[:5]) +
                                    (" ..." if len(extra_valid) > 5 else "")))

        if ok_invalid:
            q_score += part
            sub_details.append("  - Invalid emails: ✅ matched (count = %d)." % len(exp_invalid))
        else:
            sub_details.append("  - Invalid emails: ❌ mismatch.")
            sub_details.append("      Expected count: %d, student count: %d" %
                               (len(exp_invalid), len(stu_invalid)))
            if missing_invalid:
                sub_details.append("      Missing from student's invalid: %s" %
                                   (", ".join(missing_invalid[:5]) +
                                    (" ..." if len(missing_invalid) > 5 else "")))
            if extra_invalid:
                sub_details.append("      Extra in student's invalid (should not be invalid): %s" %
                                   (", ".join(extra_invalid[:5]) +
                                    (" ..." if len(extra_invalid) > 5 else "")))

        scores["Q3"] = q_score
        remarks.append("Q3 – emails: %.1f/%d" % (q_score, weights["Q3"]))
        details.append("Q3 details:")
        details.extend(sub_details)
    except Exception as e:
        remarks.append("Q3 – emails: 0/%d (error: %s)" % (weights["Q3"], e))
        details.append("Q3 details: ❌ Exception while checking emails: %s" % e)

    # ---------- Q4: names ----------
    try:
        exp_valid_n = expected["names"]["valid"]
        exp_invalid_n = expected["names"]["invalid"]
        stu_names = student_output.get("names", {})
        stu_valid_n = stu_names.get("valid", [])
        stu_invalid_n = stu_names.get("invalid", [])

        part = weights["Q4"] / 2.0
        q_score = 0.0
        sub_details = []

        ok_valid_n, missing_valid_n, extra_valid_n = diff_lists_as_sets(exp_valid_n, stu_valid_n)
        ok_invalid_n, missing_invalid_n, extra_invalid_n = diff_lists_as_sets(exp_invalid_n, stu_invalid_n)

        if ok_valid_n:
            q_score += part
            sub_details.append("  - Valid names: ✅ matched (count = %d)." % len(exp_valid_n))
        else:
            sub_details.append("  - Valid names: ❌ mismatch.")
            sub_details.append("      Expected count: %d, student count: %d" %
                               (len(exp_valid_n), len(stu_valid_n)))
            if missing_valid_n:
                sub_details.append("      Missing from student's valid: %s" %
                                   (", ".join(missing_valid_n[:5]) +
                                    (" ..." if len(missing_valid_n) > 5 else "")))
            if extra_valid_n:
                sub_details.append("      Extra in student's valid (should not be valid): %s" %
                                   (", ".join(extra_valid_n[:5]) +
                                    (" ..." if len(extra_valid_n) > 5 else "")))

        if ok_invalid_n:
            q_score += part
            sub_details.append("  - Invalid names: ✅ matched (count = %d)." % len(exp_invalid_n))
        else:
            sub_details.append("  - Invalid names: ❌ mismatch.")
            sub_details.append("      Expected count: %d, student count: %d" %
                               (len(exp_invalid_n), len(stu_invalid_n)))
            if missing_invalid_n:
                sub_details.append("      Missing from student's invalid: %s" %
                                   (", ".join(missing_invalid_n[:5]) +
                                    (" ..." if len(missing_invalid_n) > 5 else "")))
            if extra_invalid_n:
                sub_details.append("      Extra in student's invalid (should not be invalid): %s" %
                                   (", ".join(extra_invalid_n[:5]) +
                                    (" ..." if len(extra_invalid_n) > 5 else "")))

        scores["Q4"] = q_score
        remarks.append("Q4 – names: %.1f/%d" % (q_score, weights["Q4"]))
        details.append("Q4 details:")
        details.extend(sub_details)
    except Exception as e:
        remarks.append("Q4 – names: 0/%d (error: %s)" % (weights["Q4"], e))
        details.append("Q4 details: ❌ Exception while checking names: %s" % e)

    # ---------- Q5: general stats ----------
    try:
        exp_gen = expected["basicStats"]
        stu_gen = student_output.get("basicStats", {})

        part = weights["Q5"] / 5.0  # usersCount, noPurchasesCount, avgAge, oldest, youngest
        q_score = 0.0
        sub_details = []

        # usersCount – נבדוק מול השדה למעלה
        exp_users_count = expected["usersCount"]
        stu_users_count = student_output.get("usersCount")

        if exp_users_count == stu_users_count:
            q_score += part
            sub_details.append("  - usersCount: ✅ %d" % exp_users_count)
        else:
            sub_details.append("  - usersCount: ❌ expected %d, got %s"
                               % (exp_users_count, str(stu_users_count)))

        # usersWithoutPurchasesCount
        if exp_gen["usersWithoutPurchasesCount"] == stu_gen.get("usersWithoutPurchasesCount"):
            q_score += part
            sub_details.append("  - usersWithoutPurchasesCount: ✅ %d"
                               % exp_gen["usersWithoutPurchasesCount"])
        else:
            sub_details.append("  - usersWithoutPurchasesCount: ❌ expected %d, got %s"
                               % (exp_gen["usersWithoutPurchasesCount"],
                                  str(stu_gen.get("usersWithoutPurchasesCount"))))

        # averageAge
        if almost_equal(exp_gen["averageAge"], stu_gen.get("averageAge")):
            q_score += part
            sub_details.append("  - averageAge: ✅ expected %.2f, got %s"
                               % (exp_gen["averageAge"], str(stu_gen.get("averageAge"))))
        else:
            sub_details.append("  - averageAge: ❌ expected %.2f, got %s"
                               % (exp_gen["averageAge"], str(stu_gen.get("averageAge"))))

        # oldestUser by id
        if exp_gen["oldestUser"] and stu_gen.get("oldestUser"):
            if exp_gen["oldestUser"]["id"] == stu_gen["oldestUser"].get("id"):
                q_score += part
                sub_details.append("  - oldestUser: ✅ id=%s"
                                   % str(exp_gen["oldestUser"]["id"]))
            else:
                sub_details.append("  - oldestUser: ❌ expected id=%s, got id=%s"
                                   % (str(exp_gen["oldestUser"]["id"]),
                                      str(stu_gen["oldestUser"].get("id"))))
        else:
            sub_details.append("  - oldestUser: ⚠ missing or None in expected/student output.")

        # youngestUser by id
        if exp_gen["youngestUser"] and stu_gen.get("youngestUser"):
            if exp_gen["youngestUser"]["id"] == stu_gen["youngestUser"].get("id"):
                q_score += part
                sub_details.append("  - youngestUser: ✅ id=%s"
                                   % str(exp_gen["youngestUser"]["id"]))
            else:
                sub_details.append("  - youngestUser: ❌ expected id=%s, got id=%s"
                                   % (str(exp_gen["youngestUser"]["id"]),
                                      str(stu_gen["youngestUser"].get("id"))))
        else:
            sub_details.append("  - youngestUser: ⚠ missing or None in expected/student output.")

        scores["Q5"] = q_score
        remarks.append("Q5 – general stats: %.1f/%d" % (q_score, weights["Q5"]))
        details.append("Q5 details:")
        details.extend(sub_details)
    except Exception as e:
        remarks.append("Q5 – general stats: 0/%d (error: %s)" % (weights["Q5"], e))
        details.append("Q5 details: ❌ Exception while checking general stats: %s" % e)

    # ---------- Q6: purchases ----------
    try:
        exp_p = expected["purchaseStats"]
        stu_p = student_output.get("purchaseStats", {})
        exp_more3 = expected["moreThanThreePurchasesCount"]
        stu_more3 = student_output.get("moreThanThreePurchasesCount")

        part = weights["Q6"] / 5.0  # totalEvents, totalMoney, highest, top3, moreThanThree
        q_score = 0.0
        sub_details = []

        # totalPurchaseEvents
        if exp_p["totalPurchaseEvents"] == stu_p.get("totalPurchaseEvents"):
            q_score += part
            sub_details.append("  - totalPurchaseEvents: ✅ %d"
                               % exp_p["totalPurchaseEvents"])
        else:
            sub_details.append("  - totalPurchaseEvents: ❌ expected %d, got %s"
                               % (exp_p["totalPurchaseEvents"],
                                  str(stu_p.get("totalPurchaseEvents"))))

        # totalMoneySpent
        if almost_equal(exp_p["totalMoneySpent"], stu_p.get("totalMoneySpent")):
            q_score += part
            sub_details.append("  - totalMoneySpent: ✅ expected %.2f, got %s"
                               % (exp_p["totalMoneySpent"],
                                  str(stu_p.get("totalMoneySpent"))))
        else:
            sub_details.append("  - totalMoneySpent: ❌ expected %.2f, got %s"
                               % (exp_p["totalMoneySpent"],
                                  str(stu_p.get("totalMoneySpent"))))

        # highestSinglePurchase by userId
        if exp_p["highestSinglePurchase"] and stu_p.get("highestSinglePurchase"):
            if exp_p["highestSinglePurchase"]["userId"] == stu_p["highestSinglePurchase"].get("userId"):
                q_score += part
                sub_details.append("  - highestSinglePurchase.userId: ✅ %s"
                                   % str(exp_p["highestSinglePurchase"]["userId"]))
            else:
                sub_details.append("  - highestSinglePurchase.userId: ❌ expected %s, got %s"
                                   % (str(exp_p["highestSinglePurchase"]["userId"]),
                                      str(stu_p["highestSinglePurchase"].get("userId"))))
        else:
            sub_details.append("  - highestSinglePurchase: ⚠ missing or None.")

        # top3Spenders by set of ids
        exp_top_ids = set([d["id"] for d in exp_p.get("top3Spenders", [])])
        stu_top_ids = set([d.get("id") for d in stu_p.get("top3Spenders", [])])
        if exp_top_ids == stu_top_ids:
            q_score += part
            sub_details.append("  - top3Spenders: ✅ same set of user IDs.")
        else:
            missing_ids = exp_top_ids - stu_top_ids
            extra_ids = stu_top_ids - exp_top_ids
            sub_details.append("  - top3Spenders: ❌ mismatch on user IDs.")
            if missing_ids:
                sub_details.append("      Missing IDs in student's top3: %s"
                                   % (", ".join(map(str, list(missing_ids)))))
            if extra_ids:
                sub_details.append("      Extra IDs in student's top3: %s"
                                   % (", ".join(map(str, list(extra_ids)))))

        # moreThanThreePurchasesCount
        if exp_more3 == stu_more3:
            q_score += part
            sub_details.append("  - moreThanThreePurchasesCount: ✅ %d" % exp_more3)
        else:
            sub_details.append("  - moreThanThreePurchasesCount: ❌ expected %d, got %s"
                               % (exp_more3, str(stu_more3)))

        scores["Q6"] = q_score
        remarks.append("Q6 – purchases: %.1f/%d" % (q_score, weights["Q6"]))
        details.append("Q6 details:")
        details.extend(sub_details)
    except Exception as e:
        remarks.append("Q6 – purchases: 0/%d (error: %s)" % (weights["Q6"], e))
        details.append("Q6 details: ❌ Exception while checking purchases: %s" % e)

    # ---------- Q7: age groups ----------
    try:
        exp_age = expected["ageGroups"]
        stu_age = student_output.get("ageGroups", {})

        part = weights["Q7"] / 4.0  # Young, Adult, Senior, Elder
        q_score = 0.0
        sub_details = []

        for grp in ["Young", "Adult", "Senior", "Elder"]:
            exp_ids = set([d["id"] for d in exp_age.get(grp, [])])
            stu_ids = set([d.get("id") for d in stu_age.get(grp, [])])
            if exp_ids == stu_ids:
                q_score += part
                sub_details.append("  - %s: ✅ %d users" % (grp, len(exp_ids)))
            else:
                missing_ids = exp_ids - stu_ids
                extra_ids = stu_ids - exp_ids
                sub_details.append("  - %s: ❌ mismatch" % grp)
                sub_details.append("      Expected count: %d, student count: %d"
                                   % (len(exp_ids), len(stu_ids)))
                if missing_ids:
                    sub_details.append("      Missing IDs in '%s': %s"
                                       % (grp, ", ".join(map(str, list(missing_ids)[:5]))))
                if extra_ids:
                    sub_details.append("      Extra IDs in '%s': %s"
                                       % (grp, ", ".join(map(str, list(extra_ids)[:5]))))

        scores["Q7"] = q_score
        remarks.append("Q7 – age groups: %.1f/%d" % (q_score, weights["Q7"]))
        details.append("Q7 details:")
        details.extend(sub_details)
    except Exception as e:
        remarks.append("Q7 – age groups: 0/%d (error: %s)" % (weights["Q7"], e))
        details.append("Q7 details: ❌ Exception while checking age groups: %s" % e)

    # ---------- Q8: users without purchases ----------
    try:
        exp_u = expected["usersWithoutPurchases"]
        stu_u = student_output.get("usersWithoutPurchases", [])
        exp_ids = set([d["id"] for d in exp_u])
        stu_ids = set([d.get("id") for d in stu_u])

        if exp_ids == stu_ids:
            scores["Q8"] = float(weights["Q8"])
            remarks.append("Q8 – users without purchases: %.1f/%d" %
                           (scores["Q8"], weights["Q8"]))
            details.append("Q8 details: ✅ Same set of user IDs without purchases (count = %d)."
                           % len(exp_ids))
        else:
            scores["Q8"] = 0.0
            remarks.append("Q8 – users without purchases: 0/%d" % (weights["Q8"]))
            missing_ids = exp_ids - stu_ids
            extra_ids = stu_ids - exp_ids
            sub_details = []
            sub_details.append("Q8 details: ❌ mismatch in usersWithoutPurchases IDs.")
            sub_details.append("  Expected count: %d, student count: %d"
                               % (len(exp_ids), len(stu_ids)))
            if missing_ids:
                sub_details.append("  Missing IDs: %s"
                                   % (", ".join(map(str, list(missing_ids)[:10]))))
            if extra_ids:
                sub_details.append("  Extra IDs: %s"
                                   % (", ".join(map(str, list(extra_ids)[:10]))))
            details.extend(sub_details)
    except Exception as e:
        remarks.append("Q8 – users without purchases: 0/%d (error: %s)" % (weights["Q8"], e))
        details.append("Q8 details: ❌ Exception while checking users without purchases: %s" % e)

    # ---------- TOTAL ----------
    total_score = sum(scores.values())
    total_score = max(0.0, min(100.0, total_score))

    # classify questions by performance
    full_mark = []
    partial = []
    zero = []
    for q in ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"]:
        if scores[q] == weights[q]:
            full_mark.append(q)
        elif scores[q] == 0:
            zero.append(q)
        else:
            partial.append(q)

    print("=" * 60)
    print("Student ID:", student_id)
    print("Folder   :", folder_path)
    print("-" * 60)
    for r in remarks:
        print(r)
    print("-" * 60)
    print("DETAILED FEEDBACK:")
    for d in details:
        print(d)
    print("-" * 60)
    print("Summary:")
    print("  ✅ Full mark questions:", ", ".join(full_mark) if full_mark else "None")
    print("  ⚠ Partial questions   :", ", ".join(partial) if partial else "None")
    print("  ❌ Zero questions      :", ", ".join(zero) if zero else "None")
    print("-" * 60)
    print("TOTAL: %.1f/100" % total_score)
    print("=" * 60)


def main():
    print("=== HW1 Autograder – Advanced Python / JSON (detailed) ===")
    student_id = input(
        "Enter student ID (or student_id1_student_id2 if in pair): "
    ).strip()

    if not student_id:
        print("Error: student ID is required.")
        return

    folder = input(
        "Enter path to student's folder (where data_*.json and output_analysis.json are): "
    ).strip()

    if not folder:
        folder = "."

    grade_student(student_id, folder)

def grade_student_to_result(student_id, folder_path):
    """
    כמו grade_student, אבל במקום להדפיס למסך – מחזיר dict מסודר
    שנוכל להשתמש בו באתר.
    """
    # נעתיק את כל התוכן של grade_student,
    # אבל במקום print – נבנה מבנה נתונים.

    # weights per question (Total = 100)
    weights = {
        "Q1": 5,
        "Q2": 10,
        "Q3": 15,
        "Q4": 10,
        "Q5": 20,
        "Q6": 20,
        "Q7": 10,
        "Q8": 10
    }

    scores = {k: 0.0 for k in weights}
    remarks = []
    details = []

    data_filename = "data_%s.json" % student_id
    data_path = os.path.join(folder_path, data_filename)
    out_path = os.path.join(folder_path, "output_analysis.json")

    # ---------- Q1 ----------
    users, err1 = load_json_file(data_path)
    if err1 is not None:
        remarks.append("Q1 – JSON loading: 0/%d (error: %s)" % (weights["Q1"], err1))
        return {
            "student_id": student_id,
            "folder": folder_path,
            "scores": scores,
            "remarks": remarks,
            "details": details,
            "total": 0.0
        }
    if not isinstance(users, list):
        remarks.append("Q1 – JSON loading: 0/%d (root is not a list)" % weights["Q1"])
        return {
            "student_id": student_id,
            "folder": folder_path,
            "scores": scores,
            "remarks": remarks,
            "details": details,
            "total": 0.0
        }

    scores["Q1"] = float(weights["Q1"])
    remarks.append("Q1 – JSON loading: %.1f/%d" % (scores["Q1"], weights["Q1"]))
    details.append("Q1 details: ✅ JSON file '%s' loaded successfully, root is a list with %d users."
                   % (data_filename, len(users)))

    # Build expected reference
    expected = build_expected_output(users)

    # Load student's output
    student_output, err2 = load_json_file(out_path)
    if err2 is not None:
        remarks.append("Q2–Q8: cannot grade because output_analysis.json has error: %s" % err2)
        total_score = scores["Q1"]
        return {
            "student_id": student_id,
            "folder": folder_path,
            "scores": scores,
            "remarks": remarks,
            "details": details,
            "total": total_score
        }

    # מכאן והלאה – אותו קוד כמו grade_student,
    # רק בלי print, אלא עדכון scores/remarks/details.
    # אפשר להעתיק מ־grade_student שלך אחד לאחד
    # (הגרסה המורחבת שכבר כתבנו), עד לחישוב total_score
    # ובסוף להחזיר dict:

    # ... (הקוד הקיים של Q2–Q8 בדיוק כמו בגרסה האחרונה) ...

    # ---------- TOTAL ----------
    total_score = sum(scores.values())
    total_score = max(0.0, min(100.0, total_score))

    # classify questions by performance
    full_mark = []
    partial = []
    zero = []
    for q in ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"]:
        if scores[q] == weights[q]:
            full_mark.append(q)
        elif scores[q] == 0:
            zero.append(q)
        else:
            partial.append(q)

    # אפשר גם להוסיף את זה ל־details או להחזיר בנפרד
    summary = {
        "full_mark": full_mark,
        "partial": partial,
        "zero": zero
    }

    return {
        "student_id": student_id,
        "folder": folder_path,
        "scores": scores,
        "weights": weights,
        "remarks": remarks,
        "details": details,
        "summary": summary,
        "total": total_score
    }

if __name__ == "__main__":
    main()
