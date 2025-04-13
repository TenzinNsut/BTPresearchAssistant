from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
from bs4 import BeautifulSoup
import logging
import requests
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def universal_scraper(url):
    """
    A universal scraper that can extract content from any research paper website.
    Falls back to different extraction methods if one fails.
    """
    # Try multiple extraction methods in order of preference
    result = None
    
    # First try direct request with BeautifulSoup (fastest)
    try:
        result = extract_with_requests(url)
        if is_valid_content(result):
            logger.info("Successfully extracted content using requests/BeautifulSoup")
            return result
    except Exception as e:
        logger.warning(f"Request-based extraction failed: {str(e)}")
    
    # Then try Selenium with headless browser (more powerful)
    try:
        result = extract_with_selenium(url)
        if is_valid_content(result):
            logger.info("Successfully extracted content using Selenium")
            return result
    except Exception as e:
        logger.warning(f"Selenium-based extraction failed: {str(e)}")
    
    # Finally try our specialized extractors
    try:
        result = extract_with_site_specific_method(url)
        if is_valid_content(result):
            logger.info("Successfully extracted content using site-specific extractor")
            return result
    except Exception as e:
        logger.warning(f"Site-specific extraction failed: {str(e)}")
    
    # If all methods fail, try to extract minimal info from URL
    try:
        paper_id = extract_paper_id_from_url(url)
        if paper_id:
            return f"Title: Research Paper {paper_id}\nAbstract: Could not extract content from URL. Using minimal information derived from URL.\nPaper ID: {paper_id}"
    except:
        pass
        
    # If all methods fail, return an error message
    logger.error(f"All extraction methods failed for URL: {url}")
    return f"Failed to extract content from {url}. Please check if the URL is valid and accessible."


def extract_with_requests(url):
    """Extract content using simple requests and BeautifulSoup"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # Raise exception for 4XX/5XX responses
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract title
    title = soup.find('title').get_text() if soup.find('title') else ""
    
    # Extract main content
    content = ""
    
    # Try to find abstract
    abstract_candidates = [
        soup.find('div', {'id': 'abstract'}),
        soup.find('section', {'id': 'abstract'}),
        soup.find('div', {'class': 'abstract'}),
        soup.find(string=re.compile(r'Abstract')),
        soup.find('p', string=re.compile(r'Abstract'))
    ]
    
    abstract = next((c.get_text() for c in abstract_candidates if c), "")
    
    # Try to find main content sections
    main_content_tags = [
        # Common content containers
        soup.find('div', {'id': 'content'}),
        soup.find('div', {'id': 'main-content'}),
        soup.find('div', {'id': 'body'}),
        soup.find('article'),
        # For when specific sections don't exist, get all paragraphs
        [p.get_text() for p in soup.find_all('p') if len(p.get_text()) > 100]
    ]
    
    main_content = ""
    for tag in main_content_tags:
        if tag:
            if isinstance(tag, list):
                main_content = " ".join(tag)
            else:
                main_content = tag.get_text()
            break
    
    # Combine all extracted content
    content = f"Title: {title}\n\nAbstract: {abstract}\n\n{main_content}"
    return content


def extract_with_selenium(url):
    """Extract content using Selenium for JavaScript-heavy sites"""
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize the driver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Load the page
        driver.get(url)
        
        # Wait for page to load (adjust timeout as needed)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Let JavaScript execute fully
        time.sleep(3)
        
        # Get the page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract title
        title = driver.title
        
        # Extract specific elements that might contain research content
        content_elements = []
        
        # Try to find abstract section
        abstract_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Abstract') or @id='abstract' or contains(@class, 'abstract')]")
        if abstract_elements:
            for element in abstract_elements:
                content_elements.append(f"Abstract: {element.text}")
        
        # Try to find main content sections (looking for common patterns in research papers)
        section_elements = driver.find_elements(By.TAG_NAME, "section")
        for section in section_elements:
            content_elements.append(section.text)
        
        # Try to find div elements with significant text (typical for content)
        divs = driver.find_elements(By.TAG_NAME, "div")
        for div in divs:
            if len(div.text) > 200:  # Only include divs with substantial text
                content_elements.append(div.text)
        
        # Combine all content
        full_content = f"Title: {title}\n\n" + "\n\n".join(content_elements[:10])  # Limit to first 10 sections to avoid too much noise
        
        return full_content
    
    finally:
        driver.quit()


def extract_with_site_specific_method(url):
    """Extract content using site-specific selectors"""
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # Initialize the driver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Load the page
        driver.get(url)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Extract based on the domain
        domain = extract_domain(url)
        
        if "arxiv.org" in domain:
            # Specialized extraction for ArXiv
            title = get_element_text(driver, By.CLASS_NAME, "title")
            authors = get_element_text(driver, By.CLASS_NAME, "authors")
            abstract = get_element_text(driver, By.CLASS_NAME, "abstract")
            content = f"Title: {title}\nAuthors: {authors}\nAbstract: {abstract}"
            
        elif "sciencedirect.com" in domain:
            # Specialized extraction for ScienceDirect
            title = get_element_text(driver, By.CLASS_NAME, "publication-title")
            authors = get_element_text(driver, By.CLASS_NAME, "author-group")
            abstract = get_element_text(driver, By.CLASS_NAME, "abstract")
            content = f"Title: {title}\nAuthors: {authors}\nAbstract: {abstract}"
            
        elif "ieee.org" in domain:
            # Specialized extraction for IEEE
            title = get_element_text(driver, By.CLASS_NAME, "document-title")
            authors = get_element_text(driver, By.CLASS_NAME, "authors-accordion-container")
            abstract = get_element_text(driver, By.CLASS_NAME, "abstract-text")
            content = f"Title: {title}\nAuthors: {authors}\nAbstract: {abstract}"
            
        else:
            # Generic extraction for other domains
            # Get the page title
            title = driver.title
            
            # Try to find abstract and sections
            content_elements = []
            
            # Look for elements with specific keywords in their IDs or classes
            for keyword in ["abstract", "introduction", "method", "result", "conclusion", "discussion"]:
                elements = driver.find_elements(By.XPATH, f"//*[contains(@id, '{keyword}') or contains(@class, '{keyword}')]")
                for element in elements:
                    if element.text and len(element.text) > 50:
                        content_elements.append(f"{keyword.capitalize()}: {element.text}")
            
            content = f"Title: {title}\n\n" + "\n\n".join(content_elements)
        
        return content
    
    finally:
        driver.quit()


def get_element_text(driver, by, value):
    """Helper function to get text from an element safely"""
    try:
        element = driver.find_element(by, value)
        return element.text
    except NoSuchElementException:
        return ""


def extract_domain(url):
    """Extract the domain from a URL"""
    match = re.search(r'https?://([^/]+)', url)
    if match:
        return match.group(1)
    return ""


def is_valid_content(content):
    """Check if the extracted content is valid and substantial"""
    if not content or len(content) < 100:
        return False
    
    # Check if content has some structure (title, abstract, etc.)
    if not any(keyword in content.lower() for keyword in ["title", "abstract", "introduction"]):
        return False
    
    return True


def extract_paper_id_from_url(url):
    """Extract a paper ID from the URL if possible"""
    try:
        # For arXiv URLs
        if "arxiv.org" in url:
            import re
            match = re.search(r'arxiv.org/abs/(\d+\.\d+)', url)
            if match:
                return match.group(1)
        
        # For DOI URLs
        if "doi.org" in url:
            import re
            match = re.search(r'doi.org/(.+)$', url)
            if match:
                return match.group(1)
                
        # Extract any sequence that looks like a paper ID
        import re
        match = re.search(r'((?:\d+\.?\d+)|(?:[A-Z]\d+[A-Z0-9]+))', url)
        if match:
            return match.group(1)
    except:
        pass
    
    return None 