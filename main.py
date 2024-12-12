from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from simTypes.trp import trp
from simTypes.gtrn import gtrn
from simTypes.flux import flux
from simTypes.trans import trans
from simTypes.letspec import letspec
from simTypes.hup import hup
from simTypes.pup import pup
from simTypes.dose import dose
import os

load_dotenv()

# driverOpts = webdriver.ChromeOptions()
# driverOpts.add_argument("--headless")

# driver = webdriver.Chrome(options=driverOpts)

driver = webdriver.Chrome()
# driverOpts = webdriver.ChromeOptions()
# driverOpts.add_experimental_option("detach",True)


def closedriver():
    driver.quit()


driver.get("https://creme.isde.vanderbilt.edu/CREME-MC/logged_out")
driver.minimize_window()

username_box = driver.find_element(by=By.NAME, value="__ac_name")
password_box = driver.find_element(by=By.NAME, value="__ac_password")
login_box = driver.find_element(by=By.NAME, value="submit")

creme_us = os.environ.get("CREME_USERNAME")
creme_pw = os.environ.get("CREME_PASSWORD")

# check if .env has been read correctly.
if creme_us is None or len(creme_us) == 0:
    raise ValueError("CREME_USERNAME not set")
if creme_pw is None or len(creme_pw) == 0:
    raise ValueError("CREME_PASSWORD not set")

# send the keys to the boxes
username_box.send_keys(creme_us)
password_box.send_keys(creme_pw)

# click on that submit button to successfully login.
login_box.click()

print(f"Successfully logged into CREME as {creme_us}")

try:
    print("""
    Which simulation would you like to run on Creme96?
    0) TRP
    1) GTRN
    2) FLUX
    3) TRANS
    4) LETSPEC
    5) HUP
    6) PUP
    7) DOSE
    """
          )
    typeResp = int(input(":"))
except ValueError:
    "Please enter a valid simulation number."
    closedriver()
    quit(1)

match typeResp:
    case 0:
        trp(driver, creme_us, True)
    case 1:
        gtrn(driver, creme_us, True)
    case 2:
        flux(driver, creme_us, True)
    case 3:
        trans(driver, creme_us, True)
    case 4:
        letspec(driver, creme_us, True)
    case 5:
        hup(driver, creme_us, True)
    case 6:
        pup(driver, creme_us, True)
    case 7:
        dose(driver, creme_us, True)
    case _:
        print("Please enter a valid simulation number")
        closedriver()
        quit(1)

closedriver()
