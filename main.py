import os
import sqlite3

from fastmcp import FastMCP

DB_PATH = os.path.join(os.path.dirname(__file__), "expense_tracker.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

mcp = FastMCP(name="Expense Tracker")


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT Default '',
                note TEXT Default ''
            )
            """)


init_db()


@mcp.tool
def add_expense(
    date: str, amount: float, category: str, subcategory: str = "", note: str = ""
):
    """
    Add a new expense to the tracker.
    - date: format must be DD/MM/YYYY (e.g. 03/04/2026)
    - amount: in rupees, e.g. 250.0
    - category: must match one of the available categories
    - subcategory: optional, for more specific classification
    - note: optional, any extra context
    """
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            """
            INSERT INTO expenses (date, amount, category, subcategory, note)
            VALUES (?, ?, ?, ?, ?)
            """,
            (date, amount, category, subcategory, note),
        )

        return {"status": "success", "id": cur.lastrowid}


@mcp.tool
def list_expenses(start_date, end_date):
    """Fetech expenses between a specific range."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "SELECT id,date,amount,category,subcategory,note FROM expenses where date between ? and ?order by id asc",
            (start_date, end_date),
        )

        cols = [col[0] for col in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


@mcp.tool
def summarize(start_date, end_date, category=None):
    """Summarize expenses by category within an inclusive date range."""
    with sqlite3.connect(DB_PATH) as conn:
        query = """
            SELECT category, SUM(amount) as TOTAL_AMOUNT from expenses
            where date between ? and ?
            """

        params = [start_date, end_date]

        if category:
            query += "AND category = ?"
            params.append(category)

        query += "GROUP by category order by category ASC"

        cur = conn.execute(query, params)

        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, c)) for c in cur.fetchall()]


@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    """Read fresh each time so you edit the file without restarting"""
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    mcp.run()
