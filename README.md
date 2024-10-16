# SQL Query Generator with Google Gemini

This project is a Streamlit application that converts English questions into SQL queries using Google Gemini's generative AI capabilities. It allows users to retrieve data from an SQLite database named **student.db**, which contains information about students, their classes, sections, and marks.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Example Queries](#example-queries)
- [Database Schema](#database-schema)
- [Contributing](#contributing)
- [License](#license)

## Features

- Convert natural language questions into SQL queries.
- Execute generated SQL queries against the SQLite database.
- User-friendly interface built with Streamlit.
- Response cleaning to ensure valid SQL execution.

## Technologies Used

- [Streamlit](https://streamlit.io/) - For building the web application.
- [SQLite](https://www.sqlite.org/index.html) - Lightweight database to store student records.
- [Google Generative AI](https://developers.google.com/generative-ai) - To generate SQL queries from text input.
- [Python](https://www.python.org/) - Programming language used to build the application.
- [Regex](https://docs.python.org/3/library/re.html) - For cleaning generated SQL queries.

## Installation

To get started, clone the repository and install the required dependencies.

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Steps to Install

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/sql-query-generator.git
   cd sql-query-generator
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables:**
   - Create a `.env` file in the project root and add your Google API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and go to `http://localhost:8501`.

3. Input your question in the text box and click the "Ask the question" button. The app will generate an SQL query based on your input and execute it against the database, displaying the results.

## Example Queries

Here are some example questions you can ask:

- "How many entries of records are present?"
- "Tell me all the students studying in Data Science class?"
- "What is the average marks of students?"

## Database Schema

The database **student.db** has the following schema:

| Column  | Type    | Description                          |
|---------|---------|--------------------------------------|
| NAME    | VARCHAR(25) | Name of the student                  |
| CLASS   | VARCHAR(25) | Class of the student                 |
| SECTION | VARCHAR(25) | Section of the student               |
| MARKS   | INT     | Marks obtained by the student        |

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you'd like to contribute.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.




### Key Sections Explained

1. **Title & Introduction:** Brief overview of the project and its purpose.
2. **Table of Contents:** Provides easy navigation throughout the README.
3. **Features:** Highlights the main capabilities of the application.
4. **Technologies Used:** Lists the frameworks, libraries, and languages used in the project.
5. **Installation:** Step-by-step guide for setting up the project, including environment variable setup.
6. **Usage:** Instructions on how to run the application and interact with it.
7. **Example Queries:** Offers sample questions to demonstrate the app’s functionality.
8. **Database Schema:** Details the structure of the SQLite database for better understanding.
9. **Contributing:** Encourages community contributions with a guide on how to do so.
10. **License:** Information regarding the licensing of the project.

### Tips for Customization

- Replace placeholders like `yourusername` and `your_api_key_here` with actual values relevant to your project.
- Adjust the content based on any additional features or changes you have made.
- Make sure to include any additional documentation or instructions relevant to your specific project needs.
