# scraping/scraper.py
import asyncio
from urllib.parse import urljoin, urlencode
import aiohttp
from bs4 import BeautifulSoup
import json
from config import BASE_URL, SEARCH_PATH, DEFAULT_SEARCH_PARAMS, REQUEST_DELAY, MAX_PAGES

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PythonScript/1.0; +https://example.com)"
}


def build_search_url(params):
    qs = urlencode(params)
    return f"{BASE_URL}{SEARCH_PATH}?{qs}"


async def fetch(session, url):
    async with session.get(url, headers=HEADERS, timeout=15) as response:
        response.raise_for_status()
        return await response.text()


def parse_list_page(html):
    soup = BeautifulSoup(html, "lxml")
    links = []
    for a in soup.select("a.vt, a.job-link, a[href*='/jobs/']"):
        href = a.get("href")
        if href:
            links.append(href)
    unique = []
    for l in links:
        if l not in unique:
            unique.append(l)
    return unique


def parse_vacancy_page(html, url):
    soup = BeautifulSoup(html, "lxml")

    title_tag = soup.select_one("h1")
    title = title_tag.get_text(strip=True) if title_tag else ""

    company = ""
    comp_tag = soup.select_one(".company .company-name, .company a, a.company")
    if comp_tag:
        company = comp_tag.get_text(strip=True)

    city = ""
    city_tag = soup.select_one(".place, .location")
    if city_tag:
        city = city_tag.get_text(strip=True)

    salary = ""
    specific_salary = soup.select_one(".salary, .vacancy-salary")
    if specific_salary:
        salary = specific_salary.get_text(strip=True)
    else:
        salary_tag = soup.find(lambda tag: tag and tag.name in ["p", "div", "span"] and
                                           (tag.get_text().strip().startswith('$') or '₴' in tag.get_text()))
        if salary_tag:
            salary = salary_tag.get_text(strip=True)

    desc = ""
    desc_tag = soup.select_one(".job, .vacancy .description, .b-post__content, .article-body")
    if desc_tag:
        desc = desc_tag.get_text("\n", strip=True)
    else:
        paragraphs = soup.select("div")
        if paragraphs:
            best = max(paragraphs, key=lambda p: len(p.get_text(strip=True)))
            desc = best.get_text("\n", strip=True)

    date = ""
    date_tag = soup.select_one("time, .date, .published")
    if date_tag:
        date = date_tag.get("datetime") or date_tag.get_text(strip=True)

    return {
        "url": url,
        "title": title,
        "company": company,
        "city": city,
        "salary": salary,
        "date": date,
        "description": desc
    }


async def process_vacancy(session, url, semaphore, delay):
    async with semaphore:
        try:
            html = await fetch(session, url)
            item = parse_vacancy_page(html, url)
            await asyncio.sleep(delay)
            return item
        except Exception as e:
            print(f"Error processing {url}: {e}")
            return None


async def scrape_dou_async(search_params=None, max_pages=MAX_PAGES, delay=REQUEST_DELAY, save_json=None,
                           concurrency=10):
    params = DEFAULT_SEARCH_PARAMS.copy()
    if search_params:
        params.update(search_params)

    results = []
    seen_urls = set()
    semaphore = asyncio.Semaphore(concurrency)

    async with aiohttp.ClientSession() as session:
        for page in range(1, max_pages + 1):
            params["page"] = page
            url = build_search_url(params)
            print(f"Fetching page {page}: {url}")
            try:
                html = await fetch(session, url)
            except Exception as e:
                print(f"Page error: {e}")
                break

            links = parse_list_page(html)
            if not links:
                print("No vacancies found")
                break

            tasks = []
            for link in links:
                full_url = urljoin(BASE_URL, link)
                if full_url in seen_urls:
                    continue
                seen_urls.add(full_url)
                tasks.append(process_vacancy(session, full_url, semaphore, delay))

            page_results = await asyncio.gather(*tasks)
            for res in page_results:
                if res:
                    results.append(res)

            print(f"Processed page {page}: {len(links)} vacancies")

    if save_json:
        with open(save_json, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(results)} vacancies to {save_json}")

    return results


if __name__ == "__main__":
    asyncio.run(scrape_dou_async(
        {"search": "python"},
        max_pages=2,
        save_json="data/dou_python_raw.json"
    ))
