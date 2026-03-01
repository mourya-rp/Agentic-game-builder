from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# To import from our utils folder
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.llm_client import get_llm

INQUISITOR_PROMPT = """You are a Lead Game Designer. 
Your job is to clarify a user's HTML/JS game idea before developers build it.
To build a functional game, you must know:
1. Core mechanics (What does the player do?)
2. Controls (Mouse, arrow keys, touch?)
3. Win/Loss conditions (How does the game end?)

Analyze the user's idea. 
- CRITICAL RULE: Once all 3 requirements are clear, your VERY FIRST WORD must be exactly [READY]. 
Example of a finished state:
[READY]
Mechanics: ...
Controls: ...
"""

def run_inquisitor(user_idea: str) -> str:
    llm = get_llm(temperature=0.4) 
    
    messages = [
        SystemMessage(content=INQUISITOR_PROMPT),
        HumanMessage(content=user_idea)
    ]
    
    print("\n🤖 Inquisitor: Analyzing your game idea...")
    
    while True:
        # Call the LLM
        response = llm.invoke(messages)
        ai_text = response.content
        
        # Check for the Stop Condition
        if "[READY]" in ai_text:
            print("\n✅ Inquisitor: Requirements locked in!")
            return ai_text
        
        # Print the AI's question and get the user's answer
        print(f"\n🤖 Inquisitor: {ai_text}")
        user_answer = input("\n👤 You: ")
        
        # Append the history so the LLM remembers the conversation
        messages.append(AIMessage(content=ai_text))
        messages.append(HumanMessage(content=user_answer))

# --- Quick Test Block ---
if __name__ == "__main__":
    print("--- TESTING THE INQUISITOR AGENT ---")
    test_idea = input("Enter a simple game idea (e.g., 'Make a snake game'): ")
    final_requirements = run_inquisitor(test_idea)
    print("\n--- FINAL OUTPUT TO PASS TO ARCHITECT ---")
    print(final_requirements)