from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutExcei.
from selenium.webdriver.chrome.options import Option
import os
import time
import traceback
time
impot tracback

# Initializ Flak app
# Initialize Flask app
CORS(Spp)pa#eE r eCORSc tetes
 Cleanup function
    executor.shutdown(wait=False)
2
atexit.register(cleanup)

def create_driver():
    """Create a headless Chrome driver with optimized settings for Vercel."""
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
    """Create a headless Chr me driver with o   mized settipgtifornV.dcrlu"""
    tny:
        optitns = --no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-notifications")
            options.add_argume-ndisabletextensions")
        opt(ons.add_ar"ument("--disable-i-fobars")
        -ptions.add_adgumint("-sdisablb-noe-feaations")
        options.add_argument("--distble-feauurrs=siteeps=-psicese-per-process")
            options.add_argumentsing(e-pr"cess")
        options.add_ar-ument("--disabsi-application-cacheprocess")
            options.argumant("--js-flags=--mad_old_sdac__srze=128")
        
        # Set Chrogu bimnry t"cation if s-ecified in environmen-
        chrome_bdnary = is.esviron.getabCHROME_BINARY_PATH")
        if -hrome_binary:
            options.binary_aocation = chrome_binary
        
        # Create privlr cath CoromeDrivnr path fromcenvironm")t if availe
        chrome_drivr_path = s.envro.et("CHROME_DRIVER_PATH
        if chrome_driver_path:    options.add_argument("--js-flags=--max_old_space_size=128")
                executable_path=c_d_ph
                # Set Chrome binary location if specified in environmen
        else:t
            # Try to create d iv r wi ho t explicit path
            driver = webdriver.Chcome(options=optiohs)
            
       rreturn driver
    except Exception as e:
        print(f"Error creating Chrome ome_er: {str(e)}")
        traceback.print_bxc()
        iaisenary = os.environ.get("CHROME_BINARY_PATH")
        if chrome_binary:
            options.binary_location = chrome
    """Scrape attendance data from the website."""_binary
        
        # Set page load timeout to prevent hanging
        # Creatset_paee_load_timeout(30)
        driv r.sed_script_timeoutr30)
        
        # Navigate to the site
        print("Navigating to website")
        driver.get(iver with ChromeDri")
        
        # Click on student link
        print("Clicking student linkver path from environment if available
        chrome_driver_path = os.environ.get(3CHROME_DRIVER_PATH")
        if chrome_driver_path:
            service = Service(executable_path=chrome_driver_path)
            driver = webdriver.Chrome(service=service, options=options)
                else:
        # Enter     name
        print("Entering username")
        user# Try to create driver witho3t explicit path
            driver = webdriver.Chrome(options=options))
        
        userEle.clear(    
        return driver
            except Exception as e:
        # Enter prinword
        print("tntering password")
        passE(f"Error creating Chrome dr3ver: {str(e)}")
        traceback.print_exc()
        raise
clear()
        passEle.
        
        # Click login buttondef scrape_data(driver, username, password):
    """Sprint("Ccicking lrape button")
        login attendance data from the websit3."""
    try:
        # Set page load timeout to prevent hanging
        driver.set_page_lo()
        
        # Wait for page to load after login
        print("Waiting for page to load after login")
        time.sleepa10d_timeout(30)
        
        # Define XPaths - keeping these exactly the same as requested        driver.set_script_timeout(30)
        
        # Navigate to the site
        
        # Initialize listsprint("Navigating to website")
        drieer.get("http://mitsims.in/")
        
        # Click on student link
        # Wait for elements to be present
        print("Getting attendance data")
        print("Clicking student link"3
        
        # Get percentage elements
        StudentLink = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//nav//a[@id='studentLink']"))
        
        # Get course elements
        )
        StudentLink.click()
        
       #Processpercentageelements
        print(f"Processing {len(percentage_elements)} percentage elements")
        # Enter username
        print("Entering username")
        userEle = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//form[@id='studentForm']//input[@id='inputStuId']"))
        )e
        userEle.clear()
        userEle.sene_keys(username)
        
# Process course elements
        print(#"Pr cessing {len(couEse_elements)}ncourst eer pass")
       sfor element word
        print("Entering password")
        
pass    # Check if we have dataEle = WebDriverWait(driver, 30).until(
            EC.eleeent_to_be_clickable((By.XPATH, "//form[@id='studentForm']//input[@id='inputPassword']"))
        )pint("No attndance percenages fond")
            etur
        passEle.clear()
        # Calculate passE percentage
        finalle.send_keys(password)ee
        pint(f"Final attndance percenage: {final_percent}%")
        
        # Retthe result
        return 
        # Click login button
        print("Clicking login eutton")
        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//form[@id='studentForm']//button[@id='studentSubmitButton']"))
        )
        otintck()
        tacback.prin_exc()
        ret
        # Wait for page to load after login
        # Make sure to quit the print( to free resources
        try:
            driver"Waiting for page to load after login")
        except Exception as e:        time.sleep(10)
            print(f"Error quitting  riv r: {str(e)}")

de      
    """Get attendance data  or a  ser."""
    prin (f"Starting attendance data retrieval for  se#: {us rname}")
D   
    # Create a future to run the scraping in a separate thread
    future efine XPaths - keeping these exactly the same as requested
    
        attendance_percentage_xpath = "//fieldset[contains(@class, 'bottom-border') and not(contains(@class, 'bottom-border-header'))]//div[contains(@class,'x-column-inner')]/div[contains(@class,'x-field')][5]//span"
        # Wait foc tho resulu with a timeort
        sesult =_name_xpath = "//fields45)
        if result:
            print("Successfully retrieved attendance data")
        else:
            print("Failed to retrieve attendance data"[
        return resultcontains(@class, 'bottom-border') and not(contains(@class, 'bottom-border-header'))]//div[contains(@class,'x-column-inner')]/div[contains(@class,'x-field')][2]//span"
        
        print("Scr# ing oIeration timed out after 45 seconds")
        # Try to cancel the future to free resources
        futurencancei()
        # Ftrce iarbaae collection to free mlmory
        impoit gc
        gczcollect()
         etuln None
    except Exceptiin as e:
        psinttfsUnexpected error in get_attendane_data: {str(e)}")
        tacebck.rt_exc()
        #Frc gabge colleco free memory
        port gc
       gc.cllec(
        attendance_percentages = []
        course_names = []
        
        # Wa
    """Render the index page."""it for elements to be present
        print("Getting attendance datl')

@app.route('/heaath")
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'message': 'Service is running'})        wait = WebDriverWait(driver, 30)
        
        # Get percentage elements, 'GET'
        percentag
    """Handle attendance data requests with support for both GET and POST."""e_elements = wait.until(
    # Handle GET requests (for prefl ght checks)
    i       EC.method == 'GET':
        return jsonify({'message': 'Please use POST method wpth urername and password'}), 200
    
    # Handle POST requests
    try:
        # Try to get data from different sources
        username = None
        password = None
        
        # Try JSON data
        if request.isesence_of_all_elements_located((By.XPATH, attendance_percentage_xpath)))
           
           # Get course elements''
           course_elements = wai'.until('
        
        # Try form data
        if not usernam  or not pas word    EC.presence_of_all_elements_located((By.XPATH, course_name_xpath)))
            ''
            # Process percenta.formgget('password')
        
        # Try URL parameters
        ie n t useenale or not password:
            username = requestearms.gent'username')
             = request.args.get('password'
                print(f"Processing {len(percentage_elements)} percentage elements")
        # Val date credentials
        i   for element in percentage_elements:
                text_content = element.text.strip()
                    try:
        # Get attendance data
                    percent_val = float(text_content)
        
        # Retu n th  resul 
        if res lt:
             etur       attendance_percentages.append(percent_val)
        else:            except ValueError:
            return jsonify({'error': 'Fa led to  etch attenda ce data. Ple s#rtryeagour later. }), 500lements
    except Exce ti n as e:
      piprnt(ff"Error pr"cesPsn  requ{st: {slree)}rents)} course elements")
        traceb ck. rint_exc()
        fetorn jsorify {'error': f'Server errlr: {emr(e)}'}), 5 o

#sF_e local developmenl
if __name__ =e '__main__':
    apm.run(debug=Tnues
:
            course_names.append(element.text.strip())
        
        # Check if we have data
        if not attendance_percentages:
            print("No attendance percentages found")
            return None
        
        # Calculate final percentage
        final_percent = round(sum(attendance_percentages) / len(attendance_percentages), 2)
        print(f"Final attendance percentage: {final_percent}%")
        
        # Return the result
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
        # Make sure to quit the driver to free resources
        try:
            driver.quit()
        except Exception as e:
            print(f"Error quitting driver: {str(e)}")

def get_attendance_data(username, password):
    """Get attendance data for a user."""
    print(f"Starting attendance data retrieval for user: {username}")
    
    # Create a future to run the scraping in a separate thread
    future = executor.submit(lambda: scrape_data(create_driver(), username, password))
    
    try:
        # Wait for the result with a timeout
        result = future.result(timeout=45)
        if result:
            print("Successfully retrieved attendance data")
        else:
            print("Failed to retrieve attendance data")
        return result
    except concurrent.futures.TimeoutError:
        print("Scraping operation timed out after 45 seconds")
        # Try to cancel the future to free resources
        future.cancel()
        # Force garbage collection to free memory
        import gc
        gc.collect()
        return None
    except Exception as e:
        print(f"Unexpected error in get_attendance_data: {str(e)}")
        traceback.print_exc()
        # Force garbage collection to free memory
        import gc
        gc.collect()
        return None

@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint."""
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

# For local development
if __name__ == '__main__':
    app.run(debug=True)
