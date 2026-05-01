# Hanan Speaking

A minimal multilingual Streamlit chatbot powered by Hugging Face Inference API (`openai/gpt-oss-120b:groq`).

## Features
- Minimal chat UI with message bubbles
- Sidebar settings panel
- Language switch: English, Deutsch, العربية
- Theme switcher: Dark Blue, Light Blue, Green, Purple, Sunset, Custom
- Sidebar conversation history
- Uses `HF_TOKEN` from `.env`

## Requirements
- Python 3.12+
- A Hugging Face token with inference access

## Setup
```powershell
cd C:\Users\ASUS\Desktop\businessEditon\HF_gpt.OSS
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install streamlit huggingface_hub
```

Create a `.env` file in the project root:
```env
HF_TOKEN=your_huggingface_token_here
```

## Run
```powershell
cd C:\Users\ASUS\Desktop\businessEditon\HF_gpt.OSS
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

Open the local URL shown in terminal (usually `http://localhost:8501`).

## Notes
- Do not commit your `.env` file.
- If PowerShell blocks activation scripts:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
