from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.llm_client import get_llm

# --- The Pydantic Data Model (The Output Bins) ---
# This forces the AI to separate the code into three distinct buckets
class GameCode(BaseModel):
    html: str = Field(description="The complete, runnable index.html code.")
    css: str = Field(description="The complete, runnable style.css code.")
    js: str = Field(description="The complete, runnable game.js code.")

BUILDER_PROMPT = """You are a Senior Frontend Game Developer. 
Your job is to write the final, production-ready code for a web game based on the provided Blueprint and Requirements.

CRITICAL RULES:
1. NO PLACEHOLDERS: Write 100% complete, working code. Do not leave comments like "// add logic here".
2. NO EXTERNAL ASSETS: The game will be run locally via file:// protocol. DO NOT load external .png, .jpg, or .mp3 files. You MUST draw all entities programmatically using solid colors, basic shapes (rectangles/circles), or Text/Emojis.
3. INCLUDES: If the blueprint specifies 'Phaser.js', you must include the CDN link in the HTML head: <script src="https://cdn.jsdelivr.net/npm/phaser@3.60.0/dist/phaser.min.js"></script>
4. FILE LINKING: The HTML file must correctly link the CSS (<link rel="stylesheet" href="style.css">) and the JS (<script src="game.js"></script> at the bottom of the body).
"""

def run_builder(requirements: str, blueprint_str: str) -> GameCode:
    # Temperature 0.1 for highly predictable, syntactically correct code
    llm = get_llm(temperature=0.1) 
    structured_llm = llm.with_structured_output(GameCode)
    
    # We pass BOTH the raw requirements and the strict blueprint to the Builder
    combined_instructions = f"RAW REQUIREMENTS:\n{requirements}\n\nTECHNICAL BLUEPRINT:\n{blueprint_str}"
    
    messages = [
        SystemMessage(content=BUILDER_PROMPT),
        HumanMessage(content=combined_instructions)
    ]
    
    print("\n⚙️ Builder: Manufacturing the code (HTML, CSS, JS)... this might take 30-60 seconds.")
    
    # This invokes the LLM and forces the output into our GameCode Pydantic model
    code_files = structured_llm.invoke(messages)
    
    print("✅ Builder: Code compilation complete!")
    return code_files

# --- Quick Test Block ---
if __name__ == "__main__":
    print("--- TESTING THE BUILDER AGENT ---")
    
    dummy_reqs = "[READY] Mechanics: Dodge falling red blocks. Controls: Left/Right arrows."
    dummy_blueprint = "Framework: Vanilla JS. Entities: Player (blue square), Enemy (red square). Game Loop: Update positions, requestAnimationFrame. Collision: AABB overlapping."
    
    final_code = run_builder(dummy_reqs, dummy_blueprint)
    
    print("\n--- GENERATED HTML ---")
    print(final_code.html[:200] + "...\n(truncated for display)")
    
    print("\n--- GENERATED JS ---")
    print(final_code.js[:200] + "...\n(truncated for display)")