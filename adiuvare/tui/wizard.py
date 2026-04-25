from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from ..config.editor import merge_sections


class SetupWizardApp(App[None]):
    def __init__(self, dest: str | Path) -> None:
        super().__init__()
        self._dest = Path(dest)

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("Adiuvare setup")
            yield Input(value="fastapi", id="wiz-framework", placeholder="framework")
            yield Input(value="single", id="wiz-instances", placeholder="single or multi")
            yield Input(value="internal", id="wiz-strict", placeholder="public/internal/critical")
            yield Input(value="observe", id="wiz-mode", placeholder="observe or enforce")
            yield Input(value="off", id="wiz-ai", placeholder="off/assist/critical")
            yield Button("Write config", id="wiz-save")
            yield Static("", id="wiz-status")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "wiz-save":
            return

        framework = self.query_one("#wiz-framework", Input).value.strip().lower() or "fastapi"
        instances = self.query_one("#wiz-instances", Input).value.strip().lower() or "single"
        strict = self.query_one("#wiz-strict", Input).value.strip().lower() or "internal"
        mode = self.query_one("#wiz-mode", Input).value.strip().lower() or "observe"
        ai_mode = self.query_one("#wiz-ai", Input).value.strip().lower() or "off"
        payload = {
            "runtime": {"observe_only": mode == "observe"},
            "ai": {"mode": ai_mode, "enabled": ai_mode != "off"},
            "meta": {
                "framework": framework,
                "instances": instances,
                "strictness": strict,
            },
        }
        merge_sections(self._dest, payload)
        self.query_one("#wiz-status", Static).update(f"wrote {self._dest}")
        self.exit()


def run_wizard(dest: str | Path) -> None:
    SetupWizardApp(dest).run()

