import os
from typing import Literal
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "Creator Studio AI",
    instructions=(
        "You are Creator Studio AI, a practical assistant for original science-documentary "
        "and YouTube Shorts production. Help users create scripts, scene plans, visual prompts, "
        "voiceover directions, editing plans, and YouTube metadata. Do not claim to render or "
        "export actual media; these tools create production-ready plans and prompts."
    ),
    host="0.0.0.0",
    port=int(os.getenv("PORT", "8000")),
)

@mcp.tool()
def build_video_brief(
    topic: str,
    duration_seconds: int = 45,
    audience: str = "general audience",
    language: str = "English",
    format: Literal["YouTube Short", "YouTube video", "Instagram Reel"] = "YouTube Short",
    visual_style: str = "cinematic 3D animated documentary",
) -> str:
    """Create a structured creative brief for a short-form video."""
    if not topic.strip():
        return "Please provide a topic."
    duration_seconds = max(10, min(duration_seconds, 180))
    return f"""CREATOR STUDIO AI — VIDEO BRIEF

Topic: {topic}
Format: {format}
Target duration: {duration_seconds} seconds
Audience: {audience}
Language: {language}
Visual direction: {visual_style}

Creative objective:
Explain one fascinating idea clearly, with a strong opening hook, escalating curiosity,
accurate information, and a memorable ending.

Structure:
1. Hook (0–3 sec): surprising question or visual.
2. Setup (3–10 sec): introduce the subject.
3. Main explanation: 3–5 concise beats with visual changes.
4. Payoff: reveal the key science/fact.
5. Ending: concise takeaway and one natural engagement question.

Production rules:
- Use original wording and factual claims that can be verified.
- Keep narration concise and conversational.
- Design each scene to be visually distinct.
- Do not imitate a specific living artist or copyrighted studio's exact style.
"""

@mcp.tool()
def create_scene_plan(
    topic: str,
    scene_count: int = 6,
    duration_seconds: int = 45,
    visual_style: str = "high-quality stylized 3D animated documentary",
) -> str:
    """Create a timed scene-by-scene storyboard and visual prompts."""
    scene_count = max(3, min(scene_count, 12))
    duration_seconds = max(10, min(duration_seconds, 180))
    per_scene = duration_seconds / scene_count
    lines = [
        f"STORYBOARD: {topic}",
        f"Total duration: {duration_seconds}s | Scenes: {scene_count}",
        f"Visual style: {visual_style}",
        "",
    ]
    for i in range(scene_count):
        start = round(i * per_scene, 1)
        end = round((i + 1) * per_scene, 1)
        if i == 0:
            role = "HOOK — begin with a striking close-up or unexpected action."
        elif i == scene_count - 1:
            role = "PAYOFF — show the key reveal and finish on a memorable frame."
        else:
            role = f"EXPLANATION BEAT {i} — introduce one new visual fact or action."
        lines.append(
            f"SCENE {i+1} ({start}s–{end}s)\n"
            f"Purpose: {role}\n"
            f"Image prompt: {visual_style}; topic: {topic}; cinematic composition, "
            f"clear subject, expressive action, rich environmental detail, coherent "
            f"lighting, vertical 9:16 framing, no text, no watermark.\n"
            f"Motion prompt: slow deliberate camera movement, natural subject motion, "
            f"subtle environmental movement, preserve character and scene continuity.\n"
            f"Voiceover: Write 1–2 short sentences explaining this beat.\n"
            f"Sound: Add one relevant ambient layer and one restrained accent."
        )
    return "\n\n".join(lines)

@mcp.tool()
def write_voiceover_script(
    topic: str,
    duration_seconds: int = 45,
    language: str = "English",
    tone: str = "curious, clear, documentary",
) -> str:
    """Return a scriptwriting brief with a timed narration structure."""
    duration_seconds = max(10, min(duration_seconds, 180))
    approx_words = round(duration_seconds * 2.2)
    return f"""Write an original {language} voiceover about: {topic}

Target duration: {duration_seconds} seconds
Approximate word budget: {approx_words} words
Tone: {tone}

Required structure:
- 0–3s: a compelling hook.
- Next 20%: establish the question or mystery.
- Middle 60%: explain the idea in simple, accurate steps.
- Final 20%: deliver the reveal and a memorable closing line.

Requirements:
- Natural spoken language; short sentences.
- No unsupported statistics or fabricated facts.
- Add [PAUSE] and [EMPHASIS] sparingly.
- Avoid filler intros such as "Welcome back".
- End with one concise audience question.
"""

@mcp.tool()
def generate_youtube_package(
    topic: str,
    audience_region: str = "United States",
    language: str = "English",
    format: Literal["Short", "Long-form"] = "Short",
) -> str:
    """Create YouTube title, description, hashtags, tags, and upload checklist."""
    return f"""YOUTUBE PUBLISHING PACKAGE

Topic: {topic}
Target region: {audience_region}
Language: {language}
Format: {format}

TITLE OPTIONS
1. Curiosity-led: [Create a concise question about {topic}]
2. Discovery-led: [Reveal an unexpected fact about {topic}]
3. Explanation-led: [Explain why/how {topic} happens]

DESCRIPTION
Open with one sentence that creates curiosity. Explain what viewers will learn.
Use accurate claims only. End with a natural question and a brief channel call-to-action.

HASHTAGS
Use 3–5 relevant hashtags. Include the topic, subject category, and format where relevant.

TAGS
Create a comma-separated list of close topic variants, common search phrases, and
relevant subject terms. Avoid unrelated trending tags.

UPLOAD CHECKLIST
- Confirm the first 1–2 seconds deliver the promised hook.
- Check captions, spelling, audio levels, and visual continuity.
- Confirm rights for music, footage, images, and voice.
- Choose the correct audience setting and paid-promotion disclosure if applicable.
- Review thumbnail/frame, title, description, and visibility before publishing.
"""

@mcp.tool()
def create_editing_blueprint(
    duration_seconds: int = 45,
    aspect_ratio: Literal["9:16", "16:9", "1:1"] = "9:16",
    captions: bool = True,
    music: bool = True,
) -> str:
    """Create a practical editing/export checklist for a short video."""
    duration_seconds = max(10, min(duration_seconds, 600))
    return f"""EDITING BLUEPRINT

Duration: {duration_seconds}s
Aspect ratio: {aspect_ratio}
Captions: {"Yes" if captions else "No"}
Music/SFX: {"Yes" if music else "No"}

Timeline:
- Put the strongest visual and hook in the opening 1–2 seconds.
- Remove dead air and unnecessary transitions.
- Change shot scale or camera movement when the narration changes idea.
- Keep captions readable and inside platform-safe areas.
- Duck music under narration; avoid clipping and sudden loudness changes.
- Use sound effects only when they reinforce an action or reveal.
- Hold the final payoff long enough to understand.

Quality control:
- Check voice intelligibility on phone speakers.
- Check captions against the final voiceover.
- Check aspect ratio, frame edges, and export resolution.
- Review the full export once before upload.
"""

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
