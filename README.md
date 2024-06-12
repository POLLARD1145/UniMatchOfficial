# <b>Uni</b><u>Match</u>
## University Recommendation System

This project is a University Recommendation System built using the Django framework for web applications, Beautiful Soup for web scraping, and various Python libraries such as Pandas, NumPy, and other machine learning frameworks.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
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

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```sh
    python manage.py migrate
    ```

5. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

6. **Open your web browser and go to:**
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

## Contributing
We welcome contributions to enhance the project. To contribute:
1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push to your branch and create a pull request.

Please ensure your code adheres to our coding standards and includes appropriate tests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
