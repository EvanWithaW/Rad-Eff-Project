from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from simTypes.trp import composemessageandenforcetype
import time

def gtrn(driver,username,show):
    print("--------------------GTRN--------------------")
    print("""
            Which orbit would you like to run?
            A) 51.6 deg., 500 km (space station orbit) pre-calculated Trapped Proton Spectra
            B) 28.5 deg., 450 km (frequent shuttle orbit) pre-calculated Trapped Proton Spectra
            C) New Trapped Proton Spectra calculation with additional orbital parameters
            """)
    orbit_type = input(":").upper()
    driver.get(f"https://creme.isde.vanderbilt.edu/CREME-MC/Members/{username}/Gtrn")
    buttons = driver.find_elements(by=By.NAME, value="orbit")
    match orbit_type:
        case 'A':
            buttons[0].click()
            perigee, inclination, apogee, initial_longitude, initial_displacement, perigee_displacement, spectra, csv_lst, trapped_proton_model = promptforgtrn(driver,orbit_type)
            clickforgtrn(driver,orbit_type,perigee,inclination,apogee,initial_longitude,initial_displacement,perigee_displacement,spectra,csv_lst,trapped_proton_model)
        case 'B':
            buttons[1].click()
            perigee, inclination, apogee, initial_longitude, initial_displacement, perigee_displacement, spectra, csv_lst, trapped_proton_model = promptforgtrn(driver,orbit_type)
            clickforgtrn(driver,orbit_type,perigee,inclination,apogee,initial_longitude,initial_displacement,perigee_displacement,spectra,csv_lst,trapped_proton_model)
        case 'C':
            buttons[2].click()

            perigee, inclination, apogee, initial_longitude, initial_displacement, perigee_displacement, spectra, csv_lst, trapped_proton_model = promptforgtrn(driver,orbit_type)

            clickforgtrn(driver,orbit_type,perigee,inclination,apogee,initial_longitude,initial_displacement,perigee_displacement,spectra,csv_lst,trapped_proton_model)
        case _:
            print("Invalid orbit type.")
            driver.quit()
            quit(1)
    if show == True:
        driver.maximize_window()
        time.sleep(120)

    return getfilenamegtrn(orbit_type, perigee, inclination, apogee, initial_longitude, initial_displacement, perigee_displacement, spectra, csv_lst, trapped_proton_model)


def clickforgtrn(driver, orbit_type, perigee, inclination, apogee, initial_longitude, initial_displacement, perigee_displacement, spectra, csv_lst, geomagfun):
    if orbit_type == 'C':
        driver.find_element(by=By.NAME, value="perigee").send_keys(str(perigee))
        driver.find_element(by=By.NAME, value="inclination").send_keys(str(inclination))
        driver.find_element(by=By.NAME, value="apogee").send_keys(str(apogee))
        driver.find_element(by=By.NAME, value="initialLongitude").send_keys(str(initial_longitude))
        driver.find_element(by=By.NAME, value="initialDisplacement").send_keys(str(initial_displacement))
        driver.find_element(by=By.NAME, value="displacementOfPerigee").send_keys(str(perigee_displacement))

    if spectra == 0:
        driver.find_elements(by=By.NAME, value="sections")[0].click()
    else:
        driver.find_elements(by=By.NAME, value="sections")[1].click()
        textbox = driver.find_element(by=By.NAME, value="lValues")
        textbox.send_keys(csv_lst)


    if geomagfun == 0:
        driver.find_elements(by=By.NAME, value="weather_index")[0].click()
    else:
        driver.find_elements(by=By.NAME, value="weather_index")[1].click()


    filename = getfilenamegtrn(orbit_type, perigee, inclination, apogee, initial_longitude, initial_displacement, perigee_displacement, spectra, csv_lst, geomagfun)
    textfilebox = driver.find_element(by=By.NAME, value="rootname")
    textfilebox.send_keys(filename)

    driver.find_element(by=By.NAME, value="form.button.submit").click()

    print("GTRN Simulation finished.")

def promptforgtrn(driver,orbit_type):
    perigee, inclination, apogee, initial_longitude, initial_displacement, perigee_displacement, spectra, csv_lst, magweathercon = 0,0,0,0,0,0,0,0,0
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

        print("What Geomagnetic Transmission Function would you like to use?")
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

        if units == 'K':
            unitsbox[0].click()
        elif units == 'N':
            unitsbox[1].click()
        else:
            print("Invalid units.")
            driver.quit()
            quit(1)



    print("What Magnetic Weather Condition would you like to simulate?")
    print(
        """
        0) Quiet
        1) Stormy
        """
    )
    try:
        magweathercon= int(input(":"))
    except ValueError:
        print("Invalid proton model type.")
        driver.quit()
        quit(1)
    if magweathercon != 0 and magweathercon != 1:
        print("Invalid proton model type.")
        driver.quit()
        quit(1)

    return perigee, inclination, apogee, initial_longitude, initial_displacement, perigee_displacement, spectra, csv_lst, magweathercon




def getfilenamegtrn(orbit_type, perigee, inclination, apogee, initial_longitude, initial_displacement, perigee_displacement, spectra, csv_lst, weathercon):
    if orbit_type == 'A' or orbit_type == 'B':
        return f"GTRN_{orbit_type}_{weathercon}"
    else:
        return f"GTRN_{orbit_type}_{perigee}_{inclination}_{apogee}_{initial_longitude}_{initial_displacement}_{perigee_displacement}_{spectra}_{csv_lst}_{weathercon}"
