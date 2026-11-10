import os
import sys
from src.orchestrator import VedAIEngine

def run_vedai_sandbox():
    """
    Main sandbox execution script for VedAI.
    Initializes the multi-agent system and tests complex, cross-disciplinary tasks.
    """
    print("=" * 60)
    print("🏛️ WELCOME TO VEDAI: THE DIGITAL NALANDA INTELLIGENCE ENGINE 🏛️")
    print("=" * 60)

    # 1. Initialize the Master Orchestration Engine
    try:
        engine = VedAIEngine(config_path="config/taxonomy.json")
    except Exception as e:
        print(f"❌ Critical Initialization Failure: {e}")
        sys.exit(1)

    # 2. Define the complex, cross-disciplinary task requested by the user
    macro_task = (
        "Map out the entire historical and physical timeline events of the Valmiki Ramayana. "
        "Overlay ancient Vedic descriptions and terrain data onto a modern global satellite map. "
        "Pin accurate coordinates for key locations: precisely trace where Lanka and Kishkindha stood, "
        "pin where Jatayu fell, identify the exact arena where Sugriva and Bali fought, and mark where Bali fell. "
        "Locate the Sanjivani mountain range picked up by Hanumanji and map out the exact path/location where it was delivered. "
        "To achieve maximum geographic fidelity, utilize the specialized Sanskrit Jyotisha and structural space texts "
        "to calculate exact spacetime metrics from the planetary alignments, star vectors, and galactic constants "
        "recorded during these cosmic events, passing these variables to an archaeological synthesis node."
    )

    print("\n" + "#" * 50)
    print("📥 INGESTING USER PROMPT INTO THE CHAMBER")
    print("#" * 50)
    print(f"\nTask Query: {macro_task}\n")

    # 3. Execute the full Samudra Manthan Churning loop (Brahma -> Rishis -> Vishnu -> Mahesh)
    print("Executing system simulation...")
    try:
        final_synthesis = engine.solve_cosmic_task(macro_task)
        
        print("\n" + "=" * 60)
        print("🏆 MASTER SYSTEM OUTPUT DELIVERED")
        print("=" * 60)
        print(final_synthesis)
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Execution Error during agent collaboration loop: {e}")

if __name__ == "__main__":
    # Ensure local environment variables are configured before production runs
    # os.environ["OPENAI_API_KEY"] = "your-api-key-here"
    
    run_vedai_sandbox()
