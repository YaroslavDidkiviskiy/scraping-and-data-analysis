# DOU Python Job Market Analysis

![Python Technologies in Job Market](charts/top_tech.png)

This project analyzes Python-related job vacancies from DOU.ua to identify the most in-demand technologies in the Ukrainian job market.

## Features

- **Web Scraping**: Asynchronously collects Python job listings from DOU.ua
- **Technology Analysis**: Identifies and counts mentions of key technologies
- **Data Visualization**: Generates visual reports of top technologies
- **Customizable**: Easily modify search parameters and technology keywords

## Requirements

- Python 3.8+
- aiohttp
- beautifulsoup4
- pandas
- matplotlib

## Installation

```bash
git clone https://github.com/YaroslavDidkiviskiy/scraping-and-data-analysis.git
cd scraping-and-data-analysis
pip install -r requirements.txt
Usage
Run the main analysis pipeline:

bash
python main.py
Customize search parameters (in config.py):

python
# Search parameters for DOU.ua
BASE_URL = "https://jobs.dou.ua"
SEARCH_PATH = "/vacancies"
DEFAULT_SEARCH_PARAMS = {
    "category": "Python",
    "search": ""
}
REQUEST_DELAY = 1.5  # seconds between requests
MAX_PAGES = 5  # maximum pages to scrape

# Technology keywords to track
TECH_KEYWORDS = [
    "Django", "Flask", "FastAPI", "asyncio", "aiohttp",
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLAlchemy",
    "Docker", "Kubernetes", "AWS", "Azure", "GCP",
    "pandas", "numpy", "scikit-learn", "PyTorch", "TensorFlow",
    "RabbitMQ", "Celery", "REST", "GraphQL"
]
View results:

Raw job data: data/dou_python_raw.json

Technology analysis: console output

Visualization: charts/top_tech.png

Project Structure
text
scraping-and-data-analysis/
├── analysis/
│   ├── analyzer.py       # Data analysis and visualization
│   └── __init__.py
├── scraping/
│   ├── scraper.py        # Async web scraper
│   └── __init__.py
├── config.py             # Configuration parameters
├── main.py               # Main execution script
├── requirements.txt      # Dependencies
└── README.md             # Project documentation
Example Output
Top technologies from recent analysis:

Technology	Count
AWS	11
Docker	10
PostgreSQL	9
FastAPI	7
Redis	6
Azure	6
GCP	6
Django	5
Kubernetes	5
REST	5
Contributing
Contributions are welcome! Please open an issue to discuss your ideas before submitting a pull request.
