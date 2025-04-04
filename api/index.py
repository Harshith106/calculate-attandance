from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import concurrent.futuresptpn
ioportrcoecientfutus
imor atext
imprtos
me
imprt traceback
import os
import traceebacsk
pp= (__nme__)
# Iniaialls# Enablk  app for all routes

# Thread pool for selenium operations
exeutor= concurren.futurs.ThreadPoolExecuor(max_workr=2)

#app = Flask(__name__)
defCcleanup():
ORS (app)  # Enable CORS for all routes

# Thread pool for selenium operations
executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

# Cleanup function
def cleanup():
    executor.shutdwebdriver.Chromeown(wait=False)

atexit.register(cleanup)
sad_agmera("adless Chrome driver with optimized settings for Vercel."""
    try:
        ons = webdriver.ChromeOptions()
        ons.add_argument("--headless")
        ons.add_argument("--disable-gpu")
        ons.add_argument("-big--disable-vtinures")
        ons.add_argument("--("--disalle-notifications")
        options.add_argument("--disabtet--ng--je(prb
   ChromeDriver path from environment if available
chrome_dn.get("CHROME_DRIVER_PATH")
if chrome_driver_path:ervice = webdriver.chrome.service.Service(executable_path=chrome_driver_path)
 vrho(riroc ar"Error creating Chrome driver: {str(e)}")
        traceback.print_exc()
        raise
def scrape_data(driver, username, password):
    """Scr # Sega ite
        # Click on student link"
        print("Clicking student link")
        StudentLink = webdriver.chrome.service.WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//nav//a[@id='studentLink']"))
        
        tLinter usernameu
        print("Entering username")
            be_clickable((By.XPATH, "//form[@id='studentForm']//input[@id='inputStuId']"))
        )
    Ele.clear()
        sendr passwordi
        print("Entering password")
        passEle = WebDriverWait(driver, 30).until(
     EC.element_to_be_clickable((By.XPATH, "//form[@id='studentForm']//input[@id='inputPassword']"))
ssword)
        ck login buttone
        print("Clicking login button")
        login_button = WebDriverWait(driver, 30).until(
            EC.element_t ge to load afprint("Waiting for page to load after login")

        
        # Define XPaths - keepattendance_percentage_xpath = "//fieldset[contains(@class, 'bottom-border') and not(contains(@class, 'bottom-border-header'))]//div[contains(@class,'x-column-inner')]/div[contains(@class,'x-field')][5]//span"
      ox= "//fieldset[contains(@class, 'bottom-border') and not(contains(@class, 'bottom-border-header'))]//div[contains(@class,'x-column-inner')]/div[contains(@class,'x-field')][2]//span"
        v
        # Initialize lists
        attendance_percentages 
        # Wait for elements to be pre)er, 30)
        
        # Get percentage elementsl_elements_located((By.XPATH, attendance_percentage_xpath)))
        
        # Get course elemenements_located((By.XPATH, course_name_xpath)))
     
        # Process percentage elements
        print(f"Processing {len(percentage_elements)} percentage elements")
        for element in percentage_elements:
            text_content = element.text.strip()
           try:
                percent_val = float(text_content)
                attdndance_percentages.append(percent_val)
       ae_percentages.append(0)
         urse elements
        print(f"Processing {len(course_elements)} course elements")
            (element.text.strip())
        m
        #
            print("No attendance percentages found")
        one
        
        prReturn the result
        return {b
            'courses': course_names,
            'percentages': attendance_percentages,
            'attendance': final_percent
        l}g_buponpclo ke:
        nt(f"Error during scraping: {str(e)}")
        traceback.print_exc()
        e to quit the driver to free resources
    print(f"Error quitting driver: {str(e)}")

 aaes # Create a future to run the scraping in a separate thread
    future = executor.submit(lambda: scrape_data(create_driver(), username, password))
  ioa
            print("Failed to retrieve attendance data")
        urir eefF  rtN
    exceticcrt gc
        gc.collect()
        return None

def index(): ree

    """Health check endpoint."""
    return jsonify({'status': 'oksage': 'Service is running'})
o
def tc: e ani{
     # Try JSON data
     if request.is_json:
         data = request.get_jton()
          ar
    # Trform data
    if not username or notoUpa
   if nos:me = request.args.get('username')
       a
       # Valte credentials
        if name error': 'Username and password are required'}), 400
        
                ult
sult:
             n_pcntsappd(0)
        
        # Pro  sssourselemet
          i  reuPnjy({eirgr{l'n(co rFe_e  mch attendance data. Ple
       frs: {r")ntin roursfllemttif __name__ == '__main__':
    app.run(debug=True)
