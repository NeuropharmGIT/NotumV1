import asyncio
import os
import json
from playwright.async_api import async_playwright
from playwright_stealth.stealth import stealth

SESSION_FILE = "session.json"
OUTPUT_FILE = "chatgpt_conversations.jsonl"

async def authenticate():
    """
    Launches a headed browser for the user to log in to ChatGPT manually.
    Saves the session state to a file after successful login.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await stealth(page)

        print("="*80)
        print("A browser window will be opened. Please log in to your ChatGPT account.")
        print("After you have successfully logged in, please press Enter in this terminal.")
        print("="*80)

        await page.goto("https://chat.openai.com/")

        try:
            input("Please log in to the browser window, solve any CAPTCHAs, and then press Enter here to continue...")

            print("\nLogin confirmation received. Saving session state...")

            storage_state = await context.storage_state()
            with open(SESSION_FILE, 'w') as f:
                json.dump(storage_state, f, indent=4)

            print(f"Session state saved to '{SESSION_FILE}'. The browser will now close.")

        except Exception as e:
            print(f"\nAn error occurred during the authentication process: {e}")
        finally:
            await browser.close()


async def scrape_conversations():
    """
    Launches a headless browser using a saved session to scrape conversations.
    """
    if not os.path.exists(SESSION_FILE):
        print(f"Session file '{SESSION_FILE}' not found. Please run authentication first.")
        return

    all_conversations = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=SESSION_FILE)
        page = await context.new_page()

        await stealth(page)

        print("\nLogging in using saved session...")
        await page.goto("https://chat.openai.com/")

        try:
            await page.wait_for_selector("#prompt-textarea", timeout=60000)
            print("Login successful.")

            print("Finding conversation links...")
            conv_link_selector = "a[href*='/c/']"
            await page.wait_for_selector(conv_link_selector, timeout=60000)

            conv_links = await page.query_selector_all(conv_link_selector)
            urls = sorted(list(set([await link.get_attribute("href") for link in conv_links])))
            print(f"Found {len(urls)} unique conversation links.")

            for i, url in enumerate(urls):
                full_url = f"https://chat.openai.com{url}"
                print(f"Scraping conversation {i+1}/{len(urls)}: {url}")
                await page.goto(full_url)
                await page.wait_for_selector("div[data-message-author-role]", timeout=60000)

                conversation_data = {
                    "url": full_url, "title": await page.title(), "messages": []
                }

                message_containers = await page.query_selector_all("div[data-message-author-role]")
                for container in message_containers:
                    role = await container.get_attribute("data-message-author-role")
                    content_divs = await container.query_selector_all("div.prose > div")
                    content = "\n".join([await div.inner_text() for div in content_divs])
                    conversation_data["messages"].append({"role": role, "content": content.strip()})
                all_conversations.append(conversation_data)
                await asyncio.sleep(1)

        except Exception as e:
            print(f"\nAn error occurred during scraping: {e}")
        finally:
            await browser.close()
            print("Scraping finished.")

            if all_conversations:
                print(f"Saving {len(all_conversations)} conversations to {OUTPUT_FILE}...")
                with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                    for conversation in all_conversations:
                        f.write(json.dumps(conversation, ensure_ascii=False) + '\n')
                print("Save complete.")
            else:
                print("No conversations were saved.")

async def main():
    """
    Main orchestration function.
    """
    if not os.path.exists(SESSION_FILE):
        await authenticate()
    else:
        print("Session file found, proceeding directly to scrape.")

    await scrape_conversations()

if __name__ == "__main__":
    print("--- Starting Notum ChatGPT Scraper ---")
    asyncio.run(main())
    print("--- Scraper Finished ---")
