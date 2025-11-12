import os
import json
from openai import OpenAI

def handler(request, response):
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Missing OPENAI_API_KEY environment variable")

        client = OpenAI(api_key=api_key)

        try:
            body = json.loads(request.body)
        except Exception:
            body = {}

        verse = body.get("verse", "Psalm 23:1")
        version = body.get("version", "CSB")
        message = body.get("message", "")
        theme = body.get("theme", "nature")

        result = client.responses.create(
            model="gpt-4o-mini",
            input=f"Create a short devotional caption for {verse} ({version}) with a {theme} theme. Message: {message}"
        )

        caption = result.output[0].content[0].text

        response.status_code = 200
        response.headers["Content-Type"] = "application/json"
        response.body = json.dumps({"verse": verse, "caption": caption})
        return response

    except Exception as e:
        response.status_code = 500
        response.headers["Content-Type"] = "application/json"
        response.body = json.dumps({"error": str(e)})
        return response
