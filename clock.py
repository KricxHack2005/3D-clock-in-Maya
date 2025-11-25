import maya.cmds as cmds
import datetime, threading, time

# ==========================================
# CONFIGURATION
# ==========================================
AXIS = 'rotateY'       # the rotation axis of your clock hands
UPDATE_INTERVAL = 1.0  # seconds between updates
clock_thread_running = False

# names of your hands
HOUR = 'hour_hand1'
MINUTE = 'minute_hand1'
SECOND = 'second_hand1'

# ==========================================
# RESET FUNCTION
# ==========================================
def reset_clock_hands():
    """Reset all clock hand rotations to 0°."""
    for hand in [HOUR, MINUTE, SECOND]:
        if cmds.objExists(hand):
            cmds.setAttr(f'{hand}.rotateX', 0)
            cmds.setAttr(f'{hand}.rotateY', 0)
            cmds.setAttr(f'{hand}.rotateZ', 0)
    print("✅ All clock hands reset to 0° rotation.")

# ==========================================
# CLOCK UPDATE FUNCTION
# ==========================================
def update_clock():
    """Updates clock hands according to current system time."""
    try:
        now = datetime.datetime.now()
        hour = now.hour % 12
        minute = now.minute
        second = now.second + now.microsecond / 1e6

        # Clockwise rotation (negative for Maya Y-axis)
        second_angle = -6 * second
        minute_angle = -6 * (minute + second / 60.0)
        hour_angle   = -30 * (hour + minute / 60.0)

        if cmds.objExists(SECOND):
            cmds.setAttr(f'{SECOND}.{AXIS}', second_angle)
        if cmds.objExists(MINUTE):
            cmds.setAttr(f'{MINUTE}.{AXIS}', minute_angle)
        if cmds.objExists(HOUR):
            cmds.setAttr(f'{HOUR}.{AXIS}', hour_angle)

    except Exception as e:
        print(f"[Clock Error] {e}")

# ==========================================
# THREAD CONTROL
# ==========================================
def start_real_time_clock():
    """Start the real-time clock."""
    global clock_thread_running
    try:
        stop_real_time_clock()
    except:
        pass

    reset_clock_hands()  # ensure clean start
    clock_thread_running = True

    def run_clock():
        while clock_thread_running:
            cmds.evalDeferred(update_clock)
            time.sleep(UPDATE_INTERVAL)

    threading.Thread(target=run_clock, daemon=True).start()
    print("🕒 Real-time clock started (updates every second).")

def stop_real_time_clock():
    """Stop the real-time clock."""
    global clock_thread_running
    clock_thread_running = False
    print("⏹️ Real-time clock stopped.")

# ==========================================
# START
# ==========================================
start_real_time_clock()
update_clock()

# To stop the clock, call
stop_real_time_clock()
#to start it again, call
start_real_time_clock()
# To reset the clock hands to 0°, call
reset_clock_hands()
