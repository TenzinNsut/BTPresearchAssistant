from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

def extract_tags_data_with_sections(url: str, tags_info: dict) -> str:

    # Initialize Selenium WebDriver
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Visit the webpage
        driver.get(url)
        
        # Wait for the body to be fully loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "content-inner"))
        )
        
        # String to store extracted information
        extracted_data = ""

        # Extract elements by IDs
        for element_id in tags_info.get("id", []):
            try:
                element = driver.find_element(By.ID, element_id)
                extracted_data += f"ID '{element_id}': {element.text}\n"
            except Exception:
                extracted_data += f"ID '{element_id}': Not found\n"

        # Extract elements by Classes
        for class_name in tags_info.get("class", []):
            try:
                elements = driver.find_elements(By.CLASS_NAME, class_name)
                class_data = " ".join([el.text for el in elements])
                extracted_data += f"Class '{class_name}': {class_data}\n"
            except Exception:
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
                break  # Exit retry loop on success

            except StaleElementReferenceException:
                print("Encountered stale element reference while locating sections. Retrying...")

        return extracted_data.strip()

    finally:
        # Clean up and close the browser
        driver.quit()




# Example Usage
# url = "https://arxiv.org/abs/2412.04454"  # Replace with the actual URL



def arxiv_scrap(url):
    tags_info = {
    "id": [],
    "class": ["subheader","title ", "authors", "arxivdoi","abstract", "subjects"]
    }
    data = extract_tags_data_with_sections(url,tags_info)
    print(data)
    return data


# data = extract_tags_data_with_sections(url,tags_info)
# print(data)

