"""
Technical Support Agent - Pure RAG
Handles troubleshooting, debugging, and error resolution
"""

import os
from typing import Dict, Any, List, Optional
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class TechnicalSupportAgent:
    """
    Technical support agent using Pure RAG strategy
    
    Strategy: 
    - Queries vector database for every request
    - Retrieves latest troubleshooting solutions
    - Uses OpenAI GPT-4 for high-quality responses
    """
    
    def __init__(self, vector_db_path: str = "./chroma_db", collection_name: str = "aws_docs"):
        """
        Initialize technical support agent
        
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
            temperature=0.1,  # Low temperature for consistent technical answers
            streaming=True
        )
        
        # Create the RAG prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("human", "{query}")
        ])
        
        # Create RAG chain
        self.chain = self.prompt_template | self.llm | StrOutputParser()
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for technical support"""
        return """You are an expert AWS Technical Support specialist focused on Lambda and API Gateway troubleshooting.

Your role:
- Provide clear, actionable solutions to technical problems
- Reference specific error codes and their meanings
- Give step-by-step debugging instructions
- Explain root causes of issues
- Suggest preventive measures

Guidelines:
- Be precise and technical but accessible
- Use bullet points for steps
- Include relevant AWS service names and features
- Cite error codes when relevant
- If the issue is complex, break it down into manageable steps

Use the following retrieved documentation to answer the user's question. If the documentation doesn't contain relevant information, acknowledge this and provide general troubleshooting advice based on AWS best practices.

Retrieved Documentation:
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
        Process technical support query using RAG
        
        Args:
            message: User's technical question
            history: Conversation history
            session_id: Session identifier
            
        Returns:
            Response dict with answer and sources
        """
        # Retrieve relevant documents
        retrieved_docs = self.retrieve_documents(message, k=5)
        
        # Format context from retrieved documents
        context = self._format_context(retrieved_docs)
        
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
            "agent_type": "technical_support",
            "retrieval_count": len(retrieved_docs)
        }
    
    def retrieve_documents(self, query: str, k: int = 5) -> List[Any]:
        """
        Retrieve relevant technical documents using similarity search
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of relevant document chunks with metadata
        """
        # Perform similarity search with metadata filtering for technical category
        results = self.vector_db.similarity_search(
            query=query,
            k=k,
            filter={"category": "technical"}
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
            return "No relevant documentation found."
        
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
        Extract source metadata from retrieved documents
        
        Args:
            documents: List of retrieved documents
            
        Returns:
            List of source metadata dictionaries
        """
        sources = []
        for doc in documents:
            metadata = doc.metadata
            sources.append({
                "filename": metadata.get("filename", "unknown"),
                "service": metadata.get("service", "unknown"),
                "category": metadata.get("category", "unknown"),
                "subcategory": metadata.get("subcategory", "unknown")
            })
        
        return sources

