from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import concurrent.futures
import atexit
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

# Rate limiting to prevent abuse
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Thread pool for selenium operations
executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

# Cleanup function
def cleanup():
    executor.shutdown(wait=False)

atexit.register(cleanup)

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Use environment variable for Chrome binary if available
    chrome_binary = os.environ.get('CHROME_BIN')
    if chrome_binary:
        options.binary_location = chrome_binary

    try:
        # First try with ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        app.logger.warning(f"ChromeDriverManager failed: {str(e)}")
        try:
            # Fallback to direct Chrome driver
            driver = webdriver.Chrome(options=options)
        except Exception as e2:
            app.logger.error(f"All Chrome driver methods failed: {str(e2)}")
            raise

    return driver

def scrape_data(driver, username, password):
    try:
        driver.get("http://mitsims.in/")
        StudentLink = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//nav//a[@id='studentLink']"))
        )
        StudentLink.click()

        userEle = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//form[@id='studentForm']//input[@id='inputStuId']"))
        )
        userEle.send_keys(username)

        passEle = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//form[@id='studentForm']//input[@id='inputPassword']"))
        )
        passEle.send_keys(password)

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//form[@id='studentForm']//button[@id='studentSubmitButton']"))
        )
        login_button.click()

        attendance_percentage_xpath = "//fieldset[contains(@class, 'bottom-border') and not(contains(@class, 'bottom-border-header'))]//div[contains(@class,'x-column-inner')]/div[contains(@class,'x-field')][5]//span"
        course_name_xpath = "//fieldset[contains(@class, 'bottom-border') and not(contains(@class, 'bottom-border-header'))]//div[contains(@class,'x-column-inner')]/div[contains(@class,'x-field')][2]//span"

        attandance_percentages = []
        course_names = []

        wait = WebDriverWait(driver, 10)
        percentage_elements = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, attendance_percentage_xpath)))
        course_elements = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, course_name_xpath)))

        for element in percentage_elements:
            text_content = element.text.strip()
            try:
                percent_val = float(text_content)
                attandance_percentages.append(percent_val)
            except ValueError:
                attandance_percentages.append(0)

        for element in course_elements:
            course_names.append(element.text.strip())

        if not attandance_percentages:
            return None

        final_percent = round(sum(attandance_percentages) / len(attandance_percentages), 2)
        return {
            'courses': course_names,
            'percentages': attandance_percentages,
            'attendance': final_percent
        }
    except Exception as e:
        app.logger.error(f"Error during scraping: {str(e)}")
        return None
    finally:
        driver.quit()

def get_attendance_data(username, password):
    future = executor.submit(lambda: scrape_data(create_driver(), username, password))
    try:
        return future.result(timeout=60)  # 1 minute timeout
    except concurrent.futures.TimeoutError:
        app.logger.error("Scraping operation timed out")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_attendance', methods=['POST', 'OPTIONS'])
@limiter.limit("10 per minute")
def attendance():
    # Handle OPTIONS request for CORS preflight
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        return response

    # Handle POST request
    if request.method == 'POST':
        # Check if the request is form data or JSON
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.form.get('username')
            password = request.form.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        result = get_attendance_data(username, password)
        if result is not None:
            return jsonify(result)
        else:
            return jsonify({'error': 'Failed to fetch attendance data. Please try again later.'}), 500

# Health check endpoint for monitoring
@app.route('/health')
def health_check():
    return jsonify({'status': 'ok', 'message': 'Service is running'})

# Catch-all route to handle undefined routes
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({'error': f'The requested URL /{path} was not found on this server'}), 404

if __name__ == '__main__':
    # Use environment variables for host and port if available
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, threaded=True, debug=debug)