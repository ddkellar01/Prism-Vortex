import re
import html


class SecuritySanitizer:
    """Sanitizes ingested context streams to prevent indirect prompt injection and payload execution."""

    def __init__(self):
        # Patterns flagging common indirect injection techniques
        self.injection_patterns = [
            re.compile(r"ignore\s+previous\s+instructions", re.IGNORECASE),
            re.compile(r"system_prompt\s*:", re.IGNORECASE),
            re.compile(r"<\s*script[^>]*>", re.IGNORECASE),
            re.compile(r"exec\s*\(\s*eval", re.IGNORECASE),
        ]

    def sanitize_text(self, raw_input: str) -> str:
        """Sanitizes raw text strings by escaping tags and neutralizing potential injections."""
        if not raw_input:
            return ""

        clean_text = html.escape(raw_input)
        for pattern in self.injection_patterns:
            clean_text = pattern.sub("[FILTERED_INJECTION_VECTOR]", clean_text)

        return clean_text.strip()

    def sanitize_dict(self, payload: dict) -> dict:
        """Recursively sanitizes dictionary elements."""
        sanitized = {}
        for key, val in payload.items():
            clean_key = self.sanitize_text(str(key))
            if isinstance(val, str):
                sanitized[clean_key] = self.sanitize_text(val)
            elif isinstance(val, dict):
                sanitized[clean_key] = self.sanitize_dict(val)
            elif isinstance(val, list):
                sanitized[clean_key] = [
                    self.sanitize_text(item) if isinstance(item, str) else item
                    for item in val
                ]
            else:
                sanitized[clean_key] = val
        return sanitized
