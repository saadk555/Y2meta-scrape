from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


def get_mp3_downloads(video_url):
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:\\Users\\dell\\SeleniumProjects\\automation_profile")  # Your Selenium profile path
    prefs = {"download.default_directory": "D:\\Downloads"}  # Your desired download path
    options.add_experimental_option("prefs", prefs)
    options = webdriver.ChromeOptions()  # Use EdgeOptions() for Edge
    driver = webdriver.Chrome(options=options) 
    driver.get(video_url)

    try:       
        # Handle initial redirection ads (Repeated Attempts)
        for _ in range(5): 
            time.sleep(2) 
            potential_ad_elements = driver.find_elements(By.TAG_NAME, "iframe") 
            for element in potential_ad_elements:
                try:
                    driver.switch_to.frame(element)
                    close_button = driver.find_element(By.CSS_SELECTOR, "button.close")  # Adjust selector
                    close_button.click()
                except:
                    pass  
                finally:
                    driver.switch_to.default_content()  
                

        # Click the "Mp3" button 
        mp3_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Mp3")) 
        )
        mp3_button.click()

        # Find the last download button with the desired attributes
        all_download_buttons = driver.find_elements(By.CLASS_NAME, "btn-download-size")
        last_button = None
        for button in all_download_buttons:
            if button.get_attribute("data-ftype") == "mp3" and button.get_attribute("data-fquality") == "256":
                last_button = button
                break

        if last_button:
            last_button.click()
            time.sleep(3)  # Optional pause after clicking if needed
        else:
            print("Download button with specified attributes not found.")


        button = driver.find_element(By.CSS_SELECTOR, "a.btn.btn-success.btn-download-link")
       # driver.execute_script("arguments[0].click();", button)
        if button:
            download_link = button.get_attribute("href")
            print("Download Link:", download_link)
        else:
            print("Download button with specified attributes not found.")

    except Exception as e:
        print("An error occurred:", e)
    finally:
        time.sleep(10) 
        driver.quit()

# Example usage
video_url = "https://y2meta.app/en/youtube/6TbG2EJITQY"  
get_mp3_downloads(video_url)
