# <b>Uni</b><u>Match</u>
## University Recommendation System

This project is a University Recommendation System built using the Django framework for web applications, Beautiful Soup for web scraping, and various Python libraries such as Pandas, NumPy, and other machine learning frameworks.
## Screenshots
![Home](https://github.com/user-attachments/assets/e85f6a91-8aa6-410f-bf50-5f54e3add4c8)
Home Page / Landing Page

![Recommendation](https://github.com/user-attachments/assets/2ad018d3-03bb-4a41-90fe-4ea02ad97efe)
Personalised Recommendation Page


## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Important Dependencies](#important-dependencies)
- [Contributing](#contributing)
- [License](#license)

## Introduction
The University Recommendation System is designed to help students find suitable universities based on their preferences and academic performance. By scraping data from various university websites and applying machine learning algorithms, the system provides personalized university recommendations.

## Features
- User authentication and profile management
- Web scraping of university data
- Machine learning-based recommendation engine
- Interactive user interface for inputting preferences and viewing recommendations
- Data visualization for comparison of different universities

## Installation

### Prerequisites
- Python 3.8+
- Django 3.2+
- Virtualenv

### Steps
1. **Clone the repository:**
    ```sh
    git clone https://github.com/POLLARD1145/UniMatchOfficial.git
    cd UniMatchOfficial
    ```
2. **Navigate to the project folder:**
    ```sh
    cd Django
    cd UniMatch
    ```

3. **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    venv\Scripts\activate
     # On other OSs, use 'source venv/bin/activate'
    ```

4. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt #install all the required dependencies
    ```

5. **Apply migrations:**
    ```sh
    python manage.py migrate
    ```

6. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

7. **Open your web browser and go to:**
    ```sh
    http://127.0.0.1:8000/
    ```

## Usage
1. **Register and log in to your account.**
2. **Fill in your academic details and preferences.**
3. **Run the recommendation engine to get a list of recommended universities.**
4. **View detailed information about each recommended university.**

## Technologies Used
- **Django:** For building the web application
- **Beautiful Soup:** For web scraping university data
- **Pandas:** For data manipulation and analysis
- **NumPy:** For numerical computations
- **Scikit-learn:** For implementing machine learning algorithms
- **Matplotlib/Seaborn:** For data visualization

## Important Dependencies
- **asgiref:** ASGI reference implementation, required for Django's async support.
- **channels:** Adds WebSocket and asynchronous capabilities to Django.
- **joblib:** Helps in parallel processing, often used in machine learning.
- **nltk:** Natural Language Toolkit, used for text processing tasks.
- **scipy:** Scientific computing library, often used with numpy.
- **regex:** Advanced regular expressions for matching patterns.
- **rich:** For creating rich text formatting in the terminal.
- **spacy:** Industrial-strength NLP library for text processing.
- **textblob:** Simplified text processing for basic NLP tasks.

## Contributing
We welcome contributions to enhance the project. To contribute:
1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push to your branch and create a pull request.

Please ensure your code adheres to our coding standards and includes appropriate tests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
