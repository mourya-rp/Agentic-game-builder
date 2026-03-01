from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.llm_client import get_llm

# --- The Pydantic Data Model (The Quality Inspector) ---
# This FORCES the AI to output exactly these 4 fields, no exceptions.
class GameBlueprint(BaseModel):
    framework: str = Field(description="Strictly choose either 'Vanilla JS' or 'Phaser.js'.")
    entities: list[str] = Field(description="List of objects needed (e.g., ['Player', 'Enemy']).")
    game_loop: str = Field(description="Step-by-step logic of what updates every frame.")
    collision_logic: str = Field(description="Exact mathematical or logical rules for win/loss conditions.")

ARCHITECT_PROMPT = """You are a Senior Technical Game Architect. 
Your job is to read the finalized game requirements and create a strict technical blueprint for the coding team.

Rules:
1. If the game requires physics, gravity, or complex collisions, choose 'Phaser.js'.
2. If the game is a simple grid, UI-based, or basic DOM manipulation, choose 'Vanilla JS'.
3. Break the mechanics down into logical, programmatic steps. Do not write code, only write the logic.
"""

def run_architect(requirements: str) -> GameBlueprint:
    # Temperature 0.1 because we want rigid logic, zero creativity
    llm = get_llm(temperature=0.1) 
    
    # This is the magic line that binds Pydantic to the LLM
    structured_llm = llm.with_structured_output(GameBlueprint)
    
    messages = [
        SystemMessage(content=ARCHITECT_PROMPT),
        HumanMessage(content=f"Here are the requirements:\n{requirements}")
    ]
    
    print("\n📐 Architect: Drafting the technical blueprint...")
    blueprint = structured_llm.invoke(messages)
    print("✅ Architect: Blueprint finalized!")
    
    return blueprint

# --- Quick Test Block ---
if __name__ == "__main__":
    print("--- TESTING THE ARCHITECT AGENT ---")
    test_reqs = input("Paste your requirements (or just type a summary): ")
    
    final_blueprint = run_architect(test_reqs)
    
    print("\n--- FINAL BLUEPRINT ---")
    print(f"Framework: {final_blueprint.framework}")
    print(f"Entities: {', '.join(final_blueprint.entities)}")
    print(f"Game Loop: {final_blueprint.game_loop}")
    print(f"Collision: {final_blueprint.collision_logic}")