import json
import random
from typing import Dict, List, Any


FIRST_NAMES = [
    "Alice", "Bob", "Emma", "Liam", "Noah", "Olivia", "Mia",
    "Lucas", "Henry", "Grace", "Eve", "James", "Jack", "Ivy",
    "Benjamin", "Hank", "Diana", "Sophia", "Charlie", "Frank"
]

EMAIL_DOMAINS_VALID = ["example.com", "work.net", "market.org", "shop.co", "data.io"]
EMAIL_DOMAINS_INVALID = ["invalid-domain", "bad", "mail", "xx", "test"]


def random_name(rnd: random.Random) -> str:
    base = rnd.choice(FIRST_NAMES)
    mode = rnd.randint(1, 4)

    if mode == 1:
        return base
    elif mode == 2:
        return base + str(rnd.randint(1, 99))
    elif mode == 3:
        return base.lower()
    else:
        return base + "_x"


def random_email(rnd: random.Random, name: str) -> str:
    mode = rnd.randint(1, 4)

    local = name.lower().replace(" ", "")

    if mode == 1:
        domain = rnd.choice(EMAIL_DOMAINS_VALID)
        return f"{local}@{domain}"
    elif mode == 2:
        domain = rnd.choice(EMAIL_DOMAINS_VALID)
        return f"{local}_{domain}"
    elif mode == 3:
        domain = rnd.choice(EMAIL_DOMAINS_INVALID)
        return f"{local}@{domain}"
    else:
        domain = rnd.choice(EMAIL_DOMAINS_VALID)
        return f"{local}@@{domain}"


def random_purchases(rnd: random.Random) -> List[float]:
    length = rnd.randint(0, 7)
    purchases = []
    for _ in range(length):
        amount = round(rnd.uniform(10.0, 300.0), 2)
        purchases.append(amount)
    return purchases


def generate_dataset(student_id: str) -> List[Dict[str, Any]]:
    rnd = random.Random(student_id)

    n_users = rnd.randint(40, 120)

    data = []
    for i in range(1, n_users + 1):
        name = random_name(rnd)
        age = rnd.randint(18, 65)
        purchases = random_purchases(rnd)
        email = random_email(rnd, name)

        user = {
            "id": i,
            "name": name,
            "age": age,
            "purchases": purchases,
            "email": email
        }
        data.append(user)

    return data


def main():
    print("=== JSON Dataset Generator ===")
    student_id = input(
        "Enter your student ID.\n"
        "If you work in pairs, enter: student_id1_student_id2\n"
    ).strip()

    if not student_id:
        print("Error: ID cannot be empty.")
        return

    data = generate_dataset(student_id)

    filename = f"data_{student_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Dataset created successfully: {filename}")
    print("Use this file as the input JSON for your homework.")


if __name__ == "__main__":
    main()
