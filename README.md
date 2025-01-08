**Resume Analysis System Documentation**

This document provides instructions on how to set up and run the resume analysis system.

**Prerequisites:**

-   **Python:** Python 3.10 or higher is required.
-   **pip:** The Python package installer.
-   **Virtual Environment (Recommended):** It's highly recommended to use a virtual environment to isolate project dependencies.

**Setup:**

1.  **Clone the Repository:** Clone it to your local machine:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a Virtual Environment:** Navigate to the project directory in your terminal and create a virtual environment:

    ```bash
    python3 -m venv .venv  # On Windows: python -m venv .venv
    ```

3.  **Activate the Virtual Environment:**

    -   **Linux/macOS:**

        ```bash
        source .venv/bin/activate
        ```

    -   **Windows:**

        ```bash
        .venv\Scripts\activate
        ```

4.  **Install Dependencies:** Install the required Python packages using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

    This command reads the `requirements.txt` file and installs all listed packages.

5.  **Set up Gemini Credentials:** Since the system uses the Gemini API, you need to set up Google Gemini credentials.

    -   Rename the `.env.example` file to `.env` file

    -   **Set the GOOGLE_API_KEY environment variable:** Set the `GOOGLE_API_KEY` environment variable in the `.env` file. Or you can set it directly in the terminal as below

        -   **Linux/macOS:**

            ```bash
            export GOOGLE_API_KEY="YOUR API KEY"
            ```

        -   **Windows:**

            ```powershell
            $env:GOOGLE_API_KEY="YOUR API KEY"
            ```

6.  **Running the Streamlit App:** Navigate to the project directory in your terminal (with the virtual environment activated) and run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

    This will start the Streamlit server and open the app in your web browser.

**Usage:**

1.  Open the Streamlit app in your web browser.
2.  Enter the job description from the `job_description.txt` in the provided text area.
3.  Upload one or more resume PDF files using the file uploader from the `resumes` folder.
4.  Click the "Analyze Resumes" button.
5.  The system will analyze the resumes and display the results, including charts, detailed scores, and recommendations.

**File Structure:**

```
resume-analyzer/
├── src/
│   ├── llm/
│   │   └── llm_config.py
│   ├── models/
│   │   ├── base_models.py
│   │   ├── candidate.py
│   │   ├── job.py
│   │   └── scores.py
│   ├── prompts/
│   │   └── templates.py
│   ├── utils/
│   │   ├── chart_builder.py
│   │   └── pdf_loader.py
│   ├── resume_analyzer.py
├── app.py          # Streamlit app file
├── requirements.txt
└── .venv/           # Virtual environment (hidden)
```
