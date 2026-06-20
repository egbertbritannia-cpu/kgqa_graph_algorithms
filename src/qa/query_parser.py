"""Rule-based query parsing for the KGQA demo.

The research scope intentionally avoids heavy NLP models. This parser keeps the
input step transparent by matching a small set of predictable English question
patterns and converting concept names into CSO-style node IDs.
"""

import re


class RuleBasedQueryParser:
    """Extract source and target concepts from simple English questions."""

    def __init__(self):
        # Each pattern must provide named groups: source and target.
        self.patterns = [
            re.compile(r"how is (?P<source>.+?) related to (?P<target>.+)\??$", re.IGNORECASE),
            re.compile(
                r"what is the connection between (?P<source>.+?) and (?P<target>.+)\??$",
                re.IGNORECASE,
            ),
            re.compile(r"find path from (?P<source>.+?) to (?P<target>.+)\??$", re.IGNORECASE),
            re.compile(r"show relation from (?P<source>.+?) to (?P<target>.+)\??$", re.IGNORECASE),
            re.compile(r"relation:\s*(?P<source>.+?)\s*->\s*(?P<target>.+)$", re.IGNORECASE),
        ]

    def parse(self, question: str) -> dict:
        """Return a dictionary with normalized source and target node IDs."""
        question = question.strip()

        for pattern in self.patterns:
            match = pattern.search(question)
            if match:
                return {
                    "source": self._normalize_concept(match.group("source")),
                    "target": self._normalize_concept(match.group("target")),
                    "intent": "relationship",
                }

        raise ValueError(
            "Could not parse the question. Try: 'How is Data Mining related to Random Forests?'"
        )

    def _normalize_concept(self, concept: str) -> str:
        """Convert a display concept into the node ID format used in the graph."""
        concept = concept.strip().lower()
        concept = re.sub(r"[^a-z0-9\s_-]", "", concept)
        concept = re.sub(r"\s+", "_", concept)
        return concept
