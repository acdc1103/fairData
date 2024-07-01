# Fair Data Assessment Tool

## Introduction
The Fair Data Assessment Tool is designed to evaluate datasets for compliance with FAIR (Findable, Accessible, Interoperable, and Reusable) principles. This web application provides an intuitive interface for users to submit their datasets for assessment, receive feedback, and improve their data's FAIRness. Currently only datasets from finances.worldbank and data.gov can be assessed.

## Prerequisites
Before running the application, ensure you have the following installed:
- Python 3.10 or higher
- pip (Python package installer)
- Virtual environment (optional but recommended)

## Installation

1. **Clone the Repository**
   ```
   git clone https://github.com/acdc1103/fairData.git
   cd fairData
   ```

2. **Set Up a Virtual Environment (Optional)**
   - Create a virtual environment:
     ```
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```
       .\venv\Scripts\activate
       ```
     - On macOS and Linux:
       ```
       source venv/bin/activate
       ```

3. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. **Set Environment Variables**
   - You need an environment variable called 'OPENAI_API_KEY' containing an API key from OpenAI to use the GPT-4o API.
      - On Windows (Command Prompt):
        ```
        setx OPENAI_API_KEY "your_api_key_here"
        ```
     - On macOS and Linux (Terminal):
        ```
        export OPENAI_API_KEY="your_api_key_here"
        ```
   - Replace "your_api_key_here" with your OpenAI API key. (Create one here: https://openai.com/api/)

2. **Start the Server**
   - Run the application using:
     ```
     python app.py
     ```
   - The application will be available at `http://127.0.0.1/`.

## Using the Application
- Navigate to `http://127.0.0.1/` in your web browser.
- Follow the on-screen instructions to submit your dataset for assessment.
- Review the feedback provided by the tool and make necessary adjustments to improve your data's FAIRness.

## Additional Information
- This project has been developed in the course of a university project. We tried to adhere to the pep8 coding style and developed unit-tests for easier future developments and quality assurance.
- The website has been designed in Webflow.
- The project consists of a app.py that is the Flask backend of the web application, metrics.py consisting of all metrics tested in the application, mapper.py mapping the different metadata schemas to a unified schema, api_handler.py currently on consisting of handling the finances.worldbank API to retrieve metadata and data sample, scraper.py a scraper that utilizes a json to maintain elements that have to be scraped (metadata url & data sample url), logger.py a python logger that is used throughout project, utils.py consists of functions that are reused and utilities for other functions and the unittests metrics_test.py for the metrics. The frontend is using javascript metrics.js and webflow.js (for design purposes).

## Architecture
![architecture_fairdata (2)](https://github.com/acdc1103/fairData/assets/73746974/bd116bb4-9efc-4de5-ae0e-24eff6f09cdd)

