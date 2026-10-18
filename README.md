# Big Brains AI Customer Support Agent

An AI-powered customer support chatbot built with Django, Python, Retrieval-Augmented Generation (RAG), ChromaDB, and sentence-transformer embeddings.

## Project Overview

This project provides an interactive chatbot that answers customer questions using a knowledge base and AI-powered response generation. It is designed to help users find relevant information quickly.

## Features

- Interactive chatbot interface
- Django-based web application
- Retrieval-Augmented Generation (RAG)
- Semantic search using vector embeddings
- ChromaDB vector database integration
- Knowledge-base-based question answering
- Environment-based API key configuration

## Tech Stack

- **Backend:** Python, Django
- **AI Integration:** Google Gemini API
- **RAG:** Retrieval-Augmented Generation
- **Vector Database:** ChromaDB
- **Embeddings:** Sentence Transformers
- **Frontend:** HTML, CSS, JavaScript

## Project Structure

```text
bigbrains_support/
├── bigbrains_support/
├── chat/
├── screenshots/
├── knowledge_base.json
├── manage.py
└── .gitignore
```

## Setup Instructions

1. Clone this repository:

   ```bash
   git clone https://github.com/Rafay-Baloch/bigbrains-rag-customer-support-agent.git
   ```

2. Open the project directory:

   ```bash
   cd bigbrains-rag-customer-support-agent
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   Windows:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the project root and add your own API key:

   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

   Never commit your real API key or `.env` file to GitHub.

6. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

7. Start the development server:

   ```bash
   python manage.py runserver
   ```

8. Open `http://127.0.0.1:8000/` in your browser.

## Security

Store API keys in environment variables. Do not publish API keys, passwords, or other sensitive credentials.

## Author

**Abdur Rafay Hassan Baloch**

GitHub: [Rafay-Baloch](https://github.com/Rafay-Baloch)

linkedin:(https://www.linkedin.com/in/abdur-rafay-hassan-baloch-0860b9225/?isSelfProfile=true)
