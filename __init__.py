import time
import lvgl as lv
import peripherals

# App Name
NAME = "Countdown"

# LVGL widgets
scr = None
label = None
arc = None

# Countdown parameters
DEFAULT_REMAINDER = 30
remainder = DEFAULT_REMAINDER

app_mgr = None
last_recorded_time = 0
total_seconds = 0
countdown_is_running = False

ARC_COLORS = {
    'green': lv.palette_main(lv.PALETTE.GREEN),
    'yellow': lv.palette_main(lv.PALETTE.YELLOW),
    'red': lv.palette_main(lv.PALETTE.RED)
}

def get_settings_json():
    return {
        "form": [{
            "type": "input",
            "default": str(DEFAULT_REMAINDER),
            "caption": "Countdown Timer Duration(s)",
            "name": "remainder",
            "attributes": {"maxLength": 6, "placeholder": "e.g., 300"},
        }]
    }

def reset_countdown():
    global remainder, countdown_is_running, last_recorded_time, total_seconds
    last_recorded_time = 0
    countdown_is_running = False
    remainder = int(app_mgr.config().get("remainder", DEFAULT_REMAINDER))
    total_seconds = remainder

def update_label():
    global label, arc, remainder
    if label:
        label.set_text("{:02d}:{:02d}".format(remainder // 60, remainder % 60))        

def update_arc(percent):
    arc.set_value(percent)
    if percent > 30:
        arc.set_style_arc_color(ARC_COLORS['green'], lv.PART.INDICATOR)
    else:
        if percent > 15:
            arc.set_style_arc_color(ARC_COLORS['yellow'], lv.PART.INDICATOR)
        else:
            arc.set_style_arc_color(ARC_COLORS['red'], lv.PART.INDICATOR)
            
def update_ambient_color(percent):
    if percent > 30:
        peripherals.ambient_light.set_color([(0, 255, 0)], True)
    else:
        if percent > 15:
            peripherals.ambient_light.set_color([(255, 255, 0)], True)
        else:
            peripherals.ambient_light.set_color([(255, 0, 0)], True)
    peripherals.ambient_light.brightness(100)
    

def event_handler(event):
    e_code = event.get_code()
    if e_code == lv.EVENT.KEY:
        e_key = event.get_key()
        if e_key == lv.KEY.ENTER:
            global countdown_is_running, last_recorded_time
            last_recorded_time = time.ticks_ms()
            countdown_is_running = not countdown_is_running
            if countdown_is_running:
                peripherals.ambient_light.acquire()
            else:
                peripherals.ambient_light.release()
            print(countdown_is_running)

async def on_boot(apm):
    global app_mgr
    app_mgr = apm

async def on_stop():
    print('on stop')
    global scr
    if scr:
        scr.clean()
        scr.del_async()
        scr = None
    reset_countdown()

async def on_start():
    print('on start')
    global scr, label, arc
    reset_countdown()

    scr = lv.obj()
    lv.scr_load(scr)

    label = lv.label(scr)
    label.set_text("--:--")
    # label.set_style_text_font(lv.font_montserrat_48, 0)  # Increase font size
    label.center()
    
    arc = lv.arc(scr)
    arc.set_size(200, 200)
    arc.center()
    arc.set_rotation(270)
    arc.set_range(0, 100)
    arc.set_bg_angles(0,360)
    arc.set_angles(0,360)

    update_label()
    update_arc(100)

    scr.add_event(event_handler, lv.EVENT.ALL, None)

    group = lv.group_get_default()
    if group:
        group.add_obj(scr)
        lv.group_focus_obj(scr)
        group.set_editing(True)

async def on_running_foreground():
    """Called when the app is active, approximately every 200ms."""
    global remainder, last_recorded_time, countdown_is_running
    
    if not countdown_is_running or remainder <= 0:
        return

    current_time = time.ticks_ms()
    elapsed_time = time.ticks_diff(current_time, last_recorded_time) // 1000
    if elapsed_time > 0:
        remainder -= elapsed_time
        last_recorded_time = current_time
        remainder = max(remainder, 0)  
        percent = int(remainder * 100 / total_seconds)
        update_label()
        update_arc(percent)
        update_ambient_color(percent)

