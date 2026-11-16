import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    from datetime import date
    import duckdb

    as_of = date(2026, 10, 31)
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return as_of, ask


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Business Questions

    ### 1. How much of its budget has each project spent?
    """)
    return


@app.cell
def _(ask):
    q1_budget = ask("""
        SELECT
            project_id,
            project_name,
            budget,
            total_expenses,
            ROUND(100.0 * total_expenses / budget, 2) AS budget_spent_pct
        FROM project_spending
        ORDER BY total_expenses / budget DESC, project_id
    """)

    q1_budget
    return (q1_budget,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Three of the 12 projects exceeded their budgets: Internal Expense Tracker (247.37%), Hiring Workflow Tool (127.54%), and Internal Knowledge Search (120.84%).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2. Which tasks are overdue and still incomplete as of October 31, 2026?
    """)
    return


@app.cell
def _(as_of, ask):
    q2_overdue = ask(f"""
        SELECT
            t.task_id,
            t.description,
            p.project_name,
            COALESCE(pe.first_name || ' ' || pe.last_name, 'Unassigned') AS assignee,
            t.due_date
        FROM tasks AS t
        JOIN projects AS p
            ON t.project_id = p.project_id
        LEFT JOIN people AS pe
            ON t.assignee_id = pe.person_id
        WHERE t.due_date < DATE '{as_of.isoformat()}'
          AND t.completed_date IS NULL
        ORDER BY t.due_date, t.task_id
    """)

    q2_overdue
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The query returned 65 overdue and incomplete tasks across six projects.

    **Assumption.** I count a task if it was due before October 31, 2026, and has no recorded completion date. Under this definition, a task completed on November 2 is excluded.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3. How many hours per week is each person committed to active projects, and who is above 40 hours?
    """)
    return


@app.cell
def _(ask):
    q3_workload = ask("""
        WITH active_hours AS (
            SELECT
                pm.person_id,
                SUM(pm.hours_per_week) AS weekly_hours
            FROM project_members AS pm
            JOIN projects AS p
                ON pm.project_id = p.project_id
            WHERE p.status = 'active'
            GROUP BY pm.person_id
        )
        SELECT
            pe.person_id,
            pe.first_name || ' ' || pe.last_name AS person_name,
            COALESCE(ah.weekly_hours, 0) AS active_hours_per_week,
            COALESCE(ah.weekly_hours, 0) > 40 AS over_40_hours
        FROM people AS pe
        LEFT JOIN active_hours AS ah
            ON pe.person_id = ah.person_id
        ORDER BY active_hours_per_week DESC, pe.person_id
    """)

    q3_workload
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Anna Chen was the only person out of 25 whose commitments across active projects exceeded 40 hours per week, at 66 hours per week.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4. Which expense categories spent more than the average category total over the last 90 days?
    """)
    return


@app.cell
def _(as_of, ask):
    q4_expenses = ask(f"""
        WITH category_totals AS (
            SELECT
                category,
                SUM(amount) AS total_spent
            FROM expenses
            WHERE expense_date BETWEEN DATE '{as_of.isoformat()}' - INTERVAL '89 days'
                                   AND DATE '{as_of.isoformat()}'
            GROUP BY category
        ),
        category_average AS (
            SELECT AVG(total_spent) AS average_category_total
            FROM category_totals
        )
        SELECT
            ct.category,
            ct.total_spent,
            ROUND(ca.average_category_total, 2) AS average_category_total
        FROM category_totals AS ct
        CROSS JOIN category_average AS ca
        WHERE ct.total_spent > ca.average_category_total
        ORDER BY ct.total_spent DESC, ct.category
    """)

    q4_expenses
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    From August 3 through October 31, 2026, GPU cloud was the only category whose total spending (37,067.30 USD) exceeded the average among categories with recorded expenses (12,272.18 USD).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 5. Which projects have no recorded expenses?
    """)
    return


@app.cell
def _(ask):
    q5_no_expenses = ask("""
        SELECT
            p.project_id,
            p.project_name
        FROM projects AS p
        WHERE NOT EXISTS (
            SELECT 1
            FROM expenses AS e
            WHERE e.project_id = p.project_id
        )
        ORDER BY p.project_id
    """)

    q5_no_expenses
    return (q5_no_expenses,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Two of the 12 projects had no recorded expenses: Client Onboarding Tool (project 11) and Supplier Data Pipeline (project 12).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6. How many tasks does each project have, and how much has it spent?
    """)
    return


@app.cell
def _(ask):
    q6_project_totals = ask("""
        WITH task_totals AS (
            SELECT project_id, COUNT(*) AS task_count
            FROM tasks
            GROUP BY project_id
        ),
        expense_totals AS (
            SELECT project_id, SUM(amount) AS total_expenses
            FROM expenses
            GROUP BY project_id
        )
        SELECT
            p.project_id,
            p.project_name,
            COALESCE(t.task_count, 0) AS task_count,
            COALESCE(e.total_expenses, 0) AS total_expenses
        FROM projects AS p
        LEFT JOIN task_totals AS t
            ON p.project_id = t.project_id
        LEFT JOIN expense_totals AS e
            ON p.project_id = e.project_id
        ORDER BY p.project_id
    """)

    q6_project_totals
    return (q6_project_totals,)


@app.cell
def _(ask, q6_project_totals):
    q6_independent = ask("""
        SELECT
            p.project_id,
            (SELECT COUNT(*)
             FROM tasks AS t
             WHERE t.project_id = p.project_id) AS task_count,
            COALESCE(
                (SELECT SUM(e.amount)
                 FROM expenses AS e
                 WHERE e.project_id = p.project_id),
                0
            ) AS total_expenses
        FROM projects AS p
        ORDER BY p.project_id
    """)

    q6_report_rows = q6_project_totals.select(
        "project_id", "task_count", "total_expenses"
    ).to_dicts()

    assert q6_report_rows == q6_independent.to_dicts(), (
        "Question 6 totals do not match the independent calculation."
    )

    q6_independent
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Across 12 projects, the report counted 300 tasks, and the task counts and expense totals matched the independent check for all 12 projects, including two with zero recorded expenses.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7. Which tasks are assigned to people who do not work on their project?
    """)
    return


@app.cell
def _(ask):
    q7_joins = """
        FROM tasks AS t
        JOIN projects AS p
            ON t.project_id = p.project_id
        LEFT JOIN people AS pe
            ON t.assignee_id = pe.person_id
        LEFT JOIN project_members AS pm
            ON t.assignee_id = pm.person_id
           AND t.project_id = pm.project_id
    """

    q7_task_check = ask(f"""
        SELECT
            t.task_id,
            p.project_name,
            pe.first_name || ' ' || pe.last_name AS assignee,
            CASE
                WHEN t.assignee_id IS NULL THEN 'Unassigned'
                WHEN pm.person_id IS NULL THEN 'Violation'
                ELSE 'Valid'
            END AS membership_check
        {q7_joins}
        ORDER BY t.task_id
    """)

    q7_task_check
    return q7_joins, q7_task_check


@app.cell
def _(q7_task_check):
    q7_violations = q7_task_check.filter(
        q7_task_check["membership_check"] == "Violation"
    )

    q7_violations
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Of the 300 tasks checked, two violated the project membership rule: tasks 299 and 300 were assigned to people who were not members of their respective project teams.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 8. How many people report directly to each manager, and how many hours per week have they committed across all projects?
    """)
    return


@app.cell
def _(ask):
    q8_manager_workload = ask("""
        WITH person_hours AS (
        SELECT
            pm.person_id,
            SUM(pm.hours_per_week) AS weekly_hours
        FROM project_members AS pm
        JOIN projects AS p
            ON p.project_id = pm.project_id
        GROUP BY pm.person_id
    )
        SELECT
            m.person_id AS manager_id,
            m.first_name || ' ' || m.last_name AS manager_name,
            COUNT(r.person_id) AS direct_reports,
            SUM(COALESCE(h.weekly_hours, 0)) AS team_hours_per_week
        FROM people AS m
        JOIN people AS r
            ON r.manager_id = m.person_id
        LEFT JOIN person_hours AS h
            ON h.person_id = r.person_id
        GROUP BY m.person_id, m.first_name, m.last_name
        ORDER BY team_hours_per_week DESC, m.person_id
    """)

    q8_manager_workload
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Across all projects, Anna Chen’s 8 direct reports committed 138 hours per week, Ben Patel’s 7 committed 104, Carla Nguyen’s 4 and Emma Lopez’s 2 each committed 10 hours as a group, and David Kim’s 2 committed 0.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 9. What percentage of completed tasks finished on time for each project category?
    """)
    return


@app.cell
def _(as_of, ask):
    q9_on_time = ask(f"""
        SELECT
            p.category AS project_category,
            COUNT(*) AS completed_tasks,
            COUNT(*) FILTER (
                WHERE t.completed_date <= t.due_date
            ) AS on_time_tasks,
            ROUND(
                100.0 * COUNT(*) FILTER (WHERE t.completed_date <= t.due_date)
                / COUNT(*),
                2
            ) AS on_time_pct
        FROM tasks AS t
        JOIN projects AS p
            ON t.project_id = p.project_id
        WHERE t.completed_date <= DATE '{as_of.isoformat()}'
        GROUP BY p.category
        ORDER BY on_time_pct DESC, project_category
    """)

    q9_on_time
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As of October 31, 2026, 76.09% of completed LLM app tasks finished on time (70 of 92), followed by internal tools at 75.64% (59 of 78) and data pipelines at 68.33% (41 of 60).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 10. Which clients account for the largest shares of the total client-project budget?
    """)
    return


@app.cell
def _(ask):
    q10_client_budget = ask("""
        WITH client_budgets AS (
            SELECT
                client_name,
                COUNT(*) AS project_count,
                SUM(budget) AS client_budget
            FROM projects
            WHERE NULLIF(TRIM(client_name), '') IS NOT NULL
            GROUP BY client_name
        )
        SELECT
            client_name,
            project_count,
            client_budget,
            ROUND(
                100.0 * client_budget / SUM(client_budget) OVER (),
                2
            ) AS share_of_client_budget_pct
        FROM client_budgets
        ORDER BY client_budget DESC, client_name
    """)

    q10_client_budget
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Harbor Foods accounted for the largest share of the 141,000 USD client-project budget, with 24,000 USD (17.02%), followed by Oak Market at 15.60% and Birch Shop at 14.18%.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## How I Know These Numbers Are Right

    **Question 6 — Tasks and spending by project.** I checked the task count and expense total for each project by querying the two source tables separately. The independent results matched both values for all 12 projects.

    **Question 5 — Projects with no expenses.** The original query looked for projects with no matching expense rows. As a second check, I used the budget report from Question 1 to find projects whose total expenses were zero. Every recorded expense is positive, so a project with a zero total has no recorded expenses.
    """)
    return


@app.cell
def _(mo, q1_budget, q5_no_expenses):
    q5_original_ids = sorted(q5_no_expenses["project_id"].to_list())

    q5_check_ids = sorted(
        q1_budget.filter(q1_budget["total_expenses"] == 0)["project_id"].to_list()
    )

    assert q5_original_ids == q5_check_ids, (
        f"Question 5 returned {q5_original_ids}, but the budget report "
        f"showed zero expenses for {q5_check_ids}."
    )

    mo.md(
        f"**Question 5 query:** {len(q5_original_ids)} projects, IDs {q5_original_ids}.  \n"
        f"**Budget report check:** {len(q5_check_ids)} projects, IDs {q5_check_ids}."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Working With the Agent

    The agent suggested using `NOT EXISTS` in the `q5_no_expenses` cell to identify projects with no recorded expenses. I verified the result in the check cell under **How I Know These Numbers Are Right** by filtering the Question 1 budget report for projects with zero total expenses. Both methods returned the same two project IDs, 11 and 12, and the assertion confirmed that the IDs matched.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading It Back
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 7 — Are any tasks assigned to people who do not work on their project?**

    According to my prediction, the joins will return **300 rows** before grouping or filtering for violations. I begin with 300 tasks, and each task belongs to exactly one project. The left joins keep tasks even if they are unassigned or their assignee is not on the project team. Each assignee–project pair can match at most one row in `project_members`, so the joins should leave me with one row per task.
    """)
    return


@app.cell
def _(ask, q7_joins):
    q7_join_count = ask(f"""
        SELECT COUNT(*) AS joined_rows
        {q7_joins}
    """)

    q7_join_count
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The joins returned 300 rows before filtering for violations, which matched my prediction. The joins kept every task, including unassigned tasks, and each assignee–project pair could match at most one membership row, so no task was duplicated.

    Each row in the final violation list represents one task assigned to someone who is not a member of that task’s project team. For example, the row for task 299 identifies the task, its project, and the assignee who was not on that project’s team.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Going Further

    I used the results from Question 1 to chart the percentage of budget spent by each project. Three projects exceeded their budgets, and Internal Expense Tracker spent the largest share of its budget at 247.37%.
    """)
    return


@app.cell
def _(q1_budget):
    import altair as alt

    q1_chart_data = alt.Data(
        values=q1_budget.select("project_name", "budget_spent_pct").to_dicts()
    )

    q1_budget_bars = alt.Chart(q1_chart_data).mark_bar().encode(
        x=alt.X("budget_spent_pct:Q", title="Budget spent (%)"),
        y=alt.Y("project_name:N", sort="-x", title="Project"),
        color=alt.condition(
            alt.datum.budget_spent_pct > 100,
            alt.value("#BB5039"),
            alt.value("#287D79"),
        ),
    )

    q1_budget_line = (
        alt.Chart(alt.Data(values=[{"budget_limit": 100}]))
        .mark_rule(color="#555555", strokeDash=[5, 4])
        .encode(x="budget_limit:Q")
    )

    (q1_budget_bars + q1_budget_line).properties(
        title="Budget spent by project",
        width=460,
        height=320,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Time Spent

    8
    """)
    return


if __name__ == "__main__":
    app.run()
