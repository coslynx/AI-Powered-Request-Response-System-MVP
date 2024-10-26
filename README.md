<div class="hero-icon" align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
</div>

<h1 align="center">
AI-Powered-Request-Response-System-MVP
</h1>
<h4 align="center">A Python backend that simplifies interaction with OpenAI's powerful language models.</h4>
<h4 align="center">Developed with the software and tools below.</h4>
<div class="badges" align="center">
  <img src="https://img.shields.io/badge/Framework-FastAPI-blue" alt="FastAPI Framework" />
  <img src="https://img.shields.io/badge/Backend-Python-red" alt="Python Backend" />
  <img src="https://img.shields.io/badge/Database-PostgreSQL-blue" alt="PostgreSQL Database" />
  <img src="https://img.shields.io/badge/LLMs-OpenAI-black" alt="OpenAI Language Models" />
</div>
<div class="badges" align="center">
  <img src="https://img.shields.io/github/last-commit/coslynx/AI-Powered-Request-Response-System-MVP?style=flat-square&color=5D6D7E" alt="git-last-commit" />
  <img src="https://img.shields.io/github/commit-activity/m/coslynx/AI-Powered-Request-Response-System-MVP?style=flat-square&color=5D6D7E" alt="GitHub commit activity" />
  <img src="https://img.shields.io/github/languages/top/coslynx/AI-Powered-Request-Response-System-MVP?style=flat-square&color=5D6D7E" alt="GitHub top language" />
</div>

## 📑 Table of Contents
- 📍 Overview
- 📦 Features
- 📂 Structure
- 💻 Installation
- 🏗️ Usage
- 🌐 Hosting
- 📄 License
- 👏 Authors

## 📍 Overview
This repository contains the backend for an AI Powered Request Response System built with Python, FastAPI, and PostgreSQL. This MVP aims to provide a streamlined and efficient way to access OpenAI's powerful language models.

## 📦 Features
|    | Feature            | Description                                                                                                        |
|----|--------------------|--------------------------------------------------------------------------------------------------------------------|
| ⚙️ | **Architecture**   | The backend follows a modular architecture with separate components for request handling, API interaction, response formatting, and database management, ensuring maintainability and scalability. |
| 📄 | **Documentation**  | The repository includes a README file that provides a comprehensive overview of the MVP, its dependencies, and usage instructions.|
| 🔗 | **Dependencies**   | The codebase relies on various external libraries and packages, including FastAPI, OpenAI, SQLAlchemy, and PostgreSQL,  which are essential for building the API, interacting with OpenAI, and managing data storage. |
| 🧩 | **Modularity**     | The modular structure enables easier maintenance and reusability, with separate modules for different functionalities, ensuring a clean and organized codebase. |
| 🧪 | **Testing**        |  Unit tests are implemented using the `pytest` framework to ensure the reliability and robustness of the core functionalities.       |
| ⚡️  | **Performance**    | The backend is designed for efficient request handling and response processing, leveraging asynchronous operations and potential caching mechanisms. |
| 🔐 | **Security**       |  The backend prioritizes security through robust input validation, secure API key management, and adherence to best practices for data handling. |
| 🔀 | **Version Control**|  The repository utilizes Git for version control, facilitating collaboration and tracking code changes. |
| 🔌 | **Integrations**   |  The backend seamlessly integrates with the OpenAI API using its Python library, enabling communication with powerful language models like GPT-3. |
| 📶 | **Scalability**    | The backend is designed with scalability in mind, utilizing frameworks like FastAPI and PostgreSQL that offer horizontal scalability features for handling increased user load. |

## 📂 Structure
```text
├── config.py
├── startup.sh
├── commands.json
├── main.py
├── requirements.txt
├── database
│   ├── __init__.py
│   └── models.py
├── utils
│   ├── __init__.py
│   └── openai_api_call.py
└── routers
    └── process.py
```

## 💻 Installation
### 🔧 Prerequisites
- Python 3.9+
- Docker and Docker Compose
- PostgreSQL
- OpenAI API Key (obtain from [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys))

### 🚀 Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/coslynx/AI-Powered-Request-Response-System-MVP.git
   cd AI-Powered-Request-Response-System-MVP
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database:
   ```bash
   docker-compose up -d database
   alembic upgrade head
   ```
4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Fill in the required environment variables: OPENAI_API_KEY, DATABASE_URL
   ```

## 🏗️ Usage
### 🏃‍♂️ Running the MVP
1. Start the development server:
   ```bash
   uvicorn main:app --reload
   ```

## 🌐 Hosting
### 🚀 Deployment Instructions
1. Build the Docker image:
   ```bash
   docker build -t ai-request-response-system .
   ```
2. Run the container:
   ```bash
   docker run -d -p 8000:8000 ai-request-response-system
   ```

## 📜 API Documentation
### 🔍 Endpoints
- **POST /process**
    - Description: Processes a user request using OpenAI's language models.
    - Request Body (JSON):
        ```json
        {
          "text": "Your request to the AI",
          "model": "text-davinci-003" // Optional, defaults to text-davinci-003
        }
        ```
    - Response (JSON):
        ```json
        {
          "response": "AI generated response"
        }
        ```


## 📄 License & Attribution

### 📄 License
This Minimum Viable Product (MVP) is licensed under the [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/) license.

### 🤖 AI-Generated MVP
This MVP was entirely generated using artificial intelligence through [CosLynx.com](https://coslynx.com).

No human was directly involved in the coding process of the repository: AI-Powered-Request-Response-System-MVP

### 📞 Contact
For any questions or concerns regarding this AI-generated MVP, please contact CosLynx at:
- Website: [CosLynx.com](https://coslynx.com)
- Twitter: [@CosLynxAI](https://x.com/CosLynxAI)

<p align="center">
  <h1 align="center">🌐 CosLynx.com</h1>
</p>
<p align="center">
  <em>Create Your Custom MVP in Minutes With CosLynxAI!</em>
</p>
<div class="badges" align="center">
<img src="https://img.shields.io/badge/Developers-Drix10,_Kais_Radwan-red" alt="">
<img src="https://img.shields.io/badge/Website-CosLynx.com-blue" alt="">
<img src="https://img.shields.io/badge/Backed_by-Google,_Microsoft_&_Amazon_for_Startups-red" alt="">
<img src="https://img.shields.io/badge/Finalist-Backdrop_Build_v4,_v6-black" alt="">
</div>