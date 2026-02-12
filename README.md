If you are new to Python and need to install everything from scratch, follow these steps:

1.  **Install Python**:
    *   Download Python from [python.org/downloads](https://www.python.org/downloads/).
    *   **IMPORTANT**: During installation, check the box **"Add Python to PATH"**.

2.  **Install Git**:
    *   Download and install Git from [git-scm.com/downloads](https://git-scm.com/downloads).

3.  **Setup the Project (Command Prompt)**:
    *   Open Command Prompt (cmd).
    *   Navigate to your project folder:
        ```cmd
        cd "d:\Hospital patient registration"
        ```
    *   Create a virtual environment (optional but recommended):
        ```cmd
        python -m venv venv
        ```
    *   Activate the virtual environment:
        ```cmd
        venv\Scripts\activate
        ```
    *   Install dependencies:
        ```cmd
        pip install -r requirements.txt
        ```

4.  **Run the Application**:
    *   Start the server:
        ```cmd
        python app.py
        ```
    *   Open your browser and verify the futuristic website at: `http://127.0.0.1:5000/`

5.  **Use the App**:
    *   **Patient**: Register to get a token.
    *   **Staff**: Go to `/staff/login`. 
        *   **ID**: HOSP001
        *   **Email**: admin@hospital.com
        *   **Password**: admin

6.  **Deploy to GitHub (Manual Push)**:
    *   Run these commands inside your project folder:
        ```cmd
        git init
        git add .
        git commit -m "Initial commit of Hospital App"
        # Create a new repository on GitHub.com first!
        # Then replace the URL below with your new repository URL:
        git branch -M main
        git remote add origin https://github.com/YOUR_USERNAME/HOSPITAL_REPO_NAME.git
        git push -u origin main
        ```
