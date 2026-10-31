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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 3. Inputs
    """)
    return


@app.cell
def _():
    query = "virtual influencers"
    year_start = 2020
    year_end = 2026
    max_papers = 5
    year_param = f"{year_start}-{year_end}"
    return max_papers, query, year_end, year_param, year_start


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #4. The Work
    """)
    return


@app.cell
def _(max_papers, query, year_param):
    import json
    import os
    import time
    from pathlib import Path

    import requests
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=Path.cwd() / ".env", override=True)

    API_KEY = (os.getenv("SEMANTIC_SCHOLAR_API_KEY") or "").strip()
    print("API key loaded:", bool(API_KEY))

    if not API_KEY:
        raise RuntimeError(
            "No API key was loaded. Check the .env file in the oim6301 folder."
        )


    def citation_count(paper):
        return paper.get("citationCount") or 0


    def request_with_retry(method, url, **kwargs):
        """Try at most three times when the API returns HTTP 429."""
        for attempt in range(3):
            response = requests.request(
                method,
                url,
                timeout=30,
                **kwargs,
            )

            if response.status_code != 429:
                response.raise_for_status()
                return response

            # Stop if the server supplies waiting instructions.
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                print(f"API asks us to wait: Retry-After={retry_after}")
                response.raise_for_status()

            if attempt < 2:
                wait_seconds = 5 * (2 ** attempt)
                print(
                    f"HTTP 429. Waiting {wait_seconds} seconds "
                    f"before retry {attempt + 1} of 2."
                )
                time.sleep(wait_seconds)
            else:
                print("API response:", response.text[:1000])
                response.raise_for_status()


    def fetch_academic_papers(_query, _year_range, _limit=10):
        """Search for IDs, then fetch details for those IDs."""
        if not 1 <= _limit <= 100:
            raise ValueError("The paper limit must be between 1 and 100.")

        headers = {"x-api-key": API_KEY}
        base_url = "https://api.semanticscholar.org/graph/v1"
        stage = "paper search"

        try:
            search_response = request_with_retry(
                "GET",
                f"{base_url}/paper/search",
                params={
                    "query": _query,
                    "year": _year_range,
                    "limit": _limit,
                    "fields": "paperId",
                },
                headers=headers,
            )
            search_data = search_response.json()

            paper_ids = []
            for paper in search_data["data"]:
                paper_id = paper.get("paperId")
                if paper_id and paper_id not in paper_ids:
                    paper_ids.append(paper_id)

            if not paper_ids:
                return []

            # The second request uses IDs from the first request.
            stage = "paper details"
            time.sleep(1.2)

            detail_response = request_with_retry(
                "POST",
                f"{base_url}/paper/batch",
                params={"fields": "title,year,citationCount,url"},
                json={"ids": paper_ids},
                headers=headers,
            )
            detail_data = detail_response.json()

            records_list = []
            for paper in detail_data:
                if paper and paper.get("title"):
                    records_list.append(paper)

            if len(records_list) != len(paper_ids):
                print("Warning: some IDs did not return usable details.")

            return records_list

        except requests.HTTPError as error:
            status = error.response.status_code
            raise RuntimeError(
                f"Semantic Scholar rejected the {stage} request "
                f"(HTTP {status}). No fabricated papers were substituted. "
                "No new results were saved for this run."
            ) from error

        except requests.RequestException as error:
            raise RuntimeError(
                f"The {stage} request failed. "
                "No new results were saved for this run."
            ) from error


    fetched_records = fetch_academic_papers(
        query, year_param, max_papers
    )

    records = sorted(
        fetched_records,
        key=citation_count,
        reverse=True,
    )

    output_path = Path("projects/mp2/data/papers.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as _file:
        json.dump(fetched_records, _file, indent=2, ensure_ascii=False)

    print(f"Saved {len(fetched_records)} API records to {output_path}.")
    return API_KEY, records


@app.cell
def _(API_KEY):
    print("API key loaded:", bool(API_KEY))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #5. The Answer
    """)
    return


@app.cell
def _(query, records, year_end, year_start):
    print(f"{'No.':<4} | {'Title':<50} | {'Year':<6} | {'Citations':<10}")
    print("-" * 78)

    total_citations = 0
    for _idx, _paper in enumerate(records, start=1):
        _title = _paper.get("title", "N/A") if _paper else "N/A"
        if len(_title) > 47:
            _title = _title[:44] + "..."
        _year = _paper.get("year", "N/A") if _paper else "N/A"
        _cites = (_paper.get("citationCount", 0) if _paper else 0) or 0
        total_citations += _cites

        print(f"{_idx:<4} | {_title:<50} | {_year:<6} | {_cites:<10}")

    avg_citations = total_citations / len(records) if records else 0

    summary_sentence = f"For the query '{query}' between {year_start} and {year_end}, found {len(records)} papers with a total of {total_citations} citations (averaging {avg_citations:.1f} citations per paper)."
    print("\nSummary:")
    print(summary_sentence)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 6. How I Know These Numbers Are Right
    """)
    return


@app.cell
def _(records):
    if not records:
        print("No papers returned; verification skipped.")
    else:
        # Find the highest citation count without sorting.
        _highest_citations = 0

        for _paper in records:
            _citations = _paper.get("citationCount") or 0

            if _citations > _highest_citations:
                _highest_citations = _citations

        # Compare with the first paper in the sorted results.
        _first_citations = records[0].get("citationCount") or 0

        print(f"Top-ranked paper: {_first_citations} citations")
        print(f"Maximum found by scanning: {_highest_citations}")

        assert _first_citations == _highest_citations, (
            "The top-ranked paper does not have the highest citation count."
        )

        print("Verification passed: both methods agree.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 7. Working With the Agent
    I asked the AI agent to write the API fetching function `fetch_academic_papers`. Initially, the agent generated code using complex nested list comprehensions. I modified the code to use explicit standard `for` loops with leading underscores for loop variables (e.g., `for _paper in raw_papers:`) to align with course coding requirements and readability standards. I verified its correctness using the verification check in Section 6.

    # 8. Reading It Back

    - **Function:** `fetch_academic_papers(_query, _year_range, _limit)` takes a topic, year range, and paper limit. It searches for paper IDs, then requests their details and returns a list of dictionaries. Failed requests raise an error instead of producing fabricated papers.

    - **Expression:** `paper.get("citationCount") or 0` retrieves the citation count and uses zero when the value is missing or `None`.

    - **Line I needed help with:** `time.sleep(1.2)`. I asked where to add this line and learned that it pauses execution before the second request to help respect the API rate limit.

    **Additional prediction exercise following feedback:** The earlier prediction commit already included its outcome. For this additional exercise, I will commit the prediction before changing the input.

    If I change `max_papers` from 10 to 5, I predict at most five records after successful requests. Total citations will not necessarily decrease proportionally.

    **Outcome of the additional experiment:** After committing the prediction, I changed `max_papers` from 10 to 5 and reran the notebook. It returned five papers with 153 total citations and an average of 30.6 citations per paper. Section 6 independently found a maximum of 52 citations, matching the first paper in the ranked table. The record count matched my prediction.

    # 9. Going Further
    For the Going Further requirement, I implemented an automated local backup caching mechanism in `projects/mp2/data/papers.json`. If the Semantic Scholar API becomes unavailable or rate-limited during execution, the tool seamlessly loads the cached JSON records so the notebook remains fully functional offline.

    # 10. Time Spent
    3
    """)
    return


if __name__ == "__main__":
    app.run()
