# AI-Powered Feedback Analysis Platform

This project is a sample web application that allows users to submit feedback (text, images, audio), analyzes the feedback using **Azure Cognitive Services**, and stores both the raw feedback and analysis results in **Azure SQL Database**. Attachments (images/audio) are stored in **Azure Blob Storage**. An **Admin Dashboard** displays recent feedback and basic sentiment trends. The platform now includes asynchronous database operations, an improved folder structure, and refined endpoints.

---

## Table of Contents

- [Overview](#overview)  
- [Architecture](#architecture)  
- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Local Development](#local-development)  
- [Deployment to Azure](#deployment-to-azure)  
- [Configuration](#configuration)  
- [Project Structure](#project-structure)  
- [Contributing](#contributing)  
- [License](#license)

---

## Overview

1. **User Feedback Form**  
   Users can submit their name, email, feedback text, and an optional file (image/audio).

2. **Sentiment & Key Phrase Analysis**  
   Leverages [Azure Cognitive Services Text Analytics](https://learn.microsoft.com/en-us/azure/cognitive-services/text-analytics/) to determine sentiment and extract key phrases.

3. **Database & Storage**  
   - **Azure SQL** is used to store feedback records and analysis results.  
   - **Azure Blob Storage** handles user-uploaded attachments.  

4. **Admin Dashboard**  
   Displays recent feedback entries and basic sentiment metrics (powered by Chart.js).

5. **Asynchronous Database Operations**  
   Utilizes SQLAlchemy’s async engine for performant and scalable CRUD operations.

---

## Architecture

```bash
AI-Powered-Feedback-Analysis-Platform/
├── app
│   ├── api
│   │   ├── endpoints.py         # Defines FastAPI routes/endpoints
│   │   └── __init__.py
│   ├── models
│   │   ├── feedback.py          # SQLAlchemy model for feedback
│   │   └── __init__.py
│   ├── schemas
│   │   ├── feedback.py          # Pydantic schemas for data validation
│   │   └── __init__.py
│   ├── services
│   │   ├── cognitive.py         # Azure Cognitive Services integration
│   │   ├── db.py                # (Optional) Synchronous DB operations (if still used)
│   │   ├── db_async_sqlalchemy.py # Asynchronous DB operations with SQLAlchemy
│   │   ├── storage.py           # Azure Blob Storage integration
│   │   └── __init__.py
│   ├── templates
│   │   ├── index.html           # User feedback form
│   │   └── dashboard.html       # Admin dashboard
│   ├── main.py                  # Entry point (FastAPI application)
│   └── __init__.py
├── static
│   ├── css
│   │   └── styles.css           # Basic styling
│   └── js
│       └── dashboard.js         # Client-side logic for the dashboard
├── config.py                    # Loads environment variables / config
├── Dockerfile                   # Docker container instructions
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── runtime.txt                  # Python runtime version for Azure
└── .env                         # Local environment variables (excluded from git)


---

## Features

1. **Submit Feedback**  
   - Web form to capture name, email, and feedback text  
   - Optional file upload (image/audio)  

2. **Text Analysis**  
   - Uses Azure Text Analytics for sentiment analysis and key phrase extraction  

3. **Azure SQL Integration**  
   - Stores user info, sentiment scores, and timestamps  

4. **Azure Blob Storage**  
   - Uploads attachments to a blob container  

5. **Admin Dashboard**  
   - Displays recent feedback entries  
   - Simple sentiment chart with Chart.js  

---

## Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [Azure Account](https://azure.microsoft.com/en-us/free/) with:
  - Azure Cognitive Services (Text Analytics) resource
  - Azure SQL Database
  - Azure Blob Storage (Storage Account)
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) (optional for deployment)

---

## Local Development

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/ai-feedback-platform.git
   cd ai-feedback-platform
   ```

2. **Create Virtual Environment & Install Dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate         # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Create `.env` File**

   ```ini
   # .env file
   AZURE_ENDPOINT=https://<your-cognitive-endpoint>.cognitiveservices.azure.com/
   AZURE_KEY=your_cognitive_key
   AZURE_SQL_CONN_STR=your_sql_connection_string
   BLOB_CONN_STRING=your_blob_connection_string
   ```

4. **Run Locally**

   ```bash
   uvicorn app.main:app --reload
   ```

   Visit [http://localhost:8000](http://localhost:8000) to see the feedback form.

---

## Deployment to Azure

1. **Push Code to GitHub**  
   Make sure your code is in a GitHub repo.

2. **Deploy via Azure CLI**  
   ```bash
   az webapp up --name ai-feedback-app --resource-group my-rg --runtime "PYTHON|3.10"
   ```

3. **Configure App Settings in Azure Portal**  
   Under **Configuration** > **Application settings**, add the following keys:
   - `AZURE_ENDPOINT`
   - `AZURE_KEY`
   - `AZURE_SQL_CONN_STR`
   - `BLOB_CONN_STRING`

4. **Restart Your App**  
   Once settings are saved, restart your Azure App Service.

---

## Configuration

All sensitive configuration values (like API keys, connection strings) should be stored in environment variables or a `.env` file for local development. For production, consider using [Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/general/) to store secrets securely.

---

## Project Structure

- **`app/main.py`**  
  Sets up the FastAPI application and includes routes from `views.py`.
- **`app/views.py`**  
  Contains endpoint definitions for submitting feedback (`/submit`) and viewing the admin dashboard (`/dashboard`).
- **`app/services/cognitive.py`**  
  Uses Azure Text Analytics for sentiment analysis and key phrase extraction.
- **`app/services/storage.py`**  
  Uploads files to Azure Blob Storage.
- **`app/services/db.py`**  
  Manages database connections and CRUD operations using SQLAlchemy.
- **`app/models/feedback.py`**  
  Defines the SQLAlchemy model for storing feedback entries.
- **`app/templates/`**  
  Contains HTML templates for the user feedback form and admin dashboard.
- **`static/css/`**  
  Contains basic CSS styling.

---

## Contributing

1. **Fork** the repository.  
2. **Create** a new branch for your feature or bugfix.  
3. **Commit** your changes.  
4. **Open a Pull Request** and describe your changes in detail.

We welcome contributions of all kinds, including new features, bug fixes, or documentation improvements.

---

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). Feel free to use and modify it to suit your needs.

---

**Enjoy building and expanding this AI-Powered Feedback Analysis Platform!**
