import os
from pathlib import Path
import streamlit as st


LANGUAGES = {
    "English": {
        "code": "en",
        "title": "Hanan Speaking",
        "caption": "Model: openai/gpt-oss-120b:groq",
        "input_placeholder": "Type your message...",
        "thinking": "Thinking...",
        "clear_chat": "Clear chat",
        "history": "Conversation History",
        "theme_label": "Theme",
        "language_label": "Language",
        "empty_history": "No messages yet.",
        "assistant_prompt": "You are a helpful assistant. Reply in English unless asked otherwise.",
        "you": "You",
        "assistant": "Assistant",
    },
    "Deutsch": {
        "code": "de",
        "title": "Hanan Speaking",
        "caption": "Modell: openai/gpt-oss-120b:groq",
        "input_placeholder": "Nachricht eingeben...",
        "thinking": "Denke nach...",
        "clear_chat": "Chat leeren",
        "history": "Unterhaltungsverlauf",
        "theme_label": "Design",
        "language_label": "Sprache",
        "empty_history": "Noch keine Nachrichten.",
        "assistant_prompt": "Du bist ein hilfreicher Assistent. Antworte auf Deutsch, sofern nichts anderes gefragt wird.",
        "you": "Du",
        "assistant": "Assistent",
    },
    "العربية": {
        "code": "ar",
        "title": "Hanan Speaking",
        "caption": "النموذج: openai/gpt-oss-120b:groq",
        "input_placeholder": "اكتب رسالتك...",
        "thinking": "جاري التفكير...",
        "clear_chat": "مسح المحادثة",
        "history": "سجل المحادثة",
        "theme_label": "السمة",
        "language_label": "اللغة",
        "empty_history": "لا توجد رسائل بعد.",
        "assistant_prompt": "أنت مساعد مفيد. أجب باللغة العربية ما لم يُطلب غير ذلك.",
        "you": "أنت",
        "assistant": "المساعد",
    },
}

THEME_PRESETS = {
    "Dark Blue": {
        "bg": "linear-gradient(180deg, #0b1f3a 0%, #122b4d 100%)",
        "text": "#eaf2ff",
        "sidebar": "#0e2747",
        "border": "#335b8e",
        "bubble": "#173b67",
    },
    "Light Blue": {
        "bg": "linear-gradient(180deg, #eef7ff 0%, #f7fbff 100%)",
        "text": "#12324a",
        "sidebar": "#e3f2ff",
        "border": "#c6e4ff",
        "bubble": "#f8fcff",
    },
    "Green": {
        "bg": "linear-gradient(180deg, #eafff1 0%, #f5fff8 100%)",
        "text": "#103322",
        "sidebar": "#d8fbe8",
        "border": "#9ed8bb",
        "bubble": "#f4fff9",
    },
    "Purple": {
        "bg": "linear-gradient(180deg, #f4ecff 0%, #fbf7ff 100%)",
        "text": "#2b1f4a",
        "sidebar": "#eadbff",
        "border": "#cdb4f8",
        "bubble": "#fcf9ff",
    },
    "Sunset": {
        "bg": "linear-gradient(180deg, #fff1e6 0%, #fff8f2 100%)",
        "text": "#4a2815",
        "sidebar": "#ffe2cc",
        "border": "#ffc29a",
        "bubble": "#fffaf6",
    },
    "Custom": {
        "bg": "linear-gradient(180deg, #f5f7ff 0%, #ffffff 100%)",
        "text": "#1f2937",
        "sidebar": "#eef2ff",
        "border": "#c7d2fe",
        "bubble": "#ffffff",
    },
}


def load_env_file(env_path: str = ".env") -> None:
    """Load simple KEY=VALUE pairs from a .env file into os.environ."""
    path = Path(env_path)
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ[key] = value


def build_client():
    load_env_file(".env")
    hf_token = (os.getenv("HF_TOKEN") or "").strip()
    if not hf_token:
        raise RuntimeError("HF_TOKEN is missing. Add HF_TOKEN=... to your .env file.")
    try:
        from huggingface_hub import InferenceClient
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency: huggingface_hub. Install it with "
            "'.\\.venv\\Scripts\\python.exe -m pip install huggingface_hub'"
        ) from exc

    return InferenceClient(api_key=hf_token)


def apply_theme(theme_name: str, theme_override: dict | None = None) -> None:
    theme = theme_override or THEME_PRESETS.get(theme_name, THEME_PRESETS["Dark Blue"])
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: {theme["bg"]};
            color: {theme["text"]};
        }}
        [data-testid="stSidebar"] {{
            background-color: {theme["sidebar"]};
        }}
        .stChatMessage {{
            border-radius: 12px;
            border: 1px solid {theme["border"]};
            background-color: {theme["bubble"]};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def reset_messages(prompt: str) -> None:
    st.session_state.messages = [{"role": "system", "content": prompt}]


def run_streamlit_app() -> None:
    st.set_page_config(page_title="Hanan Speaking", page_icon="🤖", initial_sidebar_state="expanded")

    try:
        client = build_client()
    except RuntimeError as exc:
        st.error(str(exc))
        st.stop()

    model = "openai/gpt-oss-120b:groq"
    theme_options = list(THEME_PRESETS.keys())
    language_options = list(LANGUAGES.keys())

    if "language" not in st.session_state:
        st.session_state.language = "English"
    if "theme" not in st.session_state:
        st.session_state.theme = "Dark Blue"
    if "custom_theme" not in st.session_state:
        st.session_state.custom_theme = {
            "bg_start": "#f5f7ff",
            "bg_end": "#ffffff",
            "text": "#1f2937",
            "sidebar": "#eef2ff",
            "bubble": "#ffffff",
            "border": "#c7d2fe",
        }

    with st.sidebar:
        st.markdown("## Settings")
        selected_language = st.selectbox(
            LANGUAGES[st.session_state.language]["language_label"],
            options=language_options,
            key="language_select",
        )
        txt_preview = LANGUAGES[selected_language]
        selected_theme = st.selectbox(
            txt_preview["theme_label"],
            options=theme_options,
            key="theme_select",
        )
        if selected_theme == "Custom":
            st.session_state.custom_theme["bg_start"] = st.color_picker(
                "Background start", st.session_state.custom_theme["bg_start"]
            )
            st.session_state.custom_theme["bg_end"] = st.color_picker(
                "Background end", st.session_state.custom_theme["bg_end"]
            )
            st.session_state.custom_theme["text"] = st.color_picker(
                "Text color", st.session_state.custom_theme["text"]
            )
            st.session_state.custom_theme["sidebar"] = st.color_picker(
                "Sidebar color", st.session_state.custom_theme["sidebar"]
            )
            st.session_state.custom_theme["bubble"] = st.color_picker(
                "Chat bubble color", st.session_state.custom_theme["bubble"]
            )
            st.session_state.custom_theme["border"] = st.color_picker(
                "Bubble border color", st.session_state.custom_theme["border"]
            )

    language_changed = selected_language != st.session_state.language
    st.session_state.language = selected_language
    st.session_state.theme = selected_theme
    txt = LANGUAGES[selected_language]

    custom_override = None
    if st.session_state.theme == "Custom":
        custom_override = {
            "bg": (
                f"linear-gradient(180deg, "
                f"{st.session_state.custom_theme['bg_start']} 0%, "
                f"{st.session_state.custom_theme['bg_end']} 100%)"
            ),
            "text": st.session_state.custom_theme["text"],
            "sidebar": st.session_state.custom_theme["sidebar"],
            "border": st.session_state.custom_theme["border"],
            "bubble": st.session_state.custom_theme["bubble"],
        }

    apply_theme(st.session_state.theme, custom_override)

    if "messages" not in st.session_state or language_changed:
        reset_messages(txt["assistant_prompt"])

    st.title(txt["title"])
    st.caption(txt["caption"])

    # Main page conversation (always visible)
    for msg in st.session_state.messages:
        if msg["role"] == "system":
            continue
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    with st.sidebar:
        st.markdown(f"### {txt['history']}")
        history_items = [m for m in st.session_state.messages if m["role"] in {"user", "assistant"}]
        if not history_items:
            st.caption(txt["empty_history"])
        else:
            for idx, item in enumerate(history_items, start=1):
                speaker = txt["you"] if item["role"] == "user" else txt["assistant"]
                preview = item["content"].replace("\n", " ").strip()
                if len(preview) > 70:
                    preview = preview[:67] + "..."
                st.write(f"{idx}. {speaker}: {preview}")
        if st.button(txt["clear_chat"]):
            reset_messages(txt["assistant_prompt"])
            st.rerun()

    # Streamlit keeps chat_input fixed at the bottom of the page.
    user_text = st.chat_input(txt["input_placeholder"])
    if user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})
        with st.chat_message("user"):
            st.markdown(user_text)

        with st.chat_message("assistant"):
            with st.spinner(txt["thinking"]):
                try:
                    completion = client.chat.completions.create(
                        model=model,
                        messages=st.session_state.messages,
                    )
                    assistant_text = completion.choices[0].message.content
                except Exception as exc:
                    assistant_text = f"Request failed: {exc}"
                st.markdown(assistant_text)

        st.session_state.messages.append({"role": "assistant", "content": assistant_text})


if __name__ == "__main__":
    run_streamlit_app()
