# AgenticAI Support Bot

A multi-agent customer service bot built with LangGraph that intelligently routes customer inquiries to specialized agents (Billing, Technical Support, or Feedback).

## Architecture

This project demonstrates a **LangGraph-based agentic system** with:
- **Router Agent**: Classifies incoming customer inquiries
- **Specialized Agents**: 
  - Billing Agent
  - Technical Support Agent
  - Feedback Agent

The system uses conditional routing to direct each inquiry to the appropriate specialized agent based on the classification.

## Tech Stack

- **LangGraph**: For building the agent workflow graph
- **LangChain**: For LLM orchestration
- **FastAPI**: REST API server
- **Groq**: LLM provider (using GPT-OSS-20B model)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Then add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

You can get a free API key from [Groq](https://console.groq.com/)

### 3. Run the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Usage

### Health Check

```bash
curl http://localhost:8000/
```

### Chat Endpoint

Send a POST request to `/chat` with a message:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a billing question about my subscription"}'
```

**Response:**
```json
{
  "classification": "Billing Issue",
  "response": "I'd be happy to help you with your billing question..."
}
```

## Example Queries

- **Billing**: "I need to update my payment method"
- **Technical**: "The app keeps crashing when I try to upload files"
- **Feedback**: "I love the new feature you added!"

## Project Structure

```
service_bot/
├── agents/
│   ├── interface.py    # Router agent that classifies inquiries
│   ├── billing.py      # Billing specialist agent
│   ├── technical.py    # Technical support agent
│   └── feedback.py     # Feedback handling agent
├── graph.py            # LangGraph workflow definition
├── main.py             # FastAPI server
└── requirements.txt    # Python dependencies
```

## How It Works

1. **User sends a message** → FastAPI receives it
2. **Interface Agent** → Classifies the inquiry (Billing/Technical/Feedback)
3. **Router Decision** → Routes to appropriate specialized agent
4. **Specialized Agent** → Generates response using domain-specific prompt
5. **Response returned** → Both classification and final response sent to user

## Demo Tips

- Show the graph visualization (if using LangGraph Studio)
- Demonstrate different query types to show routing
- Explain the conditional edges in the graph
- Highlight how each agent has specialized prompts


