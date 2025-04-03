from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time
import concurrent.futures

# Initialize Flask app
app = Flask(__name__)

# Thread pool for selenium operations
executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

def create_driver():
    """Create a headless Chrome driver."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.binary_location = os.environ.get("CHROME_BINARY_PATH", "")
    
    # For Vercel serverless environment
    chrome_driver_path = os.environ.get("CHROME_DRIVER_PATH", "")
    
    if chrome_driver_path:
        service = Service(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    
    return driver

def scrape_data(driver, username, password):
    """Scrape attendance data from the website."""
    try:
        # Navigate to the site
        driver.get("http://mitsims.in/")
        
        # Click on student link
        StudentLink = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//nav//a[@id='studentLink']"))
        )
        StudentLink.click()
        
        # Enter username
        userEle = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//form[@id='studentForm']//input[@id='inputStuId']"))
        )
        userEle.clear()
        userEle.send_keys(username)
        
        # Enter password
        passEle = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//form[@id='studentForm']//input[@id='inputPassword']"))
        )
        passEle.clear()
        passEle.send_keys(password)
        
        # Click login button
        login_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//form[@id='studentForm']//button[@id='studentSubmitButton']"))
        )
        login_button.click()
        
        # Wait for page to load after login
        time.sleep(15)
        
        # Define XPaths - keeping these exactly the same as requested
        attendance_percentage_xpath = "//fieldset[contains(@class, 'bottom-border') and not(contains(@class, 'bottom-border-header'))]//div[contains(@class,'x-column-inner')]/div[contains(@class,'x-field')][5]//span"
        course_name_xpath = "//fieldset[contains(@class, 'bottom-border') and not(contains(@class, 'bottom-border-header'))]//div[contains(@class,'x-column-inner')]/div[contains(@class,'x-field')][2]//span"
        
        # Initialize lists
        attendance_percentages = []
        course_names = []
        
        # Wait for elements to be present
        wait = WebDriverWait(driver, 120)
        
        # Get percentage elements
        percentage_elements = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, attendance_percentage_xpath)))
        
        # Get course elements
        course_elements = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, course_name_xpath)))
        
        # Process percentage elements
        for element in percentage_elements:
            text_content = element.text.strip()
            try:
                percent_val = float(text_content)
                attendance_percentages.append(percent_val)
            except ValueError:
                attendance_percentages.append(0)
        
        # Process course elements
        for element in course_elements:
            course_names.append(element.text.strip())
        
        # Check if we have data
        if not attendance_percentages:
            return None
        
        # Calculate final percentage
        final_percent = round(sum(attendance_percentages) / len(attendance_percentages), 2)
        
        # Return the result
        return {
            'courses': course_names,
            'percentages': attendance_percentages,
            'attendance': final_percent
        }
    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        return None
    finally:
        # Make sure to quit the driver to free resources
        try:
            driver.quit()
        except:
            pass

def get_attendance_data(username, password):
    """Get attendance data for a user."""
    future = executor.submit(lambda: scrape_data(create_driver(), username, password))
    try:
        result = future.result()
        return result
    except Exception as e:
        print(f"Error in get_attendance_data: {str(e)}")
        return None

@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

@app.route('/get_attendance', methods=['POST'])
def attendance():
    """Handle attendance data requests."""
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    result = get_attendance_data(username, password)
    if result is not None:
        return jsonify(result)
    else:
        return jsonify({'error': 'Failed to fetch attendance data. Please try again later.'}), 500

# For local development
if __name__ == '__main__':
    app.run(debug=True)
