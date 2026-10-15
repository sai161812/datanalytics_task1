# App Category Analysis (Time-Restricted Visualization)

This project analyzes mobile app data to compare average ratings and total review counts across the top 10 app categories by number of installs.

The visualization is conditionally generated and available only between **3:00 PM and 5:00 PM IST**, as per project requirements.

## Features
- Data cleaning and normalization
- Filtering based on rating, app size, and update month
- Category-level aggregation
- Grouped bar chart visualization
- Time-based access restriction (IST)
- HTML output using Plotly

## Tech Stack
- Python
- Pandas
- Plotly
- pytz

## How to Run
```bash
pip install -r requirements.txt
python app.py

## Check numeric aggregation

Run `python -m unittest discover -s tests -v` after installing `requirements.txt`. The regression fixture uses string-valued review counts, as occurs when a malformed CSV row forces the source column to object dtype. The expected category total is arithmetic addition (`100 + 200 = 300`), not string concatenation (`100200`).

The existing 3–5 PM IST generation window remains in place. The regression check bypasses chart-file writes; it does not validate the dataset, ranking criteria, or access controls.
