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
        Retrieves relevant documents by filtering out common stop words.
        Prioritizes topic matches over content keyword matches.
        """
        query_lower = query.lower()
        
        # 1. Check for exact topic match first (High Precision)
        for item in self.knowledge_base:
            if item["topic"] in query_lower:
                return item["content"]

        # 2. Filter out stop words for content search
        stop_words = {"is", "are", "am", "you", "your", "the", "a", "an", "in", "on", "of", "to", "for", "with", "what", "how"}
        query_words = [word for word in query_lower.split() if word not in stop_words]

        # If no meaningful keywords remain, return None
        if not query_words:
            return None

        # 3. Search for meaningful keywords in content
        for item in self.knowledge_base:
            content_lower = item["content"].lower()
            # Check if any meaningful keyword exists in the content
            if any(word in content_lower for word in query_words):
                return item["content"]
        
        return None

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
                    f"🤖 **AI Answer:** Based on our documents, {retrieved_info} "
                )
            else:
                # Fallback responses for irrelevant queries
                fallback_responses = [
                    "I'm sorry, I couldn't find specific information about that in my database.",
                    "Could you please rephrase? I don't have documents related to this query.",
                    "I am an AI assistant, but I don't have access to that information right now."
                ]
                return random.choice(fallback_responses)
        
        else:
            # --- Real AI Integration Placeholder ---
            return "Real AI implementation placeholder."

chat_service = ChatService()