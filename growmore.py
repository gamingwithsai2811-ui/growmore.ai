import streamlit as st
from pypdf import PdfReader
import re
from collections import Counter
import random
import textwrap
import time
from datetime import datetime

st.set_page_config(page_title="Growmore INFINITY", layout="wide", page_icon="∞")

st.title("∞ Growmore INFINITY")
st.subheader("The Most Massive & Powerful Study System Ever Created")

# Ultimate Functions
def extract_text(file):
    try:
        reader = PdfReader(file)
        return "\n\n".join([f"Page {i+1}:\n{page.extract_text() or ''}" for i, page in enumerate(reader.pages)])
    except:
        return "Error reading document"

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s.,!?;:\-]', '', text)
    return text.strip()

def infinity_summary(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    freq = Counter(re.findall(r'\b\w+\b', text.lower()))
    scored = sorted([(sum(freq.get(w,0) * len(w) for w in re.findall(r'\b\w+\b', s.lower())), s) for s in sentences if len(s) > 30], reverse=True)
    return "\n\n".join([f"∞ {s}" for _, s in scored[:18]])

def infinity_flashcards(text, count=35):
    sentences = [s for s in re.split(r'(?<=[.!?])\s+', text) if len(s.split()) > 18]
    cards = []
    for s in sentences[:count]:
        words = s.split()
        q = "Master Question: Explain in detail " + " ".join(words[:12]) + "...?"
        cards.append((q, s))
    return cards

def infinity_quiz(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)[:18]
    quiz = []
    for s in sentences:
        if len(s.split()) > 25:
            words = s.split()
            hide = random.randint(8, len(words)-14)
            q = " ".join(words[:hide]) + " [____________] " + " ".join(words[hide+7:])
            quiz.append((q, s))
    return quiz

def infinity_study_plan():
    return [
        "Day 1: Full summary reading + deep highlighting",
        "Day 2: Master all 35 flashcards",
        "Day 3: Complete full quiz + detailed analysis",
        "Day 4: Feynman Technique - teach out loud",
        "Day 5: Create mind map + visual notes",
        "Day 6: Blind self-test without notes",
        "Day 7: Final comprehensive revision",
        "Day 8: Teach a friend or record yourself"
    ]

def full_analysis(text):
    words = len(text.split())
    sent = len(re.split(r'(?<=[.!?])\s+', text))
    return f"""
    📊 **INFINITY ANALYSIS**
    - Words: {words:,}
    - Sentences: {sent}
    - Reading Time: {max(1, words//170)} minutes
    - Complexity: High
    - Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """

# Sidebar
with st.sidebar:
    st.header("∞ INFINITY CONTROLS")
    num_cards = st.slider("Flashcards", 20, 50, 30)
    st.button("Reset All Data")

# Main Area
col1, col2 = st.columns([3, 2])
with col1:
    uploaded = st.file_uploader("Upload PDF", type="pdf")
with col2:
    pasted = st.text_area("Paste Text", height=300)

if st.button("∞ ACTIVATE INFINITY MODE - GENERATE EVERYTHING", type="primary", use_container_width=True):
    with st.spinner("Activating Infinity Mode..."):
        time.sleep(3)
        
        raw = extract_text(uploaded) if uploaded else pasted
        if raw and len(raw) > 200:
            text = clean_text(raw)
            summary = infinity_summary(text)
            flashcards = infinity_flashcards(text, num_cards)
            quiz = infinity_quiz(text)
            plan = infinity_study_plan()
            analysis = full_analysis(text)

            st.balloons()
            st.success("∞ INFINITY MODE FULLY ACTIVATED!")

            tab1, tab2, tab3, tab4, tab5 = st.tabs(["Analysis", "Summary", "Flashcards", "Quiz", "Study Plan"])

            with tab1: st.markdown(analysis)
            with tab2: st.markdown(summary)
            with tab3:
                for i, (q, a) in enumerate(flashcards, 1):
                    with st.expander(f"Card {i}"):
                        st.write("**Q:**", q)
                        st.write("**A:**", a)
            with tab4:
                for i, (q, ans) in enumerate(quiz, 1):
                    with st.expander(f"Question {i}"):
                        st.write(q)
                        if st.button("Show Answer", key=i):
                            st.success(ans)
            with tab5:
                for item in plan:
                    st.markdown(f"**{item}**")
        else:
            st.error("Please provide more content!")

st.caption("∞ Growmore INFINITY - The Most Massive Version")