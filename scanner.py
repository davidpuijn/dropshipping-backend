import httpx, time, asyncio

API_KEY = "MY_SECRET_API_KEY"
websites_to_check = ["cheaplightingshop.com", "superfurniturestore.net"]
ANALYZE_URL = "https://dropshipping-backend.onrender.com/analyze"
REPORT_URL = "https://dropshipping-backend.onrender.com/report"

async def scan_websites():
    async with httpx.AsyncClient() as client:
        for site in websites_to_check:
            response = await client.post(ANALYZE_URL,
                headers={"x-api-key": API_KEY},
                json={"url": site, "text": "shipping from china aliexpress 2-4 weeks"}
            )
            data = response.json()
            if data.get("status") == "dropshipping":
                await client.post(REPORT_URL,
                    headers={"x-api-key": API_KEY},
                    json={"url": site, "status": "dropshipping"}
                )
                print(f"Gerapporteerd: {site}")
            time.sleep(2)

if __name__ == "__main__":
    asyncio.run(scan_websites())