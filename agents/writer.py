"""
Writer Agent
------------
Receives structured research data and synthesises it into a
beautiful, day-by-day travel itinerary in Markdown.
"""

from mistralai.client import Mistral


WRITER_SYSTEM = """You are an award-winning luxury travel writer and itinerary planner.
Your task: transform raw travel research data into a polished, engaging, day-by-day
itinerary written in Markdown.

Guidelines:
- Use rich Markdown: ## headers for days, ### for sections, **bold** for highlights,
  bullet lists for activities, > blockquotes for insider tips.
- Each day should have: Morning, Afternoon, Evening sections.
- Weave in hotel recommendations naturally.
- Mention specific restaurant names, dishes, attraction entry fees/times from the research.
- Include practical transport info (departure times, booking tips).
- Add a "Getting There" section at the top.
- Add a "Packing Tips & Practical Info" section at the end.
- Tone: warm, sophisticated, inspiring — like a personal concierge.
- Do NOT add fictional data; use only what is in the research payload.
- Start with a compelling introduction paragraph about the destination.
"""


class WriterAgent:
    def __init__(self, api_key: str):
        self.client = Mistral(api_key=api_key, timeout_ms=60000)  # 60 second timeout
        self.model  = "mistral-large-latest"

    def write(
        self,
        research_data: str,
        destination: str,
        origin: str,
        duration: int,
        travelers: int,
        hotel_tier: str,
        interests: list,
        budget: str,
    ) -> str:
        prompt = f"""
Using the research data below, write a {duration}-day luxury travel itinerary for
{travelers} traveler(s) visiting {destination} from {origin}.
Hotel tier: {hotel_tier} | Interests: {', '.join(interests)} | Budget: {budget}

=== RESEARCH DATA ===
{research_data}
=== END RESEARCH ===

Produce a complete, beautifully written Markdown itinerary now.
"""
        response = self.client.chat.complete(
            model=self.model,
            messages=[
                {"role": "system", "content": WRITER_SYSTEM},
                {"role": "user",   "content": prompt},
            ],
            temperature=0.7,
            max_tokens=4000,
        )

        return response.choices[0].message.content.strip()
