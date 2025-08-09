import os
import asyncio
from scraping.scraper import scrape_dou_async
from analysis.analyzer import load_from_json, count_tech_mentions, plot_top_tech

DATA_DIR = "data"
CHART_DIR = "charts"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CHART_DIR, exist_ok=True)


async def main():
    out_json = os.path.join(DATA_DIR, "dou_python_raw.json")
    results = await scrape_dou_async({"search": "python"}, max_pages=3, save_json=out_json)

    df = load_from_json(out_json)
    tech_counts = count_tech_mentions(df)
    print(tech_counts.head(20))

    plot_path = os.path.join(CHART_DIR, "top_tech.png")
    plot_top_tech(tech_counts, top_n=10, outpath=plot_path)


if __name__ == "__main__":
    asyncio.run(main())
