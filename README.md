# CS524 Chatbot Project

This repository contains the final project for the CS524 Natural Language Processing course. The project implements an intelligent chatbot focused on Identity and Access Management (IAM) support, designed to assist users with SSO integrations, secrets management, and identity provisioning. The chatbot leverages a hybrid architecture combining structured dialog flows with advanced NLP capabilities for response generation and text summarization.

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Development Process](#development-process)
- [References](#references)

## Project Overview

### Motivation
As an IAM engineer, repetitive inquiries from customers regarding integrations (SSO, secrets management, identity provisioning) often lead to inefficiencies. This chatbot aims to reduce friction by providing guided, domain-specific conversations that convert unclear requests into engineering-ready artifacts. The system acts as a senior intake engineer, utilizing a structured knowledge base and NLP techniques to expedite understanding and improve customer interactions.

### Key Features
- **Structured Dialog Flows**: Guides users through IAM-specific scenarios using Microsoft Bot Framework
- **Response Generation**: NLP pipeline for generating contextually appropriate responses
- **Text Summarization**: BART-based summarization service for condensing long texts
- **Knowledge Base Integration**: Retrieval from IAM documentation and synthetic templates

### Target Audience
- IAM engineers seeking to streamline customer intake
- Customers requiring guidance on IAM integrations
- Developers interested in NLP applications in enterprise support systems

## Architecture

The system consists of two main microservices:

### 1. Chatbot REST Service (C#/.NET)
- **Framework**: Microsoft Bot Framework v4
- **Language**: C#
- **Purpose**: Handles user interactions, dialog management, and state persistence
- **Key Components**:
  - Dialog system with MainDialog, SsoFlowDialog, and HelpDialog (rule-based flows for simplicity)
  - Memory storage for conversation state
  - REST API endpoints for bot communication

### 2. NLP Service Stack (Python/FastAPI)
- **Framework**: FastAPI
- **Language**: Python
- **Purpose**: Provides NLP capabilities including response generation and summarization
- **Key Components**:
  - **Chatbot Inference**: Sequence-to-sequence model (Encoder-Decoder with LSTM) for generating responses
  - **Summarization Service**: BART (Bidirectional and Auto-Regressive Transformer) model for text summarization
  - **Model Artifacts**: Pre-trained TensorFlow/Keras models and metadata

### System Flow
```
User Input → Bot Framework (Dialog Management)
                    ↓
            NLP Service API Calls
                    ↓
Response Generation & Summarization
                    ↓
Summarized Output & Knowledge Retrieval
```

## Prerequisites

- **Operating System**: Windows 10/11, macOS, or Linux
- **.NET SDK**: Version 6.0 or later
- **Python**: Version 3.8 or later
- **Node.js**: Version 14 or later (for Bot Framework Emulator, optional)
- **Git**: For cloning the repository
- **Visual Studio** or **VS Code** with C# and Python extensions

## Installation and Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd cs524-chatbot-project
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up .NET Environment
Ensure .NET 6.0+ SDK is installed. The Bot Framework project is located in `chatbot/chatbot_rest_service/`.

### 4. Configure Model Artifacts
The NLP models are stored in `chatbot/nlp_service_stack/chatbot_artifacts/`. Ensure the following files are present:
- `encoder_model.keras`
- `decoder_model.keras`
- `metadata.json`

### 5. Prepare Dataset (Optional)
If you need to retrain models or modify the corpus:
```bash
cd dataset
python create_chatbot_corpus_file.py
```

## Usage

### Running the NLP Service
```bash
cd chatbot/nlp_service_stack
python main.py
```
The service will start on `http://localhost:8000` with endpoints:
- `GET /health`: Health check
- `POST /chatbot`: Generate chatbot response
- `POST /summarize`: Summarize text

### Running the Chatbot Service
```bash
cd chatbot/chatbot_rest_service
dotnet run
```
The bot service will start on `http://localhost:3978`.

### Testing the Chatbot
1. **Using Bot Framework Emulator**:
   - Download and install Bot Framework Emulator
   - Connect to `http://localhost:3978/api/messages`
   - Start chatting with the bot

2. **Direct API Testing**:
   - Use tools like Postman or curl to interact with the REST endpoints

### Example Interaction
```
User: I need help with SSO setup
Bot: I'd be happy to help you with Single Sign-On integration. What type of application are you trying to integrate?
...
```

## Directory Structure

```
cs524-chatbot-project/
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── LICENSE                      # Project license
├── hello_world.py               # Simple test script
├── book_exercise/               # Python exercises from textbook
│   ├── 1_1_4.py                 # Chapter 1, Exercise 1.4
│   ├── 1_2_2-1.py               # Chapter 1, Exercise 2.2 (part 1)
│   └── ...                      # Additional exercises
├── canvas_exercises/            # Course assignment exercises
│   ├── m1_d6.py                 # Module 1, Day 6 exercise
│   ├── m1_e4.py                 # Module 1, Exercise 4
│   ├──labs/                    # Lab assignments
│   │   ├── m2_g1/               # Module 2, Lab G1
│   │   └── ...
│   └── tfidf-example/          # TF-IDF exercises
│       ├── tf-idf-example.py   # TF-IDF implementation
│       └── tf-idf-example-advanced.py # Advanced TF-IDF
├── chatbot/                     # Main chatbot implementation
│   ├── chatbot_train.py         # Model training script
│   ├── chatbot_rest_service/    # C# Bot Framework service
│   │   ├── IamChatbot.csproj    # .NET project file
│   │   ├── Program.cs           # Application entry point
│   │   ├── Startup.cs           # Service configuration
│   │   ├── Dialogs/             # Bot dialog implementations
│   │   └── Controllers/         # API controllers
│   └── nlp_service_stack/       # Python NLP microservice
│       ├── main.py              # FastAPI application
│       ├── chatbot_inference.py # Seq2seq inference service
│       ├── summarization.py     # BART summarization service
│       └── chatbot_artifacts/   # Trained model files
├── dataset/                     # Training data and corpus
│   ├── chatbot_corpus.txt       # Compiled corpus
│   ├── create_chatbot_corpus_file.py # Corpus generation script
│   ├── books/                   # Source documents
│   ├── customer_support_tickets/# Support ticket data
│   └── iam-dev-resources/       # IAM documentation
├── models/                      # Trained model checkpoints
│   ├── lstm_m3_f1_lab/          # LSTM model for lab
    └── qa_dataset_seq2seq/      # Q&A seq2seq model

```

**Note**: The `book_exercise/` and `canvas_exercises/` directories contain standalone Python exercises and assignments completed during the course. These are not part of the main chatbot application but demonstrate foundational NLP concepts and implementation skills.

## Development Process

### Data Preparation
1. **Corpus Creation**: Compiled from multiple sources including IAM documentation, support tickets, and synthetic templates
2. **Preprocessing**: Text cleaning, tokenization, and sequence padding
3. **Dataset Generation**: Created Q&A pairs for training the seq2seq model

### Model Training
1. **Response Generation**: Trained LSTM-based sequence-to-sequence model for response generation
2. **Summarization**: Utilized pre-trained BART model for text summarization
3. **Evaluation**: Used BLEU scores and human evaluation for model assessment

### Service Integration
1. **Microservice Architecture**: Separated concerns between dialog management and NLP processing
2. **API Design**: RESTful endpoints for seamless service communication
3. **Error Handling**: Implemented robust error handling and logging

### Key Technologies and Techniques
- **NLP Techniques**: Tokenization, sequence modeling, attention mechanisms
- **Deep Learning**: LSTM networks, Transformer architecture (BART)
- **Software Engineering**: Microservices, REST APIs, dependency injection
- **Bot Development**: Dialog flows, state management, user experience design

## References

### Academic References
- "Natural Language Processing with Python" by Steven Bird, Ewan Klein, and Edward Loper
- CS524 Course Materials and Assignments

### Technical References
- **Microsoft Bot Framework**:
  - Repository: https://github.com/microsoft/botbuilder-dotnet
  - Documentation: https://learn.microsoft.com/en-us/azure/bot-service/
  - Samples: https://github.com/microsoft/BotBuilder-Samples

- **Hugging Face Transformers**:
  - BART Model: https://huggingface.co/facebook/bart-large-cnn
  - Documentation: https://huggingface.co/docs/transformers

- **TensorFlow/Keras**:
  - Documentation: https://www.tensorflow.org/guide/keras

- **GitHub Repositories**:
  - Q/A dataset generation: https://github.com/AyabongaQwabi/historybook_to_dataset
      - Forked repository: https://github.com/FenoCode/corpus_to_dataset
      - *NOTE:* This original repository was used as a reference for data preparation and model training. The forked version contains modifications specific to this project, including adjustments to the corpus and training scripts to better suit the chatbot's domain and requirements.