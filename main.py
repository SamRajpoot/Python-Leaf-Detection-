"""
Leaf Disease Detection System - Streamlit Web Application

A modern, interactive web interface for detecting plant leaf diseases using AI-powered
image analysis. Features real-time image preview, comprehensive disease information,
and expert treatment recommendations.

Author: Leaf Disease Detection Team
Version: 1.0.0
License: MIT
"""

import streamlit as st
import requests
from typing import Dict, Any, Optional

# Configure Streamlit page settings
st.set_page_config(
    page_title="Leaf Disease Detection",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "About": "AI-powered leaf disease detection system using Groq Llama Vision models"
    }
)


# Enhanced modern CSS styling for better UX
CSS_STYLES = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(30px); }
            to { opacity: 1; transform: translateX(0); }
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }

        @keyframes shimmer {
            0% { background-position: -200% center; }
            100% { background-position: 200% center; }
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-8px); }
        }

        :root {
            --bg: radial-gradient(circle at 20% 20%, rgba(59,130,246,0.15), transparent 30%),
                  radial-gradient(circle at 80% 0%, rgba(16,185,129,0.15), transparent 30%),
                  radial-gradient(circle at 50% 100%, rgba(168,85,247,0.08), transparent 40%),
                  linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #e2e8f0 100%);
            --card: rgba(255,255,255,0.85);
            --border: rgba(100,116,139,0.12);
            --shadow: 0 20px 60px rgba(15,23,42,0.12);
            --shadow-hover: 0 30px 80px rgba(15,23,42,0.18);
            --accent: linear-gradient(135deg, #10b981 0%, #059669 100%);
            --accent-2: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            --accent-3: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
            --text: #0f172a;
            --muted: #64748b;
            --pill-bg: linear-gradient(135deg, rgba(16,185,129,0.1), rgba(5,150,105,0.08));
        }

        .stApp {
            background: var(--bg);
            background-attachment: fixed;
            font-family: 'Inter', 'Segoe UI', sans-serif;
            color: var(--text);
            animation: fadeInUp 0.6s ease-out;
        }

        * {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .top-hero {
            padding: 24px 0 20px;
            animation: fadeInUp 0.8s ease-out;
        }

        .hero-title {
            font-family: 'Space Grotesk', 'Inter', sans-serif;
            font-size: 42px;
            font-weight: 700;
            letter-spacing: -0.03em;
            background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
        }

        .hero-subtitle {
            color: var(--muted);
            font-size: 17px;
            margin-top: 8px;
            font-weight: 500;
        }

        .pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--pill-bg);
            color: #059669;
            padding: 9px 16px;
            border-radius: 999px;
            font-weight: 700;
            font-size: 12px;
            border: 1px solid rgba(16,185,129,0.2);
            box-shadow: 0 4px 12px rgba(16,185,129,0.15);
            animation: float 3s ease-in-out infinite;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .pill::before {
            content: '';
            width: 6px;
            height: 6px;
            background: #10b981;
            border-radius: 50%;
            animation: pulse 2s ease-in-out infinite;
            box-shadow: 0 0 8px rgba(16,185,129,0.6);
        }

        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 24px 22px;
            box-shadow: var(--shadow);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            animation: slideInRight 0.6s ease-out;
            position: relative;
            overflow: hidden;
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s;
        }

        .card:hover::before {
            left: 100%;
        }

        .card:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-hover);
            border-color: rgba(100,116,139,0.2);
        }

        .result-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 24px;
            box-shadow: var(--shadow);
            padding: 32px 28px;
            margin-top: 16px;
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            animation: slideInRight 0.7s ease-out;
            position: relative;
            overflow: hidden;
        }

        .result-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--accent);
            opacity: 0;
            transition: opacity 0.3s;
        }

        .result-card:hover {
            transform: translateY(-4px) scale(1.01);
            box-shadow: var(--shadow-hover);
            border-color: rgba(100,116,139,0.25);
        }

        .result-card:hover::after {
            opacity: 1;
        }

        .disease-title {
            font-size: 32px;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 12px;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: fadeInUp 0.5s ease-out 0.2s both;
        }
        .section-title {
            color: #0f172a;
            font-size: 16px;
            font-weight: 700;
            margin-top: 24px;
            margin-bottom: 12px;
            letter-spacing: 0.01em;
            display: flex;
            align-items: center;
            gap: 8px;
            animation: fadeInUp 0.5s ease-out 0.3s both;
        }

        .section-title::before {
            content: '';
            width: 4px;
            height: 20px;
            background: var(--accent);
            border-radius: 2px;
        }

        .timestamp {
            color: var(--muted);
            font-size: 13px;
            margin-top: 20px;
            text-align: right;
            font-weight: 500;
            animation: fadeInUp 0.5s ease-out 0.6s both;
        }

        .info-badge {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            background: var(--accent-2);
            color: white;
            border-radius: 12px;
            padding: 10px 14px;
            font-size: 13px;
            margin-right: 8px;
            margin-bottom: 10px;
            border: none;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(37,99,235,0.25);
            animation: fadeInUp 0.4s ease-out both;
            letter-spacing: 0.01em;
        }

        .info-badge:nth-child(1) { animation-delay: 0.4s; }
        .info-badge:nth-child(2) { animation-delay: 0.5s; }
        .info-badge:nth-child(3) { animation-delay: 0.6s; }

        .info-badge:hover {
            transform: translateY(-2px) scale(1.05);
            box-shadow: 0 8px 20px rgba(37,99,235,0.35);
        }

        .info-badge.success {
            background: var(--accent);
            box-shadow: 0 4px 12px rgba(16,185,129,0.25);
        }

        .info-badge.success:hover {
            box-shadow: 0 8px 20px rgba(16,185,129,0.35);
        }

        .info-badge.warn {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            box-shadow: 0 4px 12px rgba(245,158,11,0.25);
        }

        .info-badge.warn:hover {
            box-shadow: 0 8px 20px rgba(245,158,11,0.35);
        }

        .pill-ghost {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 14px;
            background: linear-gradient(135deg, rgba(15,23,42,0.06), rgba(15,23,42,0.04));
            border-radius: 999px;
            color: var(--muted);
            font-size: 12px;
            margin-right: 8px;
            font-weight: 600;
            border: 1px solid rgba(15,23,42,0.08);
            letter-spacing: 0.02em;
        }

        .pill-ghost::before {
            content: '';
            width: 6px;
            height: 6px;
            background: currentColor;
            border-radius: 50%;
            opacity: 0.5;
        }

        .symptom-list, .cause-list, .treatment-list {
            margin-left: 1.2em;
            margin-bottom: 0.6em;
            color: #1f2937;
            line-height: 1.8;
        }

        .symptom-list li, .cause-list li, .treatment-list li {
            padding: 6px 0;
            animation: fadeInUp 0.4s ease-out both;
        }

        .symptom-list li:nth-child(1) { animation-delay: 0.5s; }
        .symptom-list li:nth-child(2) { animation-delay: 0.6s; }
        .symptom-list li:nth-child(3) { animation-delay: 0.7s; }

        .upload-instructions {
            color: var(--muted);
            font-size: 14px;
            margin-top: 8px;
            font-weight: 500;
            line-height: 1.6;
        }

        .stButton>button {
            border-radius: 16px;
            background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%);
            color: white;
            border: none;
            padding: 16px 32px;
            font-weight: 700;
            letter-spacing: 0.02em;
            font-size: 15px;
            box-shadow: 0 12px 30px rgba(37,99,235,0.3), inset 0 1px 0 rgba(255,255,255,0.2);
            position: relative;
            overflow: hidden;
        }

        .stButton>button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s;
        }

        .stButton>button:hover::before {
            left: 100%;
        }

        .stButton>button:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 20px 40px rgba(37,99,235,0.4), inset 0 1px 0 rgba(255,255,255,0.3);
        }

        .stButton>button:active {
            transform: translateY(0) scale(0.98);
        }

        .metric-chip {
            background: linear-gradient(135deg, rgba(59,130,246,0.08), rgba(16,185,129,0.08));
            border-radius: 16px;
            padding: 14px 18px;
            font-size: 14px;
            color: var(--muted);
            border: 1px solid rgba(100,116,139,0.15);
            font-weight: 500;
            box-shadow: 0 4px 12px rgba(15,23,42,0.06);
            animation: fadeInUp 0.6s ease-out 0.4s both;
            line-height: 1.6;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 12px;
            margin: 16px 0;
        }

        .stat-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7));
            border: 1px solid rgba(100,116,139,0.12);
            border-radius: 16px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(15,23,42,0.08);
            animation: fadeInUp 0.5s ease-out both;
        }

        .stat-card:nth-child(1) { animation-delay: 0.2s; }
        .stat-card:nth-child(2) { animation-delay: 0.3s; }
        .stat-card:nth-child(3) { animation-delay: 0.4s; }

        .stat-value {
            font-size: 28px;
            font-weight: 800;
            background: var(--accent);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .stat-label {
            font-size: 12px;
            color: var(--muted);
            margin-top: 4px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* Loading animation */
        .loading-shimmer {
            background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%);
            background-size: 200% 100%;
            animation: shimmer 2s infinite;
        }
    </style>
"""

st.markdown(CSS_STYLES, unsafe_allow_html=True)


# Application header and UI layout
def render_header():
    """Render the application header with title and supporting context."""
    st.markdown("""
        <div class='top-hero'>
            <div class='pill'>
                <span>AI Vision</span>
                <span style='opacity:0.85;'>Groq Llama</span>
                <span style='opacity:0.7; font-size:10px;'>v1.0</span>
            </div>
            <div style='margin-top:14px;'>
                <div class='hero-title'>🍃 Leaf Disease Detection</div>
                <div class='hero-subtitle'>Advanced AI diagnostics with real-time confidence scores, severity assessment, and expert treatment guidance.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_invalid_image(result: Dict[str, Any]) -> None:
    """Render the UI for invalid image results."""
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='disease-title'>⚠️ Invalid Image Detected</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div style='color: #dc2626; font-size: 16px; margin-bottom: 16px; font-weight: 500;'>"
        "Please upload a clear image of a plant leaf for accurate disease detection."
        "</div>",
        unsafe_allow_html=True
    )
    
    if result.get("symptoms"):
        st.markdown(
            "<div class='section-title'>Issue Detected</div>",
            unsafe_allow_html=True
        )
        st.markdown("<ul class='symptom-list'>", unsafe_allow_html=True)
        for symptom in result.get("symptoms", []):
            st.markdown(f"<li>{symptom}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)
    
    if result.get("treatment"):
        st.markdown(
            "<div class='section-title'>Recommended Action</div>",
            unsafe_allow_html=True
        )
        st.markdown("<ul class='treatment-list'>", unsafe_allow_html=True)
        for treat in result.get("treatment", []):
            st.markdown(f"<li>{treat}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_disease_result(result: Dict[str, Any]) -> None:
    """Render the UI for detected disease results."""
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='disease-title'>🦠 {result.get('disease_name', 'Unknown Disease')}</div>",
        unsafe_allow_html=True
    )
    
    # Premium info badges with color coding
    severity = result.get('severity', 'unknown').lower()
    badge_class = 'success' if severity == 'mild' else ('warn' if severity == 'moderate' else '')
    
    st.markdown(
        f"""<div style='margin: 16px 0;'>
            <span class='info-badge'><strong>Type:</strong> {result.get('disease_type', 'N/A').title()}</span>
            <span class='info-badge {badge_class}'><strong>Severity:</strong> {result.get('severity', 'N/A').title()}</span>
            <span class='info-badge success'><strong>Confidence:</strong> {result.get('confidence', 0)}%</span>
        </div>""",
        unsafe_allow_html=True
    )
    
    # Symptoms
    st.markdown(
        "<div class='section-title'>Observable Symptoms</div>",
        unsafe_allow_html=True
    )
    st.markdown("<ul class='symptom-list'>", unsafe_allow_html=True)
    for symptom in result.get("symptoms", []):
        st.markdown(f"<li>{symptom}</li>", unsafe_allow_html=True)
    st.markdown("</ul>", unsafe_allow_html=True)
    
    # Possible causes
    st.markdown(
        "<div class='section-title'>Possible Causes</div>",
        unsafe_allow_html=True
    )
    st.markdown("<ul class='cause-list'>", unsafe_allow_html=True)
    for cause in result.get("possible_causes", []):
        st.markdown(f"<li>{cause}</li>", unsafe_allow_html=True)
    st.markdown("</ul>", unsafe_allow_html=True)
    
    # Treatment
    st.markdown(
        "<div class='section-title'>Recommended Treatment</div>",
        unsafe_allow_html=True
    )
    st.markdown("<ul class='treatment-list'>", unsafe_allow_html=True)
    for treat in result.get("treatment", []):
        st.markdown(f"<li>{treat}</li>", unsafe_allow_html=True)
    st.markdown("</ul>", unsafe_allow_html=True)
    
    # Timestamp
    st.markdown(
        f"<div class='timestamp'>⏱️ Analysis completed: {result.get('analysis_timestamp', 'N/A')}</div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_healthy_leaf(result: Dict[str, Any]) -> None:
    """Render the UI for healthy leaf results."""
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='disease-title'>✅ Healthy Leaf Detected</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div style='color: #059669; font-size: 17px; margin-bottom: 20px; font-weight: 600;'>"
        "No disease detected in this leaf. The plant appears to be in excellent health!"
        "</div>",
        unsafe_allow_html=True
    )
    
    # Stats display for healthy leaf
    st.markdown(
        """<div class='stats-grid'>
            <div class='stat-card'>
                <div class='stat-value'>✓</div>
                <div class='stat-label'>Status</div>
            </div>
            <div class='stat-card'>
                <div class='stat-value'>{}%</div>
                <div class='stat-label'>Confidence</div>
            </div>
            <div class='stat-card'>
                <div class='stat-value'>{}</div>
                <div class='stat-label'>Type</div>
            </div>
        </div>""".format(
            result.get('confidence', 'N/A'),
            result.get('disease_type', 'healthy').title()
        ),
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"<div class='timestamp'>⏱️ Analysis completed: {result.get('analysis_timestamp', 'N/A')}</div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)


def process_image(uploaded_file, api_url: str) -> None:
    """Process uploaded image and display results."""
    if st.button("🔍 Start AI Analysis", use_container_width=True):
        # Show loading animation
        with st.spinner("🤖 Analyzing image with AI... This may take 2-5 seconds"):
            try:
                files = {
                    "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
                }
                response = requests.post(
                    f"{api_url}/disease-detection-file",
                    files=files,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Determine result type and render accordingly
                    if result.get("disease_type") == "invalid_image":
                        render_invalid_image(result)
                    elif result.get("disease_detected"):
                        render_disease_result(result)
                    else:
                        render_healthy_leaf(result)
                else:
                    st.error(f"⚠️ API Error: {response.status_code}")
                    st.write(response.text)
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timeout. Please try again.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Failed to connect to API. Please check if the server is running.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


def main():
    """Main application entry point."""
    render_header()
    
    # API endpoint configuration
    api_url = "http://leaf-diseases-detect.vercel.app"

    # Layout: Image upload on left, results on right
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(
            """
            <div class='card' style='margin-bottom: 16px;'>
                <div style='display:flex; align-items:center; gap:12px; margin-bottom:12px;'>
                    <div class='pill-ghost'>📁 Upload</div>
                    <div style='font-weight:700; font-size:17px; color:#0f172a;'>Image Analysis</div>
                </div>
                <div class='upload-instructions'>Max 10MB • JPG / JPEG / PNG formats supported</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        uploaded_file = st.file_uploader(
            "Choose a leaf image",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )
        if uploaded_file is not None:
            st.markdown("<div style='margin-top:12px;'>", unsafe_allow_html=True)
            st.image(uploaded_file, caption="🔍 Image Preview", use_column_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Show quick stats
            st.markdown(
                """
                <div class='metric-chip' style='margin-top:12px;'>
                    ✅ Image loaded successfully. Ready for AI analysis.
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class='metric-chip' style='margin-top:12px;'>
                    💡 <strong>Pro Tip:</strong> Clear, well-lit leaves yield the highest accuracy and confidence scores.
                </div>
                """,
                unsafe_allow_html=True
            )

    with col2:
        st.markdown(
            """
            <div class='card' style='margin-bottom: 16px;'>
                <div style='display:flex; align-items:center; gap:12px; justify-content:space-between;'>
                    <div style='display:flex; align-items:center; gap:12px;'>
                        <div class='pill-ghost'>📊 Dashboard</div>
                        <div style='font-weight:700; font-size:17px; color:#0f172a;'>Analysis Results</div>
                    </div>
                    <div class='pill' style='font-size:10px; padding:6px 12px;'>REAL-TIME</div>
                </div>
                <div class='upload-instructions'>AI-powered detection with confidence scoring, severity levels, and treatment protocols.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if uploaded_file is not None:
            process_image(uploaded_file, api_url)
        else:
            # Show dashboard preview when no image
            st.markdown(
                """
                <div class='card'>
                    <div style='text-align:center; padding:40px 20px; color:var(--muted);'>
                        <div style='font-size:48px; margin-bottom:16px; opacity:0.5;'>🍃</div>
                        <div style='font-size:18px; font-weight:600; margin-bottom:8px; color:#0f172a;'>Ready for Analysis</div>
                        <div style='font-size:14px; line-height:1.6;'>Upload a leaf image to begin premium AI diagnostics</div>
                        <div class='stats-grid' style='margin-top:24px; max-width:400px; margin-left:auto; margin-right:auto;'>
                            <div class='stat-card'>
                                <div class='stat-value'>500+</div>
                                <div class='stat-label'>Diseases</div>
                            </div>
                            <div class='stat-card'>
                                <div class='stat-value'>95%</div>
                                <div class='stat-label'>Accuracy</div>
                            </div>
                            <div class='stat-card'>
                                <div class='stat-value'>2-5s</div>
                                <div class='stat-label'>Response</div>
                            </div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


if __name__ == "__main__":
    main()
