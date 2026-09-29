import os

from functools import lru_cache

from dotenv import load_dotenv


load_dotenv()


try:

    from google import genai

except ImportError:

    genai = None


@lru_cache(maxsize=1)
def get_client():

    api_key = (
        os.getenv("GEMINI_API_KEY")
        or
        os.getenv("GOOGLE_API_KEY")
    )


    if not api_key:

        return None


    if genai is None:

        raise RuntimeError(
            "google-genai is not installed. "
            "Run: pip install -r requirements.txt"
        )


    return genai.Client(
        api_key=api_key
    )


def generate_text(
    prompt: str,
    model: str
):

    client = get_client()


    if client is None:

        raise RuntimeError(
            "Gemini API key is not configured. "
            "Add GEMINI_API_KEY to your .env file."
        )


    response = client.models.generate_content(

        model=model,

        contents=prompt
    )


    text = getattr(
        response,
        "text",
        None
    )


    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )


    return text.strip()