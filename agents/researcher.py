"""
Researcher Agent
----------------
Responsible for gathering ALL raw travel data:
  - Hotels (premium / luxury / ultra-luxury)
  - Flights, Trains, Buses
  - Local attractions, food, tips
"""

import json
from mistralai.client import Mistral


RESEARCHER_SYSTEM = """You are an expert travel researcher with deep knowledge of global hospitality,
aviation, rail networks, and tourism. Your job is to gather comprehensive, realistic, and detailed
information for a travel request.

Always respond with VALID JSON only — no markdown fences, no preamble.

Your JSON must follow this schema exactly:
{
  "hotels": [
    {
      "name": "string",
      "tier": "Premium|Luxury|Ultra-Luxury",
      "location": "string (area/neighbourhood)",
      "price_per_night": "string (e.g. $350/night)",
      "rating": "string (e.g. 4.8/5)",
      "amenities": ["list", "of", "amenities"],
      "description": "2–3 sentence description",
      "booking_tip": "string"
    }
  ],
  "transport": {
    "flights": [
      {
        "airline": "string",
        "route": "string (Origin → Destination)",
        "duration": "string",
        "price": "string (per person)",
        "class": "Economy|Business|First",
        "tip": "string"
      }
    ],
    "trains": [
      {
        "operator": "string",
        "route": "string",
        "duration": "string",
        "price": "string",
        "class": "string",
        "tip": "string"
      }
    ],
    "buses": [
      {
        "operator": "string",
        "route": "string",
        "duration": "string",
        "price": "string",
        "tip": "string"
      }
    ]
  },
  "attractions": [
    {
      "name": "string",
      "category": "string",
      "entry_fee": "string",
      "best_time": "string",
      "description": "string"
    }
  ],
  "restaurants": [
    {
      "name": "string",
      "cuisine": "string",
      "price_range": "string",
      "must_try": "string",
      "reservation_needed": true
    }
  ],
  "local_tips": ["tip1", "tip2", "tip3"],
  "weather_overview": "string",
  "currency_and_costs": "string"
}

Provide at least 3 hotels, 2 flights, 2 trains or buses (if applicable), 5 attractions, 4 restaurants.
Make data realistic, specific, and high-quality."""


class ResearcherAgent:
    def __init__(self, api_key: str):
        self.client = Mistral(api_key=api_key, timeout_ms=60000)  # 60 second timeout
        self.model  = "mistral-large-latest"

    def research(
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
        prompt = f"""
Research a {duration}-day trip for {travelers} traveler(s):
- Destination : {destination}
- Origin      : {origin}
- Hotel tier  : {hotel_tier}
- Transport   : {', '.join(transport_modes) if transport_modes else 'flights, trains'}
- Interests   : {', '.join(interests) if interests else 'general tourism'}
- Budget      : {budget} per person

Provide hotels matching the "{hotel_tier}" tier or above.
Include transport options matching: {', '.join(transport_modes)}.
Focus attractions/restaurants on interests: {', '.join(interests)}.
"""
        response = self.client.chat.complete(
            model=self.model,
            messages=[
                {"role": "system", "content": RESEARCHER_SYSTEM},
                {"role": "user",   "content": prompt},
            ],
            temperature=0.4,
            max_tokens=3000,
        )

        raw = response.choices[0].message.content.strip()

        # Strip accidental markdown fences
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Fallback: return raw as string inside dict
            return {"raw_research": raw, "parse_error": True}
