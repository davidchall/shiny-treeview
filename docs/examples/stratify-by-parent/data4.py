import csv
from io import StringIO

# Sample CSV data representing an organizational chart
# In practice, this could be loaded from a file or database
csv_data = """employee_id,name,title,manager_id
1,Sarah Chen,CEO,
2,Alex Rodriguez,CTO,1
3,Maya Patel,CFO,1
4,Jordan Kim,Senior Engineer,2
5,Riley Thompson,Engineer,2
6,Casey Davis,UX Designer,2
7,Sam Wilson,Analyst,3
8,Taylor Brown,Accountant,3"""

role_icons = {
    "CEO": "👑",
    "CTO": "💻",
    "CFO": "💰",
    "Senior Engineer": "🔧",
    "Engineer": "🔧",
    "UX Designer": "🎨",
    "Analyst": "📊",
    "Accountant": "📈",
}


def read_data() -> dict[str, dict]:
    """Parse CSV data and return list of employee records with icons."""
    reader = csv.DictReader(StringIO(csv_data))

    rows = {}
    for row in reader:
        row["icon"] = role_icons.get(row["title"], "👤")
        rows[row["employee_id"]] = row

    return rows
