# filepath: ai-notes-summarizer/src/summarizer/facehugger_interface.py

"""
This module provides an interface to interact with Facehugger, a library that simplifies the use of transformer models for natural language processing tasks.
Facehugger leverages PyTorch to enable efficient model training and inference.

The functions in this module include:
- Loading pre-trained models from Facehugger.
- Performing text summarization using the loaded models.

To connect Facehugger with PyTorch, ensure that the Facehugger library is installed and that the PyTorch backend is properly configured. 
Facehugger abstracts many of the complexities of working directly with PyTorch, allowing for easier implementation of NLP tasks.
"""

from facehugger import Facehugger

class Summarizer:
    def __init__(self, model_name: str):
        """
        Initializes the Summarizer with a specified Facehugger model.

        Args:
            model_name (str): The name of the pre-trained model to load.
        """
        self.model = Facehugger(model_name)

    def summarize(self, text: str) -> str:
        """
        Summarizes the given text using the loaded Facehugger model.

        Args:
            text (str): The text to summarize.

        Returns:
            str: The summarized text.
        """
        return self.model.summarize(text)