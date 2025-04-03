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
import time

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
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",  # Use memory storage to avoid warnings
    storage_options={"ignore_errors": True}
)

# Thread pool for selenium operations - reduce max_workers to save memory
executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

# Cleanup function
def cleanup():
    executor.shutdown(wait=False)

atexit.register(cleanup)

def create_driver():
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--log-level=3")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-popup-blocking")
            # Memory optimization
            options.add_argument("--js-flags=--max_old_space_size=128")
            options.add_argument("--disable-features=site-per-process")
            options.add_argument("--single-process")
            options.add_argument("--disable-application-cache")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            # Disable images to save memory
            prefs = {
                "profile.managed_default_content_settings.images": 2,
                "profile.default_content_setting_values.notifications": 2,
                "profile.managed_default_content_settings.stylesheets": 2,
                "profile.managed_default_content_settings.cookies": 2,
                "profile.managed_default_content_settings.javascript": 1,
                "profile.managed_default_content_settings.plugins": 2,
                "profile.managed_default_content_settings.popups": 2,
                "profile.managed_default_content_settings.geolocation": 2,
                "profile.managed_default_content_settings.media_stream": 2,
            }
            options.add_experimental_option("prefs", prefs)

            chrome_binary = os.environ.get('CHROME_BIN')
            if chrome_binary:
                options.binary_location = chrome_binary

            # Try different methods to get a working ChromeDriver
            try:
                # Method 1: Try our custom ChromeDriver installer
                try:
                    from chromedriver_installer import install_chromedriver
                    driver_path = install_chromedriver()
                    if driver_path and os.path.exists(driver_path):
                        app.logger.info(f"Using custom installed ChromeDriver at: {driver_path}")
                        service = Service(driver_path)
                        driver = webdriver.Chrome(service=service, options=options)
                        return driver
                except Exception as custom_err:
                    app.logger.warning(f"Custom ChromeDriver installer failed: {str(custom_err)}")

                # Method 2: Try ChromeDriverManager
                driver_path = ChromeDriverManager().install()
                app.logger.info(f"ChromeDriverManager installed driver at: {driver_path}")

                # Check if it's the THIRD_PARTY_NOTICES file
                if "THIRD_PARTY_NOTICES" in driver_path:
                    driver_dir = os.path.dirname(driver_path)
                    # Look for the actual chromedriver executable in the same directory
                    for root, _, files in os.walk(os.path.dirname(driver_dir)):
                        for file in files:
                            if file.startswith("chromedriver") and not file.endswith(".zip") and "THIRD_PARTY_NOTICES" not in file:
                                driver_path = os.path.join(root, file)
                                if os.path.exists(driver_path):
                                    app.logger.info(f"Found actual ChromeDriver at: {driver_path}")
                                    # Make executable on Linux
                                    if os.name != 'nt':
                                        os.chmod(driver_path, 0o755)
                                    break

                # Try to use the driver path
                service = Service(driver_path)
                driver = webdriver.Chrome(service=service, options=options)
                app.logger.info("Successfully created Chrome driver")
                return driver

            except Exception as driver_err:
                app.logger.warning(f"Standard ChromeDriver methods failed: {str(driver_err)}")

                # Method 3: Try direct Chrome driver
                try:
                    app.logger.info("Trying direct Chrome driver")
                    driver = webdriver.Chrome(options=options)
                    return driver
                except Exception as direct_err:
                    app.logger.warning(f"Direct Chrome driver failed: {str(direct_err)}")

                # Method 4: Try common locations on Linux
                if os.name != 'nt':  # Linux
                    for path in ["/usr/bin/chromedriver", "/usr/local/bin/chromedriver"]:
                        if os.path.exists(path):
                            try:
                                app.logger.info(f"Trying chromedriver at {path}")
                                service = Service(path)
                                driver = webdriver.Chrome(service=service, options=options)
                                return driver
                            except Exception as path_err:
                                app.logger.warning(f"Failed with path {path}: {str(path_err)}")

                raise Exception("All ChromeDriver methods failed")

        except Exception as e:
            retry_count += 1
            app.logger.error(f"Driver creation attempt {retry_count} failed: {str(e)}")

            if retry_count == max_retries:
                raise

            # Wait before retrying
            time.sleep(1)

def scrape_data(driver, username, password):
    try:
        # Set page load timeout to prevent hanging
        driver.set_page_load_timeout(30)

        # Set script timeout
        driver.set_script_timeout(30)

        # Reduce wait time to prevent timeouts
        short_wait = 5
        medium_wait = 10

        # Clear cookies and cache before starting
        driver.delete_all_cookies()

        # Navigate to the site
        app.logger.info("Navigating to website")
        driver.get("http://mitsims.in/")

        # Click on student link
        app.logger.info("Clicking student link")
        StudentLink = WebDriverWait(driver, short_wait).until(
            EC.element_to_be_clickable((By.XPATH, "//nav//a[@id='studentLink']"))
        )
        StudentLink.click()

        # Enter username
        app.logger.info("Entering username")
        userEle = WebDriverWait(driver, short_wait).until(
            EC.element_to_be_clickable((By.XPATH, "//form[@id='studentForm']//input[@id='inputStuId']"))
        )
        userEle.clear()
        userEle.send_keys(username)

        # Enter password
        app.logger.info("Entering password")
        passEle = WebDriverWait(driver, short_wait).until(
            EC.element_to_be_clickable((By.XPATH, "//form[@id='studentForm']//input[@id='inputPassword']"))
        )
        passEle.clear()
        passEle.send_keys(password)

        # Click login button
        app.logger.info("Clicking login button")
        login_button = WebDriverWait(driver, short_wait).until(
            EC.element_to_be_clickable((By.XPATH, "//form[@id='studentForm']//button[@id='studentSubmitButton']"))
        )
        login_button.click()

        # Define XPaths - keeping these exactly the same as requested
        attendance_percentage_xpath = "//fieldset[contains(@class, 'bottom-border') and not(contains(@class, 'bottom-border-header'))]//div[contains(@class,'x-column-inner')]/div[contains(@class,'x-field')][5]//span"
        course_name_xpath = "//fieldset[contains(@class, 'bottom-border') and not(contains(@class, 'bottom-border-header'))]//div[contains(@class,'x-column-inner')]/div[contains(@class,'x-field')][2]//span"

        # Initialize lists
        attandance_percentages = []
        course_names = []

        # Wait for elements to be present
        app.logger.info("Waiting for attendance data to load")
        wait = WebDriverWait(driver, medium_wait)

        # Get percentage elements
        app.logger.info("Getting percentage elements")
        percentage_elements = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, attendance_percentage_xpath)))

        # Get course elements
        app.logger.info("Getting course elements")
        course_elements = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, course_name_xpath)))

        # Process percentage elements
        app.logger.info(f"Processing {len(percentage_elements)} percentage elements")
        for element in percentage_elements:
            text_content = element.text.strip()
            try:
                percent_val = float(text_content)
                attandance_percentages.append(percent_val)
            except ValueError:
                attandance_percentages.append(0)

        # Process course elements
        app.logger.info(f"Processing {len(course_elements)} course elements")
        for element in course_elements:
            course_names.append(element.text.strip())

        # Check if we have data
        if not attandance_percentages:
            app.logger.warning("No attendance percentages found")
            return None

        # Calculate final percentage
        final_percent = round(sum(attandance_percentages) / len(attandance_percentages), 2)
        app.logger.info(f"Final attendance percentage: {final_percent}%")

        # Return the result
        return {
            'courses': course_names,
            'percentages': attandance_percentages,
            'attendance': final_percent
        }
    except TimeoutException as te:
        app.logger.error(f"Timeout during scraping: {str(te)}")
        return None
    except Exception as e:
        app.logger.error(f"Error during scraping: {str(e)}")
        return None
    finally:
        # Make sure to quit the driver to free resources
        try:
            driver.quit()
        except Exception as e:
            app.logger.warning(f"Error quitting driver: {str(e)}")

def get_attendance_data(username, password):
    app.logger.info(f"Starting attendance data retrieval for user: {username}")

    # Create a future to run the scraping in a separate thread
    future = executor.submit(lambda: scrape_data(create_driver(), username, password))

    try:
        # Reduce timeout to 45 seconds to prevent worker timeout
        result = future.result(timeout=45)
        if result:
            app.logger.info("Successfully retrieved attendance data")
        else:
            app.logger.warning("Failed to retrieve attendance data")
        return result
    except concurrent.futures.TimeoutError:
        app.logger.error("Scraping operation timed out after 45 seconds")
        # Try to cancel the future to free resources
        future.cancel()
        return None
    except Exception as e:
        app.logger.error(f"Unexpected error in get_attendance_data: {str(e)}")
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
    port = int(os.environ.get('PORT', 8080))  # Change default to 8080
    debug = os.environ.get('FLASK_ENV') != 'production'  # Safer debug mode check
    app.run(host='0.0.0.0', port=port, threaded=True, debug=debug)
