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

6.  **Deploy to the Cloud (Render.com)**:
    Since you want to access this website from anywhere (not just your computer), we will deploy it to **Render** (a free cloud hosting service).

    **Prerequisites**:
    *   You must have pushed your code to GitHub (follow step 6 above first).
    *   Your repository must be "Public" or "Private" (Render supports both).

    **Steps**:
    1.  **Create a Render Account**:
        *   Go to [https://render.com/](https://render.com/).
        *   Sign up using your **GitHub account**.

    2.  **Create a New Web Service**:
        *   Click on the "New +" button and select **Web Service**.
        *   Connect your GitHub repository (`hospital-app`).
        *   Give it a name (e.g., `biosync-hospital`).

    3.  **Configure Settings**:
        *   **Region**: Choose the one closest to you (e.g., Singapore, Ohio, Frankfurt).
        *   **Branch**: `main`
        *   **Root Directory**: (Leave blank)
        *   **Runtime**: `Python 3`
        *   **Build Command**: `pip install -r requirements.txt` (Render should auto-detect this).
        *   **Start Command**: `gunicorn app:app` (Render should auto-detect this from the Procfile).

    4.  **Deploy**:
        *   Click **Create Web Service**.
        *   Wait for the build to finish. It might take a few minutes.
        *   Once done, you will see a URL like `https://biosync-hospital.onrender.com`.
        *   Click it to see your live website!

    **Note on Database**:
    *   This free deployment uses a SQLite database which is stored in a file.
    *   **Warning**: On Render's free tier, the disk is ephemeral. This means if the server restarts (which happens on every new deploy or after inactivity), **the database will be reset**.
    *   For a real production app, you would use a PostgreSQL database, but for this resume project, this setup is sufficient to demonstrate your skills.
