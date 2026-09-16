import os
from dotenv import load_dotenv

from google.cloud import translate_v3 as translate

client = translate.TranslationServiceClient()

load_dotenv()  # Load environment variables from .env file
project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")

response = client.translate_text(
    request={
        "parent": f"projects/{project_id}/locations/global",
        "contents": ["My name is Larz."],
        "mime_type": "text/plain",
        "source_language_code": "en",
        "target_language_code": "zh",
    }
)

print(response.translations[0].translated_text)
