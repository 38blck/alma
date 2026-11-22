import os
from collections.abc import Callable

import libqtile.resources
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Output, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()

keys = [
	# A list of available commands that can be bound to keys can be found
	# at https://docs.qtile.org/en/latest/manual/config/lazy.html
	# Switch between windows
	Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
	Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
	Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
	Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
	Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
	# Move windows between left/right columns or move up/down in current stack.
	# Moving out of range in Columns layout will create new column.
	Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
	Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
	Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
	Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
	# Grow windows. If current window is on the edge of screen and direction
	# will be to screen edge - window would shrink.
	Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
	Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
	Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
	Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
	Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
	# Toggle between split and unsplit sides of stack.
	# Split = all windows displayed
	# Unsplit = 1 window displayed, like Max layout, but still with
	# multiple stack panes
	Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
	Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
	Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
	Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
	Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
	Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
	Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
	Key([mod], "r", lazy.spawn("dmenu_run -fn 'Hack Nerd Font Propo-10'")),
    # Sound
	Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
	Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q sset Master 2%- unmute")),
	Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q sset Master 2%+ unmute")),
    # Screenshots
    Key([], "Print", lazy.spawn("sh -c 'grim ~/Pictures/Screenshots/ss-$(date +%y%m%d%H%M%S).png'")),
    Key(["Shift"], "Print", lazy.spawn("sh -c 'grim -g \"$(slurp)\" ~/Pictures/Screenshots/ss-$(date +%y%m%d%H%M%S).png'")),
    Key(["control"], "Print", lazy.spawn("sh -c 'grim - | wl-copy -t image/png'")),
    Key(["control", "Shift"], "Print", lazy.spawn("sh -c 'grim -g \"$(slurp)\" - | wl-copy -t image/png'")),
    # Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl -q set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl -q set 10%-"))
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
	keys.append(
		Key(
			["control", "mod1"],
			f"f{vt}",
			lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
			desc=f"Switch to VT{vt}",
		)
	)


groups = [Group(i) for i in "123456789"]

for i in groups:
	keys.extend(
		[
			# mod + group number = switch to group
			Key(
				[mod],
				i.name,
				lazy.group[i.name].toscreen(),
				desc=f"Switch to group {i.name}",
			),
			# mod + shift + group number = switch to & move focused window to group
			Key(
				[mod, "shift"],
				i.name,
				lazy.window.togroup(i.name, switch_group=True),
				desc=f"Switch to & move focused window to group {i.name}",
			),
			# Or, use below if you prefer not to switch to that group.
			# # mod + shift + group number = move focused window to group
			# Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
			#		desc="move focused window to group {}".format(i.name)),
		]
	)

layouts = [layout.Columns(border_width=4, margin=8)]

widget_defaults = dict(
	font="Hack Nerd Font Propo",
	fontsize=12
)
extension_defaults = widget_defaults.copy()

screens = [
	Screen(
		bottom=bar.Bar(
			[
				widget.GroupBox(hide_unused=True, highlight_method="line"),
				widget.WindowName(background="202020", foreground="ffffff"),
				#widget.Systray(),
                widget.KeyboardLayout(background="ffffff", configured_keyboards=['us altgr-intl'], foreground="202020"),
                widget.Backlight(),
                widget.Volume(background="ffffff", foreground="202020"),
                widget.Battery(update_interval=2),
				widget.Clock(background="c6e366", foreground="202020", format="%a %b/%d/%y %H:%M")
			],
			24,
		),
		background="#000000",
		wallpaper="~/Pictures/Wallpapers/edu-lins-pIe9a3CWB4A-unsplash.jpg",
		wallpaper_mode="fill"
	)
]

# Instead of screens, you can define a function here to specify which Screen
# should correspond to which Output.
fake_screens: list[Screen] | None = None

# Instead of screens or fake screens, you can define a function here that
# returns a list of Screen objects based on the list of Outputs; that way you
# can decide based on e.g. the number of screens, or which ports are plugged
# in exactly what do render in each bar for each screen.
generate_screens: Callable[[list[Output]], list[Screen]] | None = None

# Drag floating layouts.
mouse = [
	Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
	Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
	Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []	# type: list
follow_mouse_focus = False
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
	float_rules=[
		# Run the utility of `xprop` to see the wm class and name of an X client.
		*layout.Floating.default_float_rules,
		Match(wm_class="confirmreset"), # gitk
		Match(wm_class="makebranch"),  # gitk
		Match(wm_class="maketag"),	# gitk
		Match(wm_class="ssh-askpass"),	# ssh-askpass
		Match(title="branchdialog"),	# gitk
		Match(title="pinentry"),	# GPG key password entry
	]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True

# How long (in seconds) to wait after a screen change event before firing the
# screen_change hook, coalescing bursts of events into a single one.
screen_change_debounce_timeout = 1

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

idle_timers = []	# type: list
idle_inhibitors = []	# type: list

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
