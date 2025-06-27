# filepath: ai-notes-summarizer/ai-notes-summarizer/src/main.py

"""
This is the entry point of the AI Notes Summarizer application.
It initializes the application, sets up the database connection,
and orchestrates the summarization process using Facehugger and PyTorch.
"""

from db.postgres_connector import connect_to_db
from summarizer.facehugger_interface import summarize_text
from summarizer.pytorch_model import PyTorchSummarizer

def main():
    # Initialize database connection
    db_connection = connect_to_db()
    
    # Initialize the summarization model
    summarizer = PyTorchSummarizer()

    # Example text to summarize
    text_to_summarize = "Your long text goes here."

    # Perform summarization
    summary = summarize_text(text_to_summarize, summarizer)

    # Output the summary
    print("Summary:", summary)

if __name__ == "__main__":
    main()