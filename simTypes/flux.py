from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from simTypes.trp import trp
from simTypes.gtrn import gtrn
import time


def flux(driver, username,show):
    trpfilename = trp(driver, username,False)
    gtrnfilename = gtrn(driver, username,False)
    print("--------------------FLUX--------------------")
    driver.get(f"https://creme.isde.vanderbilt.edu/CREME-MC/Members/{username}/Flux")
    atomic_lightest_number, atomic_heaviest_number, gcr_version, solar_conditions, year, location_choice = fluxprompt(driver)
    filename = click_flux(driver, atomic_lightest_number, atomic_heaviest_number, gcr_version, solar_conditions, year, location_choice,trpfilename,gtrnfilename)
    if show == True:
        driver.maximize_window()
        time.sleep(120)
    return filename

def fluxprompt(driver):
    atomic_lightest_number, atomic_heaviest_number, gcr_version, solar_conditions, year, location_choice = 0, 0, 0, 0, 0, 0
    print("What is the atomic number of the lightest species to be included?")
    try:
        atomic_lightest_number = int(input(":"))
    except ValueError:
        print("Please enter a valid atomic number.")
        driver.quit()
        quit(1)
    print("What is the atomic number of the heaviest species to be included?")
    try:
        atomic_heaviest_number = int(input(":"))
    except ValueError:
        print("Please enter a valid atomic number.")
        driver.quit()
        quit(1)
    print("""
    What GCR version would you like to use?"
        A) CREME96
        B) CREME2009
        """)
    gcr_version = input(":").upper()
    if gcr_version != 'A' and gcr_version != 'B':
        print("Invalid GCR version.")
        driver.quit()
        quit(1)

    print("""What solar conditions would you like to use?
          A) Solar Minimum
          B) Solar Maximum
          C) Enter Year
          D) Worst Week
          E) Worst Day
          F) Peak 5-minute-averaged fluxes"""
          )
    solar_conditions = input(":").upper()
    if solar_conditions not in ('A', 'B', 'C', 'D', 'E', 'F'):
        print("Invalid solar conditions.")
        driver.quit()
        quit(1)

    if solar_conditions == 'C':
        print("Enter the year for the solar conditions")
        try:
            year = float(input(":"))
        except ValueError:
            print("Please enter a valid year.")
            driver.quit()
            quit(1)

    print("""
    Which spacecraft location would you like to use?
        A) Near-Earth Interplanetary/Geosynchronous Orbit
        B) Inside Earth's Magnetosphere
        """)
    location_choice = input(":").upper()
    if location_choice != 'A' and location_choice != 'B':
        print("Invalid spacecraft location.")
        driver.quit()
        quit(1)

    return (atomic_lightest_number, atomic_heaviest_number, gcr_version, solar_conditions, year, location_choice)


def click_flux(driver, atomic_lightest_number, atomic_heaviest_number, gcr_version, solar_conditions, year,
               location_choice,trpfilename,gtrnfilename):
    driver.find_element(by=By.NAME, value="z1").clear()
    driver.find_element(by=By.NAME, value="z1").send_keys(atomic_lightest_number)
    driver.find_element(by=By.NAME, value="z2").clear()
    driver.find_element(by=By.NAME, value="z2").send_keys(atomic_heaviest_number)
    gcr_version_clicks = {"A": 0, "B": 1}
    driver.find_elements(by=By.NAME, value="version")[gcr_version_clicks[gcr_version]].click()
    solar_conditions_clicks = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5}
    driver.find_elements(by=By.NAME, value="model")[solar_conditions_clicks[solar_conditions]].click()
    if solar_conditions == 'C':
        driver.find_element(by=By.NAME, value="year").send_keys(year)
    spacecraft_location(driver, location_choice, trpfilename,gtrnfilename)
    filename = getfilenameflux(atomic_lightest_number, atomic_heaviest_number, gcr_version, solar_conditions, year,
                   location_choice)
    driver.find_element(by=By.NAME, value="rootname").send_keys(filename)
    driver.find_element(by=By.NAME, value="form.button.submit").click()
    return filename




def getfilenameflux(atomic_lightest_number, atomic_heaviest_number, gcr_version, solar_conditions, year,
                   location_choice):
    if location_choice == 'A':
        return f"FLUX_{atomic_lightest_number}_{atomic_heaviest_number}_{gcr_version}_{solar_conditions}_{year}"
    else:
        return f"FLUX_{atomic_lightest_number}_{atomic_heaviest_number}_{gcr_version}_{solar_conditions}_{year}_{location_choice}"


def spacecraft_location(driver, choice, trpfilename,gtrnfilename):
    buttons = driver.find_elements(by=By.NAME, value="location")

    if choice == 'A':
        buttons[0].click()
    else:
        buttons[1].click()
        filefindinwindow(driver, "gtrnFileId_button", gtrnfilename)
        print("Would you like to add the trapped proton file?")
        choice = input("Y/N:").upper()
        if choice != 'Y' and choice != 'N':
            print("Invalid option.")
            driver.quit()
            quit(1)
        if choice == 'Y':
            print("""
            Which trapped proton file would you like to use?
            0) Average
            1) Peak
            """)
            try:
                choice = input(":")
            except ValueError:
                print("Please enter a valid number.")
                driver.quit()
                quit(1)
            if choice != '0' and choice != '1':
                print("Invalid option.")
                driver.quit()
                quit(1)
            if choice == '0':
                filefindinwindow(driver, "aveTrpFileId_button", trpfilename+"_ave")
            else:
                filefindinwindow(driver, "aveTrpFileId_button", trpfilename+"_peak")


def filefindinwindow(driver, buttonname, filename):
    driver.find_element(by=By.ID, value=buttonname).click()
    opened_window = driver.window_handles[1]
    driver.switch_to.window(opened_window)
    driver.find_element(by=By.NAME, value="searchValue").send_keys(filename)
    driver.find_element(by=By.NAME, value="submit").click()
    WebDriverWait(driver, 20).until(
        expected_conditions.presence_of_element_located((By.XPATH, f'//tr[td/strong[contains(text(), "{filename}")]]'))
    )
    select_link = driver.find_element(By.XPATH,
                                      f'//tr[td/strong[contains(text(), "{filename}")]]//a[strong[text()="Select"]]')
    select_link.click()

    WebDriverWait(driver, 20).until(expected_conditions.number_of_windows_to_be(1))
    driver.switch_to.window(driver.window_handles[0])
