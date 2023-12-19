import asyncio
from playwright.async_api import async_playwright
import json
import fnmatch
from config import Config

enqueued_url_list = []

# Function to get page HTML
async def get_page_html(page, selector):
    await page.wait_for_selector(selector)
    element = await page.query_selector(selector)
    return await element.inner_text() if element else ""


# Crawl function
async def crawl(config):
    results = []
    queue = [config.url]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        if config.cookie:
            await page.context.add_cookies([{
                "name": config.cookie['name'], 
                "value": config.cookie['value'], "url": config.url}])

        try:
            while queue and len(results) < config.max_pages_to_crawl:
                url = queue.pop(0)
                print(f"Crawler: Crawling {url}")
                await page.goto(url)
                html = await get_page_html(page, config.selector)
                results.append({'url': url, 'html': html})
                with open(config.output_file_name, 'w') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)

                # Extract and enqueue links
                links = await page.query_selector_all("a")

                # links 去重
                links = list(set(links))  # Remove duplicate links
                
                for link in links:
                    href = await link.get_attribute("href")
                    complete_href = 'https://likegiver.com' + href if href.startswith('/') else href # process hrefs
                    if complete_href and fnmatch.fnmatch(complete_href, config.match) and complete_href not in enqueued_url_list:
                        queue.append(complete_href)
                        enqueued_url_list.append(complete_href)
                # Implement on_visit_page logic if needed
        finally:
            await browser.close()

    return results


# Main function
async def main(config):
    results = await crawl(config)
    # with open(config.output_file_name, 'w') as f:
    #     json.dump(results, f, indent=2, ensure_ascii=False)


# Running the main function
if __name__ == "__main__":
    config = Config(
        # url="https://www.laplace-ai.com/vision",
        url = "https://likegiver.com",
        match = "**/archives/**",
        # match="https://www.laplace-ai.com/intro/vision/**",
        # selector="#SITE_PAGES",
        selector="body",
        max_pages_to_crawl=100,
        output_file_name="output.json",
        # cookie={"name":"Hm_lpvt_89ea5f37167a3c99973cc9a0d687e5f5", 
        #         "value":"1702954482"}
    )
    asyncio.run(main(config))
