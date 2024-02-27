from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService  # Updated import
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_mp3_download_link(video_url):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    driver.get(video_url)

    # Click the First "Mp3" button using JavaScript
    mp3_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Mp3")) 
    )
    driver.execute_script("arguments[0].click();", mp3_button)


     # Find the 2nd download button 
    all_download_buttons = driver.find_elements(By.CLASS_NAME, "btn-download-size")
    last_button = None
    for button in all_download_buttons:
        if button.get_attribute("data-ftype") == "mp3" and button.get_attribute("data-fquality") == "256":
            last_button = button
            break

    # Click the 2nd last download button using JavaScript (if found)
    if last_button:
        driver.execute_script("arguments[0].click();", last_button)
        time.sleep(3)  
    else:
        print("Download button with specified attributes not found.")

    # Click the last download button using JavaScript
    last_download_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-success.btn-download-link"))
    )
    #driver.execute_script("arguments[0].click();", last_download_button)  

    # Extract the download link (if the button exists)
    if last_download_button: 
        download_link = last_download_button.get_attribute("href")
        print("Download Link:", download_link)
    else:
        print("Download button with specified attributes not found.")
    
    return download_link

    driver.quit()  

# Example usage
