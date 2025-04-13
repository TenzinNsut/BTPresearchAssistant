import time
import re
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def scraper(url: str):
    logger.info(f"Starting IEEE scraping for URL: {url}")
    # Initialize Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info("Successfully initialized ChromeDriver")
    except Exception as e:
        logger.error(f"Failed to initialize ChromeDriver: {str(e)}")
        # Fallback to direct initialization if webdriver-manager fails
        try:
            driver = webdriver.Chrome(options=chrome_options)
            logger.info("Initialized ChromeDriver directly")
        except Exception as e2:
            logger.error(f"Failed direct initialization: {str(e2)}")
            return f"Error initializing browser: {str(e2)}"

    try:
        logger.info(f"Loading IEEE URL: {url}")
        driver.get(url)
        
        # Wait for page to load
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            logger.info("Page content loaded successfully")
        except TimeoutException:
            logger.warning("Timeout waiting for page to load. Proceeding anyway.")
            
        elems = driver.find_elements(By.CLASS_NAME, "col-24-24")
        logger.info(f"Found {len(elems)} entries")
        
        scraped_txt = ""
        for elem in elems:
            if len(elem.text) > len(scraped_txt):
                scraped_txt = elem.text
        
        # If no good text found, try alternate methods
        if not scraped_txt or len(scraped_txt) < 100:
            logger.warning("Primary extraction method yielded insufficient data. Trying alternate methods.")
            
            # Try to get title
            try:
                title_elem = driver.find_element(By.CLASS_NAME, "document-title")
                title = title_elem.text if title_elem else "Unknown Title"
            except:
                title = driver.title
            
            # Try to get abstract
            try:
                abstract_elem = driver.find_elements(By.XPATH, "//div[contains(@class, 'abstract') or @id='abstract']")
                abstract = "\n".join([a.text for a in abstract_elem if a.text]) if abstract_elem else ""
            except:
                abstract = ""
            
            # Try to get content sections
            try:
                sections = driver.find_elements(By.TAG_NAME, "section")
                content = "\n\n".join([s.text for s in sections if len(s.text) > 50])
            except:
                content = ""
            
            scraped_txt = f"Title: {title}\n\nAbstract: {abstract}\n\n{content}"
            
        logger.info(f"Extracted {len(scraped_txt)} characters of text")
        
        # Process the text into a structured format if possible
        result = store(scraped_txt)
        return result
        
    except Exception as e:
        logger.error(f"Error during IEEE scraping: {str(e)}")
        return f"Error scraping IEEE URL: {str(e)}"
        
    finally:
        time.sleep(1)
        driver.close()
        logger.info("Browser closed")


def store(txt: str):
    try:
        lst = txt.split(sep="\n")
        logger.info(f"Processing {len(lst)} lines of text")
        
        # Prepare a more resilient processing method
        result = {
            "Title": "",
            "Authors": "",
            "Abstract": "",
            "Keywords": "",
            "Content": ""
        }
        
        # Try to extract structured data
        try:
            if len(lst) > 1:
                result["Title"] = lst[0]
                
            for i, line in enumerate(lst):
                if "Abstract" in line and i < len(lst)-1:
                    result["Abstract"] = lst[i+1] if i+1 < len(lst) else ""
                if "Author" in line or "AUTHORS" in line:
                    result["Authors"] = line.replace("Authors:", "").strip()
                if "Keyword" in line or "KEYWORDS" in line:
                    result["Keywords"] = line.replace("Keywords:", "").strip()
        except Exception as e:
            logger.warning(f"Error during structured extraction: {str(e)}")
            
        # Fallback to raw text if structured extraction fails
        if not result["Title"] and not result["Abstract"]:
            result["Content"] = txt[:5000]  # Limit to first 5000 chars
            
        # Format as a string for return
        formatted_txt = f"Title: {result['Title']}\n\nAuthors: {result['Authors']}\n\nAbstract: {result['Abstract']}\n\nKeywords: {result['Keywords']}\n\nContent: {result['Content']}"
        logger.info("Successfully processed IEEE paper data")
        return formatted_txt
        
    except Exception as e:
        logger.error(f"Error processing IEEE paper data: {str(e)}")
        # Return raw text if processing fails
        return f"Title: IEEE Paper\n\nContent: {txt[:5000]}"


def ieee_scrap(url):
    logger.info(f"IEEE scraper called for URL: {url}")
    try:
        data = scraper(url)
        if not data or len(data) < 50:
            logger.warning(f"Extracted data too short or empty")
            return f"Failed to extract meaningful content from {url}"
        
        logger.info(f"Successfully scraped IEEE URL. Data length: {len(data)}")
        return data
    except Exception as e:
        logger.error(f"Error in ieee_scrap: {str(e)}")
        return f"Error scraping IEEE URL: {str(e)}"


# URL = "https://ieeexplore.ieee.org/document/4460684"
# scraper(URL)
# print("\n\n Document2:\n")
# URL = "https://ieeexplore.ieee.org/document/9497989"
# scraper(URL)
# print("Program end.")