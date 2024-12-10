import time
import lvgl as lv
import peripherals

# App Name
NAME = "Countdown"

# App Icon
ICON: str = "A:apps/countdown/resources/icon.png"

# LVGL widgets
scr = None
label = None
arc = None
bar = None

# Countdown parameters
DEFAULT_REMAINDER = 30
remainder = [DEFAULT_REMAINDER]
remainder_index = 0
remaining_time = DEFAULT_REMAINDER
use_clock = False

app_mgr = None
last_displayed_time = 0
total_seconds = 0
countdown_is_running = False
start_time_ms = 0
start_time_value = 0

NUMBER = [ 0x5F, 0x06, 0x3B, 0x2F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F ]

def get_settings_json():
    return {
        "form": [{
            "type": "input",
            "default": str(DEFAULT_REMAINDER),
            "caption": "Countdown Timer Duration(s), comma separated",
            "name": "remainder",
            "attributes": {"maxLength": 40, "placeholder": "e.g., 300"},
        }, { 
            "type": "switch",
            "default": "false",
            "caption": "Use big clock display?",
            "name": "use_clock",
            "options": [ "keep clock", "show countdown as clock" ]
        }]
    }

def reset_countdown():
    global remainder, remainder_index, remaining_time, countdown_is_running, last_recorded_time, total_seconds, use_clock
    last_recorded_time = 0
    countdown_is_running = False
    remainder = app_mgr.config().get("remainder", DEFAULT_REMAINDER).split(",")
    print(remainder)
    total_seconds = int(remainder[remainder_index])
    remaining_time = total_seconds
    
    use_clock = app_mgr.config().get("use_clock", None)
    print(use_clock)

def update_label():
    global label, remaining_time
    if label:
        label.set_text("{:02d}:{:02d}".format(remaining_time // 60, remaining_time % 60))
        
def update_clock(remaining_time, tick):
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    
    # Set LED clock display
    peripherals.led_clock.set_display(1, NUMBER[minutes // 10])
    peripherals.led_clock.set_display(2, NUMBER[minutes % 10])
    peripherals.led_clock.set_display(3, NUMBER[seconds // 10])
    peripherals.led_clock.set_display(4, NUMBER[seconds % 10])
    peripherals.led_clock.set_display(5, 0x00)
    peripherals.led_clock.set_display(6, 0x01)

    # Set LED clock brightness
    peripherals.led_clock.brightness(100)

def update_arc(percent):
    global arc
    arc.set_value(percent)
    if percent > 30:
        arc.set_style_arc_color(lv.palette_main(lv.PALETTE.GREEN), lv.PART.INDICATOR)
        arc.set_style_bg_color(lv.palette_lighten(lv.PALETTE.GREEN, 2), lv.PART.KNOB)
    elif percent > 15:
        arc.set_style_arc_color(lv.palette_main(lv.PALETTE.YELLOW), lv.PART.INDICATOR)
        arc.set_style_bg_color(lv.palette_lighten(lv.PALETTE.YELLOW, 2), lv.PART.KNOB)
    else:
        arc.set_style_arc_color(lv.palette_main(lv.PALETTE.RED), lv.PART.INDICATOR)
        arc.set_style_bg_color(lv.palette_lighten(lv.PALETTE.RED, 2), lv.PART.KNOB)
        
def update_bar(percent):
    global bar
    bar.set_value(100-percent, 100)
    #if percent > 30:
    #    bar.set_style_bar_color(lv.palette_main(lv.PALETTE.GREEN), lv.PART.BG)
    #elif percent > 15:
    #    bar.set_style_bar_color(lv.palette_main(lv.PALETTE.YELLOW), lv.PART.BG)
    #else:
    #    bar.set_style_bar_color(lv.palette_main(lv.PALETTE.RED), lv.PART.BG)
            
def update_ambient_color(percent):
    if percent > 30:
        peripherals.ambient_light.set_color([(0, 255, 0)], True)
    elif percent > 15:
        peripherals.ambient_light.set_color([(255, 255, 0)], True)
    else:
        peripherals.ambient_light.set_color([(255, 0, 0)], True)
    peripherals.ambient_light.brightness(100)
    

def event_handler(event):
    global countdown_is_running, app_mgr
    e_code = event.get_code()
    if e_code == lv.EVENT.KEY:
        e_key = event.get_key()

        if e_key == lv.KEY.ENTER:
            global last_displayed_time, start_time_ms, start_time_value, use_clock
            countdown_is_running = not countdown_is_running
            if countdown_is_running:
                peripherals.ambient_light.acquire()
                start_time_ms = time.ticks_ms()
                last_displayed_time = remaining_time
                start_time_value = remaining_time
                if use_clock:
                    peripherals.led_clock.acquire()
            else:
                peripherals.ambient_light.release()
                if use_clock:
                    peripherals.led_clock.release()
            print(countdown_is_running)
            
        if not countdown_is_running:
            global remainder_index
            if e_key == lv.KEY.LEFT:
                remainder_index = remainder_index + 1
                if remainder_index >= len(remainder):
                    remainder_index = 0
                reset_countdown()
                update_label()
            if e_key == lv.KEY.RIGHT:
                remainder_index = remainder_index - 1
                if remainder_index < 0:
                    remainder_index = len(remainder) -1
                reset_countdown()
                update_label()
                
#        if e_key == lv.KEY.ESC:
#            global total_seconds, remaining_time
#            if total_seconds != remaining_time:
#                reset_countdown()
#                update_label()
#                update_arc(100)
#            else:
#                await app_mgr.exit()
                
                
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
    global scr, label, arc, bar
    reset_countdown()

    scr = lv.obj()
    lv.scr_load(scr)

    label = lv.label(scr)
    label.set_text("--:--")
    # label.set_style_text_font(lv.font_montserrat_48, 0)  # Increase font size
    label.center()
    
    if use_clock:
        bar = lv.bar(scr)
        bar.set_size(320,240)
        # bar.align(None,lv.ALIGN.CENTER,0,0)
        bar.set_range(0,100)
        # bar.set_anim_time(2000)
        bar.set_value(100, 100)
    else:
        arc = lv.arc(scr)
        arc.set_size(200, 200)
        arc.center()
        arc.set_rotation(270)
        arc.set_range(0, 100)
        arc.set_bg_angles(0,360)
        arc.set_angles(0,360)

    update_label()
    if use_clock:
        update_bar(0)
    else:
        update_arc(100)

    scr.add_event(event_handler, lv.EVENT.ALL, None)

    group = lv.group_get_default()
    if group:
        group.add_obj(scr)
        lv.group_focus_obj(scr)
        group.set_editing(True)

async def on_running_foreground():
    """Called when the app is active, approximately every 200ms."""
    global remaining_time, start_time_ms, countdown_is_running, start_time_value, last_displayed_time
    
    if not countdown_is_running or remaining_time <= 0:
        return

    current_time = time.ticks_ms()
    elapsed_time = time.ticks_diff(current_time, start_time_ms) // 1000
    remaining_time = max(start_time_value - elapsed_time, 0)
    if remaining_time != last_displayed_time:
        last_displayed_time = remaining_time  
        percent = int(remaining_time * 100 / total_seconds)
        update_label()
        if use_clock:
            update_clock(remaining_time)
            update_bar(percent)
        else:
            update_arc(percent)
        update_ambient_color(percent)
    


