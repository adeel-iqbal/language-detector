# Save this as app.py

import streamlit as st
import joblib
import re

# Page configuration
st.set_page_config(
    page_title="Language Detector",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    .result-box {
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        background-color: #f8f9fa;
        margin: 1rem 0;
    }
    
    .language-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 0.5rem;
        margin: 1rem 0;
    }
    
    .language-tag {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        text-align: center;
        font-size: 0.85rem;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        font-size: 1rem;
        padding: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    .detect-button {
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin: 1rem 0;
    }
    
    .footer {
        text-align: center;
        color: #888;
        font-size: 0.9rem;
        margin-top: 3rem;
        padding: 1rem;
        border-top: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Load the trained pipeline
@st.cache_resource
def load_model():
    return joblib.load('language_detector_pipeline.joblib')

pipeline = load_model()

# Function to clean and predict (unchanged core logic)
def detect_language(text):
    text = text.lower().strip()
    text = re.sub(r'\[\d+\]', '', text)
    text = text.replace('"','')
    text = text.replace('\n',' ')
    text = re.sub(r'\s+', ' ', text)
    language = pipeline.predict([text])[0]
    return language

# Header section
st.markdown('<h1 class="main-header">🌐 Language Detector</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover the language of any text with AI-powered detection</p>', unsafe_allow_html=True)

# Main input section
st.markdown("### 📝 Enter Your Text")
user_input = st.text_area(
    "",
    placeholder="Type or paste your text here... (any language from the supported list below)",
    height=150,
    help="Enter text in any of the 17 supported languages for detection"
)

# Center the button using columns
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    detect_button = st.button("🔍 Detect Language", use_container_width=True, type="primary")

# Results section
if detect_button:
    if user_input.strip() == "":
        st.warning("⚠️ Please enter some text to detect its language!")
    else:
        with st.spinner("🔄 Analyzing your text..."):
            result = detect_language(user_input)
        
        # Display result with custom styling
        st.markdown("### 🎯 Detection Result")
        st.success(f"**Detected Language:** {result.title()}")
        
        # Add some visual feedback
        st.balloons()

# Language support section
st.markdown("---")
st.markdown("### 🌍 Supported Languages")

languages = [
    "English", "Hindi", "Portugeese", "French", "Dutch", 
    "Spanish", "Greek", "Russian", "Danish", "Italian", 
    "Turkish", "Swedish", "Arabic", "German", "Kannada", 
    "Malayalam", "Tamil"
]

# Display languages in a clean, simple format
st.markdown("**This app can detect 17 different languages:**")

# Display languages in a more organized way
cols = st.columns(3)
for i, lang in enumerate(languages):
    with cols[i % 3]:
        if 'result' in locals() and lang.lower() == result.lower():  # highlight detected
            st.markdown(f"<span style='background-color:#28a745;color:white;padding:0.3rem 0.6rem;border-radius:5px;'>{lang}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"• {lang}")

# Footer
st.markdown("---")
st.markdown(
    '<div class="footer">🤖 Powered by Machine Learning | Built with Streamlit</div>',
    unsafe_allow_html=True
)

# Sidebar with additional info (optional)
with st.sidebar:
    st.markdown("### ℹ️ About")
    st.markdown("""
    This language detection tool uses machine learning to identify the language of your input text.
    
    **Features:**
    - Supports 17 languages
    - Real-time detection
    - High accuracy
    - Easy to use interface
    
    **Tips for best results:**
    - Use at least a few words
    - Avoid mixing multiple languages
    - Clear, readable text works best
    """)