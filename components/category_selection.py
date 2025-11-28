"""Category selection component for appliance types"""
import streamlit as st
from typing import Optional


def render_category_selection() -> Optional[str]:
    """
    Render category selection page with appliance categories.
    Returns selected category or None.
    """
    # Custom CSS for category selection - aggressive removal of spacing
    st.markdown("""
    <style>
    /* Remove ALL Streamlit default spacing */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
        background-color: #e8f5e9 !important;
    }
    /* Remove header completely */
    header[data-testid="stHeader"] {
        display: none !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    /* Remove all top spacing from Streamlit containers */
    [data-testid="stAppViewContainer"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    [data-testid="stVerticalBlock"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    [data-testid="stVerticalBlock"] > div {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    /* Category wrapper - no spacing */
    .category-wrapper {
        display: block;
        padding: 0 !important;
        margin: 0 !important;
        background-color: #e8f5e9;
        width: 100%;
    }
    .category-container {
        max-width: 900px;
        width: 100%;
        padding: 0 24px 24px 24px !important;
        background: white;
        border-radius: 0 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 0 auto !important;
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    .category-title {
        font-size: 32px;
        font-weight: 700;
        margin: 0 !important;
        margin-bottom: 8px !important;
        padding: 0 !important;
        padding-top: 16px !important;
        color: #000;
        text-align: center;
        line-height: 1.2 !important;
    }
    .category-subtitle {
        font-size: 18px;
        color: #000;
        margin: 0 !important;
        margin-bottom: 32px !important;
        padding: 0 !important;
        font-weight: 500;
        text-align: center;
    }
    /* Style Streamlit buttons to look like cards */
    button[data-testid*="category_"] {
        background: white !important;
        border: 2px dashed #d0d0d0 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        min-height: 200px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        align-items: center !important;
        transition: all 0.3s !important;
        color: #000 !important;
        font-size: 16px !important;
    }
    button[data-testid*="category_"]:hover {
        border-color: #2e7d32 !important;
        background-color: #f5f5f5 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }
    /* Style for category icons - black outline style */
    .category-icon-svg {
        width: 100px;
        height: 100px;
        margin-bottom: 12px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Category definitions with black outline appliance icons (matching provided style)
    categories = [
        {
            "name": "Refrigerator", 
            "key": "refrigerator",
            "icon_svg": """<svg class="category-icon-svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <!-- Two-door refrigerator -->
                <rect x="20" y="10" width="60" height="80" fill="none" stroke="#000" stroke-width="3"/>
                <line x1="50" y1="10" x2="50" y2="90" stroke="#000" stroke-width="3"/>
                <!-- Freezer compartment details -->
                <rect x="25" y="15" width="20" height="12" fill="none" stroke="#000" stroke-width="1.5"/>
                <rect x="55" y="15" width="20" height="12" fill="none" stroke="#000" stroke-width="1.5"/>
                <!-- Fridge compartment shelves -->
                <line x1="28" y1="35" x2="45" y2="35" stroke="#000" stroke-width="1.5"/>
                <line x1="28" y1="50" x2="45" y2="50" stroke="#000" stroke-width="1.5"/>
                <line x1="55" y1="35" x2="72" y2="35" stroke="#000" stroke-width="1.5"/>
                <line x1="55" y1="50" x2="72" y2="50" stroke="#000" stroke-width="1.5"/>
                <!-- Handles -->
                <rect x="30" y="20" width="2" height="5" fill="#000"/>
                <rect x="60" y="20" width="2" height="5" fill="#000"/>
            </svg>"""
        },
        {
            "name": "Washer", 
            "key": "washer",
            "icon_svg": """<svg class="category-icon-svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <!-- Front-loading washing machine -->
                <rect x="15" y="15" width="70" height="70" rx="5" fill="none" stroke="#000" stroke-width="3"/>
                <!-- Circular door/drum -->
                <circle cx="50" cy="50" r="28" fill="none" stroke="#000" stroke-width="3"/>
                <circle cx="50" cy="50" r="22" fill="none" stroke="#000" stroke-width="2"/>
                <!-- Control panel dots -->
                <circle cx="40" cy="20" r="2" fill="#000"/>
                <circle cx="50" cy="20" r="2" fill="#000"/>
                <circle cx="60" cy="20" r="2" fill="#000"/>
            </svg>"""
        },
        {
            "name": "Dryer", 
            "key": "dryer",
            "icon_svg": """<svg class="category-icon-svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <!-- Dryer -->
                <rect x="15" y="15" width="70" height="70" rx="5" fill="none" stroke="#000" stroke-width="3"/>
                <!-- Circular door -->
                <circle cx="50" cy="50" r="28" fill="none" stroke="#000" stroke-width="3"/>
                <!-- Heat symbol (wavy lines) -->
                <path d="M 35 50 Q 40 45, 45 50 T 55 50 T 65 50" stroke="#000" stroke-width="2" fill="none"/>
                <path d="M 35 55 Q 40 50, 45 55 T 55 55 T 65 55" stroke="#000" stroke-width="2" fill="none"/>
                <!-- Control panel dots -->
                <circle cx="40" cy="20" r="2" fill="#000"/>
                <circle cx="50" cy="20" r="2" fill="#000"/>
                <circle cx="60" cy="20" r="2" fill="#000"/>
            </svg>"""
        },
        {
            "name": "Range", 
            "key": "range",
            "icon_svg": """<svg class="category-icon-svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <!-- Oven/Range -->
                <rect x="15" y="20" width="70" height="60" fill="none" stroke="#000" stroke-width="3"/>
                <!-- Oven door -->
                <rect x="20" y="25" width="60" height="50" fill="none" stroke="#000" stroke-width="2"/>
                <!-- Door handle -->
                <rect x="25" y="48" width="8" height="4" fill="#000"/>
                <!-- Control panel dots -->
                <circle cx="30" cy="15" r="2" fill="#000"/>
                <circle cx="40" cy="15" r="2" fill="#000"/>
                <circle cx="50" cy="15" r="2" fill="#000"/>
                <circle cx="60" cy="15" r="2" fill="#000"/>
                <circle cx="70" cy="15" r="2" fill="#000"/>
            </svg>"""
        },
        {
            "name": "Dishwasher", 
            "key": "dishwasher",
            "icon_svg": """<svg class="category-icon-svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <!-- Dishwasher -->
                <rect x="15" y="10" width="70" height="80" fill="none" stroke="#000" stroke-width="3"/>
                <!-- Interior with dishes -->
                <rect x="20" y="15" width="60" height="70" fill="none" stroke="#000" stroke-width="2"/>
                <!-- Top rack (plates) -->
                <rect x="25" y="20" width="50" height="8" fill="none" stroke="#000" stroke-width="1.5"/>
                <ellipse cx="35" cy="24" rx="4" ry="6" fill="none" stroke="#000" stroke-width="1.5"/>
                <ellipse cx="50" cy="24" rx="4" ry="6" fill="none" stroke="#000" stroke-width="1.5"/>
                <ellipse cx="65" cy="24" rx="4" ry="6" fill="none" stroke="#000" stroke-width="1.5"/>
                <!-- Bottom rack (bowls) -->
                <rect x="30" y="55" width="40" height="25" fill="none" stroke="#000" stroke-width="1.5"/>
                <ellipse cx="40" cy="65" rx="5" ry="4" fill="none" stroke="#000" stroke-width="1.5"/>
                <ellipse cx="55" cy="65" rx="5" ry="4" fill="none" stroke="#000" stroke-width="1.5"/>
            </svg>"""
        },
        {
            "name": "Microwave", 
            "key": "microwave",
            "icon_svg": """<svg class="category-icon-svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <!-- Microwave oven -->
                <rect x="20" y="15" width="60" height="70" fill="none" stroke="#000" stroke-width="3"/>
                <!-- Door window -->
                <rect x="25" y="20" width="50" height="50" fill="none" stroke="#000" stroke-width="2"/>
                <!-- Window frame -->
                <rect x="30" y="25" width="40" height="30" fill="none" stroke="#000" stroke-width="1.5"/>
                <!-- Control panel -->
                <circle cx="40" cy="65" r="2.5" fill="#000"/>
                <circle cx="50" cy="65" r="2.5" fill="#000"/>
                <circle cx="60" cy="65" r="2.5" fill="#000"/>
                <!-- Door handle -->
                <rect x="70" y="45" width="8" height="4" fill="#000"/>
            </svg>"""
        },
        {
            "name": "Others", 
            "key": "others",
            "icon_svg": """<svg class="category-icon-svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <!-- Generic appliance icon -->
                <rect x="20" y="20" width="60" height="60" rx="5" fill="none" stroke="#000" stroke-width="3"/>
                <!-- Grid pattern inside -->
                <line x1="35" y1="30" x2="35" y2="70" stroke="#000" stroke-width="1.5"/>
                <line x1="50" y1="30" x2="50" y2="70" stroke="#000" stroke-width="1.5"/>
                <line x1="65" y1="30" x2="65" y2="70" stroke="#000" stroke-width="1.5"/>
                <line x1="25" y1="40" x2="75" y2="40" stroke="#000" stroke-width="1.5"/>
                <line x1="25" y1="50" x2="75" y2="50" stroke="#000" stroke-width="1.5"/>
                <line x1="25" y1="60" x2="75" y2="60" stroke="#000" stroke-width="1.5"/>
            </svg>"""
        },
    ]
    
    # Use empty to clear any spacing
    st.empty()
    
    # Container with proper structure
    st.markdown('<div class="category-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="category-container">', unsafe_allow_html=True)
    
    # Title at the top
    st.markdown('<div class="category-title">Select a Category</div>', unsafe_allow_html=True)
    st.markdown('<div class="category-subtitle">Choose the type of appliance you need help with</div>', unsafe_allow_html=True)
    
    # Category grid - display in rows of 3
    num_categories = len(categories)
    for i in range(0, num_categories, 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < num_categories:
                category = categories[i + j]
                with col:
                    # Display icon and name
                    st.markdown(f'<div style="text-align: center; margin-bottom: 8px;">{category["icon_svg"]}</div>', unsafe_allow_html=True)
                    button_key = f"category_{category['key']}"
                    if st.button(
                        category['name'],
                        key=button_key,
                        use_container_width=True,
                        help=f"Select {category['name']}"
                    ):
                        st.session_state.selected_category = category['name']
                        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    return st.session_state.get("selected_category")
