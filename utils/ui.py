"""
TrafficIQ - UI & Styling Design System
Provides glassmorphic CSS styling, custom sidebar themes, responsive card components,
and visual UI helpers across Streamlit pages.
"""

import streamlit as st

def apply_custom_css():
    """Injects high-end glassmorphic CSS design system into Streamlit page."""
    st.markdown("""
        <style>
        /* Import Modern Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* App Background */
        .stApp {
            background: linear-gradient(135deg, #0B1120 0%, #0F172A 50%, #1E293B 100%);
            color: #F8FAFC;
        }

        /* Header Banner Styling */
        .iq-header {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
            border: 1px solid rgba(0, 242, 254, 0.2);
            border-radius: 16px;
            padding: 24px 32px;
            margin-bottom: 24px;
            box-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(12px);
        }

        .iq-header h1 {
            background: linear-gradient(90deg, #00F2FE 0%, #4FACFE 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 2.4rem;
            margin: 0;
        }

        .iq-header p {
            color: #94A3B8;
            font-size: 1rem;
            margin-top: 8px;
            margin-bottom: 0;
        }

        /* Streamlit Native Metric Fixes (Prevent Text Truncation Everywhere) */
        [data-testid="stMetricValue"], div[data-testid="stMetricValue"] > div {
            font-size: 1.3rem !important;
            font-weight: 700 !important;
            white-space: normal !important;
            word-break: break-word !important;
            overflow: visible !important;
            text-overflow: clip !important;
            line-height: 1.2 !important;
        }

        [data-testid="stMetricLabel"], div[data-testid="stMetricLabel"] > label {
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            color: #94A3B8 !important;
            white-space: normal !important;
            word-break: break-word !important;
            overflow: visible !important;
            text-overflow: clip !important;
        }

        [data-testid="stMetric"] {
            background: rgba(30, 41, 59, 0.5) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            padding: 10px 14px !important;
        }

        /* Glassmorphic KPI Cards */
        .iq-kpi-card {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 18px 20px;
            text-align: left;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        }

        .iq-kpi-card:hover {
            transform: translateY(-4px);
            border-color: rgba(0, 242, 254, 0.4);
            box-shadow: 0 15px 25px -5px rgba(0, 242, 254, 0.15);
        }

        .iq-kpi-title {
            color: #94A3B8;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            white-space: normal !important;
            word-break: break-word !important;
        }

        .iq-kpi-val {
            color: #00F2FE;
            font-size: 1.8rem;
            font-weight: 800;
            margin-top: 4px;
            white-space: normal !important;
            word-break: break-word !important;
        }

        .iq-kpi-sub {
            color: #64748B;
            font-size: 0.78rem;
            margin-top: 2px;
        }

        /* Action Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #00ADB5 0%, #008080 100%);
            color: #FFFFFF !important;
            border: none;
            border-radius: 10px;
            padding: 10px 24px;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0, 173, 181, 0.3);
        }

        .stButton>button:hover {
            background: linear-gradient(135deg, #00F2FE 0%, #00ADB5 100%);
            box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5);
            transform: translateY(-2px);
        }

        /* Dataframe Table Customization */
        [data-testid="stDataFrame"] {
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            overflow: hidden;
        }

        /* Sidebar Customization */
        [data-testid="stSidebar"] {
            background: #0B1120;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0B1120;
        }
        ::-webkit-scrollbar-thumb {
            background: #1E293B;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #00ADB5;
        }
        </style>
    """, unsafe_allow_html=True)


def render_header(title: str, subtitle: str, icon: str = "🚥"):
    """Renders sleek glassmorphic banner header component."""
    st.markdown(f"""
        <div class="iq-header">
            <h1>{icon} {title}</h1>
            <p>{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)
