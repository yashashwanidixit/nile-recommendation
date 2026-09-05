class LLMClient:
    """Abstract interface for LLM calls."""

    def generate(self, prompt: str) -> str:
        """Send prompt to the LLM and return the text response.

        Args:
            prompt: Text prompt with instructions and candidate data.

        Returns:
            Raw response string from the model.

        Raises:
            NotImplementedError: In this initial foundation stage.
        """
        raise NotImplementedError("LLM client is not yet configured with an active provider.")
