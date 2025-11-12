import os
import json
from openai import OpenAI

def handler(request):
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Missing OPENAI_API_KEY environment variable")

        client = OpenAI(api_key=api_key)

        # Handle both Vercel test requests and POST requests
        try:
            body = json.loads(request.body)
        except Exception:
            body = {}

        verse = body.get("verse", "Psalm 23:1")
        version = body.get("version", "CSB")
        message = body.get("message", "")
        theme = body.get("theme", "nature")

        prompt = (
            f"Photorealistic {theme} scene inspired by the verse {verse} ({version}). "
            f"Include nature, peace, and divine light."
        )

        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_url = response.data[0].url

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "image_url": image_url,
                "verse": verse,
                "message": message,
                "theme": theme
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
