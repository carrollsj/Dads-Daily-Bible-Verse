import os
import json
from openai import OpenAI

def handler(request):
    try:
        # Get OpenAI API key from environment variables
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Missing OPENAI_API_KEY environment variable")

        # Initialize client
        client = OpenAI(api_key=api_key)

        # Parse incoming request body
        try:
            body = json.loads(request.body)
        except Exception:
            body = {}

        verse = body.get("verse", "Psalm 23:1")
        version = body.get("version", "CSB")
        message = body.get("message", "")
        theme = body.get("theme", "nature")

        # Call OpenAI API to generate a description (text only for now)
        response = client.responses.create(
            model="gpt-4o-mini",
            input=f"Create a short peaceful devotional caption for {verse} ({version}) with a {theme} theme. Message: {message}"
        )

        text_output = response.output[0].content[0].text

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"verse": verse, "caption": text_output})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
