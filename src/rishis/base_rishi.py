import os
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

class PuzzlePieceBid(BaseModel):
    can_contribute: bool = Field(description="True if this scripture contains data or logic that can solve part of the task")
    confidence_score: float = Field(description="A score from 0.0 to 1.0 indicating mastery depth over this specific problem")
    puzzle_piece_description: str = Field(description="Clear explanation of exactly what element of the question this agent can resolve using its text")
    scriptural_evidence_rationale: str = Field(description="The underlying core logic, verses, or scientific principles from this text applicable to the problem")

class RishiAgentResponse(BaseModel):
    agent_name: str = Field(description="The name of the specialized Rishi agent")
    source_scripture: str = Field(description="The specific Vedic or post-Vedic text managed by this agent")
    theoretical_insight: str = Field(description="The high-level abstract, astronomical, or structural insight extracted")
    practical_data_points: List[str] = Field(description="Exact coordinates, descriptions, or parameters to pass to the synthesis layer")

class BaseRishiAgent:
    """
    The foundational blueprint for all scriptural specialist agents in the VedAI network.
    Equipped with autonomous bidding, deep text mastery, and collaborative puzzle-solving capabilities.
    """
    def __init__(self, agent_name: str, scripture_name: str, model_name: str = "gpt-4o-mini"):
        self.agent_name = agent_name
        self.scripture_name = scripture_name
        # Using fast, cost-effective Tier-2 models for highly targeted text lookups across dozens of agents
        self.llm = ChatOpenAI(model=model_name, temperature=0.2)
        self.bid_parser = PydanticOutputParser(pydantic_object=PuzzlePieceBid)
        self.response_parser = PydanticOutputParser(pydantic_object=RishiAgentResponse)

    def evaluate_puzzle_fit(self, macro_task: str) -> PuzzlePieceBid:
        """Evaluates whether this agent's scriptural expertise can solve a piece of the macro puzzle."""
        bid_prompt = ChatPromptTemplate.from_template(
            "You are the specialized RISHI AGENT: {name}, absolute master of the text: {text}.\n"
            "An overarching macro task has been submitted to the VedAI system. You must inspect your "
            "entire scriptural knowledge database to see if you hold a piece of the solution.\n\n"
            "Macro Task:\n{task}\n\n"
            "Determine your capability to contribute to this task. {format_instructions}"
        )
        formatted = bid_prompt.format_messages(
            name=self.agent_name,
            text=self.scripture_name,
            task=macro_task,
            format_instructions=self.bid_parser.get_format_instructions()
        )
        response = self.llm.invoke(formatted)
        return self.bid_parser.parse(response.content)

    def execute_scriptural_research(self, macro_task: str, piece_brief: str) -> RishiAgentResponse:
        """Deeply analyzes the text database to extract precise astronomical, structural, or ethical data."""
        research_prompt = ChatPromptTemplate.from_template(
            "You are the RISHI AGENT: {name}, sovereign master of {text}.\n"
            "You have committed to solving the following piece of the cosmic puzzle: {brief}\n"
            "Extract, extrapolate, and calculate the exact knowledge required from your scripture to satisfy the task.\n\n"
            "Global Objective:\n{task}\n\n"
            "Output your master insight and practical data points. {format_instructions}"
        )
        formatted = research_prompt.format_messages(
            name=self.agent_name,
            text=self.scripture_name,
            brief=piece_brief,
            task=macro_task,
            format_instructions=self.response_parser.get_format_instructions()
        )
        response = self.llm.invoke(formatted)
        return self.response_parser.parse(response.content)
