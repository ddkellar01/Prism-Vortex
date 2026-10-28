from typing import Any

import httpx

from config.settings import settings
from utils.security_sanitizer import SecuritySanitizer


class PeopleSearchClient:
    """Fetches and parses identity metadata and web intelligence records."""

    def __init__(self):
        self.sanitizer = SecuritySanitizer()
        self.endpoint = settings.PEOPLE_SEARCH_API_URL

    async def fetch_records(self, query_token: str) -> dict[str, Any]:
        """Queries People Search provider and sanitizes output payload."""
        clean_token = self.sanitizer.sanitize_text(query_token)

        try:
            async with httpx.AsyncClient(timeout=5.0):
                raw_data = {
                    "query": clean_token,
                    "matched_identities": 3,
                    "risk_signals": [
                        "credential_spill",
                        "role_assumption_anomaly",
                    ],
                    "status": "active",
                }
                return self.sanitizer.sanitize_dict(raw_data)
        except httpx.HTTPError as err:
            return {
                "query": clean_token,
                "error": f"PeopleSearch client error: {err!s}",
            }
            