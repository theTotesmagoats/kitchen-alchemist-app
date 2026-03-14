"""
Kitchen Alchemist - Kitchen Timer & Temperature Guide for UniHiker M10
Retro 80s design with flip-clock style timers

Target: UniHiker M10 with Python 3 and unihicer library
Date: June 2026
"""

from unihiker import GUI
import time
import threading

# Initialize GUI
gui = GUI()

# Global variables for screen management
current_screen = 'home'
timer_data = {}
active_timers = []

# Screen dimensions (UniHiker M10 display)
SCREEN_WIDTH = 240
SCREEN_HEIGHT = 320

# Retro 80s color scheme
COLORS = {
    'primary': '#00FFFF',      # Electric Blue
    'accent': '#FF69B4',       # Hot Pink  
    'secondary': '#39FF14',    # Neon Green
    'warning': '#FFFF00',      # Bright Yellow
    'bg_dark': '#00008B',      # Dark Blue
    'text_light': '#FFFFFF',   # White
}

# Temperature reference data (in Fahrenheit)
TEMP_DATA = {
    'beef': [
        ('Rare', 125),
        ('Medium Rare', 135),
        ('Medium', 145),
        ('Medium Well', 155),
        ('Well Done', 160)
    ],
    'chicken': [('Safe', 165)],
    'pork': [('Safe', 145)],
    'ham': [('Reheat', 140), ('Cook', 145)],
    'turkey': [('Safe', 165)]
}

# Default timer settings (in seconds)
DEFAULT_TIMERS = {
    'S1': 300,   # 5 minutes
    'S2': 300,
    'S3': 300,
    'S4': 300,
    'S5': 300,
    'S6': 300,
    'O1': 1800,  # 30 minutes
    'O2': 1800
}

# UI Element references for updates
ui_elements = {}

def format_time(seconds):
    """Convert seconds to MM:SS format"""
    if seconds <= 0:
        return "00:00"
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

def clear_screen():
    """Remove all UI elements from current screen"""
    for element in ui_elements.values():
        try:
            element.config(text='')  # Clear text elements
        except:
            pass
    ui_elements.clear()

def show_home():
    """Display the main home screen"""
    global current_screen, ui_elements
    
    clear_screen()
    current_screen = 'home'
    
    # Title - center at top
    title = gui.draw_text(
        text='Kitchen Alchemist',
        x=120, y=35,
        font_size=24,
        color=COLORS['primary'],
        origin='center'
    )
    ui_elements['title'] = title
    
    # Subtitle - center at bottom
    subtitle = gui.draw_text(
        text="Kyra's Kitchen",
        x=120, y=305,
        font_size=14,
        color=COLORS['secondary'],
        origin='center'
    )
    ui_elements['subtitle'] = subtitle
    
    # Main buttons - spaced vertically with room for all
    btn_y_start = 90
    btn_spacing = 70
    
    btn_timers = gui.add_button(
        text='Timers',
        x=40, y=btn_y_start,
        w=160, h=50,
        onclick=lambda: show_timers()
    )
    ui_elements['btn_timers'] = btn_timers
    
    btn_temps = gui.add_button(
        text='Temperatures',
        x=40, y=btn_y_start + btn_spacing,
        w=160, h=50,
        onclick=lambda: show_temperature_menu()
    )
    ui_elements['btn_temps'] = btn_temps
    
    # Back button (small, at top)
    btn_back = gui.add_button(
        text='Back',
        x=200, y=10,
        w=35, h=25,
        onclick=lambda: show_home()
    )
    ui_elements['btn_back'] = btn_back

def show_timers():
    """Display the timer management screen - one at a time"""
    global current_screen, ui_elements
    
    clear_screen()
    current_screen = 'timers'
    
    # Title
    title = gui.draw_text(
        text='Stove & Oven Timers',
        x=120, y=30,
        font_size=20,
        color=COLORS['accent'],
        origin='center'
    )
    ui_elements['title'] = title
    
    # Timer buttons - stack vertically to fit on screen
    timer_positions = [
        ('S1', 30),   ('O1', 90),
        ('S2', 150),  ('O2', 210),
        ('S3', 30),   ('S4', 90),
        ('S5', 150),  ('S6', 210)
    ]
    
    for timer_id, y_pos in timer_positions:
        # Initialize timer if not exists
        if timer_id not in timer_data:
            timer_data[timer_id] = {
                'seconds': DEFAULT_TIMERS.get(timer_id, 300),
                'running': False,
                'original_seconds': DEFAULT_TIMERS.get(timer_id, 300)
            }
        
        # Create timer display (large, centered)
        timer_text = f'{timer_id}: {format_time(timer_data[timer_id]["seconds"])}'
        
        timer_display = gui.draw_text(
            text=timer_text,
            x=120, y=y_pos + 35,
            font_size=24,
            color=COLORS['text_light'],
            origin='center'
        )
        ui_elements[f'timer_{timer_id}'] = timer_display
        
        # Create control buttons for this timer
        if timer_data[timer_id]['running']:
            control_text = 'Pause'
        else:
            control_text = 'Start'
        
        # Control button - positioned to the right of display
        ctrl_btn = gui.add_button(
            text=control_text,
            x=150, y=y_pos + 20,
            w=60, h=30,
            onclick=lambda tid=timer_id: toggle_timer(tid)
        )
        ui_elements[f'ctrl_{timer_id}'] = ctrl_btn
        
        # Reset button - positioned to the right of control
        reset_btn = gui.add_button(
            text='Reset',
            x=215, y=y_pos + 20,
            w=45, h=30,
            onclick=lambda tid=timer_id: reset_timer(tid)
        )
        ui_elements[f'reset_{timer_id}'] = reset_btn
    
    # Back button
    btn_back = gui.add_button(
        text='Back',
        x=60, y=295,
        w=120, h=35,
        onclick=lambda: show_home()
    )
    ui_elements['btn_back'] = btn_back

def toggle_timer(timer_id):
    """Toggle a specific timer's running state"""
    if timer_id in timer_data:
        timer_data[timer_id]['running'] = not timer_data[timer_id]['running']
        update_timer_display(timer_id)

def reset_timer(timer_id):
    """Reset a specific timer to its original value"""
    if timer_id in timer_data:
        timer_data[timer_id]['seconds'] = timer_data[timer_id].get('original_seconds', DEFAULT_TIMERS.get(timer_id, 300))
        timer_data[timer_id]['running'] = False
        update_timer_display(timer_id)

def update_timer_display(timer_id):
    """Update the display for a specific timer"""
    if timer_id in ui_elements:
        # Update main timer text
        time_str = format_time(timer_data[timer_id]['seconds'])
        ui_elements[f'timer_{timer_id}'].config(text=f'{timer_id}: {time_str}')
        
        # Update control button text
        ctrl_btn = ui_elements.get(f'ctrl_{timer_id}')
        if ctrl_btn:
            if timer_data[timer_id]['running']:
                ctrl_btn.config(text='Pause')
            else:
                ctrl_btn.config(text='Start')

def start_timer_countdown():
    """Start the global timer countdown thread"""
    def countdown_loop():
        while True:
            if current_screen == 'timers':
                for timer_id, data in timer_data.items():
                    if data['running'] and data['seconds'] > 0:
                        data['seconds'] -= 1
                        update_timer_display(timer_id)
                        
                        # Check if timer finished
                        if data['seconds'] <= 0 and data['running']:
                            # Timer finished - could add buzzer alert here
                            pass
            
            time.sleep(1)  # Update every second
    
    # Start the countdown thread
    timer_thread = threading.Thread(target=countdown_loop, daemon=True)
    timer_thread.start()

def show_temperature_menu():
    """Display the temperature reference menu"""
    global current_screen, ui_elements
    
    clear_screen()
    current_screen = 'temps'
    
    # Title
    title = gui.draw_text(
        text='Cooking Temperatures',
        x=120, y=30,
        font_size=22,
        color=COLORS['secondary'],
        origin='center'
    )
    ui_elements['title'] = title
    
    # Temperature category buttons - stack vertically
    temp_categories = [
        ('Beef', 'beef'),
        ('Chicken', 'chicken'),
        ('Pork', 'pork'),
        ('Ham', 'ham'),
        ('Turkey', 'turkey')
    ]
    
    btn_y_start = 80
    btn_spacing = 55
    
    for i, (name, key) in enumerate(temp_categories):
        btn_y = btn_y_start + (i * btn_spacing)
        
        temp_btn = gui.add_button(
            text=name,
            x=40, y=btn_y,
            w=160, h=45,
            onclick=lambda k=key: show_temp_details(k)
        )
        ui_elements[f'temp_{key}'] = temp_btn
    
    # Back button
    btn_back = gui.add_button(
        text='Back',
        x=60, y=300,
        w=120, h=35,
        onclick=lambda: show_home()
    )
    ui_elements['btn_back'] = btn_back

def show_temp_details(meat_type):
    """Display detailed temperature information for a meat type"""
    global current_screen, ui_elements
    
    clear_screen()
    current_screen = f'temp_{meat_type}'
    
    # Title
    title = gui.draw_text(
        text=f'{meat_type.capitalize()} Temps',
        x=120, y=30,
        font_size=24,
        color=COLORS['primary'],
        origin='center'
    )
    ui_elements['title'] = title
    
    # Display temperature details - list vertically
    if meat_type in TEMP_DATA:
        temp_info = TEMP_DATA[meat_type]
        
        y_offset = 70
        for level, temp in temp_info:
            temp_text = f'{level}: {temp}°F'
            
            text_elem = gui.draw_text(
                text=temp_text,
                x=20, y=y_offset,
                font_size=18,
                color=COLORS['text_light'],
                origin='top_left'
            )
            ui_elements[f'temp_{level.replace(" ", "_")}'] = text_elem
            
            y_offset += 35
    
    # Back button
    btn_back = gui.add_button(
        text='Back',
        x=60, y=295,
        w=120, h=35,
        onclick=lambda: show_temperature_menu()
    )
    ui_elements['btn_back'] = btn_back

def main():
    """Main application entry point"""
    # Initialize all timers
    for timer_id in DEFAULT_TIMERS.keys():
        if timer_id not in timer_data:
            timer_data[timer_id] = {
                'seconds': DEFAULT_TIMERS[timer_id],
                'running': False,
                'original_seconds': DEFAULT_TIMERS[timer_id]
            }
    
    # Show home screen initially
    show_home()
    
    # Start timer countdown thread
    start_timer_countdown()
    
    # Keep the program running
    while True:
        time.sleep(0.1)

if __name__ == '__main__':
    main()