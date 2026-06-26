import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from agent_logic import MarketingAgent

# Load dotenv
load_dotenv()

# Set page configuration to match a clean light-mode app
st.set_page_config(
    page_title="Рабочее пространство Craft | Управление кампаниями",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enforce Craft light theme CSS via st.html
st.html("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main body background & font */
    .stApp, .stApp * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    .stApp {
        background-color: #ffffff !important;
        color: #1f2937 !important;
    }
    
    /* Hide default Streamlit header and footer */
    header {
        visibility: hidden !important;
    }
    div[data-testid="stHeader"] {
        display: none !important;
    }
    footer {
        visibility: hidden !important;
    }
    
    /* Headers styling */
    h1, h2, h3, h4, h5, h6 {
        color: #111827 !important;
        letter-spacing: -0.02em;
        margin: 0;
    }
    
    /* Sidebar styling to exactly match Craft */
    section[data-testid="stSidebar"] {
        background-color: #f4f5f6 !important;
        border-right: 1px solid #e5e7eb !important;
        width: 260px !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        padding: 0 !important;
    }
    
    /* Sidebar logo/space selector */
    .craft-logo-section {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 16px;
        margin-bottom: 0.5rem;
        margin-top: 1rem;
    }
    
    .craft-logo-icon {
        width: 22px;
        height: 22px;
        border-radius: 50%;
        background: conic-gradient(from 180deg at 50% 50%, #FF007A 0deg, #7928CA 120deg, #00DFD8 240deg, #FF007A 360deg);
        flex-shrink: 0;
    }
    
    .craft-space-selector {
        font-size: 0.9rem;
        font-weight: 600;
        color: #111827;
        display: flex;
        align-items: center;
        gap: 4px;
        cursor: pointer;
    }
    
    /* Custom New Document Button styling */
    .new-doc-btn-container {
        padding: 0 16px;
        margin-bottom: 1.2rem;
    }
    
    div.new-doc-btn-container button {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        color: #374151 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 8px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
        width: 100% !important;
        cursor: pointer !important;
        text-align: left !important;
    }
    
    div.new-doc-btn-container button:hover {
        background-color: #f9fafb !important;
        border-color: #d1d5db !important;
    }
    
    /* Sidebar Sections & Navigation */
    .sidebar-section-title {
        font-size: 0.7rem;
        font-weight: 600;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 1.2rem;
        margin-bottom: 0.3rem;
        padding-left: 20px;
    }
    
    /* Sidebar nav buttons styling */
    div.active-nav-wrapper button {
        background-color: #e5e7eb !important;
        color: #111827 !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        padding: 6px 12px !important;
        width: 100% !important;
        text-align: left !important;
        justify-content: flex-start !important;
        border: none !important;
        margin: 2px 0 !important;
    }
    div.inactive-nav-wrapper button {
        background-color: transparent !important;
        color: #4b5563 !important;
        border-radius: 6px !important;
        padding: 6px 12px !important;
        width: 100% !important;
        text-align: left !important;
        justify-content: flex-start !important;
        border: none !important;
        margin: 2px 0 !important;
    }
    div.inactive-nav-wrapper button:hover {
        background-color: rgba(0, 0, 0, 0.04) !important;
        color: #111827 !important;
    }
    
    .nav-container-padding {
        padding: 0 12px;
    }
    
    /* Star button inside cards */
    div.stButton button[key*="star_"] {
        background: transparent !important;
        border: none !important;
        color: #9ca3af !important;
        font-size: 0.8rem !important;
        text-align: right !important;
        padding: 0 !important;
        margin-bottom: -15px !important;
        cursor: pointer;
        display: block;
        margin-left: auto;
        width: auto !important;
        min-height: auto !important;
    }
    div.stButton button[key*="star_"]:hover {
        color: #d97706 !important;
        background: transparent !important;
    }
    
    /* Layout Selector Buttons */
    div.layout-btn-wrapper button {
        padding: 4px 10px !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
    }
    
    /* Document/Campaign Card Style */
    .document-card {
        background-color: #ffffff;
        border: 1px solid #eaeaea;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02), 0 1px 2px rgba(0, 0, 0, 0.03);
        padding: 20px;
        margin-bottom: 24px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 540px;
        box-sizing: border-box;
    }
    
    .document-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px -10px rgba(0, 0, 0, 0.06), 0 4px 12px -5px rgba(0, 0, 0, 0.03);
        border-color: #d1d5db;
    }
    
    .document-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #111827;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .document-meta {
        font-size: 0.75rem;
        color: #9ca3af;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    
    /* Layout diagrams/embedded mocks */
    .document-preview-image {
        background-color: #f9fafb;
        border: 1px solid #f3f4f6;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 16px;
        font-size: 0.75rem;
        line-height: 1.4;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.01);
    }
    
    .document-text {
        font-size: 0.82rem;
        color: #6b7280;
        line-height: 1.5;
        margin-bottom: 16px;
    }
    
    /* Nested tiles to match Craft's handbook style */
    .craft-tiles-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-bottom: 16px;
    }
    
    .craft-tile {
        background-color: #fafafa;
        border: 1px solid #f3f4f6;
        border-radius: 8px;
        padding: 10px;
        transition: all 0.15s ease;
    }
    
    .craft-tile:hover {
        background-color: #f5f5f7;
        border-color: #e5e7eb;
    }
    
    .craft-tile-val {
        font-size: 0.95rem;
        font-weight: 700;
        color: #111827;
    }
    
    .craft-tile-lbl {
        font-size: 0.65rem;
        font-weight: 500;
        color: #9ca3af;
        text-transform: uppercase;
        margin-top: 2px;
        letter-spacing: 0.01em;
    }
    
    /* Custom status badges */
    .doc-badge {
        font-size: 0.68rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 12px;
        text-transform: uppercase;
        display: inline-block;
        margin-left: auto;
    }
    
    .doc-badge-scale {
        background-color: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
    }
    
    .doc-badge-reduce {
        background-color: #fef2f2;
        color: #b91c1c;
        border: 1px solid #fca5a5;
    }
    
    /* Assistant block */
    .doc-assistant-box {
        background-color: #f5f3ff;
        border-left: 4px solid #8b5cf6;
        padding: 10px 12px;
        border-radius: 4px 8px 8px 4px;
        font-size: 0.8rem;
        color: #4c1d95;
        margin-top: auto;
        font-weight: 500;
        line-height: 1.4;
    }
    
    /* Header top-bar simulation */
    .craft-top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 24px;
        border-bottom: 1px solid #f3f4f6;
        margin-top: -3.5rem;
        margin-bottom: 1.5rem;
        margin-left: -1rem;
        margin-right: -1rem;
    }
    
    .craft-top-bar-flex {
        border-bottom: 1px solid #f3f4f6 !important;
        margin-top: -3.5rem !important;
        margin-bottom: 1.5rem !important;
        padding: 10px 0 !important;
        margin-left: -1rem;
        margin-right: -1rem;
    }
    
    .craft-top-bar-flex div[data-testid="stTextInput"] input {
        background-color: #f3f4f6 !important;
        border-radius: 20px !important;
        border: none !important;
        height: 36px !important;
        padding: 0 14px !important;
        font-size: 0.85rem !important;
        color: #4b5563 !important;
        text-align: center !important;
    }
    
    .craft-top-bar-actions {
        display: flex;
        align-items: center;
        gap: 16px;
        color: #4b5563;
        margin-top: 6px;
    }
    
    .top-bar-icon {
        cursor: pointer;
        transition: color 0.15s ease;
    }
    
    .top-bar-icon:hover {
        color: #111827;
    }
    
    /* Header action styling */
    .craft-btn-plus {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        padding: 6px 12px;
        font-size: 0.8rem;
        font-weight: 500;
        color: #374151;
        cursor: pointer;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
        transition: background-color 0.15s ease;
    }
    
    .craft-btn-plus:hover {
        background-color: #f9fafb;
        border-color: #d1d5db;
    }
    
    .sidebar-bottom-actions {
        display: flex;
        gap: 16px;
        padding-left: 20px;
        padding-top: 2rem;
        padding-bottom: 1rem;
        color: #9ca3af;
    }
    
    .sidebar-bottom-icon {
        cursor: pointer;
        transition: color 0.15s ease;
    }
    
    .sidebar-bottom-icon:hover {
        color: #4b5563;
    }
    
    /* High-fidelity campaign previews */
    .yandex-ad-box {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        padding: 10px;
    }
    .yandex-link {
        color: #2563eb;
        font-size: 0.82rem;
        font-weight: 600;
        text-decoration: none;
        margin-bottom: 2px;
        display: block;
    }
    .yandex-link:hover {
        text-decoration: underline;
    }
    .yandex-url {
        color: #16a34a;
        font-size: 0.68rem;
        margin-bottom: 4px;
        display: block;
    }
    .yandex-desc {
        color: #4b5563;
        font-size: 0.72rem;
        line-height: 1.3;
    }
    
    .google-banner-box {
        background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%);
        border-radius: 6px;
        height: 80px;
        position: relative;
        overflow: hidden;
        padding: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .google-banner-text {
        color: #ffffff;
        font-size: 0.72rem;
        font-weight: 600;
        line-height: 1.25;
        max-width: 65%;
    }
    .google-banner-btn {
        background-color: #ffffff;
        color: #6366f1;
        font-size: 0.62rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
        margin-top: 6px;
        display: inline-block;
    }
    .google-banner-graphic {
        width: 44px;
        height: 44px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .google-banner-graphic::after {
        content: "";
        width: 14px;
        height: 14px;
        background: rgba(255, 255, 255, 0.6);
        border-radius: 50%;
    }
    
    .insta-story-box {
        background: linear-gradient(to bottom, #111827, #1f2937);
        border-radius: 6px;
        height: 90px;
        position: relative;
        padding: 8px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .insta-header {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .insta-avatar {
        width: 14px;
        height: 14px;
        background: conic-gradient(from 180deg, #feda75, #fa7e1e, #d62976, #962fbf, #4f5bd5);
        border-radius: 50%;
    }
    .insta-username {
        color: #ffffff;
        font-size: 0.6rem;
        font-weight: 600;
    }
    .insta-play {
        width: 24px;
        height: 24px;
        background: rgba(255,255,255,0.25);
        border-radius: 50%;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .insta-play-icon {
        width: 0;
        height: 0;
        border-top: 4px solid transparent;
        border-bottom: 4px solid transparent;
        border-left: 7px solid #ffffff;
        margin-left: 2px;
    }
    .insta-footer {
        color: #ffffff;
        font-size: 0.65rem;
        text-align: center;
        font-weight: 600;
    }
    
    .telegram-ad-box {
        background-color: #e7ebf0;
        border-radius: 6px;
        padding: 8px;
    }
    .telegram-msg {
        background: #ffffff;
        border-radius: 6px;
        padding: 8px;
        box-shadow: 0 1px 1px rgba(0,0,0,0.08);
        max-width: 95%;
    }
    .telegram-sender {
        color: #2481cc;
        font-size: 0.68rem;
        font-weight: 600;
        margin-bottom: 2px;
    }
    .telegram-text {
        color: #1f2937;
        font-size: 0.72rem;
        line-height: 1.3;
    }
    .telegram-sponsored {
        color: #9ca3af;
        font-size: 0.58rem;
        text-align: right;
        margin-top: 4px;
        font-weight: 500;
    }
    
    .analytics-preview-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 10px;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .analytics-header-lbl {
        font-size: 0.65rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
    }
    .analytics-chart-container {
        display: flex;
        align-items: flex-end;
        justify-content: space-around;
        height: 45px;
        padding-top: 4px;
        border-bottom: 1px solid #e2e8f0;
    }
    .analytics-bar {
        width: 16px;
        border-radius: 3px 3px 0 0;
        transition: height 0.3s ease;
    }
    .bar-yandex { background-color: #3b82f6; }
    .bar-google { background-color: #8b5cf6; }
    .bar-insta { background-color: #ec4899; }
    .bar-tg { background-color: #10b981; }
    
    /* Control panel flow schematic */
    .flow-step-box {
        background-color: #3b82f6;
        color: white;
        padding: 4px 6px;
        border-radius: 4px;
        font-size: 0.62rem;
        font-weight: 600;
        text-align: center;
        width: 28%;
    }
    .flow-arrow {
        color: #94a3b8;
        font-size: 0.75rem;
        font-weight: bold;
    }
    
    /* Float streamlit button overrides */
    div.floating-streamlit-btn-container {
        position: fixed;
        bottom: 25px;
        right: 25px;
        z-index: 999999;
    }
    
    div.floating-streamlit-btn-container button {
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 20px !important;
        padding: 6px 16px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
        color: #1f2937 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease !important;
        height: auto !important;
    }
    
    div.floating-streamlit-btn-container button::before {
        content: "";
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: conic-gradient(from 180deg at 50% 50%, #FF007A 0deg, #7928CA 120deg, #00DFD8 240deg, #FF007A 360deg);
        flex-shrink: 0;
    }
    
    div.floating-streamlit-btn-container button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.12) !important;
        border-color: #d1d5db !important;
    }
    
    /* Primary buttons overrides */
    div.stButton button[kind="primary"] {
        background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%) !important;
        border: none !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        box-shadow: 0 2px 4px rgba(124, 58, 237, 0.1) !important;
    }
    div.stButton button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2) !important;
    }
    
    /* Style Streamlit inputs to match Craft */
    div[data-testid="stTextInput"] input {
        border-radius: 8px !important;
        border: 1px solid #e5e7eb !important;
        background-color: #ffffff !important;
        color: #1f2937 !important;
    }
    
    /* Adjust main content margins & paddings to match Craft and reduce left gap */
    div[data-testid="stAppViewBlockContainer"], div.block-container {
        padding-top: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 95% !important;
    }
    
    /* Force secondary buttons to look clean and light (Craft style) */
    div.stButton button[kind="secondary"] {
        background-color: #ffffff !important;
        color: #374151 !important;
        border: 1px solid #e5e7eb !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
        transition: all 0.15s ease !important;
    }
    
    div.stButton button[kind="secondary"]:hover {
        background-color: #f9fafb !important;
        border-color: #d1d5db !important;
        color: #111827 !important;
    }
    
    /* Layout alignments & layout wrappers */
    div[data-testid="column"] {
        position: relative !important;
    }
    
    button.custom-get-plus-btn {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(245, 158, 11, 0.2) !important;
        transition: all 0.2s ease !important;
        height: 36px !important;
    }
    button.custom-get-plus-btn:hover {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3) !important;
    }
    
    /* Layout Grid & List Buttons */
    button.custom-layout-grid-btn[kind="primary"],
    button.custom-layout-list-btn[kind="primary"] {
        background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: none !important;
        height: 36px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }
    button.custom-layout-grid-btn[kind="secondary"],
    button.custom-layout-list-btn[kind="secondary"] {
        background: #ffffff !important;
        color: #374151 !important;
        border: 1px solid #e5e7eb !important;
        height: 36px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }
    button.custom-layout-grid-btn:hover,
    button.custom-layout-list-btn:hover {
        transform: translateY(-1px) !important;
    }
    
    /* Star Button Container in Grid */
    div.custom-star-container-grid {
        position: absolute !important;
        top: 25px !important;
        right: 25px !important;
        z-index: 999 !important;
        background: transparent !important;
    }
    
    /* Star Button Container in List */
    div.custom-star-container-list {
        position: absolute !important;
        top: -46px !important;
        right: 15px !important;
        z-index: 999 !important;
        background: transparent !important;
    }
    
    /* Star Button base style */
    button.custom-star-btn {
        background: transparent !important;
        border: none !important;
        color: #9ca3af !important;
        font-size: 1.25rem !important;
        padding: 0 !important;
        box-shadow: none !important;
        width: 32px !important;
        height: 32px !important;
        min-height: 32px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.15s ease !important;
    }
    
    button.custom-star-btn:hover {
        color: #fbbf24 !important;
        background: rgba(0, 0, 0, 0.04) !important;
        border-radius: 50% !important;
    }
</style>
""")

# ----------------- SESSION STATE & INITIAL MOCK DATA -----------------
DEFAULT_CAMPAIGNS = [
    {
        "id": 1,
        "name": "Яндекс.Директ - Поиск РФ",
        "platform": "Yandex",
        "budget": 10000.0,
        "spend": 8500.0,
        "impressions": 120000,
        "clicks": 2100,
        "conversions": 45,
        "current_text": "Купите наш умный пылесос со скидкой 20%! Доставка бесплатно по всей России."
    },
    {
        "id": 2,
        "name": "Google Ads - КМС Скидки",
        "platform": "Google",
        "budget": 15000.0,
        "spend": 14000.0,
        "impressions": 85000,
        "clicks": 1800,
        "conversions": 25,
        "current_text": "Робот-пылесос нового поколения. Скидки до конца недели. Заказывай прямо сейчас!"
    },
    {
        "id": 3,
        "name": "Instagram Ads - Сториз",
        "platform": "Instagram",
        "budget": 8000.0,
        "spend": 7800.0,
        "impressions": 250000,
        "clicks": 4500,
        "conversions": 130,
        "current_text": "Уборка больше не твоя забота! Умный робот-пылесос сделает все за тебя. Жми подробнее!"
    },
    {
        "id": 4,
        "name": "Telegram - Авторские Каналы",
        "platform": "Telegram",
        "budget": 12000.0,
        "spend": 9000.0,
        "impressions": 300000,
        "clicks": 3500,
        "conversions": 18,
        "current_text": "Умные роботы-пылесосы в официальном магазине. Гарантия 2 года. Доставка от 1 дня."
    }
]

if "campaigns" not in st.session_state:
    agent = MarketingAgent()
    st.session_state.campaigns = [agent.calculate_metrics(c) for c in DEFAULT_CAMPAIGNS]

if "optimized_campaigns" not in st.session_state:
    st.session_state.optimized_campaigns = None

if "ai_results" not in st.session_state:
    st.session_state.ai_results = {}

if "current_view" not in st.session_state:
    st.session_state.current_view = "docs"

if "layout" not in st.session_state:
    st.session_state.layout = "grid"

if "starred_campaigns" not in st.session_state:
    st.session_state.starred_campaigns = set()

if "search_query_box" not in st.session_state:
    st.session_state.search_query_box = ""

# ----------------- DIALOGS & OVERLAYS -----------------
@st.dialog("Запуск новой рекламной кампании 🚀")
def show_add_campaign_dialog():
    st.write("Заполните данные для создания новой рекламной кампании:")
    name = st.text_input("Название кампании", placeholder="например, VK Реклама - Промо")
    platform = st.selectbox("Платформа", ["Yandex", "Google", "Instagram", "Telegram", "VK", "TikTok"])
    budget = st.number_input("Бюджет, ₽", min_value=1000, value=10000, step=1000)
    current_text = st.text_area("Текст объявления", placeholder="Введите рекламный текст для площадки...")
    
    st.markdown("##### Начальные показатели эффективности:")
    col_da, col_db = st.columns(2)
    with col_da:
        impressions = st.number_input("Показы", min_value=100, value=80000, step=1000)
        clicks = st.number_input("Клики", min_value=10, value=1500, step=100)
    with col_db:
        spend = st.number_input("Расход, ₽", min_value=100, value=7500, step=500)
        conversions = st.number_input("Конверсии", min_value=1, value=40, step=5)
        
    if st.button("Запустить кампанию", type="primary"):
        new_id = len(st.session_state.campaigns) + 1
        new_camp = {
            "id": new_id,
            "name": name or f"{platform} Ads - Новая #{new_id}",
            "platform": platform,
            "budget": float(budget),
            "spend": float(spend),
            "impressions": int(impressions),
            "clicks": int(clicks),
            "conversions": int(conversions),
            "current_text": current_text or "Умные роботы-пылесосы в официальном магазине. Доставка от 1 дня."
        }
        agent = MarketingAgent()
        st.session_state.campaigns.append(agent.calculate_metrics(new_camp))
        st.session_state.optimized_campaigns = None  # Reset optimizer results
        st.success("Кампания успешно создана!")
        st.rerun()

# ----------------- SIDEBAR (CRAFT STYLE REPLICATE) -----------------
# Workspace Header selection mock
st.sidebar.html("""
<div class="craft-logo-section">
    <div class="craft-logo-icon"></div>
    <div class="craft-space-selector">Моё пространство <span style="font-size: 0.6rem; color: #9ca3af; margin-left: 2px;">⌄</span></div>
</div>
""")

# New Document style button (opens campaign creator)
st.sidebar.markdown('<div class="new-doc-btn-container">', unsafe_allow_html=True)
if st.sidebar.button("➕ Создать документ", key="new_doc_btn"):
    st.session_state.show_add_dialog = True
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Helper function to render a nav item
def render_nav_item(icon, label, view_name):
    is_active = (st.session_state.current_view == view_name)
    wrapper_class = "active-nav-wrapper" if is_active else "inactive-nav-wrapper"
    st.sidebar.markdown(f'<div class="{wrapper_class} nav-container-padding">', unsafe_allow_html=True)
    if st.sidebar.button(f"{icon}  {label}", key=f"nav_{view_name}"):
        st.session_state.current_view = view_name
        st.rerun()
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Navigation Buttons
st.sidebar.html("<div class=\"sidebar-section-title\">Разделы</div>")
render_nav_item("📄", "Все документы", "docs")
render_nav_item("✓", "Задачи", "tasks")
render_nav_item("📅", "Календарь", "calendar")
render_nav_item("💡", "Вдохновение", "imagine")
render_nav_item("👥", "Доступные мне", "shared")

# Starred Documents Navigation
st.sidebar.html("<div class=\"sidebar-section-title\">Избранное</div>")
if not st.session_state.starred_campaigns:
    st.sidebar.html("<div style='font-size: 0.8rem; color: #9ca3af; padding-left: 20px; font-style: italic; margin-bottom: 0.5rem;'>Добавьте документы для быстрого доступа</div>")
else:
    for cid in st.session_state.starred_campaigns:
        camp = next((camp for camp in st.session_state.campaigns if camp["id"] == cid), None)
        if camp:
            st.sidebar.markdown('<div class="inactive-nav-wrapper nav-container-padding">', unsafe_allow_html=True)
            if st.sidebar.button(f"⭐ {camp['name'][:18]}...", key=f"star_nav_{cid}"):
                st.session_state.search_query_box = camp["name"]
                st.session_state.current_view = "docs"
                st.rerun()
            st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Interactive Folders
st.sidebar.html("<div class=\"sidebar-section-title\">Папки</div>")
st.sidebar.markdown('<div class="inactive-nav-wrapper nav-container-padding">', unsafe_allow_html=True)
if st.sidebar.button("👋 Как использовать Craft", key="folder_welcome"):
    st.session_state.search_query_box = ""
    st.session_state.current_view = "docs"
    st.rerun()
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="inactive-nav-wrapper nav-container-padding">', unsafe_allow_html=True)
if st.sidebar.button("📁 Без папки", key="folder_unorganized"):
    st.session_state.search_query_box = ""
    st.session_state.current_view = "docs"
    st.rerun()
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Interactive Tags
st.sidebar.html("<div class=\"sidebar-section-title\">Теги</div>")
for tag in ["Yandex", "Google", "Instagram", "Telegram"]:
    st.sidebar.markdown('<div class="inactive-nav-wrapper nav-container-padding">', unsafe_allow_html=True)
    if st.sidebar.button(f"🏷️ #{tag}", key=f"tag_{tag}"):
        st.session_state.search_query_box = tag
        st.session_state.current_view = "docs"
        st.rerun()
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Settings at the bottom of the sidebar
st.sidebar.html("<div class=\"sidebar-section-title\">Настройки ИИ</div>")
default_api_key = os.getenv("COHERE_API_KEY", "")
api_key = st.sidebar.text_input("Ключ Cohere API", value=default_api_key, type="password", help="Установите переменную окружения COHERE_API_KEY или введите ключ здесь")
kpi_cpo = st.sidebar.slider("Целевой CPO KPI, ₽", min_value=100.0, max_value=1000.0, value=300.0, step=20.0)

# Sidebar bottom action icons mock
st.sidebar.html("""
<div class="sidebar-bottom-actions">
    <svg class="sidebar-bottom-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
    <svg class="sidebar-bottom-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"></path><polyline points="16 6 12 2 8 6"></polyline><line x1="12" y1="2" x2="12" y2="15"></line></svg>
</div>
""")

# Trigger dialog if show state is True
if "show_add_dialog" in st.session_state and st.session_state.show_add_dialog:
    st.session_state.show_add_dialog = False
    show_add_campaign_dialog()

# ----------------- MAIN AREA -----------------
# Header Simulation Top Bar with functional center search input
st.markdown('<div class="craft-top-bar-flex">', unsafe_allow_html=True)
sc_1, sc_2, sc_3 = st.columns([1, 2, 1])
with sc_2:
    search_query = st.text_input("Поиск", placeholder="🔍 Поиск...", label_visibility="collapsed", key="search_query_box")
with sc_3:
    st.html("""
    <div class="craft-top-bar-actions">
        <svg class="top-bar-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 4px;"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
        <svg class="top-bar-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
    </div>
    """)
st.markdown('</div>', unsafe_allow_html=True)

# ----------------- VIEW ROUTING -----------------
if st.session_state.current_view == "docs":
    display_list = st.session_state.optimized_campaigns if st.session_state.optimized_campaigns is not None else st.session_state.campaigns
    # Header with title and layout switchers (wider actions column to prevent button text wrapping)
    col_title, col_actions = st.columns([1, 1.2])
    with col_title:
        st.html("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 2rem; margin-top: 0.5rem;">
            <div style="width: 28px; height: 28px; border-radius: 50%; background-color: #f3f4f6; display: flex; align-items: center; justify-content: center; font-size: 0.95rem; font-weight: 600; border: 1px solid #e5e7eb; color: #4b5563; cursor: pointer;">+</div>
            <h1 style="font-size: 1.6rem; font-weight: 700; color: #111827; letter-spacing: -0.025em;">Все документы</h1>
        </div>
        """)
    with col_actions:
        # Layout displays and Get Plus button with wider container columns
        l_col1, l_col2, l_col3 = st.columns([1.5, 1, 1])
        with l_col1:
            if st.button("👑 Get Plus", key="get_plus_btn", use_container_width=True):
                st.toast("Премиум функции активированы! Вы получили Craft Plus 👑")
        with l_col2:
            if st.button("Сетка", key="layout_grid", type="secondary" if st.session_state.layout == "list" else "primary", use_container_width=True):
                st.session_state.layout = "grid"
                st.rerun()
        with l_col3:
            if st.button("Список", key="layout_list", type="primary" if st.session_state.layout == "list" else "secondary", use_container_width=True):
                st.session_state.layout = "list"
                st.rerun()

    # Filter display list based on query
    if search_query:
        filtered = []
        for c in display_list:
            if search_query.lower() in c["name"].lower() or search_query.lower() in c["platform"].lower():
                filtered.append(c)
        display_list = filtered

    # Check if empty
    if not display_list:
        st.info("Кампании не найдены по вашему поисковому запросу.")
    
    # ----------------- GRID VIEW -----------------
    elif st.session_state.layout == "grid":
        col1, col2, col3 = st.columns(3)
        
        # Render campaign cards in 3 columns
        for idx, c in enumerate(display_list):
            cid = c["id"]
            ai_data = st.session_state.ai_results.get(cid, {"analysis": "Нажмите «Ассистент» или запустите оптимизацию для генерации анализа.", "new_creatives": []})
            
            # Star status
            is_starred = cid in st.session_state.starred_campaigns
            star_label = "⭐" if is_starred else "☆"
            
            badge_html = ""
            target_budget_text = f"Бюджет: {c['budget']:,.0f} ₽"
            if "action" in c:
                action = c["action"]
                badge_class = "doc-badge-scale" if action == "increase" else "doc-badge-reduce"
                action_text = "Масштабировать" if action == "increase" else "Сократить"
                badge_html = f'<span class="doc-badge {badge_class}">{action_text}</span>'
                color_val = "#059669" if action == "increase" else "#dc2626"
                target_budget_text = f"Бюджет: <span style='text-decoration: line-through; color: #9ca3af;'>{c['budget']:,.0f} ₽</span> → <b style='color: {color_val};'>{c['new_budget']:,.0f} ₽</b>"

            # Campaign customized previews based on platform
            preview_html = ""
            if c["platform"].lower() == "yandex":
                preview_html = f"""
                <div class="yandex-ad-box">
                    <div class="yandex-link">{c['current_text'][:40]}...</div>
                    <div class="yandex-url">yandex.ru/promo • Реклама</div>
                    <div class="yandex-desc">{c['current_text']}</div>
                </div>
                """
            elif c["platform"].lower() == "google":
                preview_html = f"""
                <div class="google-banner-box">
                    <div class="google-banner-text">
                        {c['current_text'][:55]}...
                        <div class="google-banner-btn">Купить</div>
                    </div>
                    <div class="google-banner-graphic"></div>
                </div>
                """
            elif c["platform"].lower() == "instagram":
                preview_html = f"""
                <div class="insta-story-box">
                    <div class="insta-header">
                        <div class="insta-avatar"></div>
                        <div class="insta-username">{c['name'][:12].replace(' ', '_').lower()} • Реклама</div>
                    </div>
                    <div class="insta-play"><div class="insta-play-icon"></div></div>
                    <div class="insta-footer">Подробнее ⌃</div>
                </div>
                """
            elif c["platform"].lower() == "telegram":
                preview_html = f"""
                <div class="telegram-ad-box">
                    <div class="telegram-msg">
                        <div class="telegram-sender">Спонсор</div>
                        <div class="telegram-text">{c['current_text']}</div>
                        <div class="telegram-sponsored">реклама</div>
                    </div>
                </div>
                """
            else:
                # Custom general ad layout
                preview_html = f"""
                <div style="background-color: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px; font-size: 0.72rem; color: #475569;">
                    <div style="font-weight: 700; margin-bottom: 2px;">📢 {c['platform'].upper()} AD PREVIEW</div>
                    <div style="font-style: italic;">"{c['current_text']}"</div>
                </div>
                """

            creatives_html = ""
            if len(ai_data["new_creatives"]) > 0:
                creatives_html = "<div style='font-size: 0.75rem; font-weight: 600; color: #4b5563; margin-top: 8px; margin-bottom: 4px;'>🆕 ИИ-КРЕАТИВЫ:</div>"
                for cr_text in ai_data["new_creatives"]:
                    creatives_html += f'<div style="background-color: #fdf2f8; border: 1px dashed #fbcfe8; border-radius: 6px; padding: 8px; margin-top: 4px; font-size: 0.72rem; color: #9d174d; line-height: 1.3;">📄 {cr_text}</div>'

            # Assign columns cyclically
            card_col = col1 if idx % 3 == 0 else (col2 if idx % 3 == 1 else col3)
            
            with card_col:
                # Star Toggle Button at the top of the card
                if st.button(star_label, key=f"star_{cid}"):
                    if is_starred:
                        st.session_state.starred_campaigns.remove(cid)
                    else:
                        st.session_state.starred_campaigns.add(cid)
                    st.rerun()

                st.html(f"""
                <div class="document-card">
                    <div>
                        <div class="craft-card-header">
                            <div class="document-title">{c['name']} {badge_html}</div>
                        </div>
                        <div class="document-meta">
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 4px; display: inline-block; vertical-align: middle;"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                            <span>Как использовать Craft</span>
                            <span>•</span>
                            <span>Обновлено только что</span>
                        </div>
                        
                        <div class="document-preview-image">
                            {preview_html}
                        </div>
                        
                        <div class="document-text">
                            Рекламная кампания запущена на площадке {c['platform']}. Исходный текст объявления: "{c['current_text'][:80]}..."
                        </div>
                        
                        <div class="craft-tiles-grid">
                            <div class="craft-tile">
                                <div class="craft-tile-val">{c['cpo']:,.1f} ₽</div>
                                <div class="craft-tile-lbl">CPO (Цена лида)</div>
                            </div>
                            <div class="craft-tile">
                                <div class="craft-tile-val">{c['cr']:.1f}%</div>
                                <div class="craft-tile-lbl">Конверсия</div>
                            </div>
                            <div class="craft-tile">
                                <div class="craft-tile-val">{c['cpc']:,.1f} ₽</div>
                                <div class="craft-tile-lbl">CPC (Клик)</div>
                            </div>
                            <div class="craft-tile">
                                <div class="craft-tile-val">{c['clicks']:,}</div>
                                <div class="craft-tile-lbl">Клики</div>
                            </div>
                        </div>
                        
                        <div style="font-size: 0.82rem; color: #374151; margin-bottom: 12px;">
                            💡 {target_budget_text}
                        </div>
                        {creatives_html}
                    </div>
                    
                    <div class="doc-assistant-box">
                        <b>ИИ-Аналитика:</b> "{ai_data['analysis']}"
                    </div>
                </div>
                """)

        # ----------------- SYSTEM STATS & CONTROL PANEL (ROW 2) -----------------
        st.write("---")
        col_r2_1, col_r2_2, col_r2_3 = st.columns(3)
        
        # Card 4: Workspace Analytics
        with col_r2_1:
            total_old_budget = sum([float(camp["budget"]) for camp in st.session_state.campaigns])
            
            # Calculate heights for visual chart bars
            b_yandex = display_list[0]["new_budget"] if len(display_list) > 0 and "new_budget" in display_list[0] else (display_list[0]["budget"] if len(display_list) > 0 else 0)
            b_google = display_list[1]["new_budget"] if len(display_list) > 1 and "new_budget" in display_list[1] else (display_list[1]["budget"] if len(display_list) > 1 else 0)
            b_insta = display_list[2]["new_budget"] if len(display_list) > 2 and "new_budget" in display_list[2] else (display_list[2]["budget"] if len(display_list) > 2 else 0)
            b_tg = display_list[3]["new_budget"] if len(display_list) > 3 and "new_budget" in display_list[3] else (display_list[3]["budget"] if len(display_list) > 3 else 0)
            
            max_b = max(b_yandex, b_google, b_insta, b_tg, 1)
            h_yandex = int((b_yandex / max_b) * 45)
            h_google = int((b_google / max_b) * 45)
            h_insta = int((b_insta / max_b) * 45)
            h_tg = int((b_tg / max_b) * 45)

            if st.session_state.optimized_campaigns is not None:
                total_new_budget = sum([float(camp["new_budget"]) for camp in st.session_state.optimized_campaigns])
                budget_diff = total_new_budget - total_old_budget
                diff_percent = (budget_diff / total_old_budget) * 100
                budget_diff_text = f"{budget_diff:+,.0f} ₽ ({diff_percent:+.1f}%)"
                summary_val_text = f"{total_new_budget:,.0f} ₽"
            else:
                summary_val_text = f"{total_old_budget:,.0f} ₽"
                budget_diff_text = "Оптимизация не запущена"

            st.html(f"""
            <div class="document-card">
                <div>
                    <div class="craft-card-header">
                        <div class="document-title">Workspace Analytics 📊</div>
                    </div>
                    <div class="document-meta">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 4px; display: inline-block; vertical-align: middle;"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                        <span>Управление кампаниями</span>
                        <span>•</span>
                        <span>Общая сводка</span>
                    </div>
                    
                    <div class="document-preview-image">
                        <div class="analytics-preview-box">
                            <div class="analytics-header-lbl">Распределение бюджета по кампаниям</div>
                            <div class="analytics-chart-container">
                                <div class="analytics-bar bar-yandex" style="height: {h_yandex}px;" title="Яндекс: {b_yandex:,.0f} ₽"></div>
                                <div class="analytics-bar bar-google" style="height: {h_google}px;" title="Google: {b_google:,.0f} ₽"></div>
                                <div class="analytics-bar bar-insta" style="height: {h_insta}px;" title="Instagram: {b_insta:,.0f} ₽"></div>
                                <div class="analytics-bar bar-tg" style="height: {h_tg}px;" title="Telegram: {b_tg:,.0f} ₽"></div>
                            </div>
                            <div style="display: flex; justify-content: space-around; font-size: 0.6rem; color: #94a3b8; font-weight: 600;">
                                <span>Яндекс</span>
                                <span>Google</span>
                                <span>Инста</span>
                                <span>ТГ</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="document-text">
                        Общий обзор бюджетов рекламного пространства и их корректировок. Включает метрики синхронизации в реальном времени.
                    </div>
                    
                    <div class="craft-tiles-grid">
                        <div class="craft-tile">
                            <div class="craft-tile-val">{summary_val_text}</div>
                            <div class="craft-tile-lbl">Текущий общий бюджет</div>
                        </div>
                        <div class="craft-tile">
                            <div class="craft-tile-val">{budget_diff_text}</div>
                            <div class="craft-tile-lbl">Изменение бюджета</div>
                        </div>
                        <div class="craft-tile">
                            <div class="craft-tile-val">{total_old_budget:,.0f} ₽</div>
                            <div class="craft-tile-lbl">Начальный бюджет</div>
                        </div>
                        <div class="craft-tile">
                            <div class="craft-tile-val">4 / 4</div>
                            <div class="craft-tile-lbl">Статус синхронизации</div>
                        </div>
                    </div>
                </div>
                
                <div class="doc-assistant-box" style="background-color: #ecfdf5; border-left-color: #10b981; color: #065f46;">
                    <b>Статус пространства:</b> Стабильно и работает.
                </div>
            </div>
            """)

        # Card 5: Optimizer Control Panel
        with col_r2_2:
            st.html("""
            <div class="document-card" style="border: 2px solid #c084fc; box-shadow: 0 4px 20px rgba(168, 85, 247, 0.08);">
                <div>
                    <div class="craft-card-header">
                        <div class="document-title" style="color: #7c3aed;">Панель оптимизатора ⚙️</div>
                    </div>
                    <div class="document-meta">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 4px; display: inline-block; vertical-align: middle;"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                        <span>Управление пространством</span>
                        <span>•</span>
                        <span>Активные действия</span>
                    </div>
                    
                    <div class="document-preview-image">
                        <div style="display: flex; align-items: center; justify-content: space-between; background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 6px; padding: 10px 8px;">
                            <div class="flow-step-box" style="background-color: #3b82f6;">Метрики</div>
                            <span class="flow-arrow">➔</span>
                            <div class="flow-step-box" style="background-color: #8b5cf6;">Оптимизация</div>
                            <span class="flow-arrow">➔</span>
                            <div class="flow-step-box" style="background-color: #ec4899;">Cohere</div>
                        </div>
                    </div>
                    
                    <div class="document-text">
                        Эта карточка управляет запуском ИИ-Агента маркетолога. При клике агент считывает текущие метрики, сравнивает CPO с целевым KPI, перераспределяет бюджеты и отправляет креативы в Cohere.
                    </div>
                    
                    <div class="document-text" style="font-weight: 600; margin-bottom: 20px; color: #4b5563;">
                        Нажмите кнопку ниже или используйте плавающего Ассистента в правом нижнем углу для запуска расчетов.
                    </div>
                </div>
            """)
            
            # Render the primary run button inside the card
            if st.button("🚀 Запустить ИИ-Оптимизатор", key="optimizer_trigger", type="primary"):
                with st.spinner("Оптимизация..."):
                    try:
                        agent = MarketingAgent(api_key=api_key)
                        optimized = []
                        ai_insights = {}
                        for c in st.session_state.campaigns:
                            c_met = agent.calculate_metrics(c)
                            c_opt, action = agent.optimize_budget(c_met, kpi_cpo)
                            optimized.append(c_opt)
                            ai_data = agent.generate_analysis_and_creatives(c_opt, kpi_cpo)
                            ai_insights[c["id"]] = ai_data
                        st.session_state.optimized_campaigns = optimized
                        st.session_state.ai_results = ai_insights
                    except Exception as ex:
                        st.error(f"Не удалось завершить оптимизацию: {ex}")
                    st.rerun()
                    
            st.html("</div>")

    # ----------------- LIST VIEW -----------------
    elif st.session_state.layout == "list":
        st.markdown("##### 📋 Список документов (кампаний):")
        st.html("""
        <style>
            .list-row {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 12px 18px;
                background-color: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                margin-bottom: 10px;
                transition: all 0.2s ease;
            }
            .list-row:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 6px rgba(0,0,0,0.02);
                border-color: #d1d5db;
            }
            .list-row-left {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            .list-row-icon {
                font-size: 1.2rem;
            }
            .list-row-title {
                font-weight: 600;
                color: #111827;
                font-size: 0.9rem;
            }
            .list-row-meta {
                font-size: 0.72rem;
                color: #9ca3af;
                margin-top: 2px;
            }
            .list-row-right {
                display: flex;
                align-items: center;
                gap: 16px;
            }
            .list-row-stat {
                text-align: right;
            }
            .list-row-stat-val {
                font-weight: 700;
                color: #111827;
                font-size: 0.88rem;
            }
            .list-row-stat-lbl {
                font-size: 0.6rem;
                color: #9ca3af;
                text-transform: uppercase;
            }
        </style>
        """)
        
        for c in display_list:
            cid = c["id"]
            is_starred = cid in st.session_state.starred_campaigns
            star_icon = "⭐" if is_starred else "☆"
            
            # Determine badge or action text
            action_text = ""
            action_style = ""
            if "action" in c:
                if c["action"] == "increase":
                    action_text = "Масштабировать"
                    action_style = "background-color: #ecfdf5; color: #047857; border: 1px solid #a7f3d0;"
                else:
                    action_text = "Сократить"
                    action_style = "background-color: #fef2f2; color: #b91c1c; border: 1px solid #fca5a5;"
            
            # Target budget text
            budget_text = f"{c['budget']:,.0f} ₽"
            if "new_budget" in c:
                budget_text = f"{c['new_budget']:,.0f} ₽"
                
            action_badge_html = f'<span style="font-size: 0.65rem; font-weight: 600; padding: 2px 6px; border-radius: 12px; {action_style}">{action_text}</span>' if action_text else ""
            
            st.html(f"""
            <div class="list-row">
                <div class="list-row-left">
                    <div class="list-row-icon">📁</div>
                    <div>
                        <div class="list-row-title">{c['name']} {action_badge_html}</div>
                        <div class="list-row-meta">{c['platform']} • Обновлено только что</div>
                    </div>
                </div>
                <div class="list-row-right">
                    <div class="list-row-stat">
                        <div class="list-row-stat-val">{budget_text}</div>
                        <div class="list-row-stat-lbl">Бюджет</div>
                    </div>
                    <div class="list-row-stat">
                        <div class="list-row-stat-val">{c['cpo']:,.1f} ₽</div>
                        <div class="list-row-stat-lbl">CPO (Цена лида)</div>
                    </div>
                    <div class="list-row-stat">
                        <div class="list-row-stat-val">{c['cr']:.1f}%</div>
                        <div class="list-row-stat-lbl">Конверсия</div>
                    </div>
                </div>
            </div>
            """)
            
            # Star buttons inside rows
            l_col_left, l_col_right = st.columns([12, 1])
            with l_col_right:
                if st.button(star_icon, key=f"star_list_{cid}"):
                    if is_starred:
                        st.session_state.starred_campaigns.remove(cid)
                    else:
                        st.session_state.starred_campaigns.add(cid)
                    st.rerun()

# ----------------- VIEW: TASKS -----------------
elif st.session_state.current_view == "tasks":
    st.html("<h3>✓ Задачи и рекомендации ИИ-Агента</h3>")
    st.write("Список задач, сгенерированных агентом для оптимизации рекламного бюджета на основе текущих показателей CPO.")
    
    # We show tasks list based on whether optimization has been run
    if st.session_state.optimized_campaigns is not None:
        st.markdown("##### 📋 Активные рекомендации по кампаниям:")
        for c in st.session_state.optimized_campaigns:
            action = c["action"]
            name = c["name"]
            cpo = c["cpo"]
            new_budget = c["new_budget"]
            old_budget = c["budget"]
            
            if action == "increase":
                st.checkbox(f"**Масштабировать бюджет {name}**: увеличить с {old_budget:,.0f} ₽ до {new_budget:,.0f} ₽ (CPO {cpo:.1f} ₽ в норме)", value=True, key=f"task_check_{c['id']}")
            else:
                st.checkbox(f"**Сократить бюджет {name}**: снизить с {old_budget:,.0f} ₽ до {new_budget:,.0f} ₽ (CPO {cpo:.1f} ₽ выше лимита)", value=True, key=f"task_check_{c['id']}")
                st.write(f"  └ *Рекомендация:* Заменить текущее объявление на новые креативы от Cohere.")
    else:
        st.info("Рекомендации отсутствуют. Запустите ИИ-Оптимизатор на панели «Все документы», чтобы агент сгенерировал перечень задач.")
        st.markdown("##### 📌 Базовые задачи маркетолога:")
        st.checkbox("Подключить API-ключ Cohere для работы генеративного ИИ-копирайтера", value=bool(api_key))
        st.checkbox("Настроить целевой CPO лимит для рекламного пространства (рекомендуется 300 ₽)", value=True)
        st.checkbox("Запустить ИИ-Оптимизатор для анализа эффективности", value=False)

# ----------------- VIEW: CALENDAR -----------------
elif st.session_state.current_view == "calendar":
    st.html("<h3>📅 Календарь оптимизации бюджетов</h3>")
    st.write("Расписание автоматических проверок и корректировок рекламных бюджетов.")
    
    st.html("""
    <style>
        .calendar-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        .calendar-table th {
            padding: 10px;
            text-align: center;
            background-color: #f3f4f6;
            border: 1px solid #e5e7eb;
            font-size: 0.8rem;
            color: #4b5563;
            text-transform: uppercase;
        }
        .calendar-table td {
            width: 14.2%;
            height: 80px;
            border: 1px solid #e5e7eb;
            padding: 8px;
            vertical-align: top;
            background-color: #ffffff;
        }
        .calendar-day-num {
            font-size: 0.85rem;
            font-weight: 600;
            color: #9ca3af;
        }
        .calendar-day-num.current {
            color: #111827;
        }
        .calendar-event {
            font-size: 0.68rem;
            padding: 2px 6px;
            border-radius: 4px;
            margin-top: 4px;
            font-weight: 500;
        }
        .event-blue {
            background-color: #eff6ff;
            color: #1d4ed8;
            border: 1px solid #bfdbfe;
        }
        .event-purple {
            background-color: #f5f3ff;
            color: #6d28d9;
            border: 1px solid #ddd6fe;
        }
    </style>
    <div style="font-size: 1.1rem; font-weight: 700; color: #111827; margin-bottom: 10px;">Июнь 2026</div>
    <table class="calendar-table">
        <tr>
            <th>Пн</th><th>Вт</th><th>Ср</th><th>Чт</th><th>Пт</th><th>Сб</th><th>Вс</th>
        </tr>
        <tr>
            <td><span class="calendar-day-num">1</span></td>
            <td><span class="calendar-day-num">2</span></td>
            <td><span class="calendar-day-num">3</span></td>
            <td><span class="calendar-day-num">4</span></td>
            <td><span class="calendar-day-num">5</span></td>
            <td><span class="calendar-day-num">6</span></td>
            <td><span class="calendar-day-num">7</span></td>
        </tr>
        <tr>
            <td><span class="calendar-day-num">8</span></td>
            <td><span class="calendar-day-num">9</span></td>
            <td><span class="calendar-day-num">10</span></td>
            <td><span class="calendar-day-num">11</span></td>
            <td><span class="calendar-day-num">12</span></td>
            <td><span class="calendar-day-num">13</span></td>
            <td><span class="calendar-day-num">14</span></td>
        </tr>
        <tr>
            <td><span class="calendar-day-num">15</span></td>
            <td><span class="calendar-day-num">16</span></td>
            <td><span class="calendar-day-num">17</span></td>
            <td><span class="calendar-day-num">18</span></td>
            <td><span class="calendar-day-num">19</span></td>
            <td><span class="calendar-day-num">20</span></td>
            <td><span class="calendar-day-num">21</span></td>
        </tr>
        <tr>
            <td><span class="calendar-day-num">22</span></td>
            <td><span class="calendar-day-num">23</span></td>
            <td><span class="calendar-day-num">24</span></td>
            <td><span class="calendar-day-num">25</span></td>
            <td><span class="calendar-day-num current">26 (Сегодня)</span>
                <div class="calendar-event event-blue">Проверка CPO</div>
                <div class="calendar-event event-purple">Синхронизация ИИ</div>
            </td>
            <td><span class="calendar-day-num current">27</span></td>
            <td><span class="calendar-day-num current">28</span></td>
        </tr>
        <tr>
            <td><span class="calendar-day-num current">29</span></td>
            <td><span class="calendar-day-num current">30</span></td>
            <td></td><td></td><td></td><td></td><td></td>
        </tr>
    </table>
    """)

# ----------------- VIEW: IMAGINE -----------------
elif st.session_state.current_view == "imagine":
    st.html("<h3>💡 Студия креативного вдохновения</h3>")
    st.write("Используйте мощь Cohere для мгновенной генерации рекламных креативов на основе описания вашего продукта.")
    
    col_im1, col_im2 = st.columns(2)
    with col_im1:
        prod_desc = st.text_area("Описание продукта/услуги", value="Умный робот-пылесос. Делает сухую и влажную уборку, обходит препятствия, управляется со смартфона. Идеально для владельцев животных.", height=100)
        target_aud = st.text_input("Целевая аудитория", value="Занятые люди, семьи с детьми, владельцы домашних питомцев")
    with col_im2:
        platform_select = st.selectbox("Рекламная платформа", ["Яндекс (Поиск)", "Google Ads (КМС)", "Instagram Stories", "Telegram"])
        tone_select = st.selectbox("Тон сообщений", ["Креативный и задорный", "Строгий и профессиональный", "Срочный (с акцентом на скидку)", "Дружелюбный"])
        
    if st.button("✨ Сгенерировать креативы с Cohere", type="primary", use_container_width=True):
        if not api_key:
            st.error("Пожалуйста, укажите API-ключ в настройках слева.")
        else:
            with st.spinner("Генерация рекламных вариантов..."):
                prompt = f"""
                Ты профессиональный копирайтер и маркетолог. Напиши 3 уникальных рекламных объявления для платформы '{platform_select}'.
                Продукт: {prod_desc}
                Целевая аудитория: {target_aud}
                Тон сообщений: {tone_select}
                
                Требования:
                - Текст должен быть на русском языке.
                - Каждое объявление должно быть привлекательным, содержать заголовок (для поиска/баннера) или цепляющее предложение, а также четкий призыв к действию (CTA).
                - Тексты должны быть короткими и оптимизированными под выбранную платформу.
                - Выведи строго 3 варианта, разделенных новой строкой. Без вводных слов и нумерации.
                """
                try:
                    agent = MarketingAgent(api_key=api_key)
                    # Use standard chat completion
                    response = agent.co.chat(
                        message=prompt,
                        model="command-r-plus-08-2024"
                    )
                    headlines = [h.strip() for h in response.text.strip().split("\n") if h.strip()]
                    st.session_state.generated_headlines = headlines
                except Exception as e:
                    st.error(f"Ошибка при работе с API: {e}")
                    
    if "generated_headlines" in st.session_state:
        st.markdown("---")
        st.markdown("##### 🎯 Сгенерированные варианты объявлений:")
        for idx, headline in enumerate(st.session_state.generated_headlines[:3]):
            st.html(f"""
            <div style="background-color: #fdf2f8; border: 1px dashed #fbcfe8; border-radius: 8px; padding: 12px; margin-bottom: 12px;">
                <div style="font-size: 0.75rem; font-weight: 600; color: #db2777; text-transform: uppercase; margin-bottom: 4px;">Вариант {idx+1}</div>
                <div style="font-size: 0.85rem; color: #111827; line-height: 1.4; font-style: italic;">"{headline}"</div>
            </div>
            """)

# ----------------- VIEW: SHARED -----------------
elif st.session_state.current_view == "shared":
    st.html("<h3>👥 Документы общего доступа</h3>")
    st.write("Рабочие пространства и отчёты, к которым вам предоставлен доступ другими участниками команды.")
    
    st.html("""
    <div style="background-color: #fafafa; border: 1px solid #e5e7eb; border-radius: 8px; padding: 15px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between;">
        <div>
            <div style="font-weight: 600; color: #111827; font-size: 0.9rem;">📊 Маркетинговый отчёт Q2 (Сводный)</div>
            <div style="font-size: 0.75rem; color: #9ca3af;">Владелец: ceo@craftagency.ru • Обновлено 2 дня назад</div>
        </div>
        <span style="background-color: #eff6ff; color: #1d4ed8; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: 600;">Чтение</span>
    </div>
    <div style="background-color: #fafafa; border: 1px solid #e5e7eb; border-radius: 8px; padding: 15px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between;">
        <div>
            <div style="font-weight: 600; color: #111827; font-size: 0.9rem;">📝 План рекламных кампаний на июль</div>
            <div style="font-size: 0.75rem; color: #9ca3af;">Владелец: lead_designer@craftagency.ru • Обновлено сегодня в 09:12</div>
        </div>
        <span style="background-color: #ecfdf5; color: #047857; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: 600;">Редактирование</span>
    </div>
    """)

# ----------------- FLOATING ASSISTANT BUTTON (CRAFT DESIGN ACCURACY) -----------------
st.markdown('<div class="floating-streamlit-btn-container">', unsafe_allow_html=True)
if st.button("Ассистент", key="floating_assistant_btn"):
    with st.spinner("ИИ-Ассистент работает..."):
        try:
            agent = MarketingAgent(api_key=api_key)
            optimized = []
            ai_insights = {}
            for c in st.session_state.campaigns:
                c_met = agent.calculate_metrics(c)
                c_opt, action = agent.optimize_budget(c_met, kpi_cpo)
                optimized.append(c_opt)
                ai_data = agent.generate_analysis_and_creatives(c_opt, kpi_cpo)
                ai_insights[c["id"]] = ai_data
            st.session_state.optimized_campaigns = optimized
            st.session_state.ai_results = ai_insights
            st.success("Оптимизация завершена!")
        except Exception as e:
            st.error(f"Ошибка ассистента: {e}")
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.html("""
<div style="text-align: center; margin-top: 4rem; padding-bottom: 2rem; font-size: 0.8rem; color: #9ca3af;">
    Пространство кампаний Craft • На базе Cohere API и Streamlit
</div>
""")
