class SettingsModel:
    """Handles persistent settings (e.g., theme mode)."""
    _theme_mode = "dark"  # Default

    @classmethod
    def get_theme_mode(cls) -> str:
        return cls._theme_mode

    @classmethod
    def set_theme_mode(cls, mode: str):
        if mode in ("dark", "light"):
            cls._theme_mode = mode