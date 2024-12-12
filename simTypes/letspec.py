from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from simTypes.flux import flux
from simTypes.flux import filefindinwindow
import time

def letspec(driver, username,show):
    flux_filename = flux(driver, username,False)
    print("--------------------LETSPEC--------------------")
    driver.get(f"https://creme.isde.vanderbilt.edu/CREME-MC/Members/{username}/LetSpec")

    #gather prompts
    letspec_params = letspecPrompt()

    #execute
    letspec_filename = click_letspec(driver, letspec_params, flux_filename)
    if show == True:
        driver.maximize_window()
        time.sleep(120)

    return letspec_filename

def letspecPrompt():
    print("Enter the atomic number of the lightest species to be included (Z min):")
    try:
        z_min = int(input(":"))
    except ValueError:
        print("Please enter a valid number")
        quit(1)

    print("Enter the atomic number of the heaviest species to be included (Z max)")
    try:
        z_max = int(input(":"))
    except ValueError:
        print("Please enter a valid number")
        quit(1)

    print("Enter the minimum energy value (MeV):")
    try:
        min_energy = float(input(":"))
    except ValueError:
        print("Please enter a valid number")
        quit(1)

    print("""
    Do you want a differential LET spectrum too?
        A) Yes
        B) No
    """)
    diff_spectrum_choice = input(":").upper()
    diff_spectrum = diff_spectrum_choice == "A" #true for yes, false for no

    return {
        "z_min": z_min,
        "z_max": z_max,
        "min_energy": min_energy,
        "diff_spectrum": diff_spectrum,
    }
def click_letspec(driver, letspec_params, flux_filename):
    #generate filename
    letspec_filename = getfilenameletspec(
        flux_filename,
        letspec_params["z_min"],
        letspec_params["z_max"],
        letspec_params["min_energy"],
        letspec_params["diff_spectrum"],
    )
    #browse and attach lux file
    filefindinwindow(driver, "fluxFileId_button", flux_filename)

    #input z min
    driver.find_element(By.NAME, "z1").send_keys=letspec_params["z_min"]

    #input z max
    driver.find_element(By.NAME, "z2").send_keys=letspec_params["z_max"]

    #input energy value
    driver.find_element(By.NAME, "minE").send_keys=letspec_params["min_energy"]

    #check if diff let spectrum box is selected
    if letspec_params["diff_spectrum"]:
        driver.find_element(By.NAME, "dlt").click()

    #input rootname for output file
    driver.find_element(By.NAME, "rootname").send_keys(letspec_filename)
    driver.find_element(By.NAME, "form.button.submit").click()
    print("LETSPEC simulation complete")
    return letspec_filename

def getfilenameletspec(flux_filename, z_min, z_max, min_energy, diff_spectrum):
    diff_spectrum_tag = "DLET" if diff_spectrum else "NO_DLET"
    filename = f"LETSPEC_{flux_filename}_Z{z_min}-{z_max}_E{min_energy}MeV_{diff_spectrum_tag}"
    return filename