import logging
from google import genai
from google.genai import types
from config.settings import settings
from agents.prompt_templates import ARGON_SCOUT_SYSTEM_INSTRUCTION, build_scout_prompt
from agents.tool_registry import REGISTERED_TOOLS

logger = logging.getLogger("prism-vortex")


class ArgonAgentOrchestrator:
    """Orchestrates Gemini 4 Argon deep thinking agents for high-horizon reasoning."""

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_id = settings.ARGON_MODEL_ID

    def execute_deep_scout(
        self,
        objective: str,
        context_payload: str,
        local_risk_score: float
    ) -> str:
        """Executes a high-level thinking session with Gemini 4 Argon."""
        prompt = build_scout_prompt(
            objective=objective,
            context_payload=context_payload,
            local_risk_score=local_risk_score
        )

        try:
            logger.info("Dispatching scouting mission to Gemini 4 Argon engine...")
            
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=ARGON_SCOUT_SYSTEM_INSTRUCTION,
                    thinking_config=types.ThinkingConfig(
                        thinking_level="high"
                    ),
                    temperature=0.2,
                    max_output_tokens=65536,
                    tools=[types.Tool(function_declarations=REGISTERED_TOOLS)]
                )
            )
            return response.text
        except Exception as err:
            logger.error(f"Error executing Argon reasoning loop: {str(err)}")
            return f"[ERROR]: Failed to complete deep reasoning session: {str(err)}"
