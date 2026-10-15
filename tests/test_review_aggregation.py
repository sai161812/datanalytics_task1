from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd

SCRIPT = Path(__file__).resolve().parents[1] / "main.py"


class ReviewAggregationTests(unittest.TestCase):
    def test_string_review_counts_are_added_numerically(self):
        data = pd.DataFrame({
            "Category": ["TOOLS", "TOOLS"],
            "Installs": ["1,000+", "2,000+"],
            "Size": ["20M", "30M"],
            "Rating": [4.5, 4.0],
            "Last Updated": ["January 1, 2020", "January 2, 2020"],
            "Reviews": ["100", "200"],
        })
        # Avoid writing a chart or opening a browser, regardless of local time.
        with patch("pandas.read_csv", return_value=data), patch("plotly.graph_objects.Figure.write_html"):
            result = runpy.run_path(str(SCRIPT))
        self.assertEqual(result["summary"]["Review_Count"].tolist(), [300])
        self.assertEqual(result["summary"]["Average_Rating"].tolist(), [4.25])
        self.assertEqual(list(result["chart"].data[1].y), [300])
