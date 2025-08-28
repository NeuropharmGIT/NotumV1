import asyncio
import os
import json
from playwright.async_api import async_playwright
from playwright_stealth.stealth import stealth

SESSION_FILE = "session.json"
DATA_DIR = "data"
OUTPUT_FILE = os.path.join(DATA_DIR, "chatgpt_conversations.jsonl")

async def authenticate_and_save_session():
    """
    Launches a browser for the user to log in manually.
    Saves the session state (cookies, etc.) to a file for future use.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Apply stealth measures to avoid detection
        await stealth(page)

        print("="*80)
        print("Une fenêtre de navigateur va s'ouvrir. Veuillez vous connecter à votre compte ChatGPT.")
        print("Une fois connecté, revenez à ce terminal et appuyez sur Entrée.")
        print("="*80)

        await page.goto("https://chat.openai.com/")

        try:
            input("Appuyez sur Entrée ici après vous être connecté dans le navigateur...")

            print("\nConnexion confirmée. Sauvegarde de la session...")

            storage_state = await context.storage_state()
            with open(SESSION_FILE, 'w') as f:
                json.dump(storage_state, f, indent=4)

            print(f"Session sauvegardée dans '{SESSION_FILE}'. Le navigateur va se fermer.")

        except Exception as e:
            print(f"\nUne erreur est survenue : {e}")
        finally:
            await browser.close()

async def scrape_conversations():
    """
    Uses a saved session to log in headlessly and scrape all conversations.
    """
    if not os.path.exists(SESSION_FILE):
        print(f"Fichier de session '{SESSION_FILE}' non trouvé. Veuillez d'abord vous authentifier.")
        return

    print("Démarrage du scraping en utilisant la session sauvegardée...")
    all_conversations = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            context = await browser.new_context(storage_state=SESSION_FILE)
            page = await context.new_page()
            await stealth(page)

            print("Connexion en cours...")
            await page.goto("https://chat.openai.com/")

            # Wait for the main page to load by checking for the prompt textarea
            await page.wait_for_selector("#prompt-textarea", timeout=60000)
            print("Connexion réussie.")

            print("Recherche des liens de conversation...")
            conv_link_selector = "a[href*='/c/']"
            await page.wait_for_selector(conv_link_selector, timeout=60000)

            conv_elements = await page.query_selector_all(conv_link_selector)
            urls = sorted(list(set([await link.get_attribute("href") for link in conv_elements])))
            print(f"Trouvé {len(urls)} liens de conversation uniques.")

            for i, url_path in enumerate(urls):
                full_url = f"https://chat.openai.com{url_path}"
                print(f"Scraping de la conversation {i+1}/{len(urls)}: {url_path}")
                await page.goto(full_url)
                await page.wait_for_selector("div[data-message-author-role]", timeout=60000)

                # Extract title and messages
                title = await page.title()
                messages = []
                message_containers = await page.query_selector_all("div[data-message-author-role]")
                for container in message_containers:
                    role = await container.get_attribute("data-message-author-role")
                    # The actual message content is inside a div that is a sibling of the author icon
                    content_div = await container.query_selector("div.prose")
                    content = await content_div.inner_text() if content_div else ""
                    messages.append({"role": role, "content": content.strip()})

                all_conversations.append({
                    "url": full_url,
                    "title": title,
                    "messages": messages
                })
                await asyncio.sleep(1) # Be respectful to the server

        except Exception as e:
            print(f"Une erreur est survenue pendant le scraping : {e}")
            print("Cela peut être dû à un changement dans l'interface de ChatGPT ou à une session expirée.")
            print("Essayez de supprimer le fichier 'session.json' et de vous ré-authentifier.")
        finally:
            await browser.close()
            print("Scraping terminé.")

    if all_conversations:
        # Ensure data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)
        print(f"Sauvegarde de {len(all_conversations)} conversations dans {OUTPUT_FILE}...")
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            for conversation in all_conversations:
                f.write(json.dumps(conversation, ensure_ascii=False) + '\n')
        print("Sauvegarde terminée.")

async def main():
    """
    Main function to orchestrate the authentication or scraping process.
    """
    if not os.path.exists(SESSION_FILE):
        await authenticate_and_save_session()
        if os.path.exists(SESSION_FILE):
            print("\nAuthentification réussie. Lancez à nouveau le script pour commencer le scraping.")
    else:
        await scrape_conversations()

if __name__ == "__main__":
    asyncio.run(main())
