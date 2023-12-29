# Graduation-Project

## 1. Introduction
Graduation project of for the Bachelor of Computer Science, Canadian International College (CIC).

## 2. Table of Contents
- [Introduction](#1-Introduction)
- [Table of Contents](#2-Table-of-Contents)
- [Project Description](#3-project-description)
- [Installation](#4-installation)
- [Usage](#5-usage)
- [Team Members](#6-team-members)
- [Contributing](#7-contributing)
- [License](#8-license)
- [Acknowledgements](#9-acknowledgements)
- [Project Status](#10-project-status)
- [Project Demo](#11-project-demo)
- [Project Presentation](#12-project-presentation)

## 3. Project Description
This is the source code for the graduation project of 2022-2023 academic year in the School of Computer Science, Canadian International College (CIC) - New Cairo, Cairo, Egypt.
It is a web application that helps you to Create a Creative and unique design PowerPoint Presentation for your next presentation.

### the project is divided into 5 applications:

- core: The core application is the main application that contains the main logic of the project.

- Image Generator: The Image Generator application is responsible for generating the images for the presentation.

- Text Simplifier: The Text Simplifier application is responsible for simplifying the text for the presentation.

- Video Converter: The Video Converter application is responsible for converting the video for the presentation.

- Hand Gesture Recognition: The Hand Gesture Recognition application is responsible for recognizing the hand gestures for the presentation.


The application is written in Python using the Django

## 4. Installation

To install the project, follow these steps:

1. Install python if you haven't already. You can download it from the official website: [Python](https://www.python.org/downloads/)
2. Clone the repository using git:
    ```bash
    git clone https://github.com/NourEldin-Osama/Graduation-Project.git
    ```
3. Navigate to the project directory
    ```bash
    cd Graduation-Project
    ```
4. Create a virtual environment and activate it (optional, but recommended):
    ```bash
   python -m venv venv; source venv/bin/activate
    ```
5. Install the project dependencies:
    ```bash
    pip install -r requirements.txt
    ```
6. Generate the migration files:
    ```bash
    python manage.py makemigrations
    ```
7. Apply the migrations:
    ```bash
    python manage.py migrate
    ```
8. Create a superuser (optional):
    ```bash
    python manage.py createsuperuser
    ```
9. Run the server:
    ```bash
    python manage.py runserver
    ```
10. Open the browser and navigate to [localhost](http://localhost:8000/) to see the project running.

You are now ready to use the project 🎉🤗.

Extra: If you want a one-line command to do all of the above, run the following command:
```bash
git clone https://github.com/NourEldin-Osama/Graduation-Project.git; cd Graduation-Project; pip install -r requirements.txt; python manage.py makemigrations; python manage.py migrate
```

## 5. Usage
- Run the server with the following command
```bash
python manage.py runserver 
```
- or if you want to make the server accessible from other devices in the same network, run the server with the following command
```bash
python manage.py runserver 0.0.0.0:8000
```

## 6. Team Members
- [NourEldin Osama](https://www.linkedin.com/in/noureldin-osama-saad/) - Team Leader
- [Yousr Ahmed](https://www.linkedin.com/in/yousr-ahmed/)
- [Seif Eldin Hesham](https://www.linkedin.com/in/SeifEldinIsamil/)
- [Hussein Mohamed](https://www.linkedin.com/in/hussein-elwakeel/)
- [Youssef Ahmed]()

## 7. Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## 8. License
This project is licensed under the [MIT](LICENSE.md) License - see the LICENSE file for details

## 9. Acknowledgements
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)

## 10. Project Status
This project is still under development.

## 11. Project Demo
[Click here]() to see the project demo.

## 12. Project Presentation
[Click here]() to see the project presentation.
