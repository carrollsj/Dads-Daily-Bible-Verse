import os
import json
import traceback
from openai import OpenAI

def _json(obj, code=200):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(obj),
    }

def handler(request):
    try:
        # 1) method guard: only allow POST so GET shows a friendly message
        method = getattr(request, "method", "GET")
        if method != "POST":
            return _json({
                "ok": False,
                "message": "Use POST with JSON body: { verse, version, message, theme }"
            }, 405)

        # 2) env var
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return _json({"ok": False, "error": "Missing OPENAI_API_KEY env var"}, 500)

        # 3) body parsing (Vercel passes a string in request.body)
        try:
            body = json.loads(getattr(request, "body", "{}") or "{}")
        except Exception:
            body = {}

        verse   = body.get("verse", "Psalm 23:1")
        version = body.get("version", "CSB")
        message = body.get("message", "")
        theme   = body.get("theme", "nature")

        # 4) OpenAI client (works with sk-proj keys)
        client = OpenAI(api_key=api_key)

        prompt = (
            f"Photorealistic {theme} scene for the Bible verse '{verse}' ({version}), "
            f"peaceful, beautiful lighting. Include text overlay 'Love Dad' bottom-right."
        )

        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_url = result.data[0].url
        return _json({"ok": True, "image_url": image_url}, 200)

    except Exception as e:
        # write full traceback so it appears in Vercel Runtime Logs
        print("ERROR in /api/generate:", e)
        traceback.print_exc()
        return _json({"ok": False, "error": str(e)}, 500)
