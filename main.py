from tkinter import *
from tkinter import ttk
from datetime import datetime
import pytz
from plyer import notification

# ---------------- WINDOW ----------------

root = Tk()

root.title("Smart Productivity Clock v3.0")

root.geometry("800x850")

# ---------------- SETTINGS ----------------

dark_mode = True
time_format_24 = True
timer_running = False

root.configure(bg="black")

# ---------------- CONTINENTS ----------------

continents = {
    "🌏 Asia": "Asia",
    "🌍 Europe": "Europe",
    "🌎 North America": "America",
    "🌎 South America": "America",
    "🌍 Africa": "Africa",
    "🌏 Australia/Oceania": "Australia"
}

selected_continent = StringVar()
selected_timezone = StringVar()

selected_continent.set("🌏 Asia")
selected_timezone.set("Asia/Kolkata")

# ---------------- UPDATE TIME ZONES ----------------

def update_timezone_list(event=None):

    prefix = continents[selected_continent.get()]

    zones = []

    for zone in pytz.all_timezones:

        if zone.startswith(prefix):

            zones.append(zone)

    timezone_menu["values"] = zones

    if zones:

        selected_timezone.set(zones[0])

# ---------------- DARK MODE ----------------

def toggle_theme():

    global dark_mode

    dark_mode = not dark_mode

    if dark_mode:

        bg = "black"
        fg = "white"
        entry_bg = "#1f1f1f"
        entry_fg = "white"

    else:

        bg = "white"
        fg = "black"
        entry_bg = "white"
        entry_fg = "black"

    root.configure(bg=bg)

    widgets = [
        clock_label,
        day_label,
        date_label,
        task_label,
        timer_label,
        continent_label,
        timezone_label
    ]

    for widget in widgets:

        widget.config(bg=bg, fg=fg)

    task_entry.config(
        bg=entry_bg,
        fg=entry_fg,
        insertbackground=entry_fg
    )

# ---------------- 12H / 24H ----------------

def toggle_format():

    global time_format_24

    time_format_24 = not time_format_24

# ---------------- POMODORO ----------------

def start_timer(minutes):

    global timer_running

    timer_running = True

    countdown(minutes * 60)

def countdown(seconds):

    global timer_running

    if not timer_running:

        return

    mins = seconds // 60

    secs = seconds % 60

    timer_label.config(
        text=f"🍅 {mins:02d}:{secs:02d}"
    )

    if seconds > 0:

        root.after(
            1000,
            countdown,
            seconds - 1
        )

    else:

        timer_label.config(
            text="✅ Timer Finished!"
        )

        notification.notify(
            title="Pomodoro Timer",
            message="Your session has ended!",
            timeout=10
        )

        timer_running = False

def reset_timer():

    global timer_running

    timer_running = False

    timer_label.config(
        text="🍅 25:00"
    )

# ---------------- UPDATE CLOCK ----------------

def update_clock():

    try:

        tz = pytz.timezone(
            selected_timezone.get()
        )

    except:

        tz = pytz.timezone(
            "Asia/Kolkata"
        )

    now = datetime.now(tz)

    if time_format_24:

        current_time = now.strftime(
            "%H:%M:%S"
        )

    else:

        current_time = now.strftime(
            "%I:%M:%S %p"
        )

    current_day = now.strftime(
        "%A"
    )

    current_date = now.strftime(
        "%d %B %Y"
    )

    clock_label.config(text=current_time)

    day_label.config(text=current_day)

    date_label.config(text=current_date)

    root.after(
        1000,
        update_clock
    )

# ---------------- CLOCK ----------------

clock_label = Label(
    root,
    font=("Arial", 40, "bold"),
    bg="black",
    fg="white"
)

clock_label.pack(pady=20)

# ---------------- DAY ----------------

day_label = Label(
    root,
    font=("Arial", 20),
    bg="black",
    fg="white"
)

day_label.pack()

# ---------------- DATE ----------------

date_label = Label(
    root,
    font=("Arial", 20),
    bg="black",
    fg="white"
)

date_label.pack()

# ---------------- CONTINENT ----------------

continent_label = Label(
    root,
    text="🌍 Select Continent",
    font=("Arial", 14),
    bg="black",
    fg="white"
)

continent_label.pack(pady=10)

continent_menu = ttk.Combobox(
    root,
    textvariable=selected_continent,
    values=list(continents.keys()),
    state="readonly",
    width=25
)

continent_menu.pack()

continent_menu.bind(
    "<<ComboboxSelected>>",
    update_timezone_list
)

# ---------------- TIME ZONE ----------------

timezone_label = Label(
    root,
    text="🌐 Select Time Zone",
    font=("Arial", 14),
    bg="black",
    fg="white"
)

timezone_label.pack(pady=10)

timezone_menu = ttk.Combobox(
    root,
    textvariable=selected_timezone,
    state="readonly",
    width=35
)

timezone_menu.pack()

update_timezone_list()

# ---------------- BUTTONS ----------------

Button(
    root,
    text="🌙 Dark Mode",
    command=toggle_theme
).pack(pady=5)

Button(
    root,
    text="⏰ 12h / 24h",
    command=toggle_format
).pack(pady=5)

# ---------------- CURRENT TASK ----------------

task_label = Label(
    root,
    text="📝 Current Task",
    font=("Arial", 14),
    bg="black",
    fg="white"
)

task_label.pack(pady=10)

task_entry = Entry(
    root,
    width=35,
    font=("Arial", 14),
    bg="#1f1f1f",
    fg="white",
    insertbackground="white"
)

task_entry.pack()

# ---------------- TIMER ----------------

timer_label = Label(
    root,
    text="🍅 25:00",
    font=("Arial", 24, "bold"),
    bg="black",
    fg="white"
)

timer_label.pack(pady=20)

Button(
    root,
    text="▶️ Start 25 Min",
    command=lambda: start_timer(25)
).pack(pady=5)

Button(
    root,
    text="☕ Start 5 Min Break",
    command=lambda: start_timer(5)
).pack(pady=5)

Button(
    root,
    text="⏹️ Reset",
    command=reset_timer
).pack(pady=5)

# ---------------- START ----------------

update_clock()

root.mainloop()