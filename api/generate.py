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
        
        # Build the image prompt
        prompt = f"""Create a beautiful, inspirational image for a Bible verse.
        
Verse: {verse} ({version})
Theme: {theme}
{f"Personal message: {message}" if message else ""}

Style: Clean, modern, inspirational design with elegant typography. 
The image should have a {theme} background.
Include the verse reference "{verse}" in the image.
Make it suitable for sharing with family."""

        # Generate the image using DALL-E
        result = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        
        # Get the image URL from the response
        image_url = result.data[0].url
        
        # Save to data/verses.json
        # Note: In production, use a database like Vercel KV or PostgreSQL
        # For now, we'll return the data and you can manually update verses.json
        
        verse_data = {
            "verse": verse,
            "version": version,
            "message": message,
            "image_url": image_url,
            "date": None  # You can add timestamp here
        }
        
        # Return the image URL to the frontend
        response.status_code = 200
        response.headers["Content-Type"] = "application/json"
        response.body = json.dumps(verse_data)
        
        return response
        
    except Exception as e:
        response.status_code = 500
        response.headers["Content-Type"] = "application/json"
        response.body = json.dumps({
            "error": str(e)
        })
        return response
