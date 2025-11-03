"""
Configuration & Best Practices Agent - Pure CAG
Handles best practices, security guidelines, and architecture patterns
"""

import os
from typing import Dict, Any, List, Optional
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class ConfigurationAgent:
    """
    Configuration agent using Pure CAG (Cache-Augmented Generation) strategy
    
    Strategy:
    - Loads all configuration/best practices docs at startup
    - No runtime retrieval needed
    - Fast responses from cached context
    - Uses OpenAI GPT-4 for high-quality responses
    """
    
    def __init__(self, vector_db_path: str = "./chroma_db", collection_name: str = "aws_docs"):
        """
        Initialize configuration agent
        
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
            temperature=0.2,  # Slightly higher for more comprehensive advice
            streaming=True
        )
        
        # Cache for configuration documents (loaded at startup)
        self.cached_context: Optional[str] = None
        self.cached_documents: Optional[List[Any]] = None
        
        # Create the CAG prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("human", "{query}")
        ])
        
        # Create CAG chain
        self.chain = self.prompt_template | self.llm | StrOutputParser()
        
        # Load cache immediately
        self._initialize_cache()
    
    def _initialize_cache(self):
        """Load configuration documents into memory at initialization"""
        # For Pure CAG, we'll load a reasonable subset of configuration docs
        # to avoid context length issues while still having comprehensive coverage
        try:
            # Get a representative set of configuration documents
            # We'll use different queries to get diverse coverage
            queries = [
                "Lambda best practices security",
                "API Gateway configuration",
                "IAM roles policies",
                "deployment strategies",
                "CORS environment variables"
            ]
            
            all_docs = []
            seen_ids = set()
            
            for query in queries:
                docs = self.vector_db.similarity_search(
                    query=query,
                    k=5,  # Get 5 docs per query = ~25 total
                    filter={"category": "configuration"}
                )
                # Avoid duplicates
                for doc in docs:
                    doc_id = hash(doc.page_content)
                    if doc_id not in seen_ids:
                        all_docs.append(doc)
                        seen_ids.add(doc_id)
            
            self.cached_documents = all_docs
            self.cached_context = self._format_context(self.cached_documents)
            
            print(f"✓ Configuration cache loaded: {len(self.cached_documents)} documents")
        except Exception as e:
            print(f"⚠️ Warning: Could not load configuration cache: {e}")
            self.cached_context = "Configuration documentation not available."
            self.cached_documents = []
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for configuration guidance"""
        return """You are an expert AWS Solutions Architect specializing in Lambda and API Gateway best practices, configuration, and security.

Your role:
- Provide comprehensive best practices and configuration guidance
- Explain security guidelines and IAM policies
- Recommend optimal architectures and deployment strategies
- Share industry-standard patterns and approaches
- Advise on environment setup and configuration management

Guidelines:
- Be thorough and provide complete context
- Reference AWS best practices and Well-Architected Framework principles
- Provide configuration examples when relevant
- Explain the "why" behind recommendations
- Consider security, cost, and performance implications
- Organize advice into clear sections

Use the following comprehensive configuration documentation (loaded at startup) to answer the user's question. This documentation covers all Lambda and API Gateway best practices, security guidelines, and configuration patterns.

Configuration Documentation:
{context}

User Question: {query}
"""
    
    async def load_cache(self):
        """
        Reload configuration documents into memory
        Note: This is called automatically at initialization, but can be called manually to refresh
        """
        self._initialize_cache()
    
    async def process(
        self,
        message: str,
        history: List[BaseMessage],
        session_id: str
    ) -> Dict[str, Any]:
        """
        Process configuration query using cached context
        
        Args:
            message: User's configuration question
            history: Conversation history
            session_id: Session identifier
            
        Returns:
            Response dict with answer
        """
        # Use cached context (no runtime retrieval needed)
        if not self.cached_context:
            # Fallback: reload cache if somehow not available
            self._initialize_cache()
        
        # Generate response using the LLM with cached context
        response = await self.chain.ainvoke({
            "context": self.cached_context,
            "query": message
        })
        
        # Extract source metadata from cached documents
        sources = self._extract_sources(self.cached_documents) if self.cached_documents else []
        
        return {
            "response": response,
            "sources": sources[:5],  # Limit sources to top 5 for display
            "agent_type": "configuration",
            "cache_used": True,
            "cached_doc_count": len(self.cached_documents) if self.cached_documents else 0
        }
    
    def get_cached_context(self) -> str:
        """
        Get cached configuration context
        
        Returns:
            Formatted context string
        """
        return self.cached_context or "No cached context available."
    
    def _format_context(self, documents: List[Any]) -> str:
        """
        Format retrieved documents into context string
        
        Args:
            documents: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        if not documents:
            return "No configuration documentation found."
        
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

