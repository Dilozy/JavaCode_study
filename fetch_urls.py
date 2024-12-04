import asyncio
import json

import aiohttp

from aiohttp.client_exceptions import ClientConnectorDNSError

semaphore = asyncio.Semaphore(5)

urls = [
    'https://example.com',
    'https://httpbin.org/status/404',
    'https://nonexistent.url',
    'http://example.org',
    'http://example.net',
    'http://example.edu',
    'http://example.gov',
    'http://example.co',
]


async def fetch(url: str, session: aiohttp.client.ClientSession):
    try:
        async with session.get(url) as response:
            return {"url": url, "status_code": response.status}
    except ClientConnectorDNSError:
        return {"url": url, "status_code": 0}
    except asyncio.TimeoutError:
        return {"url": url, "status_code": 408}


async def fetch_all_urls(urls: list[str], file_path: str) -> None:
    timeout = aiohttp.ClientTimeout(connect=3)

    async with semaphore:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            result = [await fetch(url, session) for url in urls]

    with open(file_path, "w", encoding="utf-8") as output_file:
        json.dump(result, output_file, indent=4)


if __name__ == "__main__":
    asyncio.run(fetch_all_urls(urls, "urls.json"))
