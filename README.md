# 🤖 Agentic Game Builder

An advanced multi-agent orchestration system that transforms natural language prompts into executable 2D games. Powered by **LangGraph**, **Gemini 1.5 Pro**, and **Streamlit**.

## Project Demo
(https://drive.google.com/file/d/1Fy9jWvClvOaPW5yToFOGZBt6kc34LYKb/view?usp=sharing)

> *Click the badge above to see the agent in action!*

---

## Overview
The **Agentic Game Builder** is a stateful AI system that handles the full game development lifecycle. Unlike simple chatbots, this system uses a **Directed Acyclic Graph (DAG)** to coordinate specialized AI agents, ensuring that game logic is planned, refined, and validated before a single line of code is written.

### The Multi-Agent Architecture
The system utilizes a **LangGraph-based state machine** to prevent premature code generation and ensure structural integrity:

* **Requirements Clarification (Inquisitor Node):** Evaluates user prompts for ambiguity. It engages in a feedback loop, asking targeted follow-up questions to define mechanics, layout, and win/loss states.
* **Planning (Architect Node):** Translates refined requirements into a rigid technical JSON blueprint, defining the **Phaser.js** framework setup, game loop, and core systems.
* **Execution (Builder Node):** Consumes the architectural blueprint to generate production-ready HTML/CSS/JavaScript.

---

## Technical Stack
* **Orchestration:** LangGraph (Stateful Agent Flows)
* **LLM:** Gemini 1.5 Pro (via Google Generative AI)
* **Interface:** Streamlit (Full-stack Web UI)
* **Validation:** Pydantic (Strict Schema Enforcement)
* **Environment:** Docker (Ships with a production-grade Dockerfile, ready for AWS, GCP, or Azure.)

---

## Getting Started

###  Run with Docker (Recommended)
This agent is fully containerized for a "zero-config" setup.

1.  **Environment Configuration:**
    Create a `.env` file in the root directory:
    ```text
    OPENROUTER_API_KEY=your_api_key_here
    ```

2.  **Build the Container:**
    ```bash
    docker build -t agentic-game-builder .
    ```

3.  **Run the Agent:**
    ```bash
    docker run -p 8501:8501 --env-file .env agentic-game-builder
    ```

4.  **Access the UI:**
    Open your browser to `http://localhost:8501`.

---

##  Engineering Trade-Offs
* **Model Selection:** Utilized **Gemini 1.5 Flash**. While smaller models offer lower latency, Gemini’s superior "spatial intelligence" significantly reduces coordinate errors and rendering bugs in HTML5 Canvas layouts.
* **UX vs. Exhaustion:** The Inquisitor node is tuned to ask a maximum of 2-3 targeted questions to balance technical precision with a frictionless user experience.

##  Future Roadmap
* **Self-Correction Loop:** Integrating **Playwright** for automated runtime verification. The agent will "test-boot" the game, capture console errors, and auto-heal the code.
* **RAG Integration:** Utilizing a vector database (ChromaDB) to store player preferences and "memory" for hyper-personalized game design.

