import os
import openai

from dotenv import load_dotenv

load_dotenv()


openai.api_key = os.getenv("OPENAI_KEY")


def get_openai_summarization(prompt: str, max_tokens: int, temperature: float | int):
    """Return summarized text

    Args:
        prompt (str): the input to feed the model
        max_tokens (int): maximum tokens to output
        temperature (float | int): parameter that controls randomness

    Returns:
        text: string
    """
    response = openai.Completion.create(
        model="text-curie-001",
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response
