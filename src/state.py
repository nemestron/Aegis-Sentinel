"""
Global State Schema Definition
Author: Dhiraj Malwade
"""
from pydantic import BaseModel, Field
from typing import List, Optional

class AgentState(BaseModel):
    ticker: str
    raw_data: str = ""
    retrieved_docs: List[str] = Field(default_factory=list)
    source_links: List[str] = Field(default_factory=list)
    verified: bool = False
    final_brief: str = ""
    current_price: Optional[str] = None
    change_percent: Optional[str] = None
    company_name: Optional[str] = None