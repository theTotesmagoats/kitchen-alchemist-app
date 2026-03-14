# Kitchen Alchemist - UniHiker M10 Application

A retro 80s-themed kitchen timer and temperature reference guide for the UniHiker M10 device.

## Features

### Main Screen (Kitchen Alchemist)
- Title "Kitchen Alchemist" with subtitle "Kyra's Kitchen"
- Three main buttons: Home, Timers, and Temperatures
- Retro electric blue and hot pink color scheme

### Timer Screen
- 8 timer controls: S1-S6 for stove burners, O1-O2 for ovens
- Flip-clock style display showing MM:SS format
- Large touch-friendly buttons (100x45 pixels)
- Start/Pause/Reset controls for each timer
- Default times: 5 minutes for stove timers, 30 minutes for oven timers

### Temperature Reference Screen
- Quick reference for major meat types: Beef, Chicken, Pork, Ham, Turkey
- Detailed cooking levels for beef (Rare, Medium Rare, Medium, Medium Well, Well Done)
- Safe minimum temperatures based on USDA guidelines (2026 standards)

## Retro 80s Design
- **Primary Color**: Electric Blue (#00FFFF)
- **Accent Color**: Hot Pink (#FF69B4)  
- **Secondary Color**: Neon Green (#39FF14)
- **Warning Color**: Bright Yellow (#FFFF00)
- Large, readable fonts (24px+ for main text)
- Blocky timer display format

## Hardware Requirements
- UniHiker M10 device
- Python 3 environment
- unihiker library installed

## Installation & Usage

### Option 1: Direct Copy to Device
1. Copy `kitchen_alchemist.py` to your UniHiker M10 device
2. Run directly on the device using Jupyter Notebook or Python IDLE:
   ```python
   from kitchen_alchemist import *
   main()
   ```

### Option 2: Using Jupyter Notebook
1. Open a new Jupyter Notebook on your UniHiker
2. Copy and paste the code into a cell
3. Execute the cell to start the application

## Testing Guide

### Main Screen Tests
1. **Title Display**: Verify "Kitchen Alchemist" appears in electric blue at top center
2. **Subtitle Display**: Confirm "Kyra's Kitchen" appears in neon green at bottom center  
3. **Button Navigation**: Test each button (Home, Timers, Temperatures) to ensure proper navigation

### Timer Screen Tests
1. **Timer Display**: Verify all 8 timers (S1-S6, O1-O2) appear with correct labels and times
2. **Timer Controls**: 
   - Test Start/Pause functionality
   - Test Reset functionality  
   - Verify time display updates correctly
3. **Navigation**: Confirm Back button returns to main menu

### Temperature Screen Tests
1. **Category Menu**: Verify all 5 meat categories appear as buttons
2. **Detailed Views**:
   - Beef: Check for Rare (125°F), Medium Rare (135°F), Medium (145°F), Medium Well (155°F), Well Done (160°F)
   - Chicken: Verify safe temperature 165°F
   - Pork: Verify safe temperature 145°F
   - Ham: Check reheat (140°F) and cook (145°F) temperatures
   - Turkey: Verify safe temperature 165°F

## Technical Details

### Timer System
- Uses threading for concurrent countdown operations
- Updates display every second
- Preserves timer state when navigating between screens
- Handles default values for all timers

### Temperature Reference
- Based on USDA Food Safety Guidelines (2026)
- Includes both safe minimum temperatures and cooking level preferences
- Organized by meat type with clear temperature labels

## Customization

### Changing Colors
Edit the COLORS dictionary at the top of the file:
```python
COLORS = {
    'primary': '#00FFFF',      # Electric Blue
    'accent': '#FF69B4',       # Hot Pink  
    'secondary': '#39FF14',    # Neon Green
    'warning': '#FFFF00',      # Bright Yellow
    'bg_dark': '#00008B',      # Dark Blue
    'bg_black': '#000000',     # Black
    'text_light': '#FFFFFF',   # White
}
```

### Adjusting Timer Defaults
Modify the DEFAULT_TIMERS dictionary:
```python
DEFAULT_TIMERS = {
    'S1': 300,   # 5 minutes for stove timers
    'O1': 1800,  # 30 minutes for oven timers
    # ... etc
}
```

## Troubleshooting

### Common Issues
1. **Buttons not responding**: Ensure unihiker library is properly installed
2. **Display issues**: Check screen resolution compatibility (designed for ~240x320)
3. **Timer not counting down**: Verify threading support in your Python environment

### Error Messages
If you see "ModuleNotFoundError: No module named 'unihiker'", install the library:
```bash
pip install unihiker
```

## Credits
- Designed for UniHiker M10
- Retro 80s color scheme inspiration from classic kitchen appliances
- Temperature guidelines based on USDA Food Safety Standards (2026)

## License
This project is open source and available for personal use.
