# AI Notes Summarizer

This project is an AI-powered notes summarizer that utilizes advanced natural language processing techniques to condense information from notes into concise summaries. The application is built using Python and leverages several technologies, including PostgreSQL for database management, Facehugger for model handling, and PyTorch for deep learning.

## Project Structure

```
ai-notes-summarizer
├── src
│   ├── main.py                # Entry point of the application
│   ├── summarizer             # Module for summarization logic
│   │   ├── __init__.py        # Initializes the summarizer module
│   │   ├── facehugger_interface.py  # Interface for Facehugger interactions
│   │   └── pytorch_model.py    # Defines the PyTorch model for summarization
│   ├── db                     # Module for database interactions
│   │   ├── __init__.py        # Initializes the database module
│   │   └── postgres_connector.py  # Connects to PostgreSQL database
│   └── aws                    # Module for AWS interactions
│       ├── __init__.py        # Initializes the AWS module
│       └── s3_utils.py        # Utility functions for AWS S3
├── Dockerfile                  # Docker configuration for the application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── docker-compose.yml          # Docker services configuration
```

## Technologies Used

- **Facehugger**: A library that simplifies the use of transformer models for natural language processing tasks. In this project, Facehugger is used to load pre-trained models and perform text summarization efficiently.
  
- **PyTorch**: An open-source machine learning library that provides tools for building and training deep learning models. The summarization model is implemented using PyTorch, allowing for flexibility and scalability in training and inference.

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd ai-notes-summarizer
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Set up the PostgreSQL database**:
   - Ensure you have PostgreSQL installed and running.
   - Create a database for the application and update the connection settings in `src/db/postgres_connector.py`.

4. **Run the application**:
   ```
   python src/main.py
   ```

5. **Using Docker**:
   - Build the Docker image:
     ```
     docker build -t ai-notes-summarizer .
     ```
   - Run the application using Docker Compose:
     ```
     docker-compose up
     ```

## Usage

Once the application is running, you can input notes, and the summarizer will generate concise summaries using the underlying Facehugger and PyTorch models. The results can be stored in the PostgreSQL database or uploaded to AWS S3 for further processing.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features you would like to add.