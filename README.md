# E399-Rad-Eff-Project

### Authors: Evan Weidner & Adi Aurora

## Project Description

This project provides a CLI to run CREME96 Simulations. The goal of project is to ease the use of CREME96 by providing a consistent flow which experienced (or new)
users can follow to run simulations. Each simulation runs all required previous simulations to generate necessary files.

## What can this project do?
- Guide the user through the process of running CREME96 simulations by enforcing all required parameters are provided for each simulation.
- Automatically run CREME96 simulations with user input parameters provided from the CLI without the complications of the website GUI.
- Send the user to the result page of the simulation on the CREME96 website to view/download their simulation results.
- Error check many input simulation parameters to ensure the user is providing valid inputs.

## Getting Started

This project was created and tested on **Python 3.12.2.** There should be no issues with other versions as long as they support the required Python libraries.
Follow the steps below to get started:

**1. Clone the Repository**
- Clone this repository to your local machine with Python 3 installed.
- Open a terminal and navigate to the project directory ***E399-Rad-Eff-Project/***
- Run the following command to install the required Python libraries:
```pip install -r requirements.txt```

**2. Create a .env file**
- This system requires active CREME96 credentials in order to login and operate.
- Create a file named '.env' in the root directory of the project.
- Add the following lines to the .env file, replacing the curly brackets with your values:
```
CREME_USERNAME={YOUR CREME96 USERNAME}
CREME_PASSWORD={YOUR CREME96 PASSWORD}
```

**3. Run the CLI**
- Run the following command to start the CLI: ```python3 main.py```
- Enter the values that corresponds to the simulation parameters you want to run. The CLI will guide you through the process.