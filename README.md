# Creator Studio AI Dashboard update

Upload these files to the root of https://github.com/shiv2098/creator-studio-ai-:
- Replace `server.py`
- Replace `requirements.txt`
- Add `dashboard/index.html` (create the dashboard folder)
- Optionally replace `README.md`

Then commit to `main`. Your existing Render service is configured for automatic deployment. Wait for its next deployment to show **Live**, then open the Render URL on your phone.

Dashboard: `/` | MCP endpoint: `/mcp`

Features: Video Brief, Scene Plan, Voiceover Brief, YouTube Package, Editing Blueprint, Copy and Save .txt.

Limitations: this creates text plans and prompts only, not rendered images/audio/video or MP4 exports. The service has no authentication; anyone with its public URL can use it. Do not enter secrets or private data. Add authentication and rate limiting before public sharing.
