"""Desktop notifications via pystray (balloon tips from system tray)."""
from typing import Optional

from pomtimer import Phase
from lang import _


def notify_phase_change(
    icon: object,
    phase: Phase,
    lang: str = "en",
    session_count: int = 0,
) -> None:
    """Send a tray balloon notification for a phase transition."""
    title, msg = "", ""
    if phase == Phase.WORK:
        title = _("notify_work_title", lang)
        msg = _("notify_work_msg", lang)
    elif phase == Phase.SHORT_BREAK:
        title = _("notify_short_break_title", lang)
        msg = _("notify_short_break_msg", lang)
    elif phase == Phase.LONG_BREAK:
        title = _("notify_long_break_title", lang)
        msg = _("notify_long_break_msg", lang)
    else:
        return

    try:
        icon.notify(msg, title)
    except Exception:
        pass
