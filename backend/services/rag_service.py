import os
import json
import random
from typing import List, Optional

# Define the path to the knowledge base file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_FILE = os.path.join(BASE_DIR, "data", "knowledge.json")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ChatService:
    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()

    def _load_knowledge_base(self) -> List[dict]:
        """Loads the knowledge base from the JSON file."""
        try:
            with open(KNOWLEDGE_FILE, "r") as f:
                data = json.load(f)
                print(f"[RAG Service] Loaded {len(data)} documents from knowledge base.")
                return data
        except FileNotFoundError:
            print("[RAG Service] Warning: knowledge.json not found!")
            return []

    def _retrieve_documents(self, query: str) -> Optional[str]:
        """
        Retrieves the most relevant document using a Scoring Algorithm.
        Prioritizes Topic Match > Content Match.
        """
        query_lower = query.lower()
        
        # Stop words to filter out
        stop_words = {"is", "are", "am", "you", "your", "the", "a", "an", "in", "on", "of", "to", "for", "with", "what", "how", "process", "do", "does", "please", "tell", "me"}
        
        # Extract meaningful keywords
        query_words = [word for word in query_lower.split() if word not in stop_words]
        
        if not query_words:
            return None

        best_match = None
        highest_score = 0

        for item in self.knowledge_base:
            score = 0
            topic_lower = item["topic"].lower()
            content_lower = item["content"].lower()

            # Scoring Logic:
            for word in query_words:
                # 1. Topic Match (High Priority: +10 points)
                if word in topic_lower:
                    score += 10
                
                # 2. Content Match (Lower Priority: +1 point)
                if word in content_lower:
                    score += 1

            # Keep track of the document with the highest score
            if score > highest_score:
                highest_score = score
                best_match = item["content"]

        # Only return if the score is meaningful (threshold e.g., > 0)
        return best_match if highest_score > 0 else None

    async def get_response(self, user_query: str) -> str:
        """
        Generates a response using Retrieval-Augmented Generation (RAG).
        """
        # 1. Retrieve relevant context
        retrieved_info = self._retrieve_documents(user_query)

        # 2. Generate Response
        if not OPENAI_API_KEY or OPENAI_API_KEY.startswith("sk-proj-xxx"):
            # --- Mock Response Logic ---
            if retrieved_info:
                return (
                    f"🔍 **Retrieved Context:** {retrieved_info}\n\n"
                    f"🤖 **AI Answer:** Based on our documents, {retrieved_info}"
                )
            else:
                fallback_responses = [
                    "I'm sorry, I couldn't find specific information about that in my database.",
                    "Could you please rephrase? I don't have documents related to this query.",
                    "I am an AI assistant, but I don't have access to that information right now."
                ]
                return random.choice(fallback_responses)
        
        else:
            # --- Real AI Integration Placeholder ---
            # In a real scenario, you would send 'retrieved_info' + 'user_query' to OpenAI here.
            return "Real AI implementation placeholder."

chat_service = ChatService()