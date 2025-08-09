import re
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from config import TECH_KEYWORDS


def load_from_json(path):
    return pd.read_json(path)


def count_tech_mentions(df, tech_keywords=TECH_KEYWORDS):
    counts = Counter()
    # Create a regex pattern for all keywords
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, tech_keywords)) + r')\b', re.IGNORECASE)

    for desc in df["description"].fillna("").astype(str):
        # Find all matches in the description
        matches = pattern.findall(desc)
        for match in matches:
            # Normalize to lowercase for counting
            counts[match.lower()] += 1

    res = pd.DataFrame([
        {"tech": k, "count": counts[k.lower()]}
        for k in tech_keywords
    ])
    res = res.sort_values("count", ascending=False).reset_index(drop=True)
    return res


def plot_top_tech(df_counts, top_n=10, outpath="charts/top_tech.png"):
    top = df_counts.head(top_n)
    plt.figure(figsize=(10, 6))
    # Use horizontal bar plot with sorted values
    ax = top.sort_values("count").plot.barh(x="tech", y="count", legend=False)
    ax.set_xlabel("Count of vacancies mentioning the technology")
    ax.set_title(f"Top {top_n} Python Technologies (DOU)")
    plt.tight_layout()
    plt.savefig(outpath)
    print("Saved chart:", outpath)
    plt.close()
