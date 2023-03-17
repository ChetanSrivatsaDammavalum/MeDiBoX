# MeDiBoX

An IoT‑based medication management system.

The project aims to develop an End-to-end IoT based medicine management system with web application, cloud server, database and an ESP32 microcontroller based smart medicine pill box. 

Designed to provide medicine inventory management and medication alert, the system aims to ensure the following-
 - The user is appropriatly stocked with medicines.
 - The user takes the mediction at the correct time.
 - The user takes the correct medication.
 
To achieve these core functionalities, the system is envisioned to utlize web based server & database solutions for maintaining user information, and an IoT enabled ESP32 microcontroller medicine pill box. The ESP32 is to be programmed to notify the user of the medication times and which medicine to take.  

## Solution Stack
- Python 
- Embedded C
- PySide6
- Pandas
- SQLLite
- Django

## Milestones

 - [x] Build a prototype software in Python as a proof of concept for the core backend management system with local database.
 - [ ] Add UI and build as a desktop application using QT.
 - [ ] Develop a web server backend in the Django framework and SQL database.
 - [ ] Develop web application frontend in Django and deploy webapp in mobile devices
 - [ ] Program ESP32 to access server, perform database commit queries, and user functionalities. 


## Current state

### 10.03.2023
 - Built core backend script using Python 3.8 and Pandas in Linux.
 
 The application takes in user & prescription information which are stored in a local database. The user can view personal data, prescription information, modify or add new perscriptions and assign dependents. The application notifies the user to refill medicine, take specific medicine at the prescribed times and records if the user fails to acknowledge the notification(considered as 'missed dose'). The user can be assigned the roles of caregiver and/or dependent. A cargiver can view the prescription of the dependent and also the record of 'missed doses'. The caregiver can have a maximum of 5 dependents and can be a dependent themselves to another caregiver.  
 
 The use cae diagram for the application is shown below. It shows the various functionalities in the application and actors interacting with the application. 
 <img src="https://github.com/ChetanSrivatsaDammavalum/MeDiBoX/blob/Development/MeDiBoX%20-%20Use%20case%20diagram.png" width="900" height="700">
 
The applciation is programmed with the object oriented paradigm and follows the microservice architecture. The applciation uses dedicated services to access user database & user prescription, user creation/handling, prescription creation/handling and user interface. The class diagram for the application progra is shown below.

#### Run script
- install packages: pandas, numpy, inputimeout
- run new_test.py

## Next stage
Implement the UI for application using PySide6 wrapper of QT. 
