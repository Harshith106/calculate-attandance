from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def get_attendance_data(username, password):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-running-insecure-content")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("http://mitsims.in/")
        time.sleep(2)
        
        student_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//nav//a[@id='studentLink']")))
        student_link.click()
        
        username_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//form[@id='studentForm']//input[@id='inputStuId']")))
        username_field.send_keys(username)
        
        password_field = driver.find_element(By.XPATH, "//form[@id='studentForm']//input[@id='inputPassword']")
        password_field.send_keys(password)
        
        login_button = driver.find_element(By.XPATH, "//form[@id='studentForm']//button[@id='studentSubmitButton']")
        login_button.click()
        
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x-fieldset-body')]")))
        
        subject_rows = driver.find_elements(By.XPATH, "//fieldset[contains(@class, 'x-fieldset') and not(contains(@id, 'fieldset-1129')) and not(contains(@id, 'fieldset-1219'))]")
        
        attended = []
        conducted = []
        
        for row in subject_rows:
            try:
                attended_elems = row.find_elements(By.XPATH, ".//div[contains(@class, 'x-form-item')][3]//span[contains(@style, 'padding')]")
                conducted_elems = row.find_elements(By.XPATH, ".//div[contains(@class, 'x-form-item')][4]//span[contains(@style, 'padding')]")
                
                if attended_elems:
                    attended_val = attended_elems[0].text.strip()
                    attended.append(int(attended_val) if attended_val else 0)
                else:
                    attended.append(0)
                
                if conducted_elems:
                    conducted_val = conducted_elems[0].text.strip()
                    conducted.append(int(conducted_val) if conducted_val else 0)
                else:
                    conducted.append(0)
                    
            except Exception:
                attended.append(0)
                conducted.append(0)
                continue
                
        return attended, conducted
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return [], []
    finally:
        driver.quit()

def calculate_attendance():
    username = "YOUR_USERNAME"
    password = "YOUR_PASSWORD"
    
    attended, conducted = get_attendance_data(username, password)
    
    if attended and conducted:
        total_attended = sum(attended)
        total_conducted = sum(conducted)
        percentage = (total_attended / total_conducted) * 100 if total_conducted > 0 else 0
        
        print("Attended Classes:", attended)
        print("Total Conducted:", conducted)
        print(f"\nTotal Attended: {total_attended}")
        print(f"Total Conducted: {total_conducted}")
        print(f"Attendance Percentage: {percentage:.2f}%")
    else:
        print("Failed to retrieve attendance data")

get_attendance_data("22691A0572", "ph2241484@gmail.com")
