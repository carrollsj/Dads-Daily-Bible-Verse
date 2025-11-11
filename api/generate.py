from openai import OpenAI
import os, json

client = OpenAI(api_key=os.getenv("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"))

def handler(request):
    try:
        data = request.json()
        verse = data.get("verse", "")
        version = data.get("version", "CSB")
        message = data.get("message", "")
        theme = data.get("theme", "nature")

        prompt = (
            f"Photorealistic {theme} scene, high-resolution, beautiful lighting, "
            f"inspired by the verse {verse} ({version}). "
            f"Include subtle spiritual warmth, like divine sunlight or peace."
        )

        # Generate image
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_url = response.data[0].url

        return {
            "statusCode": 200,
            "body": json.dumps({
                "image_url": image_url,
                "verse": verse,
                "message": message,
                "theme": theme
            }),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }

