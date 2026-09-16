from google.cloud import translate_v3 as translate

client = translate.TranslationServiceClient()

project_id = "project-d46d15ba-c5a2-41e0-93d"

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