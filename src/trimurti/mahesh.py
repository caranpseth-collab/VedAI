import os
from typing import Dict, Any
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

class EvaluationResult(BaseModel):
    is_valid: bool = Field(description="True if the reasoning is sound and passes logical checks; False if fallacies are found")
    nyaya_critique: str = Field(description="Detailed critique applying logical analysis to dismantle errors or validate truths")
    detected_fallacies: list[str] = Field(description="List of specific flaws, assumptions, or inaccuracies found in the input")
    remediation_instructions: str = Field(description="Clear, actionable instructions telling the worker agent exactly how to rewrite and fix their code/theory")

class MaheshAgent:
    """
    The Critic and Destroyer of Illusion (Hallucination) in the Trimurti layer.
    Enforces rigorous logical verification rules based on Nyaya Shastra.
    """
    def __init__(self, model_name: str = "gpt-4o"):
        # Utilizing a Tier-1 Frontier model to ensure maximum evaluation accuracy
        self.llm = ChatOpenAI(model=model_name, temperature=0.1)  # Low temperature for strict adherence to rules
        self.parser = PydanticOutputParser(pydantic_object=EvaluationResult)
        
    def evaluate_output(self, task_brief: str, proposed_solution: str) -> EvaluationResult:
        mahesh_prompt = ChatPromptTemplate.from_template(
            "You are the MAHESH AGENT, the supreme judge and ultimate critic of the VedAI system.\n"
            "Your function is to apply absolute, rigorous logical vetting onto proposed answers using a structural framework.\n"
            "You must expose assumptions, factual inaccuracies, and any structural flaws.\n\n"
            "Original Assignment Brief:\n{brief}\n\n"
            "Proposed Agent Solution:\n{solution}\n\n"
            "Analyze the solution strictly. If it is flawed, mark is_valid as False and provide precise remediation steps.\n"
            "{format_instructions}"
        )
        
        formatted_prompt = mahesh_prompt.format_messages(
            brief=task_brief,
            solution=proposed_solution,
            format_instructions=self.parser.get_format_instructions()
        )
        
        response = self.llm.invoke(formatted_prompt)
        return self.parser.parse(response.content)

if __name__ == "__main__":
    print("Mahesh Logic & Evaluation Agent initialized successfully.")
