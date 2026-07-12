# AI Online Compiler

Welcome to the **AI Online Compiler** project! This is a web-based online compiler powered by Flask that also features AI capabilities using Mistral AI. It provides an intuitive platform to write, compile, and execute code directly in your browser.

## Features

- **Multi-language Support:** Write and execute code in various programming languages (e.g., C, Java, Python).
- **AI-Powered Assistance:** Integrated with Mistral AI for intelligent code analysis, debugging assistance, and recommendations.
- **User Authentication:** Secure user sign-up, login, and session management using `Flask-Login` and `Flask-Bcrypt`.
- **Database Integration:** Utilizes `Flask-SQLAlchemy` to manage user data and saved code snippets.
- **Sleek Web Interface:** Clean and responsive UI for an enhanced coding experience.

## Technology Stack

- **Backend:** Python, Flask
- **Database:** SQLAlchemy (SQLite/MySQL/PostgreSQL depending on configuration)
- **Authentication:** Flask-Login, Flask-Bcrypt
- **AI Integration:** Mistral AI API (`mistralai` Python package)
- **Environment Management:** `python-dotenv` for managing sensitive environment variables.

## Getting Started

Follow these instructions to set up the project locally.

### Prerequisites

- Python 3.8 or higher
- `pip` (Python package manager)

### Installation

1. **Clone the repository:**
   If you have a remote Git repository:
   ```bash
   git clone <repository-url>
   cd "AI_ONLINE_COMPILER - Copy"
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add your necessary environment variables (such as secret keys and API keys):
   ```env
   SECRET_KEY=your_secret_key_here
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```

### Running the Application

To start the Flask development server, simply run:

```bash
python run.py
```

The application will start, and you can access it by navigating to `http://localhost:5000` or `http://127.0.0.1:5000` in your web browser.

## Project Structure

- `app/` - Contains the main Flask application module, routes, and logic.
- `compilers/` - Holds compiler-related scripts and logic for different languages.
- `instance/` - Instance-specific folder (commonly holds the SQLite database).
- `run.py` - The entry point script to run the application.
- `requirements.txt` - Lists all Python dependencies required by the project.
- `.env` - Environment configuration file (ignored by version control).
