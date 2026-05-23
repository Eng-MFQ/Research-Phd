from typing import List
from pydantic import BaseModel, Field


# 1. Class for the 'resources' objects (the source citation)
class Resource(BaseModel):
    """
    Represents a single source citation from the Islamic knowledge base.
    """
    page_number: str = Field(..., description="The page number where the information was found.")
    book_name: str = Field(..., description="The full title of the book and the part (if applicable).")
    book_part_number: int = Field(..., description="The numeric part number of the book.")


# 2. Class for the main JSON structure (the final output)
class ScholarResponse(BaseModel):
    """
    Represents the complete structured output from the Islamic scholar system.
    """
    answer: str = Field(..., description="The main answer content formatted in Markdown.")
    relevant_questions: List[str] = Field(...,
                                          description="A list of three follow-up questions relevant to the answer.")
    resources: List[Resource] = Field(..., description="A list of resource citations used to construct the answer.")


import json
import re
from typing import Any, Iterable

_CODE_FENCE_RE = re.compile(
    r"```(?:\s*json)?\s*(.*?)\s*```",
    re.IGNORECASE | re.DOTALL,
)

def _json_candidates(text: str) -> Iterable[str]:
    """
    Yield likely JSON snippets from `text`.
    1) Prefer fenced code blocks (```json ... ``` or ``` ... ```).
    2) Fall back to scanning for the first balanced {...} block.
    """
    # 1) Any fenced blocks first (prefer ones labeled json, but accept unlabeled too)
    for m in _CODE_FENCE_RE.finditer(text):
        yield m.group(1)

    # 2) Balanced-brace scan for a top-level JSON object
    in_string = False
    escape = False
    depth = 0
    start = -1

    for i, ch in enumerate(text):
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
        elif ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            if depth > 0:
                depth -= 1
                if depth == 0 and start != -1:
                    yield text[start:i+1]
                    # If you only want the *first* object, return after yielding once.
                    # return

def extract_json(text: str) -> Any:
    for snippet in _json_candidates(text):
        return json.loads(snippet)
    return text




