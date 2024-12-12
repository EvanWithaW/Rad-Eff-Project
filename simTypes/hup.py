from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from simTypes.letspec import letspec
from simTypes.flux import filefindinwindow
import time

def hup(driver, username,show):
    letspec_filename = letspec(driver, username,False)
    print("--------------------HUP--------------------")
    driver.get(f"https://creme.isde.vanderbilt.edu/CREME-MC/Members/{username}/Hup")

    hup_params = hup_prompt()

    hup_filename = click_hup(driver, hup_params, letspec_filename)
    if show == True:
        driver.maximize_window()
        time.sleep(120)

    return hup_filename

def hup_prompt():
    print("Please enter the number of devices you would like to use. (Up to 10)")
    try:
        num_devices = int(input(":"))
        if num_devices <= 0:
            raise ValueError
    except ValueError:
        print("Please enter a valid number of devices (greater than 0)")

    devices = []
    for i in range(num_devices):
        print(f"\n--- Device {i} Parameters ---")

        label = input("Enter device label: ")

        print("How many comments do you want to add? (0, 1, or 2)")
        try:
            num_comments = int(input(":"))
            if num_comments < 0 or num_comments > 2:
                raise ValueError
        except ValueError:
            print("Please enter a valid number of comments (0, 1, or 2).")
            quit(1)

        comment1 = comment2 = None
        if num_comments >= 1:
            comment1 = input("Please enter first comment: ")
        if num_comments == 2:
            comment2 = input("Please enter second comment: ")

        print("Enter Bit RPP for X, Y, Z (in µm):")
        try:
            rpp_x = float(input("X: "))
            rpp_y = float(input("Y: "))
            rpp_z = float(input("Z: "))
        except ValueError:
            print("Please enter valid numbers for Bit RPP.")
            quit(1)

        print("Enter Bits/Device")
        try:
            bits_per_device = int(input(":"))
        except ValueError:
            print("Please enter valid numbers for Bit/Device.")
            quit(1)

        print("""
        Choose between Weibull or Critical Charge:
            A) Weibull
            B) Critical Charge
        """)
        charge_choice = input(":").upper()
        if charge_choice not in ("A", "B"):
            print("Invalid choice, please enter A or B")
            quit(1)

        weibull_params = None
        crit_charge_params = None

        if charge_choice == "A":
            print("Enter Weibull Parameters:")
            try:
                onset = float(input("Onset (MeV-cm^2/mg): "))
                width = float(input("Width (MeV-cm^2/mg): "))
                exponent = float(input("Exponent: "))
                limiting_xs = float(input("Limiting XS (µm^2): "))
            except ValueError:
                print("Please enter valid Weibull parameters.")
                quit(1)

            weibull_params = {
                "onset": onset,
                "width": width,
                "exponent": exponent,
                "limiting_xs": limiting_xs,
            }

        else:
            print("Enter Critical Charge parameters:")
            try:
                qcrit = float(input("Qcrit (pC): "))
                xs_bit = float(input("XS/Bit (µm^2): "))
            except ValueError:
                print("Please enter valid critical charge parameters.")
                quit(1)

            crit_charge_params = {
                "qcrit": qcrit,
                "xs_bit": xs_bit,
            }

        devices.append({
            "label": label,
            "num_comments": num_comments,
            "comment1": comment1,
            "comment2": comment2,
            "rpp_x": rpp_x,
            "rpp_y": rpp_y,
            "rpp_z": rpp_z,
            "bits_per_device": bits_per_device,
            "weibull_params": weibull_params,
            "crit_charge_params": crit_charge_params,
        })

    return {"num_devices": num_devices, "devices": devices}

def click_hup(driver, hup_params, letspec_filename):
    #generate filename
    hup_filename = getfilename(letspec_filename, hup_params["num_devices"])

    filefindinwindow(driver, "letFileId_button", letspec_filename)

    #loop through devices and input parameters
    for i, device in enumerate (hup_params["devices"]):
        #input label and comment
        driver.find_element(By.ID, f"label{i}").send_keys(device["label"])

        #check if comments should be added
        num_comments = device.get("num_comments", 0) #default is 0 comments
        if num_comments >= 1:
            driver.find_element(By.ID, f"comment1{i}").send_keys(device["comment1"])
        if num_comments == 2:
            driver.find_element(By.ID, f"comment2{i}").send_keys(device["comment2"])

        #input bit rpp values
        driver.find_element(By.ID, f"rppx{i}").send_keys(device["rpp_x"])
        driver.find_element(By.ID, f"rppy{i}").send_keys(device["rpp_y"])
        driver.find_element(By.ID, f"rppz{i}").send_keys(device["rpp_z"])

        #bits/device
        driver.find_element(By.ID, f"bitsPerDevice{i}").send_keys(device["bits_per_device"])

        #weibull/crit charge
        if device["weibull_params"]:
            driver.find_element(By.CSS_SELECTOR, f"input[name='xsInputMethod{i}'][value='Weibull']").click()
            weibull = device["weibull_params"]
            driver.find_element(By.ID, f"onset{i}").send_keys(weibull["onset"])
            driver.find_element(By.ID, f"width{i}").send_keys(weibull["width"])
            driver.find_element(By.ID, f"exponent{i}").send_keys(weibull["exponent"])
            driver.find_element(By.ID, f"limitingXS{i}").send_keys(weibull["limiting_xs"])
        else:
            driver.find_element(By.CSS_SELECTOR, f"input[name='xsInputMethod{i}'][value='Crit Charge']").click()
            crit_charge = device["crit_charge_params"]
            driver.find_element(By.ID, f"qcrit{i}").send_keys(crit_charge["qcrit"])
            driver.find_element(By.ID, f"xsPerBit{0}").send_keys(crit_charge["xs_bit"])

    driver.find_element(By.NAME, "jobName").send_keys(hup_filename)

    #submit
    driver.find_element(By.NAME, "form.button.submit").click()
    print(f"HUP simulation complete. Filename: {hup_filename}")

    return hup_filename

def getfilename(letspec_filename, num_devices):
    filename = f"HUP_{letspec_filename}_Devices{num_devices}"
    return filename