from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from simTypes.flux import flux
from simTypes.flux import filefindinwindow
import time

def pup(driver, username, show):
    flux_filename = flux(driver, username,False)
    print("--------------------PUP--------------------")
    driver.get(f"https://creme.isde.vanderbilt.edu/CREME-MC/Members/{username}/Pup")

    pup_params = pup_prompt()
    pup_filename = click_pup(driver, pup_params, flux_filename)
    if show == True:
        driver.maximize_window()
        time.sleep(120)

    return pup_filename

def pup_prompt():
    print("Please enter the number of devices you would like to use. (Up to 10)")
    try:
        num_devices = int(input(":"))
        if num_devices <= 0 or num_devices > 10:
            raise ValueError
    except ValueError:
        print("Please enter a valid number of devices")
        quit(1)

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
            print("Please enter a valid number of comments (0, 1, or 2)")
            quit(1)

        comment1 = comment2 = None
        if num_comments >= 1:
            comment1 = input("Enter first comment: ")
        if num_comments == 2:
            comment2 = input("Enter second comment: ")

        print("Enter Bits/Device")
        try:
            bits_per_device = int(input(":"))
        except ValueError:
            print("Please enter a valid number for Bits/Device")
            quit(1)

        print("""
        Choose between Weibull, Bendel 2, or Bendel 1:
            A) Weibull
            B) Bendel 2
            C) Bendel 1
        """)
        model_choice = input(":").upper()
        if model_choice not in ("A", "B", "C"):
            print("Invalid choice. Please enter A, B, or C")
            quit(1)

        weibull_params = None
        bendel_params = None

        if model_choice == "A":
            print("Enter Weibull parameters:")
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
        elif model_choice == "B":
            print("Enter Bendel 2 Parameters:")
            try:
                value_a = float(input("Value A: "))
                value_b = float(input("Value B: "))
            except ValueError:
                print("Please enter valid Bendel parameters")
                quit(1)

            bendel_params = {
                "value_a": value_a,
                "value_b": value_b,
                "model_type": "Bendel 2"
            }
        elif model_choice == "C":
            print("Enter Bendel 1 Parameter:")
            try:
                value_a = float(input("Value A: "))
            except ValueError:
                print("Please enter a valid Bendel 1 parameter.")
                quit(1)

            bendel_params = {
                "value_a": value_a,
                "model_type": "Bendel 1"
            }

        devices.append({
            "label": label,
            "num_comments": num_comments,
            "comment1": comment1,
            "comment2": comment2,
            "bits_per_device": bits_per_device,
            "weibull_params": weibull_params,
            "bendel_params": bendel_params,
        })

    return {"num_devices": num_devices, "devices": devices}

def click_pup(driver, pup_params, flux_filename):
    pup_filename = getfilenamepup(flux_filename, pup_params["num_devices"])
    filefindinwindow(driver, "letFileId_button", flux_filename)

    for i, device in enumerate(pup_params["devices"]):
        driver.find_element(By.ID, f"label{i}").send_keys(device["label"])

        num_comments = device.get("num_comments", 0)
        if num_comments >= 1:
            driver.find_element(By.ID, f"comment1{i}").send_keys(device["comment1"])
        if num_comments == 2:
            driver.find_element(By.ID, f"comment1{i}").send_keys(device["comment2"])

        driver.find_element(By.ID, f"bitsPerDevice{i}").send_keys(device["bits_per_device"])

        if device["weibull_params"]:
            driver.find_element(By.CSS_SELECTOR, f"input[name='xsInputMethod{i}'][value='Weibull']").click()
            weibull = device["weibull_params"]
            driver.find_element(By.ID, f"onset{i}").send_keys(weibull["onset"])
            driver.find_element(By.ID, f"width{i}").send_keys(weibull["width"])
            driver.find_element(By.ID, f"exponent{i}").send_keys(weibull["exponent"])
            driver.find_element(By.ID, f"limitingXS{i}").send_keys(weibull["limiting_xs"])
        elif device["bendel_params"]["model_type"] == "Bendel 2":
            driver.find_element(By.CSS_SELECTOR, f"input[name='xsInputMethod{i}'][value='Bendel 2']").click()
            driver.find_element(By.ID, f"bendel_2_A{i}").send_keys(device["bendel_params"]["value_a"])
            driver.find_element(By.ID, f"bendel_2_B{i}").send_keys(device["bendel_params"]["value_b"])
        elif device["bendel_params"]["model_type"] == "Bendel 1":
            driver.find_element(By.CSS_SELECTOR, f"input[name='xsInputMethod{i}'][value='Bendel 1']").click()
            driver.find_element(By.ID, f"bendel_1_A{i}").send_keys(device["bendel_params"]["value_a"])

    driver.find_element(By.NAME, "jobName").send_keys(pup_filename)

    driver.find_element(By.NAME, "form.button.submit").click()
    print(f"PUP Simulation complete. Filename: {pup_filename}")

    return pup_filename

def getfilenamepup(flux_filename, num_devices):
    filename = f"PUP_{flux_filename}_Devices{num_devices}"
    return filename