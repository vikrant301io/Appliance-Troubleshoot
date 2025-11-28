"""Landing page component for appliance troubleshooting"""
import streamlit as st
from pathlib import Path
import os
from typing import Optional, Dict


def render_landing_page() -> Optional[str]:
    """
    Render the landing page with options to upload photo or type manually.
    Returns the selected action: 'photo', 'manual', 'help', or None
    """
    # Custom CSS for the new design
    st.markdown("""
    <style>
    /* Set page background to light green */
    .stApp {
        background-color: #e8f5e9 !important;
    }
    /* Remove Streamlit default padding at top */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
        background-color: #e8f5e9;
    }
    /* Remove header spacing */
    header[data-testid="stHeader"] {
        display: none;
    }
    /* Remove all top spacing */
    .landing-wrapper {
        display: flex;
        justify-content: center;
        align-items: flex-start;
        padding: 0;
        margin: 0;
        margin-top: 0 !important;
        padding-top: 0 !important;
        background-color: #e8f5e9;
    }
    .landing-container {
        max-width: 600px;
        width: 100%;
        padding: 12px 24px 16px 24px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 0 auto;
        margin-top: 0 !important;
        padding-top: 12px !important;
    }
    .progress-indicator {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 0 !important;
        margin-bottom: 20px;
        padding-top: 0;
        padding-bottom: 12px;
        border-bottom: 1px solid #e0e0e0;
    }
    .progress-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        flex: 1;
    }
    .progress-circle {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 14px;
        margin-bottom: 8px;
    }
    .progress-circle.active {
        background-color: #000;
        color: white;
    }
    .progress-circle.inactive {
        background-color: #e0e0e0;
        color: #999;
    }
    .progress-label {
        font-size: 12px;
        color: #666;
        text-align: center;
    }
    .progress-label.active {
        color: #000;
        font-weight: 600;
    }
    .landing-title {
        font-size: 36px !important;
        font-weight: 700 !important;
        margin-bottom: 10px;
        color: #000 !important;
    }
    .landing-subtitle {
        font-size: 19px !important;
        color: #000 !important;
        margin-bottom: 24px;
        font-weight: 600 !important;
    }
    /* Make all text in container dark black */
    .landing-container {
        color: #000 !important;
    }
    .landing-container * {
        color: #000 !important;
    }
    .landing-container p, .landing-container div, .landing-container span {
        color: #000 !important;
    }
    /* Style upload button - dark black background, white text, larger bold font */
    div[data-testid*="photo_upload_btn"] button,
    button[data-testid*="photo_upload_btn"],
    .stButton > button:has-text("Upload Appliance Label Photo") {
        width: 100% !important;
        padding: 20px 24px !important;
        margin-bottom: 12px !important;
        background-color: #000000 !important;
        background: #000000 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        font-family: inherit !important;
        cursor: pointer !important;
        transition: background-color 0.3s !important;
    }
    div[data-testid*="photo_upload_btn"] button:hover,
    button[data-testid*="photo_upload_btn"]:hover {
        background-color: #1a1a1a !important;
        background: #1a1a1a !important;
    }
    .upload-button {
        width: 100%;
        padding: 18px 24px;
        margin-bottom: 12px;
        background-color: #2e7d32;
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: background-color 0.3s;
    }
    .upload-button:hover {
        background-color: #1b5e20;
    }
    /* Style manual button - larger bold black text */
    div[data-testid*="manual_input_btn"] button,
    button[data-testid*="manual_input_btn"] {
        width: 100% !important;
        padding: 20px 24px !important;
        background-color: white !important;
        background: white !important;
        color: #000000 !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 12px !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        font-family: inherit !important;
        cursor: pointer !important;
        transition: border-color 0.3s, background-color 0.3s !important;
        margin-bottom: 16px !important;
    }
    div[data-testid*="manual_input_btn"] button:hover,
    button[data-testid*="manual_input_btn"]:hover {
        border-color: #999 !important;
        background-color: #f9f9f9 !important;
        background: #f9f9f9 !important;
    }
    .manual-button {
        width: 100%;
        padding: 18px 24px;
        background-color: white;
        color: #000;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: border-color 0.3s, background-color 0.3s;
        margin-bottom: 16px;
    }
    .manual-button:hover {
        border-color: #999;
        background-color: #f9f9f9;
    }
    .help-link {
        text-align: left;
        margin-top: 0;
        margin-bottom: 20px;
    }
    /* Style help link button */
    button[key="help_label_btn"] {
        background: transparent !important;
        border: none !important;
        color: #3498DB !important;
        text-decoration: underline !important;
        cursor: pointer !important;
        font-size: 16px !important;
        padding: 5px 0 !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Container with centered layout
    st.markdown('<div class="landing-wrapper">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([0.5, 3, 0.5], gap="small")
    with col2:
        st.markdown('<div class="landing-container">', unsafe_allow_html=True)
        
        # Progress indicator
        st.markdown("""
        <div class="progress-indicator">
            <div class="progress-step">
                <div class="progress-circle active">1</div>
                <div class="progress-label active">Add Item</div>
            </div>
            <div class="progress-step">
                <div class="progress-circle inactive">2</div>
                <div class="progress-label">Detect Model</div>
            </div>
            <div class="progress-step">
                <div class="progress-circle inactive">3</div>
                <div class="progress-label">Troubleshoot</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Title
        st.markdown('<div class="landing-title">Add Appliance Information</div>', unsafe_allow_html=True)
        
        # Display selected category if available
        selected_category = st.session_state.get("selected_category", "")
        if selected_category:
            st.markdown(f'<div style="font-size: 18px; color: #000; margin-bottom: 16px; font-weight: 600;">**Category:** {selected_category}</div>', unsafe_allow_html=True)
        
        # Subtitle
        st.markdown('<div class="landing-subtitle">Upload the product label or enter details manually.</div>', unsafe_allow_html=True)
        
        # Use Streamlit buttons with custom CSS styling (stacked vertically)
        if st.button("📷 Upload Appliance Label Photo", key="photo_upload_btn", use_container_width=True):
            st.session_state.landing_action = "photo"
            st.rerun()
        
        if st.button("Enter Details Manually", key="manual_input_btn", use_container_width=True):
            st.session_state.landing_action = "manual"
            st.rerun()
        
        # Show brand and subcategory dropdowns (always visible below the button)
        st.markdown("---")
        
        # Header for label location guidance
        st.markdown("### To Locate Your Product Label")
        st.markdown("Please select your appliance brand and model from the options below to receive personalized guidance on locating the product label on your appliance.")
        
        # Brand to subcategory mapping
        brand_subcategories = {
            "GE": ["Compact Refrigerator", "Full-Size Refrigerator", "Mini Fridge", "Top-Freezer Refrigerator", "Bottom-Freezer Refrigerator", "Side-by-Side Refrigerator", "French Door Refrigerator", "Built-in Refrigerator"],
            "Samsung": ["French Door Refrigerator", "Side-by-Side Refrigerator", "Top-Freezer Refrigerator", "Bottom-Freezer Refrigerator", "Compact Refrigerator", "Beverage Center", "Wine Cooler"],
            "LG": ["French Door Refrigerator", "Side-by-Side Refrigerator", "Bottom-Freezer Refrigerator", "Top-Freezer Refrigerator", "Compact Refrigerator"],
            "Whirlpool": ["Top-Freezer Refrigerator", "Bottom-Freezer Refrigerator", "Side-by-Side Refrigerator", "French Door Refrigerator", "Compact Refrigerator"],
            "Maytag": ["Top-Freezer Refrigerator", "Bottom-Freezer Refrigerator", "Side-by-Side Refrigerator", "French Door Refrigerator"],
            "KitchenAid": ["Built-in Refrigerator", "French Door Refrigerator", "Side-by-Side Refrigerator", "Bottom-Freezer Refrigerator"],
            "Frigidaire": ["Top-Freezer Refrigerator", "Bottom-Freezer Refrigerator", "Side-by-Side Refrigerator", "French Door Refrigerator", "Compact Refrigerator"],
            "Bosch": ["Built-in Refrigerator", "French Door Refrigerator", "Bottom-Freezer Refrigerator", "Side-by-Side Refrigerator"],
            "Kenmore": ["Top-Freezer Refrigerator", "Bottom-Freezer Refrigerator", "Side-by-Side Refrigerator", "French Door Refrigerator"],
            "Haier": ["Compact Refrigerator", "Top-Freezer Refrigerator", "Bottom-Freezer Refrigerator", "Side-by-Side Refrigerator"],
            "Amana": ["Top-Freezer Refrigerator", "Bottom-Freezer Refrigerator", "Compact Refrigerator"],
            "Electrolux": ["French Door Refrigerator", "Side-by-Side Refrigerator", "Bottom-Freezer Refrigerator"],
            "Miele": ["Built-in Refrigerator", "French Door Refrigerator", "Bottom-Freezer Refrigerator"],
            "Sub-Zero": ["Built-in Refrigerator", "Integrated Refrigerator", "Wine Storage"],
            "Viking": ["Built-in Refrigerator", "French Door Refrigerator", "Side-by-Side Refrigerator"]
        }
        
        brands = list(brand_subcategories.keys())
        
        # Brand selection dropdown
        selected_brand = st.selectbox(
            "Select Brand *",
            [""] + brands,
            key="landing_brand_select",
            help="Select the brand of your appliance"
        )
        
        # Subcategory selection (only show if brand is selected)
        selected_subcategory = None
        if selected_brand:
            subcategories = brand_subcategories.get(selected_brand, [])
            if subcategories:
                selected_subcategory = st.selectbox(
                    "Select Sub Category *",
                    [""] + subcategories,
                    key="landing_subcategory_select",
                    help="Select the specific type/model category"
                )
                
                # If subcategory is selected, trigger API call
                if selected_subcategory:
                    # Store selections
                    prev_subcategory = st.session_state.get("landing_subcategory", "")
                    st.session_state.landing_brand = selected_brand
                    st.session_state.landing_subcategory = selected_subcategory
                    st.session_state.landing_category = st.session_state.get("selected_category", "Refrigerator")
                    
                    # Trigger API call if subcategory changed and not already shown
                    if prev_subcategory != selected_subcategory:
                        # Mark that we need to fetch guidance
                        st.session_state.show_landing_guidance = True
                        st.session_state.landing_guidance_shown = False
                        st.session_state.landing_guidance_text = None
        
        # Show nameplate guidance if subcategory is selected
        if selected_subcategory and st.session_state.get("landing_subcategory") == selected_subcategory:
            # Check if we need to fetch guidance
            if st.session_state.get("show_landing_guidance", False) and not st.session_state.get("landing_guidance_shown", False):
                from app.services.openai_service import OpenAIService
                
                try:
                    openai_service = OpenAIService()
                    brand = st.session_state.get("landing_brand", selected_brand)
                    subcategory = st.session_state.get("landing_subcategory", selected_subcategory)
                    category = st.session_state.get("landing_category", st.session_state.get("selected_category", "Refrigerator"))
                    
                    with st.spinner("Getting nameplate location guidance..."):
                        guidance_text = openai_service.get_nameplate_guidance(category, subcategory, brand)
                        
                        # Store the guidance
                        st.session_state.landing_guidance_text = guidance_text
                        st.session_state.landing_guidance_shown = True
                        st.session_state.show_landing_guidance = False
                        
                except Exception as e:
                    st.error(f"Error getting guidance: {str(e)}")
                    st.session_state.show_landing_guidance = False
                    st.session_state.landing_guidance_shown = False
            
            # Display the guidance if available
            if st.session_state.get("landing_guidance_shown", False) and st.session_state.get("landing_guidance_text"):
                st.markdown("---")
                st.markdown("### 📍 Where to Find Your Nameplate")
                
                # Display the response as-is (markdown will render it)
                st.markdown(st.session_state.landing_guidance_text)
                
                # Display example nameplate images BELOW the text answer
                st.markdown("")  # Spacing
                st.markdown("**📸 Example Nameplates:**")
                st.markdown("*Here are some examples of what nameplates look like:*")
                
                # Directly load and display images from nameplates folder
                import os
                from PIL import Image
                
                base_dir = Path(os.getcwd()).resolve()
                nameplates_dir = base_dir / "nameplates"
                
                # Try alternative path if needed
                if not nameplates_dir.exists():
                    nameplates_dir = Path(__file__).parent.parent / "nameplates"
                
                if nameplates_dir.exists():
                    # Get all PNG files (case-insensitive)
                    image_files = sorted(list(nameplates_dir.glob("*.png"))) + sorted(list(nameplates_dir.glob("*.PNG")))
                    
                    if image_files:
                        # Display in 2x2 grid
                        cols = st.columns(2)
                        for idx, img_path in enumerate(image_files[:4]):
                            col_idx = idx % 2
                            with cols[col_idx]:
                                try:
                                    # Open with PIL and display
                                    img = Image.open(str(img_path))
                                    st.image(img, caption=f"Example {idx + 1}", use_container_width=True)
                                except Exception as e:
                                    st.error(f"Error loading {img_path.name}: {str(e)}")
                    else:
                        st.warning(f"No PNG files found in {nameplates_dir}")
                else:
                    st.error(f"Nameplates folder not found: {nameplates_dir}")
                
                st.markdown("---")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return st.session_state.get("landing_action")


def render_manual_input_form() -> Optional[Dict]:
    """
    Render manual input form for appliance details (Model Number and Serial Number only).
    Brand and subcategory are already selected from the landing page.
    Returns dict with appliance info or None if not submitted.
    """
    st.markdown("### Enter Appliance Details")
    
    # Get brand and subcategory from session state (selected from landing page)
    selected_brand = st.session_state.get("landing_brand", "")
    selected_subcategory = st.session_state.get("landing_subcategory", "")
    
    # Display selected brand and subcategory (read-only)
    if selected_brand:
        st.info(f"**Brand:** {selected_brand}" + (f" | **Subcategory:** {selected_subcategory}" if selected_subcategory else ""))
    
    # Continue with manual form (only Model Number and Serial Number)
    with st.form("manual_appliance_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            model = st.text_input("Model Number *", placeholder="e.g., RF28R7351SG", key="manual_model")
        
        with col2:
            serial = st.text_input("Serial Number", placeholder="Optional", key="manual_serial")
        
        submitted = st.form_submit_button("Continue", use_container_width=True)
        
        if submitted:
            if selected_brand and model:
                return {
                    "brand": selected_brand,
                    "model": model.strip(),
                    "serial": serial.strip() if serial else "",
                    "appliance_type": st.session_state.get("selected_category"),
                    "subcategory": selected_subcategory
                }
            else:
                st.error("Please ensure Brand is selected and enter Model Number (required fields)")
    
    # Back button outside form
    if st.button("← Back", key="back_from_manual"):
        st.session_state.landing_action = None
        st.session_state.nameplate_guidance_shown = False
        st.session_state.show_nameplate_guidance = False
        st.rerun()
    
    return None


def render_product_label_help():
    """Render help information about finding product labels"""
    
    st.markdown("## 📋 How to Find Your Product Label")
    
    st.markdown("""
    The product label (also called a nameplate, serial plate, or model tag) contains important information 
    about your appliance including the **Brand**, **Model Number**, and **Serial Number**.
    """)
    
    # General Guidance Section
    st.markdown("### ⚠️ General Guidance")
    
    st.markdown("""
    **Safety First:** Before searching for the label, ensure the appliance is turned off and unplugged from 
    the power supply, especially if you need to move it or look in hard-to-reach areas.
    
    **Look for "Model No.", "Serial No.", "Mod", or "S/N":** The label will contain several alphanumeric codes. 
    Look for text that explicitly identifies the Model Number and Serial Number. The brand name is usually 
    prominently displayed on the appliance itself.
    
    **Use a Flashlight/Phone Camera:** The labels are often in dimly lit areas. A flashlight or your phone's 
    camera (using flash) can help you see the details clearly without having to move the appliance completely.
    
    **Check the Manual:** The owner's manual or warranty card often has a diagram or section that tells you 
    exactly where to find the product information label.
    """)
    
    # Common Label Locations Table
    st.markdown("### 📍 Common Label Locations by Appliance Type")
    
    # Create a table using markdown
    locations_data = {
        "Appliance Type": [
            "Refrigerators/Freezers",
            "Washing Machines",
            "Dryers",
            "Dishwashers",
            "Ovens/Ranges",
            "Microwaves",
            "Cooktops/Hobs",
            "Small Appliances (Blenders, Kettles, etc.)"
        ],
        "Common Locations": [
            "Inside the fridge compartment on a side wall (often near the top or behind the crisper/salad drawer), or on the back of the unit.",
            "Inside the door or door frame on front-loading machines; on the back or side of the machine for top-loading models.",
            "Inside the door frame/rim or on the back panel of the appliance.",
            "On the side, top, or inner edge of the dishwasher door/frame.",
            "Around the frame, just inside the oven door opening, or on the frame of the storage/broiler drawer.",
            "Inside the door frame/rim, or on the back of the appliance.",
            "On the underside of the unit (may require access from below).",
            "On the base, side, or back of the product."
        ]
    }
    
    # Display as a formatted table
    for i, (appliance_type, location) in enumerate(zip(locations_data["Appliance Type"], locations_data["Common Locations"])):
        st.markdown(f"**{appliance_type}**")
        st.markdown(f"→ {location}")
        if i < len(locations_data["Appliance Type"]) - 1:
            st.markdown("")  # Add spacing between items
    
    # What to Look For Section
    st.markdown("### 🔍 What to Look For on the Label")
    
    st.markdown("""
    - **Brand Name** (e.g., Samsung, LG, Whirlpool, GE)
    - **Model Number** (usually starts with letters/numbers like "RF28R7351SG")
    - **Serial Number** (unique identifier, often labeled as "S/N" or "Serial No.")
    - Sometimes includes manufacturing date or part numbers
    """)
    
    # Tips Section
    st.markdown("### 💡 Additional Tips")
    
    st.markdown("""
    - Use good lighting when taking the photo
    - Make sure the text is clear and readable
    - If the label is faded, try using a flashlight or your phone's flash
    - Some labels may be behind removable panels or covers
    - Take the photo from directly above or straight on to avoid distortion
    - Ensure all text is in focus before uploading
    """)
    
    st.markdown("---")
    st.markdown("""
    Once you find the label, take a clear photo and upload it using the **"USE PRODUCT LABEL PHOTO"** button, 
    or manually enter the information using the **"TYPE MANUALLY"** option.
    """)
    
    # Back button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("← Back to Options", key="back_from_help", use_container_width=True):
            st.session_state.landing_action = None
            st.rerun()


def _display_nameplate_examples():
    """Display example nameplate images from the nameplates folder - directly below the text answer"""
    import os
    from PIL import Image
    
    # Get the base directory - use current working directory as it's more reliable with Streamlit
    base_dir = Path(os.getcwd()).resolve()
    nameplates_dir = base_dir / "nameplates"
    
    # Find all image files in the nameplates directory
    existing_images = []
    
    if not nameplates_dir.exists():
        # Try alternative path (from __file__)
        try:
            alt_base = Path(__file__).parent.parent.resolve()
            alt_nameplates_dir = alt_base / "nameplates"
            if alt_nameplates_dir.exists():
                nameplates_dir = alt_nameplates_dir
        except:
            pass
    
    if nameplates_dir.exists():
        # Get all image files (png, jpg, jpeg)
        image_extensions = ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']
        
        try:
            for img_file in sorted(nameplates_dir.iterdir()):
                if img_file.is_file() and img_file.suffix in image_extensions:
                    existing_images.append(img_file.resolve())  # Use absolute path
        except Exception as e:
            st.error(f"Error reading nameplates folder: {str(e)}")
            return
    
    # Display images in a grid if they exist
    if existing_images:
        st.markdown("")  # Add spacing
        st.markdown("**📸 Example Nameplates:**")
        st.markdown("*Here are some examples of what nameplates look like:*")
        
        # Display in a 2x2 grid (limit to 4 images)
        cols = st.columns(2)
        for idx, img_path in enumerate(existing_images[:4]):
            col_idx = idx % 2
            with cols[col_idx]:
                try:
                    # Open image with PIL and display
                    img = Image.open(str(img_path))
                    st.image(img, caption=f"Example {idx + 1}", use_container_width=True)
                except Exception as e:
                    # Fallback: try reading as bytes
                    try:
                        with open(img_path, 'rb') as f:
                            img_bytes = f.read()
                        st.image(img_bytes, caption=f"Example {idx + 1}", use_container_width=True)
                    except Exception as e2:
                        st.warning(f"Could not display {img_path.name}: {str(e2)}")
    else:
        # Debug info if images not found
        st.markdown("")  # Add spacing
        st.warning(f"⚠️ No image files found in: {nameplates_dir}")
    
    st.markdown("---")

