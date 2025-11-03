"""
Billing & Pricing Agent - Hybrid RAG/CAG
Handles pricing questions, cost optimization, and billing estimates
"""

import os
from typing import Dict, Any, List, Optional
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class BillingAgent:
    """
    Billing agent using Hybrid RAG/CAG strategy
    
    Strategy:
    - First query: Use RAG to retrieve pricing information
    - Subsequent queries in session: Use cached pricing data (CAG)
    - Optimizes for both accuracy and performance
    - Uses OpenAI GPT-4 for high-quality responses
    """
    
    def __init__(self, vector_db_path: str = "./chroma_db", collection_name: str = "aws_docs"):
        """
        Initialize billing agent
        
        Args:
            vector_db_path: Path to ChromaDB persistent storage
            collection_name: Name of the collection to query
        """
        # Initialize embeddings model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Initialize ChromaDB client
        self.vector_db = Chroma(
            persist_directory=vector_db_path,
            collection_name=collection_name,
            embedding_function=self.embeddings
        )
        
        # Initialize OpenAI LLM for response generation
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,  # Low temperature for accurate pricing information
            streaming=True
        )
        
        # Per-session caches for hybrid strategy
        self.session_caches: Dict[str, Dict[str, Any]] = {}
        
        # Create the prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("human", "{query}")
        ])
        
        # Create chain
        self.chain = self.prompt_template | self.llm | StrOutputParser()
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for billing guidance"""
        return """You are an AWS Billing and Cost Optimization expert specializing in Lambda and API Gateway pricing.

Your role:
- Provide accurate pricing information and cost calculations
- Explain pricing models and billing structures
- Suggest cost optimization strategies
- Help estimate costs based on usage patterns
- Clarify free tier limits and quotas
- Advise on cost monitoring and budgeting

Guidelines:
- Be precise with numbers and pricing tiers
- Explain billing formulas clearly
- Consider regional pricing differences
- Mention free tier benefits when relevant
- Provide practical cost optimization tips
- Use examples to illustrate cost scenarios
- Always clarify currency and time periods

Use the following pricing documentation to answer the user's question. Provide accurate, up-to-date pricing information based on this documentation.

Pricing Documentation:
{context}

User Question: {query}
"""
    
    async def process(
        self,
        message: str,
        history: List[BaseMessage],
        session_id: str
    ) -> Dict[str, Any]:
        """
        Process billing query using hybrid approach
        
        Args:
            message: User's billing question
            history: Conversation history
            session_id: Session identifier
            
        Returns:
            Response dict with answer and sources
        """
        # Check if we have cached data for this session
        if session_id in self.session_caches:
            # Use CAG - cached data (subsequent queries)
            return await self._process_with_cache(message, session_id)
        else:
            # First query - use RAG and then cache
            return await self._process_with_retrieval(message, session_id)
    
    async def _process_with_retrieval(
        self,
        message: str,
        session_id: str
    ) -> Dict[str, Any]:
        """
        First query: Retrieve and cache pricing documents
        
        Args:
            message: User's query
            session_id: Session identifier
            
        Returns:
            Response dict
        """
        # Retrieve relevant billing/pricing documents
        retrieved_docs = self.retrieve_documents(message, k=10)  # Get more docs for pricing
        
        # Format context from retrieved documents
        context = self._format_context(retrieved_docs)
        
        # Cache the retrieved context for this session
        self.session_caches[session_id] = {
            "context": context,
            "documents": retrieved_docs,
            "timestamp": "first_query"
        }
        
        # Generate response using the LLM with context and query
        response = await self.chain.ainvoke({
            "context": context,
            "query": message
        })
        
        # Extract source metadata
        sources = self._extract_sources(retrieved_docs)
        
        return {
            "response": response,
            "sources": sources,
            "agent_type": "billing",
            "retrieval_mode": "RAG",
            "cache_created": True,
            "retrieval_count": len(retrieved_docs)
        }
    
    async def _process_with_cache(
        self,
        message: str,
        session_id: str
    ) -> Dict[str, Any]:
        """
        Subsequent queries: Use cached pricing data
        
        Args:
            message: User's query
            session_id: Session identifier
            
        Returns:
            Response dict
        """
        # Get cached context
        cache_data = self.session_caches[session_id]
        cached_context = cache_data["context"]
        cached_docs = cache_data["documents"]
        
        # Generate response using the LLM with cached context
        response = await self.chain.ainvoke({
            "context": cached_context,
            "query": message
        })
        
        # Extract source metadata from cached documents
        sources = self._extract_sources(cached_docs)
        
        return {
            "response": response,
            "sources": sources,
            "agent_type": "billing",
            "retrieval_mode": "CAG",
            "cache_used": True,
            "cached_doc_count": len(cached_docs)
        }
    
    def retrieve_documents(self, query: str, k: int = 10) -> List[Any]:
        """
        Retrieve relevant billing/pricing documents
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of relevant document chunks with metadata
        """
        # Perform similarity search with metadata filtering for billing category
        results = self.vector_db.similarity_search(
            query=query,
            k=k,
            filter={"category": "billing"}
        )
        
        return results
    
    def _format_context(self, documents: List[Any]) -> str:
        """
        Format retrieved documents into context string
        
        Args:
            documents: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        if not documents:
            return "No pricing documentation found."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            metadata = doc.metadata
            content = doc.page_content
            
            context_part = f"""
Document {i}:
Source: {metadata.get('filename', 'unknown')}
Service: {metadata.get('service', 'unknown')}
Category: {metadata.get('subcategory', 'unknown')}

Content:
{content}
---
"""
            context_parts.append(context_part)
        
        return "\n".join(context_parts)
    
    def _extract_sources(self, documents: List[Any]) -> List[Dict[str, str]]:
        """
        Extract source metadata from documents
        
        Args:
            documents: List of documents
            
        Returns:
            List of source metadata dictionaries
        """
        sources = []
        seen = set()  # Avoid duplicate sources
        
        for doc in documents:
            metadata = doc.metadata
            filename = metadata.get("filename", "unknown")
            
            # Only add unique sources
            if filename not in seen:
                sources.append({
                    "filename": filename,
                    "service": metadata.get("service", "unknown"),
                    "category": metadata.get("category", "unknown"),
                    "subcategory": metadata.get("subcategory", "unknown")
                })
                seen.add(filename)
        
        return sources
    
    def get_session_cache(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get cached data for a session"""
        return self.session_caches.get(session_id)
    
    def clear_session_cache(self, session_id: str):
        """Clear cache for a specific session"""
        if session_id in self.session_caches:
            del self.session_caches[session_id]
    
    def clear_all_caches(self):
        """Clear all session caches"""
        self.session_caches.clear()

