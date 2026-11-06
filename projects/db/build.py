import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import csv
    from datetime import date

    return csv, date, duckdb, mo


@app.cell
def _(mo):
    mo.md("""
    # BabsonAI Labs Database Build

    This notebook builds the database for Scenario A.

    It creates the tables, loads generated CSV data, checks the
    database rules, and creates a reusable view.
    """)
    return


@app.cell
def _(date, duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"
    data_dir = mo.notebook_dir() / "data"

    as_of = date(2026, 10, 31)

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return as_of, ask, data_dir, database


@app.cell
def _(mo):
    mo.md("""
    ## The Tables

    The database contains five tables: people, projects,
    project_members, tasks, and expenses.

    Each table has a declared primary key. Foreign keys connect
    related records, while constraints enforce the applicable rules.
    """)
    return


@app.cell
def _():
    people_sql = """
    CREATE TABLE people (
        person_id INTEGER PRIMARY KEY,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR NOT NULL,
        work_email VARCHAR NOT NULL,
        title VARCHAR NOT NULL,
        start_date DATE NOT NULL,
        manager_id INTEGER REFERENCES people(person_id),

        CHECK (
            manager_id IS NULL
            OR manager_id <> person_id
        )
    );
    """
    return (people_sql,)


@app.cell
def _():
    projects_sql = """
    CREATE TABLE projects (
        project_id INTEGER PRIMARY KEY,
        project_name VARCHAR NOT NULL,
        client_name VARCHAR,
        category VARCHAR NOT NULL
            CHECK (
                category IN (
                    'LLM app',
                    'data pipeline',
                    'internal tool'
                )
            ),
        budget DECIMAL(12, 2) NOT NULL
            CHECK (budget > 0),
        start_date DATE NOT NULL,
        status VARCHAR NOT NULL DEFAULT 'planned'
            CHECK (
                status IN (
                    'planned',
                    'active',
                    'paused',
                    'done'
                )
            )
    );
    """
    return (projects_sql,)


@app.cell
def _():
    project_members_sql = """
    CREATE TABLE project_members (
        person_id INTEGER NOT NULL
            REFERENCES people(person_id),
        project_id INTEGER NOT NULL
            REFERENCES projects(project_id),
        project_role VARCHAR NOT NULL,
        hours_per_week INTEGER NOT NULL
            CHECK (hours_per_week BETWEEN 1 AND 40),
        joined_date DATE NOT NULL,

        PRIMARY KEY (person_id, project_id)
    );
    """
    return (project_members_sql,)


@app.cell
def _():
    tasks_sql = """
    CREATE TABLE tasks (
        task_id INTEGER PRIMARY KEY,
        project_id INTEGER NOT NULL
            REFERENCES projects(project_id),
        description VARCHAR NOT NULL,
        created_date DATE NOT NULL,
        assignee_id INTEGER
            REFERENCES people(person_id),
        assigned_date DATE,
        due_date DATE NOT NULL,
        completed_date DATE,

        CHECK (
            completed_date IS NULL
            OR completed_date >= created_date
        ),

        CHECK (
            (assignee_id IS NULL AND assigned_date IS NULL)
            OR
            (assignee_id IS NOT NULL AND assigned_date IS NOT NULL)
        ),

        CHECK (
            assigned_date IS NULL
            OR assigned_date >= created_date
        )
    );
    """
    return (tasks_sql,)


@app.cell
def _():
    expenses_sql = """
    CREATE TABLE expenses (
        expense_id INTEGER PRIMARY KEY,
        project_id INTEGER NOT NULL
            REFERENCES projects(project_id),
        expense_date DATE NOT NULL,
        amount DECIMAL(12, 2) NOT NULL
            CHECK (amount > 0),
        category VARCHAR NOT NULL
            CHECK (
                category IN (
                    'GPU cloud',
                    'data labeling',
                    'software',
                    'travel'
                )
            ),
        note VARCHAR NOT NULL
    );
    """
    return (expenses_sql,)


@app.cell
def _(
    duckdb,
    expenses_sql,
    mo,
    people_sql,
    project_members_sql,
    projects_sql,
    tasks_sql,
):
    with duckdb.connect(":memory:") as _check_con:
        for _statement in [
            people_sql,
            projects_sql,
            project_members_sql,
            tasks_sql,
            expenses_sql,
        ]:
            _check_con.execute(_statement)

        _table_names = _check_con.execute(
            "SHOW TABLES"
        ).fetchall()

    mo.ui.table(
        [
            {
                "table": _row[0],
                "check": "Created successfully",
            }
            for _row in _table_names
        ]
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## The Data

    The CSV files are generated by make_data.py using seed 6301.
    The reporting period is November 1, 2025 through October 31, 2026.
    The as_of date is October 31, 2026.

    Tasks 299 and 300 intentionally violate the project membership rule.
    Projects 11 and 12 intentionally have no expenses.
    """)
    return


@app.cell
def _(
    csv,
    data_dir,
    database,
    duckdb,
    expenses_sql,
    mo,
    people_sql,
    project_members_sql,
    projects_sql,
    tasks_sql,
    view_sql,
):
    _required_files = [
        "people.csv",
        "projects.csv",
        "project_members.csv",
        "tasks.csv",
        "expenses.csv",
    ]

    for _filename in _required_files:
        if not (data_dir / _filename).is_file():
            raise FileNotFoundError(f"Missing CSV file: {_filename}")

    with (data_dir / "people.csv").open(
        newline="", encoding="utf-8"
    ) as _file:
        _people_rows = sorted(
            csv.DictReader(_file),
            key=lambda row: int(row["person_id"]),
        )

    database.unlink(missing_ok=True)

    with duckdb.connect(database) as _con:
        for _statement in [
            people_sql,
            projects_sql,
            project_members_sql,
            tasks_sql,
            expenses_sql,
        ]:
            _con.execute(_statement)

        # Insert managers before the employees who reference them.
        for _person in _people_rows:
            _con.execute(
                """
                INSERT INTO people (
                    person_id, first_name, last_name,
                    work_email, title, start_date, manager_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    int(_person["person_id"]),
                    _person["first_name"],
                    _person["last_name"],
                    _person["work_email"],
                    _person["title"],
                    _person["start_date"],
                    int(_person["manager_id"])
                    if _person["manager_id"] else None,
                ],
            )

        for _table in [
            "projects",
            "project_members",
            "tasks",
            "expenses",
        ]:
            _con.execute(
                f"""
                INSERT INTO {_table} BY NAME
                SELECT *
                FROM read_csv(?, header=true, nullstr='')
                """,
                [str(data_dir / f"{_table}.csv")],
            )

        _con.execute(view_sql)

    build_complete = True

    mo.md("**Database rebuilt and all five CSV files loaded.**")
    return (build_complete,)


@app.cell
def _():
    import polars as pl

    return (pl,)


@app.cell
def _(data_dir, mo, pl):
    tasks_csv = pl.read_csv(
        data_dir / "tasks.csv",
        try_parse_dates=True,
    )

    mo.vstack([
        mo.md("""
        ## A Look at the Data

        The first ten rows below show the generated task data.
        Blank assignment or completion fields represent missing values.
        """),
        mo.ui.table(tasks_csv.head(10)),
    ])
    return (tasks_csv,)


@app.cell
def _(pl, tasks_csv):
    import matplotlib.pyplot as plt

    weekday_counts = (
        tasks_csv
        .with_columns(
            pl.col("created_date").dt.weekday().alias("weekday")
        )
        .group_by("weekday")
        .agg(pl.len().alias("task_count"))
        .sort("weekday")
    )

    _weekday_totals = dict(
        weekday_counts.select("weekday", "task_count").iter_rows()
    )

    _fig, _ax = plt.subplots(figsize=(8, 4))

    _ax.bar(
        ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        [_weekday_totals.get(day, 0) for day in range(1, 8)],
        color="#237A57",
    )

    _ax.set_title("Tasks Created by Day of Week")
    _ax.set_xlabel("Day of Week")
    _ax.set_ylabel("Number of Tasks")
    _ax.set_ylim(bottom=0)
    _fig.tight_layout()

    _fig
    return


@app.cell
def _(mo):
    mo.md("""
    Most tasks were created on weekdays, with far fewer on weekends.
    This pattern is plausible for a business team, although the data
    are synthetic and do not represent actual company activity.
    """)
    return


@app.cell
def _(ask, build_complete, mo):
    mo.stop(not build_complete)

    row_counts = ask("""
        SELECT 'people' AS table_name, COUNT(*) AS row_count
        FROM people
        UNION ALL
        SELECT 'projects', COUNT(*) FROM projects
        UNION ALL
        SELECT 'project_members', COUNT(*) FROM project_members
        UNION ALL
        SELECT 'tasks', COUNT(*) FROM tasks
        UNION ALL
        SELECT 'expenses', COUNT(*) FROM expenses
    """)

    mo.vstack([
        mo.md("## Row Counts"),
        mo.ui.table(row_counts),
    ])
    return


@app.cell
def _(build_complete, database, duckdb, mo):
    mo.stop(not build_complete)

    with duckdb.connect(database) as _con:
        _con.execute("BEGIN TRANSACTION")

        try:
            _con.execute("""
                INSERT INTO expenses (
                    expense_id,
                    project_id,
                    expense_date,
                    amount,
                    category,
                    note
                )
                VALUES (
                    99999,
                    1,
                    DATE '2026-10-31',
                    -50.00,
                    'software',
                    'Invalid negative expense for constraint testing'
                )
            """)
        except duckdb.ConstraintException as _error:
            _refused = True
            _error_message = str(_error)
        else:
            _refused = False
            _error_message = "The invalid row was unexpectedly accepted."
        finally:
            _con.execute("ROLLBACK")

    assert _refused, _error_message

    mo.vstack([
        mo.md("""
        ## A Row It Refuses

        **Expected:** An expense of -50.00 must be rejected because
        the amount must be greater than zero.

        **Actual:** DuckDB rejected the row.
        The transaction was rolled back, leaving the data unchanged.
        """),
        mo.plain_text(_error_message),
    ])
    return


@app.cell
def _(ask, build_complete, mo):
    mo.stop(not build_complete)

    _known_checks = [
        (
            "People without a manager",
            2,
            """
            SELECT COUNT(*) AS actual
            FROM people
            WHERE manager_id IS NULL
            """,
        ),
        (
            "Tasks with intentional membership violations",
            2,
            """
            SELECT COUNT(*) AS actual
            FROM tasks AS t
            WHERE t.assignee_id IS NOT NULL
              AND NOT EXISTS (
                  SELECT 1
                  FROM project_members AS pm
                  WHERE pm.person_id = t.assignee_id
                    AND pm.project_id = t.project_id
              )
            """,
        ),
        (
            "Projects without expenses",
            2,
            """
            SELECT COUNT(*) AS actual
            FROM projects AS p
            WHERE NOT EXISTS (
                SELECT 1
                FROM expenses AS e
                WHERE e.project_id = p.project_id
            )
            """,
        ),
    ]

    _check_results = []

    for _label, _expected, _sql in _known_checks:
        _actual = ask(_sql).item()

        assert _actual == _expected, f"{_label}: expected {_expected}, got {_actual}"

        _check_results.append({
            "check": _label,
            "expected": _expected,
            "actual": _actual,
            "result": "PASS" if _actual == _expected else "FAIL",
        })

    mo.vstack([
        mo.md("""
        ## Answers You Already Knew

        Before running these queries, the generator gives three
        expected answers:

        - **Expected: 2 people without a manager** (the two founders).
        - **Expected: 2 tasks with assignees outside their project teams** (tasks 299 and 300).
        - **Expected: 2 projects without expenses** (projects 11 and 12).

        The table compares these expectations with the database results.
        """),
        mo.ui.table(_check_results),
    ])
    return


@app.cell
def _(ask, build_complete, mo):
    mo.stop(not build_complete)

    _violations = ask("""
        SELECT t.task_id
        FROM tasks AS t
        WHERE t.assignee_id IS NOT NULL
          AND NOT EXISTS (
              SELECT 1 FROM project_members AS pm
              WHERE pm.person_id = t.assignee_id
                AND pm.project_id = t.project_id
          )
        ORDER BY t.task_id
    """)
    _actual_ids = _violations["task_id"].to_list()
    assert _actual_ids == [299, 300], f"Unexpected task IDs: {_actual_ids}"

    _early_assignments = ask("""
        SELECT COUNT(*) AS violations
        FROM tasks AS t
        JOIN people AS p ON p.person_id = t.assignee_id
        WHERE t.assigned_date < p.start_date
    """).item()
    assert _early_assignments == 0, "A task was assigned before the employee started."

    _empty_projects = ask("""
        SELECT COUNT(*) AS violations
        FROM projects AS p
        WHERE NOT EXISTS (
            SELECT 1 FROM project_members AS pm
            WHERE pm.project_id = p.project_id
        )
    """).item()
    assert _empty_projects == 0, "A project has no members."

    mo.md(f"""
    **Additional rule checks**

    - Expected membership violation IDs: 299 and 300. Actual: {_actual_ids}.
    - Expected assignments before employment: 0. Actual: {_early_assignments}.
    - Expected projects without members: 0. Actual: {_empty_projects}.

    These assertions stop this cell if the expected results do not match.
    """)
    return


@app.cell
def _():
    view_sql = """
    CREATE VIEW project_spending AS
    SELECT
        p.project_id,
        p.project_name,
        p.status,
        p.budget,
        COALESCE(SUM(e.amount), 0) AS total_expenses,
        p.budget - COALESCE(SUM(e.amount), 0) AS remaining_budget
    FROM projects AS p
    LEFT JOIN expenses AS e
        ON p.project_id = e.project_id
    GROUP BY
        p.project_id,
        p.project_name,
        p.status,
        p.budget;
    """
    return (view_sql,)


@app.cell
def _(ask, build_complete, mo):
    mo.stop(not build_complete)

    spending_preview = ask("""
        SELECT *
        FROM project_spending
        ORDER BY project_id
    """)

    mo.vstack([
        mo.md("""
        ## A View

        The project_spending view summarizes each project's budget,
        total expenses, and remaining budget.

        Projects without expenses are included with zero spending.
        A manager could review this view weekly to monitor budgets.
        """),
        mo.ui.table(spending_preview),
    ])
    return


if __name__ == "__main__":
    app.run()
