import os
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

class TaskDecomposition(BaseModel):
    cognitive_framework: str = Field(description="The underlying philosophical or scientific Vedic school needed (e.g., Vaisheshika, Nyaya, Ayurveda)")
    abstract_theory: str = Field(description="The conceptual or abstract principle pulled from the source text to solve the issue")
    practical_application: str = Field(description="How to translate this theory into modern practical engineering, code, or design instructions")
    assigned_rishi_agents: List[str] = Field(description="The specific scriptural specialist agents to route this brief to")

class BrahmaAgent:
    """
    The Proposer Layer of the Trimurti framework.
    Parses, deconstructs, and routes strategic briefs down to the Rishi Agent network.
    """
    def __init__(self, model_name: str = "gpt-4o"):
        # Utilizing a Tier-1 Frontier model for complex macro reasoning and task routing
        self.llm = ChatOpenAI(model=model_name, temperature=0.3)
        self.parser = PydanticOutputParser(pydantic_object=TaskDecomposition)
        
    def generate_rishi_briefs(self, master_task: str) -> TaskDecomposition:
        brahma_prompt = ChatPromptTemplate.from_template(
            "You are the BRAHMA AGENT, the sovereign creator and supreme architect of the VedAI system.\n"
            "Your function is to receive an overarching human task, analyze it through the vast scope of the "
            "Nalanda Library taxonomy, and decompose it into deep structural briefs for the specialized Rishi Agents.\n\n"
            "Master Task:\n{task}\n\n"
            "Deconstruct this query perfectly. {format_instructions}"
        )
        
        # Formatting structural output definitions for the agent
        formatted_prompt = brahma_prompt.format_messages(
            task=master_task,
            format_instructions=self.parser.get_format_instructions()
        )
        
        response = self.llm.invoke(formatted_prompt)
        return self.parser.parse(response.content)

if __name__ == "__main__":
    # Test stub for initialization checks
    print("Brahma Agent Core initialized successfully.")
