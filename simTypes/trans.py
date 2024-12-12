from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from simTypes.flux import flux
from simTypes.flux import filefindinwindow
import time


def trans(driver, username,show):
    flux_filename = flux(driver, username,False)
    print("--------------------TRANS--------------------")
    driver.get(f"https://creme.isde.vanderbilt.edu/CREME-MC/Members/{username}/Trans")

    #gather input for trans
    trans_params = transPrompt()

    #execute
    trans_filename = click_trans(driver, trans_params, flux_filename)
    if show == True:
        driver.maximize_window()
        time.sleep(120)

    return trans_filename

def transPrompt():
    print("""
    Automatically selected Aluminum because it is the only material available.
    """)
    shielding_material = "Aluminum" #default only option

    print("""
    Choose shield thickness type:
        A) Specify a single value
        B) Use an existing distribution file
    """)

    shield_type = input(":").upper()
    if shield_type not in ('A', 'B'):
        print("Invalid shield type")
        quit(1)

    shield_value = None
    shield_unit = None
    shield_file = None
    if shield_type == 'A':
        print("Enter the single value for the shield thickness:")
        try:
            shield_value = float(input(":"))
        except ValueError:
            print("Please enter a valid number")
            quit(1)
        print("""
        Choose the unit for shield thickness:
            A) mils
            B) cm
            C) g/cm^2
        """)
        unit_choice = input(":").upper()
        shield_unit_map = {"A": "mils", "B": "cm", "C": "g/cm^2"}
        if unit_choice not in shield_unit_map:
            print("Invalid unit type")
            quit(1)
        shield_unit = shield_unit_map[unit_choice]
    else:
        print("Provide the filename for the shield thickness distribution file:")
        shield_file = input(":")

    print("""
    Choose the transport:
        A) Creme96 TRANS/UPROP
        B) HZETRN1995/Nucfrg2
    """)
    transport_code_choice = input(":").upper()
    transport_code_map = {"A": "Creme96 TRANS/UPROP", "B": "HZETRN1995/Nucfr2"}
    if transport_code_choice not in transport_code_map:
        print("Invalid transport code")
        quit(1)
    transport_code = transport_code_map[transport_code_choice]

    return {
        "shielding_material": shielding_material,
        "shield_type": shield_type,
        "shield_value": shield_value,
        "shield_unit": shield_unit,
        "shield_file": shield_file,
        "transport_code": transport_code
    }

def click_trans(driver, trans_params, flux_filename):
    # generate filename
    trans_filename = getfilenametrans(
        flux_filename,
        trans_params["shielding_material"],
        trans_params["shield_type"],
        trans_params["shield_value"],
        trans_params["shield_unit"],
        trans_params["shield_file"],
        trans_params["transport_code"]
    )

    filefindinwindow(driver, "fluxFileId_button", flux_filename)

    #select shielding material
    # dropdown = Select(driver.find_element(By.NAME, "material").click())
    # dropdown.select_by_visible_text("Aluminum")

    #shield thickness
    if trans_params["shield_type"] == "A":
        driver.find_element(By.NAME, "thickness").send_keys(trans_params["shield_value"])
        driver.find_element(By.NAME, "units").send_keys(trans_params["shield_unit"])
        pass
    else:
        #browse and attach shield thickness file
        filefindinwindow(driver, "shdFileId_button", trans_params["shield_file"])

    #select transport code
    transport_code_clicks = {"Creme96 TRANS/UPROP":0, "HZETRN1995/Nucfr2":1}
    driver.find_elements(By.NAME, "transport_code")[transport_code_clicks[trans_params["transport_code"]]].click()

    #enter rootname for output file
    driver.find_element(By.NAME, "rootname").send_keys(trans_filename)

    #submit
    driver.find_element(By.NAME, "form.button.submit").click()
    print("TRANS simulation setup completed.")
    return trans_filename

def getfilenametrans(flux_filename, shielding_material, shield_type, shield_value, shield_unit, shield_file, transport_code):
    base_name = f"TRANS_{flux_filename}_{shielding_material}"

    if shield_type == 'A': # single value
        shield_info = f"{shield_value}{shield_unit}"
    else: #distribution file
        shield_info = f"DISTR_{shield_file}"

    filename = f"{base_name}_{shield_info}_{transport_code.replace(' ', '_')}"
    return filename