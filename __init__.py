import time
import lvgl as lv
import peripherals

# App Name
NAME = "Countdown"

# App Icon
ICON = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00.\x00\x00\x00.\x08\x03\x00\x00\x00`g\xdb\x05\x00\x00\x00\x9cPLTE\x00\x00\x00L\xafP\xff\xff\xff\xfa\xfc\xfaN\xb0R\xf6\xfa\xf6\xdd\xeb\xdd\xee\xf5\xef\xcb\xe1\xcc\xc7\xdf\xc9]\xb3a\xf1\xf7\xf1\xab\xd1\xad\x96\xc7\x98\xed\xf4\xed\xd4\xe6\xd4\xd0\xe4\xd1\xce\xe3\xcf\xb8\xd8\xba\xb4\xd5\xb5\xae\xd2\xaf\x8c\xc3\x8e}\xbe\x80\xe4\xef\xe5\xda\xe9\xda\x9d\xca\x9fx\xbc{r\xbauQ\xb0U\xf3\xf8\xf3\xea\xf3\xea\xc2\xdc\xc3\xbc\xd9\xbd\xa8\xcf\xa9\xa3\xcd\xa4u\xbaw\xe6\xf0\xe6\x86\xc1\x88\x83\xc0\x85m\xb8pc\xb5fX\xb2[\xfc\xfe\xfc\xe7\xf1\xe7\xe0\xed\xe1\xd6\xe7\xd6\xc5\xde\xc6\xbe\xdb\xbf\x9f\xcb\xa1\x9b\xc9\x9d\x93\xc6\x94V\xb2Z\xc6z(P\x00\x00\x00\x01tRNS\x00@\xe6\xd8f\x00\x00\x01\xc8IDATH\xc7\x9d\x95\xd7r\x830\x10E\xbdW\xf4jz\x89{\x89\x9d\xde\xfe\xff\xdf\x12b4\x92\x12\xa1xr\x1e\x98a9\x88E,\xbb\xb3\x9f\x90\xc2\xcc\x08i\x98\x96'\x98\xb4\xaf\xf7\xc9\xc8\xb4\x1d\xaf\x9d\x04_,\x1f\xa3\t_\xd8\xe7\xb5\r\x01I\xe8\xec\x92\rV\xf8\xf4\\\x14\xfe\xd3\xca\xff\x8a\xbc\xe6\x96\xf0U;p\x86\x1c6{\x12\xdc0\xdc\xfeZ\x7f\xbc\x94\x00,\xbf#\x19\x0f\x0eqT\xfb\x14\x02\xcd\x9eT6n/Nd\xfb\xa3\x01\xe6\x16\xe9\xa8\xbd\x1b\xc9\xe7\x8f\xc5\x9c\xb4\xc4\x0c\x85\xd0\xc7\x18\xd0,\xf4\xba\x0b'\xa0\x0b\\\xb7\x12\xb0\x9e\xf4\xec\xf8^\n}\x0b\xe4\xf47<\x97\x15\xec\xc0\xe4\xdd\xbe\x8d>\r\x1c\x01\xdf \x1f\x13\xa0\x96\xf4\x17\xa02\xe8%l_^\xdd\x01#\x89\xd3:\x8b\xac\xcb\x16X\xdf\xc7\xea\x8ed\xdd\xc5\x83d\xefm\x00MzX\xb9\xf7\x08EX\xe8@J\x82\x0c\x02G\xa7\xab_\xf40\xaa\xac\x8dN\x97H\xe5\xcd\xb7\x93\xba\x87\x81\xac\x13\xc5\xf9\x000%\xf7V.\xf2\x10?\n\xa8*\x8aX\xd2\x1f\x91\x90\xc4\xb9\xf4\xdfH\x03\xd7\xd7\xc0\x99TLz\x0c\xecL%\xd0-\x14\x9dl8\x06=\x81](\xba\x07\xd4\xd3z\xe4\xc2QJ\xb2\x07Z2\xd0\x07J\xbdS\xca\xb37\"\xba\x06\x03\xd3\xa7S\x1ebI\xe7~\t\x84\xbdN\x7f\x06\"\xb9s\x88\xc2Z\xf2\xa2\xdf\xad\xda\x8e\xff\xa0\x96\x8fV\xd3h\xac\x14`\x9b\x05\x7f\x13\xd8\x19O\xa2\x0etm\x8c|\x00n4\xdc\xb0\xc17\xb6\xb7\xd7\xf5`\x1e\xe8\x96\x83\x93n\x8f\xaf\x18i4\xba\xf0\x83\xdc\x86\x82gn\xf0\x14l\x1d&\xeclr|\x08\x16U\xe9\x87\x18\xc8\xaf\x18N\xbc\x93\xe0>\xbaz\xf6u\x00{\xbf~\xb0\x06\xa1[\xffon\xcf\x8c\x98\xddOw-\x19\x84\x8bn:\xe1\x00\x00\x00\x00IEND\xaeB`\x82"


# LVGL widgets for UI elements
scr = None  # Main screen object
label = None  # Label to display countdown time
arc = None  # Arc widget for circular progress
bar = None  # Bar widget for linear progress

# Countdown configuration parameters
DEFAULT_REMAINDER = 30  # Default countdown duration in seconds
remainder = [DEFAULT_REMAINDER]  # List of countdown durations
remainder_index = 0  # Current index in remainder list
remaining_time = DEFAULT_REMAINDER  # Current remaining time
use_clock = False  # Whether to use LED clock display
ambient_light = True  # Whether to use ambient light indicators
time_display = 1  # Display mode (1=bar, 2=arc)

# App state variables
app_mgr = None  # App manager instance
last_displayed_time = 0  # Last displayed countdown time
total_seconds = 0  # Total duration of current countdown
countdown_is_running = False  # Whether countdown is active
start_time_ms = 0  # Start time in milliseconds
start_time_value = 0  # Initial countdown value

# LED segment display patterns for digits 0-9
NUMBER = [0x5F, 0x06, 0x3B, 0x2F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F]


def get_settings_json():
    """
    Returns the settings configuration for the app UI. Includes input for duration, 
    switches for clock/ambient light, and display mode selection.

    See https://dock.myvobot.com/developer/reference/web-page/ for reference.
    """
    return {
        "form": [
            {
                "type": "input",
                "default": str(DEFAULT_REMAINDER),
                "caption": "Countdown Timer Duration(s), comma separated",
                "name": "remainder",
                "attributes": {"maxLength": 40, "placeholder": "e.g., 300"},
            },
            {
                "type": "switch",
                "default": "false",
                "caption": "Use big clock display for countdown?",
                "name": "use_clock",
                "tip": "Use the big clock to display the countdown or do you want to see the current time?",
            },
            {
                "type": "switch",
                "default": "true",
                "caption": "Use ambient light?",
                "name": "ambient_light",
                "tip": "If on, the ambient light shows, if you are getting close to the end. At 30% remaining time it switches to yellow and at 15% it switches to red.",
            },
            {
                "type": "radio",
                "default": "1",
                "caption": "How to display the remaining time?",
                "name": "display",
                "options": [
                    ("Display remaining time as bar", "1"),
                    ("Display remaining time as arc", "2"),
                ],
            },
        ]
    }


def reset_countdown():
    """
    Resets the countdown timer to initial state.
    Loads settings from app config and initializes countdown parameters
    """
    global remainder, remainder_index, remaining_time, countdown_is_running, last_recorded_time, total_seconds, use_clock, ambient_light, time_display

    last_recorded_time = 0
    countdown_is_running = False
    remainder = app_mgr.config().get("remainder", str(DEFAULT_REMAINDER)).split(",")
    print(remainder)
    total_seconds = int(remainder[remainder_index])
    remaining_time = total_seconds
    use_clock = app_mgr.config().get("use_clock", False)
    ambient_light = app_mgr.config().get("ambient_light", True)
    time_display = int(app_mgr.config().get("display", "1"))


def update_label():
    """
    Updates the time display label with current remaining time.

    Formats time as MM:SS
    """
    global label, remaining_time
    if label:
        label.set_text(
            "{:02d}:{:02d}".format(remaining_time // 60, remaining_time % 60)
        )


def update_clock(remaining_time):
    """
    Updates the LED clock display with current remaining time.
    Sets individual LED segments for each digit and brightness.
    """
    minutes = remaining_time // 60
    seconds = remaining_time % 60

    # Set LED clock display
    peripherals.led_clock.set_display(1, NUMBER[minutes // 10])
    peripherals.led_clock.set_display(2, NUMBER[minutes % 10])
    peripherals.led_clock.set_display(3, NUMBER[seconds // 10])
    peripherals.led_clock.set_display(4, NUMBER[seconds % 10] | 0x80) # Show the : between minute and second
    peripherals.led_clock.set_display(5, 0x00)
    peripherals.led_clock.set_display(6, 0x00)

    # Set LED clock brightness
    peripherals.led_clock.brightness(100)


def update_arc(percent):
    """
    Updates the arc progress indicator with remaining percentage.
    Changes color based on remaining time thresholds.
    """
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
    """
    Updates the progress bar with remaining percentage. Changes color based on remaining time thresholds.
    """
    global bar
    bar.set_value(100 - percent, lv.ANIM.ON)
    if percent > 30:
        bar.set_style_bg_color(lv.palette_main(lv.PALETTE.GREEN), lv.PART.INDICATOR)
    elif percent > 15:
        bar.set_style_bg_color(lv.palette_main(lv.PALETTE.YELLOW), lv.PART.INDICATOR)
    else:
        bar.set_style_bg_color(lv.palette_main(lv.PALETTE.RED), lv.PART.INDICATOR)


def update_ambient_color(percent):
    """
    Updates the ambient light color based on remaining percentage
    """
    if percent > 30:
        peripherals.ambient_light.set_color([(0, 255, 0)], True)
    elif percent > 15:
        peripherals.ambient_light.set_color([(255, 255, 0)], True)
    else:
        peripherals.ambient_light.set_color([(255, 0, 0)], True)
    peripherals.ambient_light.brightness(100)


def event_handler(event):
    """
    Handles UI input events:
     * ENTER starts/stops countdown
     * LEFT/RIGHT changes timer duration when stopped
    """
    global countdown_is_running, app_mgr
    e_code = event.get_code()
    if e_code == lv.EVENT.KEY:
        e_key = event.get_key()

        if e_key == lv.KEY.ENTER:
            global last_displayed_time, start_time_ms, start_time_value, use_clock, ambient_light
            countdown_is_running = not countdown_is_running
            if countdown_is_running:
                start_time_ms = time.ticks_ms()
                last_displayed_time = remaining_time
                start_time_value = remaining_time
                if ambient_light:
                    peripherals.ambient_light.acquire()
                if use_clock:
                    peripherals.led_clock.acquire()
            else:
                if use_clock:
                    peripherals.led_clock.release()
                if ambient_light:
                    peripherals.ambient_light.release()
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
                    remainder_index = len(remainder) - 1
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
    """
    Initializes app manager on boot.
    """
    global app_mgr
    app_mgr = apm


async def on_stop():
    """
    Cleanup when app stops. Removes screen and resets countdown.
    """
    print("on stop")
    global scr
    if scr:
        scr.clean()
        scr.del_async()
        scr = None
    reset_countdown()


async def on_start():
    """
    Initializes UI when app starts.
    Creates screen, progress indicator (bar/arc) and time label.
    """
    print("on start")
    global scr, label, arc, bar, time_display
    reset_countdown()

    scr = lv.obj()
    lv.scr_load(scr)

    if time_display == 1:
        bar = lv.bar(scr)
        bar.set_size(320, 240)
        bar.set_range(0, 100)
        bar.set_value(0, lv.ANIM.OFF)
        bar.set_style_bg_color(lv.palette_main(lv.PALETTE.GREEN), lv.PART.INDICATOR)
        bar.set_style_radius(0, lv.PART.MAIN)
        bar.set_style_radius(0, lv.PART.INDICATOR)
    else:
        arc = lv.arc(scr)
        arc.set_size(200, 200)
        arc.center()
        arc.set_rotation(270)
        arc.set_range(0, 100)
        arc.set_bg_angles(0, 360)
        arc.set_angles(0, 360)

    label = lv.label(scr)
    label.set_text("--:--")
    if time_display == 1:
        # Increase font size
        # see https://discuss.myvobot.com/t/how-to-increase-font-size-of-a-label/165/2 for available fonts
        label.set_style_text_font(lv.font_numbers_92, 0)
    else:
        # Increase font size
        # see https://discuss.myvobot.com/t/how-to-increase-font-size-of-a-label/165/2 for available fonts
        label.set_style_text_font(lv.font_ascii_bold_48, 0)
    label.center()

    update_label()
    if time_display == 1:
        update_bar(100)
    else:
        update_arc(100)

    scr.add_event(event_handler, lv.EVENT.ALL, None)

    group = lv.group_get_default()
    if group:
        group.add_obj(scr)
        lv.group_focus_obj(scr)
        group.set_editing(True)


async def on_running_foreground():
    """
    Main app loop that runs while app is active.
    Updates countdown time and display elements every 200ms.
    """
    global remaining_time, start_time_ms, countdown_is_running, start_time_value, last_displayed_time, use_clock, ambient_light, time_display

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

        if time_display == 1:
            update_bar(percent)
        else:
            update_arc(percent)

        if ambient_light:
            update_ambient_color(percent)
