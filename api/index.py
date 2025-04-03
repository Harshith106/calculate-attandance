from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time, concurrent.futures

# Initialize Flask app and thread pool
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

# XPaths - keeping these exactly the same as requested
XPATHS = {
    'student_link': "//nav//a[@id='studentLink']",
    'username_field': "//form[@id='studentForm']//input[@id='inputStuId']",
    'password_field': "//form[@id='studentForm']//input[@id='inputPassword']",
    'login_button': "//form[@id='studentForm']//button[@id='studentSubmitButton']",
    'attendance': "//fieldset[contains(@class, 'bottom-border') and not(contains(@class, 'bottom-border-header'))]//div[contains(@class,'x-column-inner')]/div[contains(@class,'x-field')][5]//span",
    'course': "//fieldset[contains(@class, 'bottom-border') and not(contains(@class, 'bottom-border-header'))]//div[contains(@class,'x-column-inner')]/div[contains(@class,'x-field')][2]//span"
}

def create_driver():
    """Create a headless Chrome driver."""
    options = webdriver.ChromeOptions()
    for arg in ["--headless", "--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage",
               "--disable-extensions", "--disable-infobars", "--disable-notifications"]:
        options.add_argument(arg)

    options.binary_location = os.environ.get("CHROME_BINARY_PATH", "")
    chrome_driver_path = os.environ.get("CHROME_DRIVER_PATH", "")

    return webdriver.Chrome(
        service=webdriver.chrome.service.Service(executable_path=chrome_driver_path) if chrome_driver_path else None,
        options=options
    )

def scrape_data(driver, username, password):
    """Scrape attendance data from the website."""
    try:
        # Navigate and login
        driver.get("http://mitsims.in/")

        # Click student link
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, XPATHS['student_link']))).click()

        # Enter username
        user_field = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, XPATHS['username_field'])))
        user_field.clear()
        user_field.send_keys(username)

        # Enter password
        pass_field = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, XPATHS['password_field'])))
        pass_field.clear()
        pass_field.send_keys(password)

        # Click login
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, XPATHS['login_button']))).click()

        # Wait for page load
        time.sleep(15)

        # Get data with long wait
        wait = WebDriverWait(driver, 120)
        percentage_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, XPATHS['attendance'])))
        course_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, XPATHS['course'])))

        # Process data
        attendance_percentages = []
        for element in percentage_elements:
            try:
                attendance_percentages.append(float(element.text.strip()))
            except ValueError:
                attendance_percentages.append(0)

        course_names = [element.text.strip() for element in course_elements]

        # Return results if we have data
        if not attendance_percentages:
            return None

        return {
            'courses': course_names,
            'percentages': attendance_percentages,
            'attendance': round(sum(attendance_percentages) / len(attendance_percentages), 2)
        }
    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        return None
    finally:
        try:
            driver.quit()
        except:
            pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health_check():
    return jsonify({'status': 'ok', 'message': 'Service is running'})

@app.route('/get_attendance', methods=['POST'])
def attendance():
    username, password = request.form.get('username'), request.form.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Get data using thread pool
    result = executor.submit(lambda: scrape_data(create_driver(), username, password)).result()

    return jsonify(result) if result else jsonify(
        {'error': 'Failed to fetch attendance data. Please try again later.'}), 500

# For local development
if __name__ == '__main__':
    app.run(debug=True)
