from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Vertical, Horizontal, Container
from textual.screen import Screen
import pyperclip
import os
import platform
import psutil
import asyncio
import random

class LoadingScreen(Screen):
    """A hacker-style loading screen."""
    
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("", id="loading-text"),
            Static("", id="loading-hex"),
            id="loading-container"
        )

    def on_mount(self) -> None:
        self.active = True
        self.loading_messages = [
            "SCANNING KERNEL LOGS...",
            "DECRYPTING STACK TRACE...",
            "ISOLATING MALFUNCTION...",
            "BYPASSING PERMISSION GUARDS...",
            "ANALYZING BINARY SIGNATURES...",
            "COLLECTING TELEMETRY..."
        ]
        self.update_animation()
        # Automatically dismiss after 0.8 seconds for snappier feel
        self.set_timer(0.8, self.finish)

    def finish(self) -> None:
        self.active = False
        self.app.pop_screen()

    def update_animation(self) -> None:
        if not getattr(self, "active", False):
            return
            
        try:
            text_widget = self.query_one("#loading-text", Static)
            hex_widget = self.query_one("#loading-hex", Static)
            
            msg = random.choice(self.loading_messages)
            hex_chars = "0123456789ABCDEF"
            hex_dump = " ".join("".join(random.choice(hex_chars) for _ in range(4)) for _ in range(8))
            
            text_widget.update(f"[bold]{msg}[/bold]")
            hex_widget.update(f"[dim]{hex_dump}[/dim]")
            
            self.set_timer(0.15, self.update_animation)
        except Exception:
            self.active = False

class OopsTUI(App):
    """A Retro, Nerdy TUI for explaining Linux errors."""
    
    BINDINGS = [
        ("c", "copy_fix", "Copy Fix"),
        ("t", "toggle_theme", "Switch Theme"),
        ("q", "quit", "Quit"),
    ]
    
    # Define themes as classes on the App
    CSS = """
    /* Global layout */
    Vertical {
        padding: 0 2;
        height: auto;
    }
    .section {
        margin: 1 0;
        padding: 0 1;
        height: auto;
    }
    .header-label {
        width: 100%;
        padding: 0 1;
        text-style: bold;
    }
    .content {
        margin: 1 1;
    }
    .fix-command {
        padding: 0 2;
        text-style: bold;
        margin: 1 1;
    }
    .status-bar {
        height: 1;
        padding: 0 1;
        text-style: dim;
    }
    .copy-hint {
        text-style: italic dim;
        margin: 0 1;
    }
    #loading-container {
        align: center middle;
    }

    /* MATRIX THEME (Default) */
    Screen { background: #000000; }
    .section { border: solid #00ff41; background: #001a0033; }
    .header-label { color: #00ff41; background: #001a00; }
    .content { color: #00ff41; }
    .fix-command { color: #00ff41; background: #000000; border: double #00ff41; }
    .status-bar { color: #00ff41; background: #001a00; }
    .copy-hint { color: #00ff41; }
    #loading-container { color: #00ff41; }

    /* AMBER THEME */
    .theme-amber Screen { background: #1a1000; }
    .theme-amber .section { border: solid #ffb000; background: #33220033; }
    .theme-amber .header-label { color: #ffb000; background: #1a0f00; }
    .theme-amber .content { color: #ffcc00; }
    .theme-amber .fix-command { color: #ffb000; background: #1a1000; border: double #ffb000; }
    .theme-amber .status-bar { color: #ffb000; background: #1a0f00; }
    .theme-amber .copy-hint { color: #ffb000; }
    .theme-amber #loading-container { color: #ffb000; }

    /* CLASSIC THEME */
    .theme-classic Screen { background: #000080; }
    .theme-classic .section { border: solid #ffffff; background: #0000aa33; }
    .theme-classic .header-label { color: #ffffff; background: #000044; }
    .theme-classic .content { color: #ffffff; }
    .theme-classic .fix-command { color: #ffffff; background: #000080; border: double #ffffff; }
    .theme-classic .status-bar { color: #ffffff; background: #000044; }
    .theme-classic .copy-hint { color: #ffffff; }
    .theme-classic #loading-container { color: #ffffff; }

    /* CYBERPUNK THEME */
    .theme-cyberpunk Screen { background: #2b213a; }
    .theme-cyberpunk .section { border: solid #00ffff; background: #1a1a2e33; }
    .theme-cyberpunk .header-label { color: #ff00ff; background: #120d1a; }
    .theme-cyberpunk .content { color: #f8f8f2; }
    .theme-cyberpunk .fix-command { color: #00ffff; background: #2b213a; border: double #00ffff; }
    .theme-cyberpunk .status-bar { color: #ff00ff; background: #120d1a; }
    .theme-cyberpunk .copy-hint { color: #00ffff; }
    .theme-cyberpunk #loading-container { color: #00ffff; }
    """

    ASCII_HEADERS = {
        "WHAT": "[[ WHAT_WENT_WRONG ]]",
        "WHY":  "[[ WHY_IT_HAPPENED ]]",
        "HOW":  "[[ HOW_TO_FIX_IT  ]]",
        "LEARN":"[[ LEARN_MORE      ]]"
    }

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.theme_classes = ["", "theme-amber", "theme-classic", "theme-cyberpunk"]
        self.current_theme_idx = 0
        self.system_info = self._get_sys_info()

    def _get_sys_info(self):
        uname = platform.uname()
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        return f"SYS: {uname.system} {uname.release} | CPU: {cpu}% | RAM: {mem}% | USER: {os.getlogin()}"

    def compose(self) -> ComposeResult:
        yield Static(self.system_info, classes="status-bar", id="status-bar")
        with Vertical():
            with Vertical(classes="section"):
                yield Static(self.ASCII_HEADERS["WHAT"], classes="header-label")
                yield Static(self.data["what"], classes="content")
            
            with Vertical(classes="section"):
                yield Static(self.ASCII_HEADERS["WHY"], classes="why-label header-label")
                yield Static(self.data["why"], classes="content")
            
            with Vertical(classes="section"):
                yield Static(self.ASCII_HEADERS["HOW"], classes="fix-label header-label")
                yield Static(f"$ {self.data['fix']}", classes="content fix-command", id="fix-text")
                yield Static("(Press 'C' to copy | 'T' to switch theme)", classes="copy-hint")
            
            with Vertical(classes="section"):
                yield Static(self.ASCII_HEADERS["LEARN"], classes="learn-label header-label")
                yield Static(self.data["learn"], classes="content")
        yield Footer()

    async def on_mount(self) -> None:
        await self.push_screen(LoadingScreen())

    def action_copy_fix(self) -> None:
        """Copies the fix command to the clipboard."""
        try:
            pyperclip.copy(self.data["fix"])
            self.notify("Buffer updated: Fix copied to clipboard.")
        except Exception:
            self.notify("Error: No system clipboard found.", severity="error")

    def action_toggle_theme(self) -> None:
        """Toggles through available retro themes using CSS classes."""
        # Remove current theme class if it exists
        old_class = self.theme_classes[self.current_theme_idx]
        if old_class:
            self.remove_class(old_class)
        
        # Increment index
        self.current_theme_idx = (self.current_theme_idx + 1) % len(self.theme_classes)
        
        # Add new theme class
        new_class = self.theme_classes[self.current_theme_idx]
        if new_class:
            self.add_class(new_class)
        
        # Instant notification
        theme_display = new_class.replace("theme-", "").upper() if new_class else "MATRIX"
        self.notify(f"Theme: {theme_display}", timeout=0.5)

if __name__ == "__main__":
    demo_data = {
        "what": "Permission denied",
        "why": "Process lacks required credentials.",
        "fix": "sudo !!",
        "learn": "The principle of least privilege ensures security."
    }
    app = OopsTUI(demo_data)
    app.run()
