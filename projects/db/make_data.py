import csv
import random
from datetime import date, timedelta
from pathlib import Path


SEED = 6301
rng = random.Random(SEED)

AS_OF = date(2026, 10, 31)
START_DATE = date(2025, 11, 1)

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def random_date(start, end):
    """Return a random date between start and end, inclusive."""
    days = (end - start).days
    return start + timedelta(days=rng.randint(0, days))


def write_csv(filename, rows):
    """Write dictionaries to a CSV file with a header."""
    path = DATA_DIR / filename

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"{filename}: {len(rows)} rows")


# All people and email addresses below are fictional.
names = [
    ("Anna", "Chen"),
    ("Ben", "Patel"),
    ("Carla", "Nguyen"),
    ("David", "Kim"),
    ("Emma", "Lopez"),
    ("Frank", "Wilson"),
    ("Grace", "Shah"),
    ("Henry", "Brown"),
    ("Iris", "Tran"),
    ("James", "Lee"),
    ("Kira", "Davis"),
    ("Leo", "Garcia"),
    ("Maya", "Singh"),
    ("Noah", "Martin"),
    ("Olivia", "Wang"),
    ("Peter", "Clark"),
    ("Quinn", "Adams"),
    ("Rosa", "Ahmed"),
    ("Sam", "Taylor"),
    ("Tina", "Park"),
    ("Uma", "Scott"),
    ("Victor", "Reed"),
    ("Wendy", "Pham"),
    ("Xavier", "Brooks"),
    ("Yara", "Ali"),
]

people = []

for person_id, (first_name, last_name) in enumerate(names, start=1):
    if person_id <= 2:
        manager_id = None
        start_date = START_DATE
        title = (
            "Co-founder and CEO"
            if person_id == 1
            else "Co-founder and CTO"
        )
    else:
        manager_id = rng.choice(
            list(range(1, min(person_id, 6)))
        )
        manager = people[manager_id - 1]

        earliest_start = max(
            START_DATE + timedelta(days=7),
            manager["start_date"],
        )

        start_date = random_date(
            earliest_start,
            date(2026, 6, 30),
        )

        title = (
            "Team Lead"
            if person_id <= 5
            else rng.choice([
                "AI Engineer",
                "Data Analyst",
                "Software Developer",
                "Product Designer",
            ])
        )

    people.append({
        "person_id": person_id,
        "first_name": first_name,
        "last_name": last_name,
        "work_email": (
            f"{first_name.lower()}.{last_name.lower()}"
            "@babsonai.example"
        ),
        "title": title,
        "start_date": start_date,
        "manager_id": manager_id,
    })


write_csv("people.csv", people)
# Project names, clients, and budgets are fictional.
project_specs = [
    (1, "Customer Support Chatbot",
     "Maple Retail", "LLM app", 18000,
     date(2025, 11, 1), "active"),

    (2, "Sales Data Pipeline",
     "Harbor Foods", "data pipeline", 24000,
     date(2025, 12, 1), "active"),

    (3, "Invoice Assistant",
     "Cedar Accounting", "LLM app", 12000,
     date(2026, 1, 5), "done"),

    (4, "Internal Knowledge Search",
     None, "internal tool", 8000,
     date(2026, 2, 2), "done"),

    (5, "Inventory Forecast Pipeline",
     "Oak Market", "data pipeline", 22000,
     date(2026, 3, 2), "active"),

    (6, "Hiring Workflow Tool",
     None, "internal tool", 6000,
     date(2026, 4, 1), "paused"),

    (7, "Restaurant Review Assistant",
     "River Cafe", "LLM app", 14000,
     date(2026, 5, 1), "active"),

    (8, "Marketing Data Integration",
     "Pine Studio", "data pipeline", 16000,
     date(2026, 6, 1), "done"),

    (9, "Internal Expense Tracker",
     None, "internal tool", 5000,
     date(2026, 7, 1), "done"),

    (10, "Product Recommendation Assistant",
     "Birch Shop", "LLM app", 20000,
     date(2026, 8, 3), "active"),

    (11, "Client Onboarding Tool",
     None, "internal tool", 7000,
     date(2026, 10, 20), "planned"),

    (12, "Supplier Data Pipeline",
     "Elm Supply", "data pipeline", 15000,
     date(2026, 10, 26), "planned"),
]

projects = []

for (
    project_id,
    project_name,
    client_name,
    category,
    budget,
    start_date,
    status,
) in project_specs:
    projects.append({
        "project_id": project_id,
        "project_name": project_name,
        "client_name": client_name,
        "category": category,
        "budget": budget,
        "start_date": start_date,
        "status": status,
    })

write_csv("projects.csv", projects)
# Create the people-project pairings.
project_members = []

for project in projects:
    eligible_people = [
        person
        for person in people
        if person["start_date"] <= project["start_date"]
    ]

    if project["project_id"] in (1, 2):
        # Anna participates in both active projects.
        other_people = [
            person
            for person in eligible_people
            if person["person_id"] != 1
        ]

        selected_people = [people[0]] + rng.sample(
            other_people,
            k=min(3, len(other_people)),
        )
    else:
        selected_people = rng.sample(
            eligible_people,
            k=min(4, len(eligible_people)),
        )

    for position, person in enumerate(selected_people):
        if (
            person["person_id"] == 1
            and project["project_id"] in (1, 2)
        ):
            hours = 25
        else:
            hours = rng.choice([4, 6, 8, 10, 12])

        latest_join = min(
            AS_OF,
            project["start_date"] + timedelta(days=14),
        )

        joined_date = (
            project["start_date"]
            if position == 0
            else random_date(
                project["start_date"],
                latest_join,
            )
        )

        project_members.append({
            "person_id": person["person_id"],
            "project_id": project["project_id"],
            "project_role": (
                "Project Lead"
                if position == 0
                else rng.choice([
                    "Developer",
                    "Analyst",
                    "Designer",
                ])
            ),
            "hours_per_week": hours,
            "joined_date": joined_date,
        })

write_csv("project_members.csv", project_members)
# Create tasks using the project membership records.
membership_pairs = {
    (member["person_id"], member["project_id"])
    for member in project_members
}

people_by_id = {
    person["person_id"]: person
    for person in people
}

task_descriptions = [
    "Review business requirements",
    "Prepare sample data",
    "Implement application feature",
    "Test model responses",
    "Review data quality",
    "Write technical documentation",
    "Collect client feedback",
    "Fix reported issues",
]

tasks = []

# Create 298 tasks that follow the membership rule.
for task_id in range(1, 299):
    project = (
        projects[0]
        if task_id <= 2
        else rng.choice(projects[:10])
    )

    if task_id == 1:
        created_date = START_DATE
    elif task_id == 2:
        created_date = AS_OF
    else:
        created_date = random_date(
            project["start_date"], AS_OF
        )

        # Most tasks are created on weekdays.
        if rng.random() < 0.9:
            while created_date.weekday() >= 5:
                created_date = random_date(
                    project["start_date"], AS_OF
                )

    available_members = [
        member
        for member in project_members
        if member["project_id"] == project["project_id"]
        and member["joined_date"] <= created_date
    ]

    assignee_id = None
    assigned_date = None
    completed_date = None

    # Completed projects have assigned, completed tasks.
    should_assign = (
        project["status"] == "done"
        or task_id % 7 != 0
    )

    if should_assign:
        member = rng.choice(available_members)
        assignee_id = member["person_id"]

        assigned_date = min(
            AS_OF,
            created_date + timedelta(
                days=rng.randint(0, 3)
            ),
        )

        if project["status"] == "done" or rng.random() < 0.7:
            completed_date = min(
                AS_OF,
                assigned_date + timedelta(
                    days=rng.randint(1, 21)
                ),
            )

    tasks.append({
        "task_id": task_id,
        "project_id": project["project_id"],
        "description": (
            f"{rng.choice(task_descriptions)} "
            f"for task {task_id}"
        ),
        "created_date": created_date,
        "assignee_id": assignee_id,
        "assigned_date": assigned_date,
        "due_date": created_date + timedelta(
            days=rng.randint(7, 28)
        ),
        "completed_date": completed_date,
    })


# Add exactly two intentional membership violations.
# Both assignees exist, but neither belongs to project 1.
outsiders = [
    person
    for person in people
    if (person["person_id"], 1) not in membership_pairs
    and person["start_date"] <= AS_OF
]

for task_id, person in zip([299, 300], outsiders[:2]):
    created_date = max(
        AS_OF - timedelta(days=30),
        person["start_date"],
        projects[0]["start_date"],
    )

    tasks.append({
        "task_id": task_id,
        "project_id": 1,
        "description": (
            f"Intentional membership violation {task_id}"
        ),
        "created_date": created_date,
        "assignee_id": person["person_id"],
        "assigned_date": created_date,
        "due_date": created_date + timedelta(days=7),
        "completed_date": None,
    })


# Verify the intended exceptions before writing the CSV.
invalid_task_ids = [
    task["task_id"]
    for task in tasks
    if task["assignee_id"] is not None
    and (
        task["assignee_id"], task["project_id"]
    ) not in membership_pairs
]

assert len(tasks) == 300
assert invalid_task_ids == [299, 300]

assert all(
    task["assignee_id"] is None
    or task["assigned_date"]
    >= people_by_id[task["assignee_id"]]["start_date"]
    for task in tasks
)

write_csv("tasks.csv", tasks)
print("Intentional membership violations:", invalid_task_ids)
# Create expenses for projects 1 to 10.
# Projects 11 and 12 intentionally have no expenses.
expense_categories = [
    "GPU cloud",
    "data labeling",
    "software",
    "travel",
]

# Amount ranges are expressed in cents.
amount_ranges = {
    "GPU cloud": (10000, 150000),
    "data labeling": (5000, 80000),
    "software": (2000, 30000),
    "travel": (5000, 60000),
}

expenses = []

for expense_id in range(1, 181):
    # Give each of the first ten projects an expense.
    if expense_id <= 10:
        project = projects[expense_id - 1]
    else:
        project = rng.choice(projects[:10])

    category = rng.choices(
        expense_categories,
        weights=[50, 20, 25, 5],
        k=1,
    )[0]

    minimum, maximum = amount_ranges[category]
    amount_cents = rng.randint(minimum, maximum)

    amount = (
        f"{amount_cents // 100}."
        f"{amount_cents % 100:02d}"
    )

    expense_date = random_date(
        project["start_date"], AS_OF
    )

    # Ensure the expense history reaches both endpoints.
    if expense_id == 1:
        expense_date = START_DATE
    elif expense_id == 180:
        expense_date = AS_OF

    expenses.append({
        "expense_id": expense_id,
        "project_id": project["project_id"],
        "expense_date": expense_date,
        "amount": amount,
        "category": category,
        "note": (
            f"{category} expense for "
            f"{project['project_name']}"
        ),
    })


assert len(expenses) == 180

projects_with_expenses = {
    expense["project_id"]
    for expense in expenses
}

assert projects_with_expenses == set(range(1, 11))

write_csv("expenses.csv", expenses)
print("Projects with no expenses: [11, 12]")
