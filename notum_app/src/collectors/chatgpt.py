import asyncio
from playwright.async_api import async_playwright
import json

SESSION_FILE = "session.json"

async def authenticate():
    """
    Launches a headed browser for the user to log in to ChatGPT manually.
    Saves the session state to a file after successful login.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("="*80)
        print("A browser window will be opened. Please log in to your ChatGPT account.")
        print("After you have successfully logged in, this script will automatically detect it,")
        print("save your session, and close the browser. Please do not close it manually.")
        print("="*80)

        await page.goto("https://chat.openai.com/")

        # This is a selector for the main prompt input area, a reliable indicator of being logged in.
        login_success_selector = "#prompt-textarea"

        try:
            # The script will now pause here until you press Enter in the console.
            input("Please log in to the browser window, solve any CAPTCHAs, and then press Enter here to continue...")

            print("\nLogin confirmation received. Saving session state...")

            # Save storage state to the file.
            storage_state = await context.storage_state()
            with open(SESSION_FILE, 'w') as f:
                json.dump(storage_state, f, indent=4)

            print(f"Session state saved to '{SESSION_FILE}'. The browser will now close.")

        except Exception as e:
            print(f"\nAn error occurred or the login was not completed in time: {e}")
        finally:
            await browser.close()

import os

async def scrape_conversations():
    """
    Launches a headless browser using a saved session state,
    and scrapes all conversations from the user's account.
    """
    if not os.path.exists(SESSION_FILE):
        print(f"Session file '{SESSION_FILE}' not found. Please run the authentication first.")
        return []

    all_conversations = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=SESSION_FILE)
        page = await context.new_page()

        print("Logging in using saved session...")
        await page.goto("https://chat.openai.com/")

        try:
            # Wait for the main page to load after login
            await page.wait_for_selector("#prompt-textarea", timeout=60000)
            print("Login successful.")

            print("Finding conversation links...")
            # This selector targets the links in the conversation history sidebar.
            conv_link_selector = "a[href*='/c/']"
            await page.wait_for_selector(conv_link_selector, timeout=60000)

            conv_links = await page.query_selector_all(conv_link_selector)
            urls = [await link.get_attribute("href") for link in conv_links]
            # Remove duplicates and sort
            urls = sorted(list(set(urls)))
            print(f"Found {len(urls)} unique conversation links.")

            for i, url in enumerate(urls):
                full_url = f"https://chat.openai.com{url}"
                print(f"Scraping conversation {i+1}/{len(urls)}: {url}")
                await page.goto(full_url)
                # Wait for the first message to ensure the conversation is loaded
                await page.wait_for_selector("div[data-message-author-role]", timeout=60000)

                conversation_data = {
                    "url": full_url,
                    "title": await page.title(),
                    "messages": []
                }

                message_containers = await page.query_selector_all("div[data-message-author-role]")
                for container in message_containers:
                    role = await container.get_attribute("data-message-author-role")
                    # The actual text content is within a div that contains prose.
                    content_divs = await container.query_selector_all("div.prose > div")
                    content = "\n".join([await div.inner_text() for div in content_divs])

                    conversation_data["messages"].append({
                        "role": role,
                        "content": content.strip()
                    })
                all_conversations.append(conversation_data)
                # Be a polite scraper
                await asyncio.sleep(1)

        except Exception as e:
            print(f"An error occurred during scraping: {e}")
            print("It's possible the page structure has changed or there was a network issue.")
        finally:
            await browser.close()
            print("Scraping finished.")

            if all_conversations:
                output_file = "notum_app/data/chatgpt_conversations.jsonl"
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                print(f"Saving {len(all_conversations)} conversations to {output_file}...")
                with open(output_file, 'w', encoding='utf-8') as f:
                    for conversation in all_conversations:
                        f.write(json.dumps(conversation, ensure_ascii=False) + '\n')
                print("Save complete.")

            return all_conversations

async def main():
    """Helper function to run the authentication or scraping process directly for testing."""
    if not os.path.exists(SESSION_FILE):
        print("Session file not found. Starting authentication process.")
        await authenticate()
    else:
        print("Session file found. To test scraping, you would call scrape_conversations().")
        # Example of how to run the scraper for testing (commented out by default)
        # conversations = await scrape_conversations()
        # if conversations:
        #     print(f"Successfully scraped {len(conversations)} conversations.")
        #     # print("Sample:", conversations[0])


if __name__ == "__main__":
    # This allows running the module by itself for testing.
    asyncio.run(main())
