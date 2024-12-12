from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

def trp(driver,username,show):
    print("--------------------TRP--------------------")
    print("""
            Which orbit would you like to run?
            A) 51.6 deg., 500 km (space station orbit) pre-calculated Trapped Proton Spectra
            B) 28.5 deg., 450 km (frequent shuttle orbit) pre-calculated Trapped Proton Spectra
            C) New Trapped Proton Spectra calculation with additional orbital parameters
            """)
    orbit_type = input(":").upper()
    driver.get(f"https://creme.isde.vanderbilt.edu/CREME-MC/Members/{username}/Trp")
    buttons = driver.find_elements(by=By.NAME, value="orbit")
    match orbit_type:
        case 'A':
            buttons[0].click()
            perigee, inclination, apogee, initial_longitude, initial_displacement, perigee_displacement, number_of_orbits, orbitdict, spectra, csv_lst, trapped_proton_model = promptfortrp(driver,orbit_type)
            clickfortrp(driver,orbit_type,perigee,inclination,apogee,initial_longitude,initial_displacement,perigee_displacement,number_of_orbits,orbitdict,spectra,csv_lst,trapped_proton_model)
        case 'B':
            buttons[1].click()
            perigee, inclination, apogee, initial_longitude, initial_displacement, perigee_displacement, number_of_orbits, orbitdict, spectra, csv_lst, trapped_proton_model = promptfortrp(driver,orbit_type)
            clickfortrp(driver,orbit_type,perigee,inclination,apogee,initial_longitude,initial_displacement,perigee_displacement,number_of_orbits,orbitdict,spectra,csv_lst,trapped_proton_model)
        case 'C':
            buttons[2].click()

            perigee, inclination, apogee, initial_longitude, initial_displacement, perigee_displacement, number_of_orbits, orbitdict, spectra, csv_lst, trapped_proton_model = promptfortrp(driver,orbit_type)

            clickfortrp(driver,orbit_type,perigee,inclination,apogee,initial_longitude,initial_displacement,perigee_displacement,number_of_orbits,orbitdict,spectra,csv_lst,trapped_proton_model)
        case _:
            print("Invalid orbit type.")
            driver.quit()
            quit(1)
    if show == True:
        driver.maximize_window()
        time.sleep(120)
    return getfilenametrp(orbit_type, perigee, inclination, apogee, initial_longitude, initial_displacement, perigee_displacement, number_of_orbits, orbitdict, spectra, csv_lst, trapped_proton_model)

def clickfortrp(driver,orbit_type,perigee,inclination,apogee,initial_longitude,initial_displacement,perigee_displacement,number_of_orbits,orbitdict,spectra,csv_lst,trapped_proton_model):
    if orbit_type == 'C':
        driver.find_element(by=By.NAME, value="perigee").send_keys(str(perigee))
        driver.find_element(by=By.NAME, value="inclination").send_keys(str(inclination))
        driver.find_element(by=By.NAME, value="apogee").send_keys(str(apogee))
        driver.find_element(by=By.NAME, value="initialLongitude").send_keys(str(initial_longitude))
        driver.find_element(by=By.NAME, value="initialDisplacement").send_keys(str(initial_displacement))
        driver.find_element(by=By.NAME, value="displacementOfPerigee").send_keys(str(perigee_displacement))

        orbitsel = driver.find_element(by=By.NAME, value="numberOfOrbits")
        Select(orbitsel).select_by_index(orbitdict[number_of_orbits])
        if spectra == 0:
            driver.find_elements(by=By.NAME, value="sections")[0].click()
        else:
            driver.find_elements(by=By.NAME, value="sections")[1].click()
            textbox = driver.find_element(by=By.NAME, value="lValues")
            textbox.send_keys(csv_lst)

    if trapped_proton_model == 0:
        driver.find_elements(by=By.NAME, value="model_index")[0].click()
    else:
        driver.find_elements(by=By.NAME, value="model_index")[1].click()

    filename = getfilenametrp(orbit_type, perigee, inclination, apogee, initial_longitude, initial_displacement, perigee_displacement, number_of_orbits, orbitdict, spectra, csv_lst, trapped_proton_model)
    textfilebox = driver.find_element(by=By.NAME, value="rootname")
    textfilebox.send_keys(filename)

    driver.find_element(by=By.NAME, value="form.button.submit").click()

    print("TRP Simulation finished.")




def promptfortrp(driver,orbit_type):
    perigee, inclination, apogee, initial_longitude, initial_displacement, perigee_displacement, number_of_orbits, orbitdict, spectra, csv_lst, proton_model = 0,0,0,0,0,0,0,0,0,0,0
    if orbit_type == 'C':
        try:
            print("Are the Apogee Units in kilometers or nautical miles?")
            units = input("Input 'k' for kilometers or 'n' for nautical miles:").upper()
        except ValueError:
            print("Invalid units.")
            driver.quit()
            quit(1)
        unitsbox = driver.find_elements(by=By.NAME, value="units")
        unitsdict = {"K": "kilometers", "N": "Nautical Miles"}
        apogee = composemessageandenforcetype(driver, "apogee", float, unitsdict[units])
        perigee = composemessageandenforcetype(driver, "perigee", float, unitsdict[units])
        inclination = composemessageandenforcetype(driver, "inclination", float, "degrees")
        initial_longitude = composemessageandenforcetype(driver, "initial longitude", float, "degrees")
        initial_displacement = composemessageandenforcetype(driver, "initial displacement from ascending node", float,
                                                            "degrees")
        perigee_displacement = composemessageandenforcetype(driver, "displacement of perigee from ascending node", float,
                                                            "degrees")
        number_of_orbits = composemessageandenforcetype(driver, "number of orbits", int, "")

        attempts = 0
        orbitdict = {200: 0, 100: 1, 75: 2, 50: 3, 35: 4, 10: 5}
        while number_of_orbits not in orbitdict.keys() or attempts == 3:
            print("Invalid number of orbits, must be one of 10, 35, 50, 75, 100, or 200.")
            number_of_orbits = composemessageandenforcetype(driver, "number of orbits", float, "")
            attempts += 1
            if attempts == 3:
                print("Too many attempts.")
                driver.quit()
                quit(1)

        print("What Trapped Proton Spectra would you like to calculate?")
        print(
            """
            0) Whole Orbit
            1) Sections of Orbits (delineated by Mcllwain L)
            """
        )
        csv_lst = []
        try:
            spectra = int(input(":"))
        except ValueError:
            print("Invalid spectra type.")
            driver.quit()
            quit(1)
        if spectra != 0 and spectra != 1:
            print("Invalid spectra type.")
            driver.quit()
            quit(1)
        elif spectra == 1:
            print("Please enter a comma separate list of lower limits on L.")
            csv_lst = input(":").strip(' ').strip(':')

    print("What Trapped Proton Model would you like to use?")
    print(
        """
        0) AP8MIN
        1) AP8MAX
        """
    )
    try:
        proton_model= int(input(":"))
    except ValueError:
        print("Invalid proton model type.")
        driver.quit()
        quit(1)
    if proton_model != 0 and proton_model != 1:
        print("Invalid proton model type.")
        driver.quit()
        quit(1)

    if orbit_type =='C':
        if units == 'K':
            unitsbox[0].click()
        elif units == 'N':
            unitsbox[1].click()
        else:
            print("Invalid units.")
            driver.quit()
            quit(1)


    return (perigee, inclination, apogee, initial_longitude, initial_displacement, perigee_displacement,
            number_of_orbits, orbitdict,spectra,csv_lst,proton_model)


def getfilenametrp(orbit_type, perigee, inclination, apogee, initial_longitude, initial_displacement, perigee_displacement, number_of_orbits, orbitdict, spectra, csv_lst, trapped_proton_model):
    if orbit_type == 'A' or orbit_type == 'B':
        return f"TRP_{orbit_type}_{trapped_proton_model}"
    else:
        return f"TRP_{orbit_type}_{perigee}_{inclination}_{apogee}_{initial_longitude}_{initial_displacement}_{perigee_displacement}_{number_of_orbits}_{orbitdict[number_of_orbits]}_{spectra}_{csv_lst}_{trapped_proton_model}"

def composemessageandenforcetype(driver,nameOfValue, typeOfValue, units):
    if units == "":
        print(f"Enter the {nameOfValue} of the orbit.")
    else:
        print(f"Enter the {nameOfValue} of the orbit in {units}.")
    try:
        value = typeOfValue(input(":"))
    except ValueError:
        print(f"Invalid {nameOfValue} value.")
        driver.quit()
        quit(1)
    return value