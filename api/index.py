from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures
import atexit
import os
import time
import traceback

app = Flask(__name__)
CORS(app)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

def cleanup():
    executor.shutdown(wait=False)
atexit.register(cleanup)

def is_vercel_env():
    """Check if we're running on Vercel."""
    return 'VERCEL' in os.environ

def create_driver():
    """Create a headless Chrome driver with optimized settings."""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-features=site-per-process")
        options.add_argument("--single-process")
        options.add_argument("--disable-application-cache")
        options.add_argument("--js-flags=--max_old_space_size=128")

        # Set Chrome binary location if specified in environment
        chrome_binary = os.environ.get("CHROME_BINARY_PATH")
        if chrome_binary:
            options.binary_location = chrome_binary

        # Create driver with ChromeDriver path from environment if available
        chrome_driver_path = os.environ.get("CHROME_DRIVER_PATH")
        if chrome_driver_path:
            service = webdriver.chrome.service.Service(executable_path=chrome_driver_path)
            driver = webdriver.Chrome(service=service, options=options)
        else:
            # Try to create driver without explicit path
            driver = webdriver.Chrome(options=options)

        # Set timeouts
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)
        return driver
    except Exception as e:
        print(f"Error creating Chrome driver: {str(e)}")
        traceback.print_exc()
        raise

def scrape_data(driver, username, password):
    try:
        driver.get("http://mitsims.in/")

        StudentLink = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//nav//a[@id='studentLink']"))
        )
        StudentLink.click()

        userEle = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//form[@id='studentForm']//input[@id='inputStuId']"))
        )
        userEle.clear()
        userEle.send_keys(username)

        passEle = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//form[@id='studentForm']//input[@id='inputPassword']"))
        )
        passEle.clear()
        passEle.send_keys(password)

        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//form[@id='studentForm']//button[@id='studentSubmitButton']"))
        )
        login_button.click()

        time.sleep(10)

        attendance_percentage_xpath = "//fieldset[contains(@class, 'bottom-border') and not(contains(@class, 'bottom-border-header'))]//div[contains(@class,'x-column-inner')]/div[contains(@class,'x-field')][5]//span"
        course_name_xpath = "//fieldset[contains(@class, 'bottom-border') and not(contains(@class, 'bottom-border-header'))]//div[contains(@class,'x-column-inner')]/div[contains(@class,'x-field')][2]//span"

        attendance_percentages = []
        course_names = []

        wait = WebDriverWait(driver, 30)
        percentage_elements = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, attendance_percentage_xpath))
        )
        course_elements = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, course_name_xpath))
        )

        for element in percentage_elements:
            text_content = element.text.strip()
            try:
                percent_val = float(text_content)
                attendance_percentages.append(percent_val)
            except ValueError:
                pass

        for element in course_elements:
            course_names.append(element.text.strip())

        if not attendance_percentages:
            return None

        final_percent = round(sum(attendance_percentages) / len(attendance_percentages), 2)

        return {
            'courses': course_names,
            'percentages': attendance_percentages,
            'attendance': final_percent
        }
    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        traceback.print_exc()
        return None
    finally:
        try:
            driver.quit()
        except Exception as e:
            print(f"Error quitting driver: {str(e)}")

def get_attendance_data(username, password):
    print(f"Starting attendance data retrieval for user: {username}")
    future = executor.submit(lambda: scrape_data(create_driver(), username, password))

    try:
        result = future.result(timeout=45)
        return result
    except concurrent.futures.TimeoutError:
        future.cancel()
        import gc
        gc.collect()
        return None
    except Exception as e:
        print(f"Unexpected error in get_attendance_data: {str(e)}")
        traceback.print_exc()
        import gc
        gc.collect()
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health_check():
    return jsonify({'status': 'ok', 'message': 'Service is running'})

@app.route('/get_attendance', methods=['POST', 'GET'])
def attendance():
    """Handle attendance data requests with support for both GET and POST."""
    # Handle GET requests (for preflight checks)
    if request.method == 'GET':
        return jsonify({'message': 'Please use POST method with username and password'}), 200

    # Handle POST requests
    try:
        # Try to get data from different sources
        username = None
        password = None

        # Try JSON data
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

        # Try form data
        if not username or not password:
            username = request.form.get('username')
            password = request.form.get('password')

        # Try URL parameters
        if not username or not password:
            username = request.args.get('username')
            password = request.args.get('password')

        # Validate credentials
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        # Get attendance data
        result = get_attendance_data(username, password)

        # Return the result
        if result:
            return jsonify(result)
        else:
            return jsonify({'error': 'Failed to fetch attendance data. Please try again later.'}), 500
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
