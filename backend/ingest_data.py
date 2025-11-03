"""
Data Ingestion Script for AWS Customer Service AI
Loads AWS documentation from markdown files into ChromaDB vector database.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# LangChain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document as LangChainDocument

# Environment setup
from dotenv import load_dotenv

load_dotenv()


class DocumentIngestion:
    """Handles ingestion of markdown documents into ChromaDB."""
    
    def __init__(
        self,
        data_dir: str = "./data",
        persist_directory: str = "./chroma_db",
        collection_name: str = "aws_docs",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        """
        Initialize the document ingestion pipeline.
        
        Args:
            data_dir: Root directory containing document categories
            persist_directory: Directory to persist ChromaDB data
            collection_name: Name of the ChromaDB collection
            embedding_model: Hugging Face embedding model to use
        """
        self.data_dir = Path(data_dir)
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Initialize embeddings
        print(f"Loading embedding model: {embedding_model}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={'device': 'cpu'},  # Use 'cuda' if GPU available
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize text splitter for chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n## ", "\n### ", "\n#### ", "\n\n", "\n", " ", ""]
        )
        
        self.vector_store = None
        
    def parse_frontmatter(self, content: str) -> tuple[Dict[str, Any], str]:
        """
        Parse YAML frontmatter from markdown content.
        
        Args:
            content: Raw markdown content with frontmatter
            
        Returns:
            Tuple of (metadata dict, content without frontmatter)
        """
        metadata = {}
        
        # Match YAML frontmatter between --- delimiters
        pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
        match = re.match(pattern, content, re.DOTALL)
        
        if match:
            frontmatter = match.group(1)
            content = match.group(2)
            
            # Parse YAML-like key-value pairs
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
        
        return metadata, content
    
    def load_documents(self, category: str) -> List[LangChainDocument]:
        """
        Load all markdown documents from a specific category directory.
        
        Args:
            category: Category directory name (technical, configuration, billing)
            
        Returns:
            List of LangChain Document objects
        """
        category_dir = self.data_dir / category
        documents = []
        
        if not category_dir.exists():
            print(f"Warning: Category directory not found: {category_dir}")
            return documents
        
        # Find all markdown files, excluding templates and READMEs
        md_files = [
            f for f in category_dir.glob("*.md") 
            if not f.name.startswith('_') and f.name != 'README.md'
        ]
        
        print(f"\nLoading {len(md_files)} documents from '{category}' category...")
        
        for file_path in md_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse frontmatter
                metadata, main_content = self.parse_frontmatter(content)
                
                # Add additional metadata
                metadata['category'] = category
                metadata['filename'] = file_path.name
                metadata['file_path'] = str(file_path)
                metadata['ingestion_date'] = datetime.now().isoformat()
                
                # Create LangChain document
                doc = LangChainDocument(
                    page_content=main_content,
                    metadata=metadata
                )
                documents.append(doc)
                
                print(f"  ✓ Loaded: {file_path.name}")
                
            except Exception as e:
                print(f"  ✗ Error loading {file_path.name}: {str(e)}")
        
        return documents
    
    def chunk_documents(self, documents: List[LangChainDocument]) -> List[LangChainDocument]:
        """
        Split documents into smaller chunks for better retrieval.
        
        Args:
            documents: List of documents to chunk
            
        Returns:
            List of chunked documents with preserved metadata
        """
        print(f"\nChunking {len(documents)} documents...")
        
        chunked_docs = self.text_splitter.split_documents(documents)
        
        # Add chunk metadata
        for i, chunk in enumerate(chunked_docs):
            chunk.metadata['chunk_id'] = i
            chunk.metadata['chunk_size'] = len(chunk.page_content)
        
        print(f"  ✓ Created {len(chunked_docs)} chunks")
        return chunked_docs
    
    def ingest_to_vector_store(self, documents: List[LangChainDocument]):
        """
        Ingest documents into ChromaDB vector store.
        
        Args:
            documents: List of documents to ingest
        """
        print(f"\nIngesting {len(documents)} chunks into ChromaDB...")
        print(f"  Collection: {self.collection_name}")
        print(f"  Persist directory: {self.persist_directory}")
        
        try:
            # Create or load vector store
            self.vector_store = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                collection_name=self.collection_name,
                persist_directory=self.persist_directory
            )
            
            print(f"  ✓ Successfully ingested all documents")
            
        except Exception as e:
            print(f"  ✗ Error ingesting documents: {str(e)}")
            raise
    
    def run_ingestion(self):
        """Run the complete ingestion pipeline."""
        print("=" * 70)
        print("AWS CUSTOMER SERVICE AI - DATA INGESTION PIPELINE")
        print("=" * 70)
        
        # Define categories to ingest
        categories = ['technical', 'configuration', 'billing']
        
        all_documents = []
        stats = {
            'technical': 0,
            'configuration': 0,
            'billing': 0,
            'total_chunks': 0
        }
        
        # Load documents from each category
        for category in categories:
            docs = self.load_documents(category)
            stats[category] = len(docs)
            all_documents.extend(docs)
        
        if not all_documents:
            print("\n⚠️  No documents found to ingest!")
            return
        
        # Chunk documents
        chunked_documents = self.chunk_documents(all_documents)
        stats['total_chunks'] = len(chunked_documents)
        
        # Ingest into vector store
        self.ingest_to_vector_store(chunked_documents)
        
        # Print summary
        print("\n" + "=" * 70)
        print("INGESTION SUMMARY")
        print("=" * 70)
        print(f"Technical Documents:      {stats['technical']}")
        print(f"Configuration Documents:  {stats['configuration']}")
        print(f"Billing Documents:        {stats['billing']}")
        print(f"Total Documents:          {sum([stats[c] for c in categories])}")
        print(f"Total Chunks Created:     {stats['total_chunks']}")
        print(f"Average Chunks/Document:  {stats['total_chunks'] / sum([stats[c] for c in categories]):.1f}")
        print("=" * 70)
        print("✅ Data ingestion completed successfully!")
        print("=" * 70)
    
    def test_retrieval(self, query: str, k: int = 3):
        """
        Test retrieval from the vector store.
        
        Args:
            query: Query string to test
            k: Number of results to retrieve
        """
        if not self.vector_store:
            print("Vector store not initialized. Please run ingestion first.")
            return
        
        print(f"\n{'=' * 70}")
        print(f"Testing Retrieval: '{query}'")
        print(f"{'=' * 70}")
        
        results = self.vector_store.similarity_search(query, k=k)
        
        for i, doc in enumerate(results, 1):
            print(f"\n[Result {i}]")
            print(f"Category: {doc.metadata.get('category', 'N/A')}")
            print(f"Service: {doc.metadata.get('service', 'N/A')}")
            print(f"Filename: {doc.metadata.get('filename', 'N/A')}")
            print(f"Difficulty: {doc.metadata.get('difficulty', 'N/A')}")
            print(f"\nContent Preview:")
            print(f"{doc.page_content[:300]}...")
            print(f"-" * 70)


def main():
    """Main execution function."""
    # Initialize ingestion pipeline
    ingestion = DocumentIngestion(
        data_dir="./data",
        persist_directory="./chroma_db",
        collection_name="aws_docs"
    )
    
    # Run ingestion
    ingestion.run_ingestion()
    
    # Test retrieval with sample queries
    print("\n" + "=" * 70)
    print("TESTING RETRIEVAL")
    print("=" * 70)
    
    test_queries = [
        "Lambda timeout errors",
        "API Gateway pricing",
        "Lambda security best practices"
    ]
    
    for query in test_queries:
        ingestion.test_retrieval(query, k=2)
    
    print("\n" + "=" * 70)
    print("✅ All tests completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()

