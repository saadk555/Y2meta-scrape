from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager

def get_mp3_download_link(video_url):
    chrome_options = Options()
    chrome_options.add_argument('--headless=chrome')
    chrome_options.add_argument("--window-size=1920x1080") 
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    service = Service(ChromeDriverManager().install()) # Create Service object
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("Driver initialized")

    driver.get(video_url)
    print("URL loaded")

    mp3_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Mp3")) 
    )
    print("Mp3 button found")
    driver.execute_script("arguments[0].click();", mp3_button)
    print("Mp3 button clicked")

    all_download_buttons = driver.find_elements(By.CLASS_NAME, "btn-download-size")
    print("Download buttons found")
    last_button = None
    for button in all_download_buttons:
        if button.get_attribute("data-ftype") == "mp3" and button.get_attribute("data-fquality") == "256":
            last_button = button
            break

    if last_button:
        driver.execute_script("arguments[0].click();", last_button)
        print("2nd Last button clicked")
        time.sleep(3)  
    else:
        print("Download button with specified attributes not found.")

    last_download_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-success.btn-download-link"))
    )
    print("Last download button found")

    if last_download_button: 
        download_link = last_download_button.get_attribute("href")
        print("Download link found")
        return download_link  # Return for use in the API
    else:
        print("Download button not found.")  # Indicate error in the API response
        return "Download button not found."

video_url = "https://y2meta.app/en/youtube/Etkd-07gnxM" 
result = get_mp3_download_link(video_url)
print(result) 