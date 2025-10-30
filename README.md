# Smart Robotic Car with LLM Interaction
An end-to-end embedded robotic car project combining speech interaction, perception, navigation, and LLM-based dialogue.
## Features
- [x] Local dialogue service (echo mock)
- [ ] ASR (offline Vosk → Whisper)
- [ ] TTS (pyttsx3 or edge-tts)
- [ ] Obstacle avoidance
- [ ] Motion control
- [ ] Visual perception
- [ ] LLM intent parser
- [ ] On-device deployment
## Structure
smart-robotic-car-llm/
├── apps/
├── llm/
├── speech/
├── perception/
├── navigation/
├── embedded/
├── tests/
├── docs/
└── examples/
## Quick Start
python apps/voice_loop.py
# or
uvicorn apps.api_server:app --reload
