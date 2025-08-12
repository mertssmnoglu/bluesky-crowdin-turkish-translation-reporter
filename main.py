import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from typing import Optional, Dict
from dotenv import load_dotenv

from config import Config
from type import CheckResult
from notification import notify_discord_webhook

load_dotenv()
config = Config(discord_webhook_url=os.environ.get("DISCORD_WEBHOOK_URL"))


class BlueskyCrowdinScraper:
    def __init__(self):
        """Initialize the Bluesky Crowdin scraper with Firefox WebDriver."""
        self.driver: Optional[webdriver.Firefox] = None
        self.wait: Optional[WebDriverWait] = None
        self.setup_driver()

    def setup_driver(self):
        """Setup Firefox WebDriver with appropriate options."""
        firefox_options = Options()
        firefox_options.add_argument("--headless")  # Run in background
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--window-size=1920,1080")

        # Use system geckodriver (make sure it's installed)
        self.driver = webdriver.Firefox(options=firefox_options)
        self.wait = WebDriverWait(self.driver, 20)

    def scrape_turkish_translation_stats(self):
        """Scrape Turkish translation statistics from Bluesky Crowdin page."""
        if not self.driver or not self.wait:
            raise RuntimeError("WebDriver not properly initialized")

        # Bluesky Turkish translation page URL
        url = "https://bluesky.crowdin.com/bluesky-social"

        try:
            print(f"Navigating to: {url}")
            self.driver.get(url)

            # Wait for page to load
            time.sleep(5)

            # XPath selectors for the translation statistics
            translated_percent_xpath = "/html/body/div[4]/div[1]/div/div[3]/div[2]/div[1]/div[1]/div[2]/div/div[44]/div[3]/span[1]"
            approved_percent_xpath = "/html/body/div[4]/div[1]/div/div[3]/div[2]/div[1]/div[1]/div[2]/div/div[44]/div[3]/span[3]"
            words_to_translate_xpath = "/html/body/div[4]/div[1]/div/div[3]/div[2]/div[1]/div[1]/div[2]/div/div[44]/div[4]"

            results = {}

            # Get translated percentage
            try:
                translated_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, translated_percent_xpath))
                )
                results["translated_percent"] = translated_element.text.strip()
                print(f"✓ Found translated percentage: {results['translated_percent']}")
            except Exception as e:
                print(f"✗ Could not find translated percentage: {e}")
                results["translated_percent"] = "Not found"

            # Get approved percentage
            try:
                approved_element = self.driver.find_element(
                    By.XPATH, approved_percent_xpath
                )
                results["approved_percent"] = approved_element.text.strip()
                print(f"✓ Found approved percentage: {results['approved_percent']}")
            except Exception as e:
                print(f"✗ Could not find approved percentage: {e}")
                results["approved_percent"] = "Not found"

            # Get words to translate
            try:
                words_element = self.driver.find_element(
                    By.XPATH, words_to_translate_xpath
                )
                results["words_to_translate"] = words_element.text.strip()
                print(f"✓ Found words to translate: {results['words_to_translate']}")
            except Exception as e:
                print(f"✗ Could not find words to translate: {e}")
                results["words_to_translate"] = "Not found"

            return results

        except Exception as e:
            print(f"Error during scraping: {e}")
            return None

    def close(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def check_results(results: Dict[str, str]) -> CheckResult:
    """
    check_results is a function that checks the results dict
    Returns:
        True, if all strings are translated and approved
        False, otherwise
    """

    return CheckResult(
        translated_percent=results["translated_percent"],
        approved_percent=results["approved_percent"],
        words_to_translate=results["words_to_translate"],
        is_there_a_job=not validate_results(results),
    )


def validate_results(results: Dict[str, str]) -> bool:
    """
    validate_results is a function that validates the CheckResult object
    Returns:
        True, if all strings are translated and approved
        False, otherwise
    """

    return (
        results["translated_percent"] == "100%" and results["approved_percent"] == "100%"
    )


def main():
    """Main function to run the Bluesky Crowdin scraper."""
    print("🚀 Starting Bluesky Crowdin Turkish Translation Scraper")
    print("=" * 60)

    try:
        with BlueskyCrowdinScraper() as scraper:
            results = scraper.scrape_turkish_translation_stats()

            if results:
                print("\n📊 BLUESKY TURKISH TRANSLATION STATISTICS")
                print("=" * 60)
                print(f"📈 Translated Percentage: {results['translated_percent']}")
                print(f"✅ Approved Percentage:  {results['approved_percent']}")
                print(f"📝 Words to Translate:   {results['words_to_translate']}")
                print("=" * 60)
                check_result = check_results(results)
                if check_result.is_there_a_job:
                    print("Translation job found.")
                    notify_discord_webhook(check_result, config.discord_webhook_url)
                else:
                    print("No translation job found.")
            else:
                print("❌ Failed to scrape translation statistics")

    except Exception as e:
        print(f"❌ Application error: {e}")


if __name__ == "__main__":
    main()
