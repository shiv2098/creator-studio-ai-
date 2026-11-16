# Creator Studio AI

A free-first MCP starter server for planning short-form videos. It exposes tools for:
- Video briefs
- Scene-by-scene storyboards and visual prompts
- Voiceover script briefs
- YouTube metadata packages
- Editing blueprints

## Important limitations

This first version creates production plans and prompts. It does **not** render images,
generate video, synthesize voice, or export MP4 files. Those capabilities require external
services and may have free-tier limits or paid usage. No paid API key is required for the
included tools.

## 1. Run locally

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python server.py
```

The MCP server uses Streamable HTTP. The default port is 8000; the deployment platform can
provide a `PORT` environment variable.

## 2. Put it on GitHub

1. Sign in at https://github.com
2. Create a new **private** repository named `creator-studio-ai`.
3. Upload the contents of this folder (not the ZIP itself).
4. Keep the repository private while testing. Never commit API keys or passwords.

## 3. Deploy for free (testing only)

The included `render.yaml` is a Render Blueprint starting point. In Render:
1. Sign in at https://render.com
2. Choose New > Blueprint.
3. Connect the GitHub repository.
4. Review the service and deploy.
5. Copy the public HTTPS service URL.

Free web services may sleep when idle and have resource/availability limits. This is suitable
for experimentation, not a production guarantee. Verify that the deployed MCP endpoint is
reachable at `https://YOUR-SERVICE/mcp`.

## 4. Connect to ChatGPT

ChatGPT custom MCP availability is plan- and workspace-dependent. Current OpenAI help
documentation lists custom MCP server connections for Business and Enterprise/Edu workspaces;
Pro has more limited read/fetch support. Go is not listed as supported for custom MCP server
connections. Custom MCP setup is web-only, not Android-app-only.

If your account/workspace offers Plugins > Add custom MCP server:
1. Open ChatGPT on the web.
2. Go to Plugins, press +, then Add custom MCP server.
3. Enter `https://YOUR-SERVICE/mcp`.
4. Select the authentication method supported by your server (this starter is unauthenticated;
   do not expose private user data or sensitive actions).
5. Review the warning, create the plugin, and test each tool.

If this option is not available, the server can still be tested with an MCP Inspector or used
from another MCP-compatible client, but it cannot be forced into a Go account by uploading
a ZIP.

## 5. Public directory submission

Public publication is a separate process and is not automatic:
1. Verify your individual or business developer identity in the OpenAI Platform.
2. Prepare a stable public HTTPS MCP endpoint.
3. Create the plugin package and metadata required by the current submission guide.
4. Upload the ZIP in the OpenAI developer plugin submission portal.
5. Connect and scan the MCP server, complete the required positive and negative test cases,
   privacy and safety information, and submit for review.
6. Publish only after approval.

Official guide: https://developers.openai.com/plugins/deploy/submission

## Security

- This starter has no authentication and should be treated as a demo.
- Do not add tools that publish, delete, purchase, or access private accounts without
  authentication and explicit user confirmation.
- Before public release, add OAuth 2.1, rate limiting, input validation, privacy policy,
  logging controls, and security testing.
