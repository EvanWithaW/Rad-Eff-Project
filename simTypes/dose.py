from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from simTypes.flux import flux, filefindinwindow
from selenium.webdriver.common.by import By
import time


def dose(driver, username, show):
    flux_filename = flux(driver, username, False)
    print("--------------------DOSE--------------------")
    driver.get(f"https://creme.isde.vanderbilt.edu/CREME-MC/Members/{username}/Dose")
    lowest_atomic_element, highest_atomic_element = dose_prompt()
    click_for_dose(driver, lowest_atomic_element, highest_atomic_element, flux_filename)
    print(f"DOSE Simulation complete.")
    if show == True:
        driver.maximize_window()
        time.sleep(120)


def dose_prompt():
    lowestatomicelement, highestatomicelement = 0, 0
    try:
        lowestatomicelement = int(input("Enter the atomic number of the lightest element included: "))
    except:
        print("Please enter a valid atomic number.")
        quit(1)
    try:
        highestatomicelement = int(input("Enter the atomic number of the heaviest element included: "))
    except:
        print("Please enter a valid atomic number.")
        quit(1)
    return lowestatomicelement, highestatomicelement


def click_for_dose(driver, lowest_atomic_element, highest_atomic_element, flux_filename):
    # print(flux_filename)
    filefindinwindow(driver, "fluxFileId_button", flux_filename)
    driver.find_element(by=By.NAME, value="z1").clear()
    driver.find_element(by=By.NAME, value="z1").send_keys(str(lowest_atomic_element))
    driver.find_element(by=By.NAME, value="z2").clear()
    driver.find_element(by=By.NAME, value="z2").send_keys(str(highest_atomic_element))
    thisFileName = get_dose_filename(lowest_atomic_element, highest_atomic_element, flux_filename)
    driver.find_element(by=By.NAME, value="rootname").send_keys(thisFileName)
    driver.find_element(by=By.NAME, value="form.button.submit").click()
    WebDriverWait(driver, 15).until(
        expected_conditions.presence_of_element_located((By.CLASS_NAME, "documentDescription")))


def get_dose_filename(lowest_atomic_element, highest_atomic_element, flux_filename):
    return f"DOSE_{lowest_atomic_element}_{highest_atomic_element}_{flux_filename}"
