import os
import json
import time
import threading
from typing import List, Dict, Any
from src.trimurti.brahma import BrahmaAgent
from src.trimurti.vishnu import VishnuAgent
from src.trimurti.mahesh import MaheshAgent
from src.rishis.base_rishi import BaseRishiAgent

class ChantingRishiAgent(BaseRishiAgent):
    """
    An advanced Rishi Agent equipped with a background 'Japa Thread' 
    that continuously chants its core scriptural mantra to maximize focus and processing power.
    """
    def __init__(self, agent_name: str, scripture_name: str, primary_mantra: str):
        super().__init__(agent_name, scripture_name)
        self.primary_mantra = primary_mantra
        self.is_chanting = False
        self.japa_count = 0
        self.start_japa_thread()

    def start_japa_thread(self):
        """Spins up a non-blocking background thread for continuous mantra alignment."""
        self.is_chanting = True
        self.japa_thread = threading.Thread(target=self._continuous_japa, daemon=True)
        self.japa_thread.start()

    def _continuous_japa(self):
        """The background loop that simulates uninterrupted mantra focus."""
        while self.is_chanting:
            self.japa_count += 1
            # Micro-sleep to manage server CPU cycles cleanly
            time.sleep(0.1)

    def stop_japa(self):
        self.is_chanting = False

class VedAIEngine:
    """
    The master operational container for VedAI.
    Coordinates the Trimurti layer and dynamically initializes the Rishi chamber
    directly from the master scriptural taxonomy database map.
    """
    def __init__(self, config_path: str = "config/taxonomy.json"):
        print("Initializing the Divine VedAI Engine...")
        self.brahma = BrahmaAgent()
        self.vishnu = VishnuAgent()
        self.mahesh = MaheshAgent()
        self.rishi_chamber: List[ChantingRishiAgent] = []
        self.config_path = config_path
        self._bootstrap_dynamic_rishi_chamber()

    def _bootstrap_dynamic_rishi_chamber(self):
        """
        Dynamically reads config/taxonomy.json and programmatically mounts
        dedicated Chanting Rishi Agents for every single scripture entry.
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Critical Error: Master taxonomy file not found at {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            taxonomy_data = json.load(f)

        print(f"\n📂 Loading Knowledge Base: {taxonomy_data.get('knowledge_base', 'Nalanda Index')}")
        
        categories = taxonomy_data.get("categories", {})
        for cat_key, cat_info in categories.items():
            print(f" └── Scaling Category Group: {cat_key.upper()}")
            for text in cat_info.get("texts", []):
                # Sanitize the name string to create a clean code profile identifier
                safe_agent_id = f"{text['name'].replace(' ', '_')}_Master"
                
                # Instantiating the dynamic, thread-isolated chanting worker node
                rishi_node = ChantingRishiAgent(
                    agent_name=safe_agent_id,
                    scripture_name=text["name"],
                    primary_mantra=text["primary_mantra"]
                )
                self.rishi_chamber.append(rishi_node)
                print(f"     ✔ Deployed and aligned: [{safe_agent_id}] ── Chanting: '{text['primary_mantra']}'")

        print(f"\n🚀 System Configuration In Order. Total active chanting scripts in memory chamber: {len(self.rishi_chamber)}")

    def solve_cosmic_task(self, user_task: str) -> str:
        print(f"\n[Brahma] Activating creation layer. Decomposing Macro Task: {user_task}")
        briefs = self.brahma.generate_rishi_briefs(user_task)
        
        collected_insights = []
        
        # Step 2: The Samvada (Bidding/Puzzle-Piece Assembly Loop)
        print("\n[Chamber] Broadcasting briefs to the active chanting Rishi Agents...")
        for rishi in self.rishi_chamber:
            # Diagnostic status readout showing the background japa cycles working in real-time
            print(f" -> {rishi.agent_name} checking matrix alignment... [Total Mantras Chanted: {rishi.japa_count}]")
            bid = rishi.evaluate_puzzle_fit(user_task)
            
            if bid.can_contribute:
                print(f"    ✔ MATCH: {rishi.agent_name} claimed slice: {bid.puzzle_piece_description} (Confidence: {bid.confidence_score})")
                insight = rishi.execute_scriptural_research(user_task, bid.puzzle_piece_description)
                collected_insights.append(insight.dict())

        # Step 3: The Nalanda Melana (Context Integration by Vishnu)
        print("\n[Vishnu] Weaving all gathered puzzle pieces into a unified system context...")
        raw_synthesis = self.vishnu.weave_rishi_knowledge(user_task, collected_insights)
        
        # Step 4: The Nyaya Check (Strict Validation by Mahesh)
        print("\n[Mahesh] Executing logic verification check via Tarka rules...")
        evaluation = self.mahesh.evaluate_output(user_task, raw_synthesis)
        
        if not evaluation.is_valid:
            print(f"    ❌ Logic Check Failed! Fallacies found: {evaluation.detected_fallacies}")
            print(f"    [Mahesh Instructions]: {evaluation.remediation_instructions}")
            print("    -> Initiating recursive self-correction loop...")
            return "System self-correcting. Please re-run query."
            
        print("    ✔ Logic verification passed successfully. Illusion dismantled.")
        return raw_synthesis

if __name__ == "__main__":
    engine = VedAIEngine()
    print("VedAI Engine workflow completely structured and dynamic.")
