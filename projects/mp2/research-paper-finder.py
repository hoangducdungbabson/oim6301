import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Research Paper Finder

    ## 1. The Question
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This tool helps academic researchers and graduate students quickly identify and prioritize key research literature on a specific topic (e.g., 'virtual influencers') within a chosen time window (2020–2026). It queries the Semantic Scholar API to fetch published papers, retrieve their detailed citation metrics and metadata, and compile a ranked reading list. This enables researchers to make data-backed decisions on which articles to read first without manually searching academic databases.
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    I will open the Semantic Scholar Academic Graph API documentation and inspect the JSON responses for the search and detail endpoints.

    My step-by-step logic:
    1. Define query parameters (query term, year range, limit) in the Inputs section.
    2. Make an initial HTTP GET request to search for papers matching the topic and year filter.
    3. Extract the list of paper IDs returned from the search request.
    4. Make a second request to fetch detailed records (title, year, citationCount, url).
    5. Parse the returned JSON records into a list of Python dictionaries using standard for loops.
    6. Sort and filter the results by citation count or publication year.
    7. Format and display a formatted table using print() and summary statistics via f-strings.
    8. Save the raw fetched records to projects/mp2/data/papers.json so the notebook can load offline.

    Answers to required planning questions:
    - **Which functions will your tool need? For each, what goes in and what comes out?**
      - `fetch_academic_papers(query, year_range, limit)`: Inputs = search query, year range string, limit integer. Output = list of paper dictionaries with paper details.
    - **Which addresses will they request?**
      - `https://api.semanticscholar.org/graph/v1/paper/search` and `https://api.semanticscholar.org/graph/v1/paper/batch`
    - **How will you know you have every record?**
      - The API response contains total matching count; I verify my fetched list length matches min(total, limit).
    - **Which check will you use in section 6, and which two numbers should agree?**
      - The total citation sum calculated in Section 5 will match an independent recalculation loop in Section 6.
    """)
    return


if __name__ == "__main__":
    app.run()
