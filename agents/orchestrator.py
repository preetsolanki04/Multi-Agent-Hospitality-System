"""
Orchestrator Agent
------------------
Master controller. Manages:
  1. State management across the pipeline
  2. Hand-off protocol: Researcher → Writer
  3. Final output assembly
"""

import json
from agents.researcher import ResearcherAgent
from agents.writer      import WriterAgent


class HospitalityOrchestrator:
    """
    Workflow:
      [User Input]
           │
           ▼
      ResearcherAgent  ──(structured JSON)──►  WriterAgent
           │                                        │
           └──────────── Orchestrator ──────────────┘
                              │
                         Final Output
    """

    def __init__(self, api_key: str):
        self.api_key    = api_key
        self.researcher = ResearcherAgent(api_key)
        self.writer     = WriterAgent(api_key)
        self.state      = {}          # Shared pipeline state

    # ── Hand-off Protocol ─────────────────────────────────────────────────────
    def _handoff_to_researcher(self, **kwargs) -> dict:
        """Phase 1: Activate Researcher Agent and capture its output."""
        self.state["phase"] = "researching"
        self.state["input"] = kwargs

        research = self.researcher.research(**kwargs)

        self.state["research"] = research
        self.state["phase"]    = "research_complete"
        return research

    def _handoff_to_writer(self, research: dict, **kwargs) -> str:
        """Phase 2: Hand research to Writer Agent."""
        self.state["phase"] = "writing"

        # Serialize research neatly for the writer prompt
        research_str = json.dumps(research, indent=2) if isinstance(research, dict) else str(research)

        itinerary = self.writer.write(
            research_data=research_str,
            **kwargs,
        )

        self.state["itinerary"] = itinerary
        self.state["phase"]     = "complete"
        return itinerary

    # ── Main Entry ────────────────────────────────────────────────────────────
    def run(
        self,
        destination: str,
        origin: str,
        duration: int,
        travelers: int,
        hotel_tier: str,
        transport_modes: list,
        interests: list,
        budget: str,
    ) -> dict:
        """
        Orchestrate the full pipeline and return a unified result dict.
        """
        common = dict(
            destination=destination,
            origin=origin,
            duration=duration,
            travelers=travelers,
            hotel_tier=hotel_tier,
            interests=interests,
            budget=budget,
        )

        # ── Phase 1: Research ─────────────────────────────────────────────────
        research = self._handoff_to_researcher(
            transport_modes=transport_modes,
            **common,
        )

        # ── Phase 2: Write ────────────────────────────────────────────────────
        itinerary = self._handoff_to_writer(
            research=research,
            **common,
        )

        # ── Phase 3: Assemble Final Output ────────────────────────────────────
        final = {
            "destination" : destination,
            "origin"      : origin,
            "duration"    : duration,
            "travelers"   : travelers,
            "hotel_tier"  : hotel_tier,
            "budget"      : budget,
            "itinerary"   : itinerary,
            "hotels"      : research.get("hotels", [])      if isinstance(research, dict) else [],
            "transport"   : research.get("transport", {})   if isinstance(research, dict) else {},
            "attractions" : research.get("attractions", []) if isinstance(research, dict) else [],
            "restaurants" : research.get("restaurants", []) if isinstance(research, dict) else [],
            "local_tips"  : research.get("local_tips", [])  if isinstance(research, dict) else [],
            "weather"     : research.get("weather_overview", "") if isinstance(research, dict) else "",
            "raw_research": research,
        }

        self.state["final"] = final
        return final
