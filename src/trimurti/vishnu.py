import os
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class UnifiedContext(BaseModel):
    integrated_synthesis: str = Field(description="The seamlessly woven explanation merging philosophy, science, and practical steps")
    cross_references: List[str] = Field(description="List of exact textual references harmonized across different Vedic categories")
    system_stability_status: str = Field(description="Operational note on whether conflicting philosophies were balanced safely")

class VishnuAgent:
    """
    The System Preserver and Context Weaver of the Trimurti layer.
    Coordinates memory states, manages context pipelines, and interfaces with the Nalanda Database.
    """
    def __init__(self, model_name: str = "gpt-4o"):
        # Utilizing a Tier-1 Frontier model to ensure comprehensive contextual stitching
        self.llm = ChatOpenAI(model=model_name, temperature=0.2)
        
    def weave_rishi_knowledge(self, original_task: str, rishi_outputs: List[Dict[str, Any]]) -> str:
        vishnu_prompt = ChatPromptTemplate.from_template(
            "You are the VISHNU AGENT, the supreme preserver and context weaver of the VedAI system.\n"
            "Your function is to maintain operational harmony across the entire multi-agent network.\n"
            "You receive raw, isolated theoretical and practical contributions from individual Rishi Agents "
            "and must seamlessly synthesize them into a unified, non-conflicting masterpiece.\n\n"
            "Original Objective:\n{task}\n\n"
            "Collected Rishi Intelligence inputs:\n{inputs}\n\n"
            "Weave these inputs together into a balanced, clear solution. Ensure no text overlaps or contradicts."
        )
        
        # Formatting inputs into an easily readable layout for the LLM
        formatted_inputs = "\n---\n".join([str(output) for output in rishi_outputs])
        
        formatted_prompt = vishnu_prompt.format_messages(
            task=original_task,
            inputs=formatted_inputs
        )
        
        response = self.llm.invoke(formatted_prompt)
        return response.content

if __name__ == "__main__":
    print("Vishnu Context & Preservation Agent initialized successfully.")
