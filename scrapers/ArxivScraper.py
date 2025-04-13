from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_tags_data_with_sections(url: str, tags_info: dict) -> str:
    logger.info(f"Extracting data from Arxiv URL: {url}")
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
        # Visit the webpage
        logger.info(f"Loading URL: {url}")
        driver.get(url)
        
        # Wait for the body to be fully loaded
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "content-inner"))
            )
            logger.info("Page content loaded successfully")
        except TimeoutException:
            logger.warning("Timeout waiting for page to load. Proceeding anyway.")
        
        # String to store extracted information
        extracted_data = ""

        # Extract elements by IDs
        for element_id in tags_info.get("id", []):
            try:
                element = driver.find_element(By.ID, element_id)
                extracted_data += f"ID '{element_id}': {element.text}\n"
                logger.info(f"Successfully extracted ID '{element_id}'")
            except Exception as e:
                logger.warning(f"Failed to find element with ID '{element_id}': {str(e)}")
                extracted_data += f"ID '{element_id}': Not found\n"

        # Extract elements by Classes
        for class_name in tags_info.get("class", []):
            try:
                elements = driver.find_elements(By.CLASS_NAME, class_name)
                class_data = " ".join([el.text for el in elements])
                extracted_data += f"Class '{class_name}': {class_data}\n"
                logger.info(f"Successfully extracted Class '{class_name}'")
            except Exception as e:
                logger.warning(f"Failed to find elements with Class '{class_name}': {str(e)}")
                extracted_data += f"Class '{class_name}': Not found\n"

        # Extract sections with IDs like 'sec1', 'sec2', etc.
        for _ in range(3):  # Retry mechanism to handle dynamic changes
            try:
                sections = driver.find_elements(By.TAG_NAME, "section")
                section_data = ""

                for section in sections:
                    section_id = section.get_attribute("id")
                    if section_id and section_id.startswith("sec"):
                        section_data += f"Section ID '{section_id}': {section.text}\n"

                if section_data:
                    extracted_data += section_data
                    logger.info(f"Successfully extracted {len(sections)} sections")
                break  # Exit retry loop on success

            except StaleElementReferenceException:
                logger.warning("Encountered stale element reference while locating sections. Retrying...")

        if not extracted_data.strip():
            # Fallback extraction if nothing found with the specified classes/IDs
            logger.warning("No data extracted with specified selectors. Using fallback extraction.")
            title = driver.title
            page_text = driver.find_element(By.TAG_NAME, "body").text
            extracted_data = f"Title: {title}\n\nContent: {page_text[:5000]}"
            
        logger.info(f"Extraction completed. Extracted {len(extracted_data)} characters")
        return extracted_data.strip()

    except Exception as e:
        logger.error(f"Error during extraction: {str(e)}")
        return f"Error extracting data: {str(e)}"

    finally:
        # Clean up and close the browser
        driver.quit()
        logger.info("Browser closed")



def arxiv_scrap(url):
    logger.info(f"Starting Arxiv scraping for URL: {url}")
    tags_info = {
    "id": [],
    "class": ["subheader","title ", "authors", "arxivdoi","abstract", "subjects"]
    }
    
    try:
        data = extract_tags_data_with_sections(url, tags_info)
        if not data or len(data) < 50:
            logger.warning(f"Extracted data too short or empty: {data}")
            return f"Failed to extract meaningful content from {url}"
            
        logger.info(f"Successfully scraped Arxiv URL. Data length: {len(data)}")
        return data
    except Exception as e:
        logger.error(f"Error in arxiv_scrap: {str(e)}")
        return f"Error scraping Arxiv URL: {str(e)}"


# Example Usage
# url = "https://arxiv.org/abs/2412.04454"  # Replace with the actual URL



# data = extract_tags_data_with_sections(url,tags_info)
# print(data)

