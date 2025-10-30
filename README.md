# Smart Robotic Car with LLM Interaction

An end-to-end **embedded robotic car** project combining **speech interaction**, **perception**, **navigation**, and **LLM-based dialogue**.  
Goal: say “Hey car, come here.” The car wakes, understands, **navigates toward you**, **avoids obstacles**, and **speaks back**.

---

## 🚀 Highlights

- Modular, hardware-agnostic architecture (Raspberry Pi 5 + Arduino/STM32 recommended)  
- Offline-first (Vosk ASR, pyttsx3 TTS), upgradable to Whisper/Edge-TTS  
- LLM intent parsing with **tool-calling** stubs for motion/navigation  
- Clear separation of **dialogue**, **sensing**, **control**, **firmware**  
- Works on macOS/Linux (simulation/mock), deployable on Raspberry Pi  

---

## 🧭 Feature Matrix & Roadmap

- [x] Local dialogue service (echo mock)  
- [x] HTTP API for `/chat`  
- [ ] ASR (Vosk offline → Whisper optional)  
- [ ] TTS (pyttsx3 offline → edge-tts optional)  
- [ ] Obstacle avoidance (ultrasonic/ToF + simple controller)  
- [ ] Motion control (RPi → Arduino/STM32 serial bridge)  
- [ ] Visual perception (USB/CSI camera + OpenCV)  
- [ ] LLM intent parser (navigate/stop/follow/come-here)  
- [ ] On-device deployment (RPi 5, systemd service)  
- [ ] Calibration & logging (IMU, wheel odom, PID tuning)  
- [ ] Web dashboard (status, video, teleop)  
- [ ] CI (lint, unit tests), release packaging  

---

## 📦 Repository Structure

- **apps/** — Entry points (CLI, API, demos)  
  - **api_server.py** — FastAPI server exposing `/chat`, etc.  
  - **voice_loop.py** — Simple REPL demo (mock LLM)  
- **llm/** — LLM adapters and intent parser  
  - **echo_agent.py** — Echo mock (works offline)  
  - **openai_agent.py** — (optional) Real LLM adapter  
  - **intent_parser.py** — Rule-based or light classifier  
- **speech/** — ASR/TTS modules  
  - **asr_vosk.py** — Offline ASR  
  - **asr_whisper.py** — (optional) Whisper  
  - **tts_pyttsx3.py** — Offline TTS  
  - **tts_edge.py** — (optional) Edge-TTS  
- **perception/** — Sensors: camera, ultrasonic, IMU/ToF  
  - **camera.py**  
  - **ultrasonic.py**  
  - **imu.py**  
- **navigation/** — Control, planning, obstacle avoidance  
  - **motion_stub.py** — Mock motion for laptops  
  - **motion_serial.py** — RPi→MCU serial bridge  
  - **avoid.py** — Simple obstacle avoidance  
- **embedded/** — MCU firmware (Arduino/STM32)  
  - **arduino/** — Motor, encoder, ultrasonic drivers  
- **examples/** — Minimal runnable demos  
  - **follow_me_sim.py**  
- **tests/** — Unit tests  
- **docs/** — Diagrams, wiring, BOM, deployment  
  - **architecture.md**  
  - **wiring.pdf**  
  - **images/**  
- **scripts/** — Utilities (install, run, service)  
- **requirements.txt**  
- **requirements-rpi.txt**  
- **.env.example**  
- **README.md**

## 🧱 System Architecture

**Layers**  
1. **Speech** — ASR → text; TTS ← response  
2. **LLM & Intent** — dialogue policy, intent extraction, tool-calling  
3. **Perception** — ultrasonic/ToF/camera/IMU  
4. **Navigation/Control** — motion commands, obstacle avoidance  
5. **Embedded** — MCU firmware drives motors/sensors via serial  

**Dataflow (MVP)**  
Mic → ASR → text → LLM/Intent → actions → Motion/Perception → state → LLM → TTS → Speaker  

---

## 🧰 Hardware (Suggested)

- **Compute**: Raspberry Pi 5 (8GB) + 128GB microSD  
- **MCU**: Arduino Uno R3 / Nano / STM32  
- **Locomotion**: 2× DC motors + driver (L298N/TB6612FNG)  
- **Sensors**: Ultrasonic HC-SR04 / ToF (VL53L0X/L1X), IMU (MPU-6050), Camera (USB or CSI)  
- **Audio**: USB mic + speaker  
- **Power**: 2S–3S Li-ion/LiPo + BMS + 5V buck  
- **Safety**: Inline fuse, E-stop switch  

---

## 🧑‍💻 Software Stack

- **Python** 3.10+  
- **FastAPI**, **Uvicorn**, **Vosk**, **pyttsx3**  
- **OpenCV**, **pyserial**, **requests**  
- **Arduino C/C++ firmware** for STM32/Arduino  
- **OS**: macOS/Linux development, Raspberry Pi OS deployment  

---

## ⚙️ Installation

~~~bash
git clone https://github.com/WJDdidi-1/Smart-Robotic-Car-with-LLM-Interaction.git
cd Smart-Robotic-Car-with-LLM-Interaction
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip wheel
pip install -r requirements.txt
~~~

**Raspberry Pi Setup**

~~~bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-rpi.txt
~~~

---

## ▶️ Quick Start

**Local Echo Demo**

~~~bash
python apps/voice_loop.py
~~~

**HTTP API Mode**

~~~bash
uvicorn apps.api_server:app --reload
~~~

**Test**

~~~bash
curl -X POST http://127.0.0.1:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"text":"hello car"}'
~~~

---

## 🗣️ Speech (ASR/TTS) Setup

**ASR (Vosk Offline Example)**  

~~~python
from vosk import Model, KaldiRecognizer
import sounddevice as sd, json, queue

def transcribe(duration=4, samplerate=16000):
    q = queue.Queue()
    def cb(indata, frames, time, status): q.put(bytes(indata))
    model = Model("models/vosk-en")
    rec = KaldiRecognizer(model, samplerate)
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16', channels=1, callback=cb):
        text = ""
        for _ in range(int(duration * samplerate / 8000)):
            data = q.get()
            if rec.AcceptWaveform(data):
                j = json.loads(rec.Result())
                text += " " + j.get("text", "")
        j = json.loads(rec.FinalResult())
        text += " " + j.get("text","")
        return text.strip()
~~~

**TTS (pyttsx3 Offline Example)**  

~~~python
import pyttsx3
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
~~~

---

## 🤖 Intent Parser Example

~~~python
def parse_intent(text: str):
    t = text.lower()
    if "forward" in t or "ahead" in t:
        return ("MOVE", {"v": 0.5})
    if "back" in t:
        return ("MOVE", {"v": -0.5})
    if "left" in t:
        return ("TURN", {"w": 0.6})
    if "right" in t:
        return ("TURN", {"w": -0.6})
    if "stop" in t:
        return ("STOP", {})
    if "come here" in t or "approach" in t:
        return ("GOTO_USER", {})
    return ("SMALLTALK", {"text": text})
~~~

---

## 🧪 Testing

~~~bash
pytest -q
~~~

---

## 🖥️ Deployment (Raspberry Pi)

~~~bash
sudo systemctl daemon-reload
sudo systemctl enable smartcar.service
sudo systemctl start smartcar.service
~~~

---

## 🌐 HTTP API (MVP)

POST `/chat`  

Example:

~~~bash
curl -X POST http://127.0.0.1:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"text":"come here"}'
~~~

---

## 🧩 Examples

`examples/follow_me_sim.py` — simulate robot following a target point with proportional control.  

~~~bash
python examples/follow_me_sim.py
~~~

---

## 📜 License

MIT License © 2025 Jiandi (Felix) Wang

---

## 🧾 Citation

```
@software{smart_robotic_car_llm,
  title  = {Smart Robotic Car with LLM Interaction},
  author = {Wang, Jiandi (Felix) and Contributors},
  year   = {2025},
  url    = {https://github.com/WJDdidi-1/Smart-Robotic-Car-with-LLM-Interaction}
}
```
