import os
from urllib import response
from dotenv import load_dotenv

from google.cloud import translate_v3 as translate

client = translate.TranslationServiceClient()

load_dotenv()  # Load environment variables from .env file
project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")

def translate(text, source_language="en", target_language="zh"): # TODO: HARDCODED CHANGE IN FUTURE
    response = client.translate_text(
        request={
            "parent": f"projects/{project_id}/locations/global",
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    return response.translations[0].translated_text
