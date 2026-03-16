---
name: Agent
description: Use when building real-time voice and video AI applications, deploying conversational agents to production, integrating with phone networks, processing video with computer vision models, or adding speech-to-speech capabilities to applications. Reach for this skill when working with Stream's edge network, configuring LLM/STT/TTS providers, building custom processors, or deploying agents at scale.
metadata:
    mintlify-proj: agent
    version: "1.0"
---

# Vision Agents Skill

## Product summary

Vision Agents is an open-source Python framework for building real-time voice and video AI applications. It provides a unified Agent class that orchestrates LLM, speech-to-text (STT), text-to-speech (TTS), video processing, and tool calling via Model Context Protocol (MCP). The framework ships with Stream's global edge network for low-latency transport but is edge-agnostic. Install with `uv add vision-agents` and add provider packages as needed (e.g., `uv add "vision-agents[gemini]"`). Key files: agent configuration in Python code, environment variables for API keys (.env), HTTP server via Runner class. Primary docs: https://visionagents.ai

## When to use

Reach for this skill when:
- Building voice agents (customer support, phone bots, voice assistants)
- Creating video AI applications (coaching, avatars, surveillance, manufacturing)
- Integrating agents with phone networks via Twilio
- Processing video frames with computer vision (YOLO, Roboflow, custom models)
- Deploying agents to production with HTTP server or Kubernetes
- Adding tool calling and knowledge bases (RAG) to agents
- Choosing between realtime speech-to-speech vs traditional STT/LLM/TTS pipelines
- Monitoring agent performance with metrics and tracing
- Testing agents with TestSession and LLMJudge

## Quick reference

### Agent configuration pattern

```python
from vision_agents.core import Agent, User
from vision_agents.plugins import openai, deepgram, elevenlabs, getstream

# Traditional STT/LLM/TTS mode
agent = Agent(
    edge=getstream.Edge(),
    agent_user=User(name="Assistant", id="agent"),
    instructions="You are a helpful voice assistant.",
    llm=openai.LLM(model="gpt-4o-mini"),
    stt=deepgram.STT(),
    tts=elevenlabs.TTS(),
    processors=[video_processor],  # Optional
)

# Realtime speech-to-speech mode (built-in STT/TTS)
agent = Agent(
    edge=getstream.Edge(),
    agent_user=User(name="Assistant", id="agent"),
    instructions="You are a helpful voice assistant.",
    llm=openai.Realtime(model="gpt-realtime", voice="marin"),
)
```

### HTTP server setup

```python
from vision_agents.core import Runner, AgentLauncher

async def create_agent(**kwargs) -> Agent:
    return Agent(...)

async def join_call(agent: Agent, call_type: str, call_id: str, **kwargs) -> None:
    call = await agent.create_call(call_type, call_id)
    async with agent.join(call):
        await agent.simple_response("Hello!")
        await agent.finish()

runner = Runner(AgentLauncher(create_agent=create_agent, join_call=join_call))
runner.cli()  # Runs on http://127.0.0.1:8000
```

### API endpoints (HTTP server mode)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/calls/{call_id}/sessions` | Spawn new agent session |
| DELETE | `/calls/{call_id}/sessions/{session_id}` | Close session |
| GET | `/calls/{call_id}/sessions/{session_id}` | Get session info |
| GET | `/calls/{call_id}/sessions/{session_id}/metrics` | Real-time metrics |
| GET | `/health` | Liveness check |
| GET | `/ready` | Readiness check |

### Provider selection table

| Component | Use Case | Providers |
|-----------|----------|-----------|
| **LLM** | Fast, low-cost responses | OpenAI (gpt-4o-mini), Gemini (2.5-flash-lite) |
| **LLM** | Realtime speech-to-speech | OpenAI Realtime, Gemini Live, AWS Nova, Qwen |
| **STT** | High accuracy, multiple languages | Deepgram, AssemblyAI, Fish Audio |
| **STT** | Local/offline processing | Fast-Whisper, Wizper |
| **TTS** | Expressive, natural voices | ElevenLabs, Cartesia, Inworld |
| **TTS** | Local/offline processing | Kokoro, Pocket |
| **Video Processing** | Object detection, pose estimation | Ultralytics YOLO, Roboflow |
| **Turn Detection** | Built-in to realtime models | OpenAI Realtime, Gemini Live |
| **Turn Detection** | Separate plugin | Deepgram (eager_turn_detection), Smart Turn, Vogent |

### Tool calling and MCP

```python
# Register a function
@agent.llm.register_function(description="Get weather for a location")
async def get_weather(location: str) -> dict:
    return {"temperature": "22°C", "condition": "Sunny"}

# Connect to MCP server
agent = Agent(
    llm=gemini.LLM(),
    mcp_servers=[
        MCPServer(
            name="my-tools",
            command="python",
            args=["-m", "my_mcp_server"],
        )
    ],
)
```

### Video processors

```python
from vision_agents.plugins import ultralytics

# Use built-in processor
agent = Agent(
    processors=[
        ultralytics.YOLOPoseProcessor(model_path="yolo11n-pose.pt")
    ],
)

# Custom processor
class MyProcessor(VideoProcessor):
    name = "my_processor"
    
    async def process_video(self, track, participant_id, shared_forwarder=None):
        self._forwarder = shared_forwarder
        self._forwarder.add_frame_handler(self._on_frame, fps=5.0)
    
    async def _on_frame(self, frame):
        # Process frame
        pass
```

### Environment variables

```bash
STREAM_API_KEY=your_key
STREAM_API_SECRET=your_secret
DEEPGRAM_API_KEY=your_key
ELEVENLABS_API_KEY=your_key
GOOGLE_API_KEY=your_key
OPENAI_API_KEY=your_key
```

## Decision guidance

### Realtime vs Traditional pipeline

| Aspect | Realtime (Speech-to-Speech) | Traditional (STT→LLM→TTS) |
|--------|---------------------------|--------------------------|
| **Latency** | Ultra-low (50-200ms) | Higher (500ms-2s) |
| **Interruption** | Built-in at model level | Requires turn detection plugin |
| **Setup** | Single LLM parameter | Three separate components |
| **Providers** | OpenAI Realtime, Gemini Live, AWS Nova, Qwen | Any LLM + any STT + any TTS |
| **Use when** | Natural conversation, low latency critical | Custom provider combinations, specific voices |

### Video processing approach

| Scenario | Approach |
|----------|----------|
| Object detection, pose estimation | Use Ultralytics YOLO or Roboflow processor |
| Custom ML model | Extend VideoProcessor base class |
| Frame annotation/transformation | Use VideoProcessorPublisher |
| Multiple detections in sequence | Chain processors |

### Knowledge base approach

| Scenario | Tool |
|----------|------|
| Managed RAG with auto-chunking | Gemini FileSearch |
| Vector search with custom embeddings | Turbopuffer |
| Simple function calling | @llm.register_function |

### Deployment approach

| Scenario | Method |
|----------|--------|
| Development/testing | Console mode (runner.cli()) |
| Production single-node | HTTP server (runner.serve()) |
| Production multi-node | HTTP server + Redis session registry + load balancer |

## Workflow

### Building a voice agent

1. **Set up environment**: Create .env with API keys (STREAM_API_KEY, provider keys)
2. **Choose components**: Decide between realtime (single LLM) or traditional (STT/LLM/TTS)
3. **Create Agent instance**: Configure edge, user, instructions, LLM, and speech components
4. **Register tools**: Use @llm.register_function() or connect MCP servers
5. **Define join_call**: Implement what happens when agent joins a call
6. **Test locally**: Use TestSession with LLMJudge to verify behavior
7. **Deploy**: Use Runner with HTTP server for production

### Building a video agent

1. **Choose video processor**: YOLO for pose/detection, Roboflow for custom models, or extend VideoProcessor
2. **Configure FPS**: Set fps parameter on LLM (e.g., fps=3 for Gemini Realtime)
3. **Add processor to Agent**: Pass processors list to Agent constructor
4. **Test with local video**: Use agent.set_video_track_override_path() for reproducible testing
5. **Monitor detections**: Subscribe to VideoProcessorDetectionEvent for frame-by-frame results
6. **Deploy with metrics**: Enable Prometheus export for production visibility

### Adding interruption handling

1. **For realtime models**: No action needed—built-in at model level
2. **For traditional pipeline**: Add turn detection plugin:
   - Deepgram: `stt=deepgram.STT(eager_turn_detection=True)`
   - Smart Turn: `turn_detection=smart_turn.SmartTurn()`
   - Vogent: `turn_detection=vogent.Vogent()`
3. **Test interruption**: Verify TTS stops immediately when user speaks
4. **Tune sensitivity**: Adjust speech_threshold and silence_release_ms if needed

### Deploying to production

1. **Choose deployment mode**: Single-node (HTTP server) or multi-node (HTTP + Redis)
2. **Create Dockerfile**: Base on Python 3.12, install vision-agents and providers
3. **Set environment variables**: Use secrets management for API keys
4. **Enable metrics**: Configure Prometheus exporter for monitoring
5. **Set up health checks**: Use /health and /ready endpoints
6. **Configure CORS**: Use ServeOptions if frontend is on different domain
7. **Test endpoints**: POST to /calls/{call_id}/sessions to spawn agents
8. **Monitor latency**: Track llm.latency.ms, stt.latency.ms, tts.latency.ms

## Common gotchas

- **Missing API keys**: Agents fail silently if provider keys aren't set. Always check .env and environment variables before testing.
- **Realtime models don't support separate STT/TTS**: If using openai.Realtime(), don't pass stt/tts parameters—they're built-in.
- **Call IDs must match pattern**: call_id values must be lowercase alphanumeric, hyphens, and underscores only (^[a-z0-9_-]+$). Invalid IDs return HTTP 400.
- **Turn detection not automatic**: Traditional STT/LLM/TTS pipelines require explicit turn detection plugin. Without it, agent won't detect user interruptions.
- **Video processors need shared_forwarder**: Custom processors must use the shared_forwarder to add frame handlers. Forgetting this breaks video processing.
- **Metrics are no-ops by default**: If no OpenTelemetry provider is configured, metrics collection has no performance impact but also no data. Configure Prometheus exporter to see metrics.
- **Session closure is async**: DELETE /close returns HTTP 202 (Accepted), not 200. The session closes on the next maintenance cycle, not immediately.
- **Conversation context requires Stream Chat**: In-memory conversations are development-only. Production agents need Stream Chat for persistent context.
- **FPS parameter affects latency**: Higher fps on video processors increases latency. Start with fps=1-3 and increase only if needed.
- **Custom plugins need error handling**: Distinguish between temporary errors (emit event, continue) and permanent errors (raise exception).

## Verification checklist

Before submitting agent code:

- [ ] All required API keys are set in .env or environment
- [ ] Agent instantiation includes edge, agent_user, instructions, and LLM
- [ ] If using traditional pipeline, both STT and TTS are configured
- [ ] If using realtime model, no separate STT/TTS parameters are passed
- [ ] Tool functions are registered with @llm.register_function() or MCP servers
- [ ] join_call() function creates a call and joins it with agent.join()
- [ ] TestSession tests pass with expected function calls and outputs
- [ ] Video processors (if used) have process_video() and close() methods
- [ ] Turn detection is configured if using traditional STT/LLM/TTS
- [ ] HTTP server endpoints are tested with curl or client library
- [ ] Environment variables are set before running runner.serve()
- [ ] Prometheus metrics are exported if monitoring production agents
- [ ] Error handlers are subscribed to STTErrorEvent, LLMErrorEvent, TTSErrorEvent
- [ ] Call IDs match the pattern ^[a-z0-9_-]+$ before posting to /calls

## Resources

**Comprehensive navigation**: https://visionagents.ai/llms.txt

**Critical documentation pages**:
- [Introduction & Overview](https://visionagents.ai/introduction/overview) — Framework capabilities, integrations, and getting started
- [Agent Core Architecture](https://visionagents.ai/core/agent-core) — Agent class, MCP integration, event system, video override
- [HTTP Server & Deployment](https://visionagents.ai/guides/http-server) — API endpoints, ServeOptions, custom FastAPI, session management

---

> For additional documentation and navigation, see: https://visionagents.ai/llms.txt
