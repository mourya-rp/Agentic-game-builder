import os
from typing import TypedDict, Annotated, Sequence
import operator
from langgraph.graph import StateGraph, END


from agents.inquisitor import run_inquisitor
from agents.architect import run_architect
from agents.builder import run_builder


class AgentState(TypedDict):
    user_idea: str
    requirements: str
    blueprint_str: str
   
    final_code: dict 


def clarification_node(state: AgentState):
    print("🤖 Inquisitor: Analyzing your game idea...")
    reqs = run_inquisitor(state["user_idea"])
    return {"requirements": reqs}

def planning_node(state: AgentState):
    print("🤖 Architect: Mapping out the game logic...")
    blueprint_obj = run_architect(state["requirements"])
  
    blueprint_str = (f"Framework: {blueprint_obj.framework}\n"
                     f"Entities: {blueprint_obj.entities}\n"
                     f"Loop: {blueprint_obj.game_loop}")
    return {"blueprint_str": blueprint_str}

def coding_node(state: AgentState):
    print("🤖 Builder: Writing the Phaser.js code...")
    code_obj = run_builder(state["requirements"], state["blueprint_str"])
    # Using getattr to safely handle Pydantic objects or Dictionaries
    return {"final_code": {
        "html": getattr(code_obj, 'html', ""),
        "css": getattr(code_obj, 'css', ""),
        "js": getattr(code_obj, 'js', "")
    }}

def save_files_node(state: AgentState):
    print("\n💾 Manager: Saving files to 'generated_game' folder...")
    os.makedirs("generated_game", exist_ok=True)
    
    code = state["final_code"]
    with open("generated_game/index.html", "w", encoding="utf-8") as f:
        f.write(code.get("html", ""))
    with open("generated_game/style.css", "w", encoding="utf-8") as f:
        f.write(code.get("css", "/* Empty */"))
    with open("generated_game/game.js", "w", encoding="utf-8") as f:
        f.write(code.get("js", "// Empty"))
        
    print("🎉 SUCCESS! All files saved.")
    return state

# 3. Build the LangGraph Pipeline
workflow = StateGraph(AgentState)
workflow.add_node("clarify", clarification_node)
workflow.add_node("plan", planning_node)
workflow.add_node("build", coding_node)
workflow.add_node("save", save_files_node)

workflow.set_entry_point("clarify")
workflow.add_edge("clarify", "plan")
workflow.add_edge("plan", "build")
workflow.add_edge("build", "save")
workflow.add_edge("save", END)

game_builder_agent = workflow.compile()

if __name__ == "__main__":
    print("\n🚀 Welcome to the Agentic Game Builder!")
    print("-" * 40)
    initial_idea = input("Enter your game idea: ")
    
    # Start the engine with a fully initialized state
    game_builder_agent.invoke({
        "user_idea": initial_idea,
        "requirements": "",
        "blueprint_str": "",
        "final_code": {}
    })


    from langchain_core.runnables.graph import MermaidDrawMethod

