import os
from pathlib import Path
from typing import Literal
import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse
from starlette.routing import Mount, Route

BASE = Path(__file__).resolve().parent
mcp = FastMCP("Creator Studio AI", instructions="Create original science documentary and YouTube Shorts production plans, scripts, prompts and metadata. Do not claim to render or export media.", host="0.0.0.0", port=int(os.getenv("PORT", "8000")))

@mcp.tool()
def build_video_brief(topic: str, duration_seconds: int = 45, audience: str = "general audience", language: str = "English", format: Literal["YouTube Short", "YouTube video", "Instagram Reel"] = "YouTube Short", visual_style: str = "cinematic 3D animated documentary") -> str:
    """Create a structured creative brief."""
    if not topic.strip(): return "Please provide a topic."
    duration_seconds = max(10, min(duration_seconds, 180))
    return f"""VIDEO BRIEF\nTopic: {topic}\nFormat: {format}\nDuration: {duration_seconds}s\nAudience: {audience}\nLanguage: {language}\nVisual direction: {visual_style}\n\nStructure: 0–3s hook; 3–10s setup; 3–5 explanation beats; key reveal; memorable ending.\nRules: original wording, verifiable facts, concise narration, visually distinct scenes. Do not imitate a specific living artist or copyrighted studio's exact style."""

@mcp.tool()
def create_scene_plan(topic: str, scene_count: int = 6, duration_seconds: int = 45, visual_style: str = "high-quality stylized 3D animated documentary") -> str:
    """Create a timed storyboard and visual prompts."""
    scene_count = max(3, min(scene_count, 12)); duration_seconds = max(10, min(duration_seconds, 180))
    step = duration_seconds / scene_count; out = [f"STORYBOARD: {topic}", f"Duration: {duration_seconds}s | Scenes: {scene_count}", f"Style: {visual_style}"]
    for i in range(scene_count):
        a, b = round(i*step, 1), round((i+1)*step, 1)
        role = "HOOK" if i == 0 else ("PAYOFF" if i == scene_count-1 else f"EXPLANATION BEAT {i}")
        out.append(f"SCENE {i+1} ({a}s–{b}s)\nPurpose: {role}\nImage prompt: {visual_style}; {topic}; cinematic composition, clear subject, expressive action, rich detail, vertical 9:16, no text or watermark.\nMotion: natural subject motion, deliberate camera movement, continuity preserved.\nVoiceover: 1–2 short explanatory sentences.\nSound: relevant ambience and restrained accent.")
    return "\n\n".join(out)

@mcp.tool()
def write_voiceover_script(topic: str, duration_seconds: int = 45, language: str = "English", tone: str = "curious, clear, documentary") -> str:
    """Create a timed narration writing brief."""
    duration_seconds = max(10, min(duration_seconds, 180))
    return f"Write an original {language} voiceover about: {topic}\nDuration: {duration_seconds}s; approx. {round(duration_seconds*2.2)} words; tone: {tone}.\nStructure: 0–3s hook; next 20% mystery/setup; middle 60% simple accurate explanation; final 20% reveal and closing. Use short spoken sentences, no fabricated facts, sparse [PAUSE]/[EMPHASIS], finish with one audience question."

@mcp.tool()
def generate_youtube_package(topic: str, audience_region: str = "United States", language: str = "English", format: Literal["Short", "Long-form"] = "Short") -> str:
    """Create YouTube metadata guidance and upload checklist."""
    return f"""YOUTUBE PUBLISHING PACKAGE\nTopic: {topic}\nRegion: {audience_region}\nLanguage: {language}\nFormat: {format}\n\nTITLE OPTIONS\n1. Curiosity-led question about {topic}\n2. Discovery-led unexpected fact about {topic}\n3. Explain why/how {topic} happens\n\nDESCRIPTION\nOpen with curiosity, explain what viewers learn, use accurate claims, end with a natural question and brief CTA.\n\nHASHTAGS\nUse 3–5 relevant hashtags.\n\nTAGS\nUse close topic variants and relevant search phrases; avoid unrelated trending tags.\n\nUPLOAD CHECKLIST\nCheck hook, captions, audio, continuity, rights, audience setting, disclosures, title, description and visibility."""

@mcp.tool()
def create_editing_blueprint(duration_seconds: int = 45, aspect_ratio: Literal["9:16", "16:9", "1:1"] = "9:16", captions: bool = True, music: bool = True) -> str:
    """Create an editing and quality-control checklist."""
    duration_seconds = max(10, min(duration_seconds, 600))
    return f"""EDITING BLUEPRINT\nDuration: {duration_seconds}s\nAspect ratio: {aspect_ratio}\nCaptions: {captions}\nMusic/SFX: {music}\n\nPut strongest hook in first 1–2s; remove dead air; change shots with idea changes; keep captions readable; duck music under narration; use purposeful SFX; hold final payoff. QC: phone-speaker intelligibility, caption accuracy, aspect ratio, frame edges, export resolution and full playback review."""

async def home(request: Request):
    return FileResponse(BASE / "dashboard" / "index.html")

async def endpoint(request: Request, fn):
    try:
        data = await request.json()
        if not isinstance(data, dict): return JSONResponse({"error": "JSON object required"}, status_code=400)
        return JSONResponse({"result": fn(**data)})
    except TypeError as e: return JSONResponse({"error": f"Invalid input: {e}"}, status_code=400)
    except Exception: return JSONResponse({"error": "Request failed. Check inputs and retry."}, status_code=500)

async def brief(r): return await endpoint(r, build_video_brief)
async def scenes(r): return await endpoint(r, create_scene_plan)
async def voice(r): return await endpoint(r, write_voiceover_script)
async def youtube(r): return await endpoint(r, generate_youtube_package)
async def edit(r): return await endpoint(r, create_editing_blueprint)

app = Starlette(routes=[
    Route("/", home, methods=["GET"]),
    Route("/api/brief", brief, methods=["POST"]),
    Route("/api/scenes", scenes, methods=["POST"]),
    Route("/api/voice", voice, methods=["POST"]),
    Route("/api/youtube", youtube, methods=["POST"]),
    Route("/api/edit", edit, methods=["POST"]),
    Mount("/mcp", app=mcp.streamable_http_app()),
])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
