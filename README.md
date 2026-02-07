# Polyend Tracker MIDI Export (Dockerized & Patched)

> 🎹 **Context:** This is a specialized fork designed to run as a Docker Container with a Web Interface. It includes critical fixes for **Firmware 1.6+** headers and specific **"Orphan Note-Off"** crashes.

## 🤖 Disclaimer: AI-Assisted Development
This project is a result of **"Vibecoding"**.
* **The Code:** All patches, Docker configurations, and the web interface were written by **Google Gemini (Pro model)**.
* **The Maintainer:** A musician that was fond of the original tool and wanted to help fix it, but has no other experience with Python other than copy-pasting YAML code into his Home Assistant instance 🤓.
* **The Process:** The Maintainer provided the initial problem, crash logs, testing, and workflow context. The AI analyzed the stack traces and generated the patches and treated the maintainer like a fool that doesn't know what hes doing every now and then. 

*If the code looks unconventional, blame the AI. If it works perfectly, credit the collaboration.* 

## 🚀 Why use this version?
Use this version if the original crashes for you or if you want to self-host it easily via Docker.

### Changes & Fixes
1.  **Dockerized:** packaged with Streamlit for easy self-hosting (or running on Render).
*So I could have a fast private version in my own Docker*
2.  **Fix (FW 1.6+):** Updated the file header check (`1572` vs `2324` bytes) to support newer firmware.
*We used my current Firmware version 1.9.2 for testing but Gemini keeps insisting 1.6+ in it's drafts. Anyway the problem was that after version 1.6 the project file sizes became larger than accounted for. Gemini's fix was to cut off the extra data assuming it would be new settings we won't need for MIDI export.*
3.  **Fix (Crash):** Patched the `midiutil` library to prevent `IndexError` crashes caused by "Orphan Note-Offs" (common in some tracking workflows).
*So I have a lot of patterns that start with Note-Offs on all tracks. I do this to stop all samples (or instruments over MIDI) from playing, since I don't always have room for that in the former pattern. The original tool didn't like that, because there were no notes being triggered in that pattern before the Note-Offs.*

## 🛠️ Usage


### Option 1: Docker (Recommended)
You can run this locally on any machine with Docker.

```bash
docker build -t polymidi .
docker run -d -p 8501:8501 polymidi
```
Then open http://localhost:8501 in your browser.

Option 2: Deploy to Cloud
You can host this for free on Render.com (for personal use or sharing).

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## CREDITS & LICENSE
* **Original Tool:** * **Original Tool:** Created by [DataGreed](https://github.com/DataGreed/polyendtracker-midi-export).

* **Maintenance & Dockerization:** SaturnsGithubSaga 

* **Fix Methodology:** The midiutil patch was developed by analyzing specific crash logs related to pattern clean-up commands.

This project is open-source and follows the license of the original repository.


