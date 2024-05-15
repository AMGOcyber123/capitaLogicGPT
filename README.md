# CapitaLogic - Financial Consultancy-based LLM-model

## Project Overview

This project aims to develop an intelligent sales chatbot dedicated to providing guidance and insights into investment opportunities, focusing on financial products such as mutual funds. By harnessing advanced conversational AI techniques, this chatbot engages users in meaningful dialogues tailored to their investment preferences and goals.

## Objectives

- **Enhance Investment Advisory Services:** Utilize AI to deliver personalized, accurate investment advice.
- **Improve User Engagement:** Provide a conversational interface for an intuitive user experience.
- **Incorporate Data Analytics:** Integrate an Excel analyzer module for processing user-uploaded financial data.

## Features

- **Conversational AI:** Uses GPT-3.5-turbo models to understand and generate human-like responses.
- **Data Analytics:** Allows users to upload Excel files for personalized advice based on their financial data.
- **User-friendly Interface:** Designed to be accessible on both desktop and mobile platforms.


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourgithubusername/financial-llm-model.git
   ```

2. Install dependencies:
    ```bash
    cd financial-llm-model
    pip install -r requirements.txt
    ```
Once you have obtained the relevant API keys, you can stored them in a .env file, in the following format:
```bash
OPENAI_API_KEY="fill me in"
SERPER_API_KEY="fill me in"
```

## Run the Project
```bash
docker-compose up -build
```
