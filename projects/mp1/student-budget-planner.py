# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of option, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


app._unparsable_cell(
    r"""
    This tool is designed for students who aim to have a cost-effective budget plan for their academic year. This way can help them make informed decisions about their expenses, savings, and overall financial management during their studies.
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


app._unparsable_cell(
    r"""
    The ways I solve it is through those 6 main steps (with its purposes):
    + Step 1: Monthly budget => To calculate the amount of money that students have per month.
    + Step 2: Monthly expenses in different types => To calculate the expenses in each type of expenditure, know what the students spent more or less.
    + Step 3: The sum of all monthly expenses => To know exactly the total amount of expenses monthly.
    + Step 4: Calculate remaining budget => To know exactly what the amount of the remaining budget is.
    + Step 5: Calculate percentage of budget used => To understand the percentage use of the budget monthly.
    + Step 6: Display results and budget warning + Smart Budget Recommendations to help students make better financial decisions.
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    For the Student Budget Planner, it is important to let the loop carry running total of expenses from one step to the next.
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    In section 6, I will calculate the total expenses using a loop and independently verify the result using Python's sum() function.
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your option from the Mini Project 1 page. If you chose D, your own option, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    # Student Monthly Budget Planner - Inputs

    monthly_budget = 2000

    expenses = {
        "Rent": 1000,
        "Food": 350,
        "Transportation": 100,
        "Entertainment": 150,
        "Other": 100
    }
    # Additional input for Section 8
    savings_goal = 500
    return expenses, monthly_budget, savings_goal


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(expenses):
    #Step 3: Calculate total expenses using a loop 
    total_expenses = 0

    for category, amount in expenses.items():
        total_expenses += amount
        print(f"{category}: ${amount}")

    print(f"Total Expenses: ${total_expenses}")
    return (total_expenses,)


@app.cell
def _(monthly_budget, total_expenses):

    # Step 4: Calculate remaining budget

    remaining_budget = monthly_budget - total_expenses

    print(f"Monthly Budget: ${monthly_budget}")
    print(f"Total Expenses: ${total_expenses}")
    print(f"Remaining Budget: ${remaining_budget}")

    return (remaining_budget,)


@app.cell
def _(monthly_budget, total_expenses):

    # Step 5: Calculate percentage of budget used

    if monthly_budget > 0:
        budget_used_percentage = (total_expenses / monthly_budget) * 100
    else:
        budget_used_percentage = 0

    print(f"Budget Used: {budget_used_percentage:.1f}%")

    return (budget_used_percentage,)


@app.cell
def _(budget_used_percentage):

    # Step 6: Display results and budget warning + Smart Budget Recommendations

    if budget_used_percentage > 100:
        budget_status = "Over budget"
        advice = "Warning! You have exceeded your monthly budget."

    elif budget_used_percentage > 80:
        budget_status = "High spending"
        advice = "Consider reducing non-essential expenses."

    elif budget_used_percentage > 50:
        budget_status = "Moderate spending"
        advice = "Monitor your expenses carefully."

    else:
        budget_status = "Low spending"
        advice = "You have plenty of budget remaining."

    print(f"Budget Status: {budget_status}")
    print(f"Advice: {advice}")

    return advice, budget_status


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(
    advice,
    budget_status,
    budget_used_percentage,
    monthly_budget,
    remaining_budget,
    total_expenses,
):

    # Section 5: Student Budget Planner - Results

    print("STUDENT MONTHLY BUDGET PLANNER")
    print("-" * 45)
    print(f"{'Metric':<25} {'Result':>15}")
    print("-" * 45)

    print(f"{'Monthly Budget':<25} ${monthly_budget:>14,.2f}")
    print(f"{'Total Expenses':<25} ${total_expenses:>14,.2f}")
    print(f"{'Remaining Budget':<25} ${remaining_budget:>14,.2f}")
    print(f"{'Budget Used':<25} {budget_used_percentage:>14.1f}%")
    print(f"{'Budget Status':<25} {budget_status:>15}")

    print("-" * 45)
    print(f"Recommendation: {advice}")

    return


app._unparsable_cell(
    r"""
    Conclusion
    With a monthly budget of $2,000 and total expenses of $1,700, the student has $300 remaining (15% of the budget), but should consider reducing non-essential expenses because 85% of the monthly budget has already been used.
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(expenses, total_expenses):

    # Section 6: Verify total expenses independently

    # Method 1: Total calculated using a for loop
    loop_total = total_expenses

    # Method 2: Total calculated using sum()
    sum_total = sum(expenses.values())

    # Compare the two results
    print(f"Total using for loop: ${loop_total}")
    print(f"Total using sum(): ${sum_total}")

    if loop_total == sum_total:
        print("Verification successful! Both totals match.")
    else:
        print("Warning! The two totals do not match.")
    assert total_expenses == sum(expenses.values())

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


app._unparsable_cell(
    r"""
    At first, the AI agent had a basic suggestion related to budget warning system. It is only classified as "Within budget" or "Over budget". However, I wanted the tool to provide a more detailed and thoughtful financial guidnace before students exceeded their budgets.

    I applied different spending thresholds (50%, 80%, and 100%) to distinguish between low, moderate, high, and excessive spending.

    I believe that this shift is ideal for the students to raise their awareness of the importance of managing a cost-effective spending behavior. I checked the updated logic using my example, where $1,700 in expenses out of a $2,000 budget represents 85% usage and triggers a "High spending" warning.

    This improvement can be found in Section 4, Step 6 - Smart Budget Recommendations.
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell
def _(remaining_budget, savings_goal):

    # Section 8: Going Further - Savings Goal Simulator



    current_savings = remaining_budget

    additional_savings_needed = max(
        0, savings_goal - current_savings
    )

    print("SAVINGS GOAL SIMULATOR")
    print("-" * 40)
    print(f"Monthly Savings Goal: ${savings_goal}")
    print(f"Current Savings: ${current_savings}")
    print(f"Additional Savings Needed: ${additional_savings_needed}")

    if additional_savings_needed > 0:
        print(f"Recommendation: Reduce expenses by ${additional_savings_needed} to reach your goal.")
    else:
        print("Congratulations! You have reached your savings goal.")

    return


app._unparsable_cell(
    r"""
    In my opinion, the Student Budget Planner will be more efficient when it has a simulator that can help students determine how much they need to reduce their expenses to achieve a monthly savings target.

    I introduced a $500 monthly savings goal and compared it with the remaining budget calculated earlier. With a $2,000 monthly budget and $1,700 in expenses, the students has $300 remaining and needs to reduce expenses by an additional $200 to reach the savings goal.

    The new feature is implemented in the code cell under Section 8 - Going Further. It helps provide an actionable recommendation beyond simply tracking expenses.
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
