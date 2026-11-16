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


if __name__ == "__main__":
    app.run()
