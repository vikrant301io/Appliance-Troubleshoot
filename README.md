# Appliance Troubleshoot Assistant

A friendly chat assistant that helps people with home appliance problems. It can guide users through simple self-fix steps or help them book a technician visit.

## Features

- **Chat Interface**: WhatsApp/ChatGPT-style conversation interface
- **Appliance Identification**: 
  - Type brand/model/serial number in chat
  - Upload a photo of the appliance nameplate (uses OpenAI Vision API)
- **Problem Understanding**: Analyzes user's problem description
- **Safety Classification**: Automatically detects dangerous situations (burning smell, gas leaks, etc.) and recommends technician
- **Self-Troubleshooting**: Step-by-step guidance for simple problems with parts suggestions
- **Technician Booking**: Complete booking flow with time slots and cost calculation
- **Conversation Memory**: Remembers context throughout the conversation
- **Rich UI**: Markdown formatting, image display, and clear step-by-step instructions

## Installation

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set OpenAI API Key:**
   
   On Windows (PowerShell):
   ```powershell
   $env:OPENAI_API_KEY="your-api-key-here"
   ```
   
   On Linux/Mac:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   
   Or create a `.env` file (not included in repo for security):
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

4. **Run the app:**
   ```bash
   streamlit run app/main.py
   ```

   The app will open in your browser automatically.

## How It Works

### 1. Appliance Identification

The assistant needs to know:
- What appliance it is (refrigerator, washing machine, etc.)
- Brand
- Model number
- Serial number
- Rough age (if available)

**Option A:** Type the information in the chat:
- "Samsung refrigerator, model RT42, serial ABC1234"

**Option B:** Upload a photo of the nameplate:
- Click "Upload a photo of your appliance nameplate"
- The assistant uses OpenAI Vision API to read the text
- It extracts brand, model, serial, and estimates age
- You can confirm or correct the information

### 2. Problem Description

Once the appliance is identified, the assistant asks:
- "What problem are you facing with this appliance?"

Examples:
- "The fridge light isn't working"
- "The washing machine doesn't spin"
- "The fridge is making a burning smell"
- "It's not cooling properly"

### 3. Safety Check

The assistant automatically checks for dangerous keywords:
- "burning smell", "smoke", "sparks", "gas leak", etc.

If detected, it **immediately recommends booking a technician** for safety.

### 4. Troubleshooting Flow (Self-Fix)

If the problem is simple and safe:
- The assistant provides clear, numbered troubleshooting steps
- Suggests parts needed (with part numbers and prices)
- Asks if the steps fixed the problem
- If not, offers to book a technician

### 5. Technician Booking Flow

The booking flow can start:
- Automatically (if problem is complex or dangerous)
- On user request (user can say "I want to book a technician" at any time)

**Booking Steps:**
1. Confirm appliance details
2. Collect customer information:
   - Name
   - Phone number
   - Address
3. Show available time slots
4. User selects a time slot
5. Show cost breakdown:
   - Technician fee: $125 (fixed)
   - Parts cost (if applicable)
   - Total
6. User confirms booking
7. Booking is saved to `bookings.json`
8. Confirmation shown with Booking ID

## Example Scenarios

### Scenario 1: Simple Fix (Fridge Light)

1. User: "Samsung fridge, model RT42"
2. Bot: "Does this look correct?" → User: "Yes"
3. Bot: "What problem are you facing?"
4. User: "The light isn't working"
5. Bot: Provides step-by-step bulb replacement instructions + part info
6. User: "Yes, it's fixed!" → Done

### Scenario 2: Dangerous Problem (Burning Smell)

1. User uploads nameplate image
2. Bot extracts info and confirms
3. Bot: "What problem are you facing?"
4. User: "There's a burning smell"
5. Bot: ⚠️ Safety alert → Recommends technician
6. Bot guides through booking flow
7. Booking confirmed with ID

### Scenario 3: Complex Problem (Not Cooling)

1. User types appliance info
2. Bot confirms
3. User: "It's not cooling properly"
4. Bot: Recognizes as complex → Suggests technician
5. Booking flow completes

## File Structure

```
.
├── config.py             # Configuration settings
├── env.example           # Environment variables example
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── data/                  # Data files folder
│   ├── knowledge_base.json    # Problems, troubleshooting steps, parts, safety keywords
│   ├── bookings.json         # Saved bookings (starts empty)
│   └── README.md
├── assets/                # Sample assets
│   ├── sample_nameplates/    # Sample nameplate images for testing
│   └── README.md
├── components/            # UI components
│   ├── __init__.py
│   ├── forms.py          # Modular forms (AddressForm, BookingForm)
│   └── ui_helpers.py     # UI helper functions
├── tests/                 # Unit tests
│   ├── __init__.py
│   └── test_serial_decoder.py
└── app/                   # Main application package
    ├── __init__.py
    ├── main.py           # Main Streamlit application entry point (ApplianceTroubleshootApp class)
    ├── models/           # Data models
    │   ├── __init__.py
    │   ├── appliance.py  # Appliance data class
    │   ├── booking.py    # Booking, TimeSlot, CostBreakdown classes
    │   └── problem.py    # Problem and Part classes
    ├── services/         # Business logic services
    │   ├── __init__.py
    │   ├── openai_service.py      # OpenAI API interactions
    │   ├── appliance_service.py   # Appliance identification logic
    │   ├── problem_service.py     # Problem matching and classification
    │   └── booking_service.py     # Booking flow logic
    ├── repositories/     # Data access layer
    │   ├── __init__.py
    │   ├── knowledge_base_repository.py  # Knowledge base data access
    │   └── booking_repository.py         # Booking data access
    └── utils/            # Utility functions
        ├── __init__.py
        ├── state_manager.py   # Streamlit session state management
        ├── image_utils.py      # Image handling utilities
        ├── serial_decoder.py   # Serial number decoding and age estimation
        └── payment.py          # Mock payment processing service
```

## Architecture

The application follows **Object-Oriented Programming (OOP)** principles with a clean architecture:

- **Models**: Data classes representing domain entities (Appliance, Booking, Problem, etc.)
- **Repositories**: Data access layer for loading/saving data (KnowledgeBase, Bookings)
- **Services**: Business logic layer (OpenAI, Appliance, Problem, Booking services)
- **Utils**: Utility functions for state management and image processing
- **Main App**: Orchestrates all components using dependency injection

## Data Storage

- **No SQL database**: All data stored in local JSON files
- **Knowledge Base** (`knowledge_base.json`): Problems, steps, parts, prices
- **Bookings** (`bookings.json`): All confirmed bookings

## Safety Features

- Automatic detection of dangerous keywords
- Immediate technician recommendation for safety issues
- Clear warnings for potentially unsafe situations
- User can always request technician at any time

## Customization

You can customize the app by editing:

- **`knowledge_base.json`**: Add more problems, steps, parts, or adjust prices
- **`app.py`**: Modify flows, UI, or add features

## Notes

- This is a demo application
- No real payment processing (costs are shown but not charged)
- OpenAI API usage will incur costs (Vision API is more expensive than text)
- Image OCR results are cached per session to reduce API calls
- All bookings are stored locally in JSON format

## Troubleshooting

**App won't start:**
- Check that OpenAI API key is set correctly
- Ensure all dependencies are installed: `pip install -r requirements.txt`

**Image upload not working:**
- Ensure image is in JPG, JPEG, or PNG format
- Check that OpenAI API key has access to Vision API (gpt-4o model)

**Can't read nameplate:**
- Try uploading a clearer, well-lit photo
- Or type the information manually in chat

## License

This is a demo project for educational purposes.

