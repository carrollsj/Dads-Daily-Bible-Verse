import os
import json
from openai import OpenAI

def handler(request):
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Missing OPENAI_API_KEY environment variable")

        # ✅ Initialize OpenAI client (works with sk-proj keys)
        client = OpenAI(api_key=api_key)

        # Handle Vercel test and POST requests
        try:
            body = json.loads(request.body)
        except Exception:
            body = {}

        verse = body.get("verse", "Psalm 23:1")
        version = body.get("version", "CSB")
        message = body.get("message", "")
        theme = body.get("theme", "nature")

        # ✅ Generate an image (simple text prompt)
        prompt = f"Create a serene background for the Bible verse '{verse}' in {version} about {theme}, add text 'Love Dad' in bottom right."

        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_url = result.data[0].url
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"image_url": image_url})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
