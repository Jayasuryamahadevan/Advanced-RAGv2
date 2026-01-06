
import chromadb
import uuid
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

class CodeMemory:
    """
    Long-term semantic memory for the Code Engine.
    Stores successfully executed code snippets mapped to natural language intents.
    """

    def __init__(self, persist_path: str = "./chroma_db", collection_name: str = "code_snippets"):
        self.client = chromadb.PersistentClient(path=persist_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        logger.info(f"Initialized CodeMemory at {persist_path} with collection '{collection_name}'")

    def save_context(self, intent: str, code: str, metadata: Dict[str, Any] = None):
        """
        Save a successful code snippet.
        
        Args:
            intent (str): The user's original query or refined intent.
            code (str): The python code that solved it.
            metadata (dict): Additional info (runtime, tables used, etc).
        """
        if metadata is None:
            metadata = {}
        
        # Add basic metadata
        metadata["type"] = "code_snippet"
        
        doc_id = str(uuid.uuid4())
        
        self.collection.add(
            documents=[intent], # Embedding comes from the intent
            metadatas=[{**metadata, "code": code}], # Store code in metadata to avoid embedding it as text
            ids=[doc_id]
        )
        logger.info(f"Saved memory: '{intent}' -> ID: {doc_id}")

    def recall(self, query: str, n_results: int = 1) -> List[Dict[str, Any]]:
        """
        Find similar past solutions.
        
        Returns:
            List of dicts with keys: 'intent', 'code', 'distance', 'metadata'
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        memories = []
        if not results['ids']:
            return memories
            
        for i in range(len(results['ids'][0])):
            meta = results['metadatas'][0][i]
            code = meta.pop('code', '') # Extract code from metadata
            
            memories.append({
                "intent": results['documents'][0][i],
                "code": code,
                "distance": results['distances'][0][i] if results['distances'] else 0.0,
                "metadata": meta
            })
            
        return memories

    def clear(self):
        """Delete all memories."""
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(self.collection.name)
