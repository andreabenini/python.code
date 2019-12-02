# Get system uptime
def uptimeGet(self):
    try:
        with open("/proc/uptime", "r") as f:
            secs = f.read().split(" ")[0].strip()
        secs = float(secs)
        MINUTE  = 60
        HOUR    = MINUTE * 60
        DAY     = HOUR * 24
        # Get days, hours, etc:
        days    = int( secs / DAY )
        hours   = int( ( secs % DAY ) / HOUR )
        minutes = int( ( secs % HOUR ) / MINUTE )
        seconds = int( secs % MINUTE )
        return "{}d, {}h, {}m, {}s".format(days, hours, minutes, seconds)
    except Exception:
        return ""
