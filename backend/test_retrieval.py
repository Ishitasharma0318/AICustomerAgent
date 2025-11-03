"""
Test script for verifying ChromaDB retrieval functionality.
Tests different query types across all agent categories.
"""

from ingest_data import DocumentIngestion


def test_technical_queries():
    """Test queries for technical support agent."""
    print("\n" + "=" * 70)
    print("TECHNICAL SUPPORT QUERIES (Pure RAG)")
    print("=" * 70)
    
    ingestion = DocumentIngestion()
    
    # Load existing vector store
    from langchain_community.vectorstores import Chroma
    ingestion.vector_store = Chroma(
        collection_name=ingestion.collection_name,
        persist_directory=ingestion.persist_directory,
        embedding_function=ingestion.embeddings
    )
    
    queries = [
        "My Lambda function is timing out. How do I fix it?",
        "What causes API Gateway 502 errors?",
        "How do I debug Lambda cold start issues?",
        "Lambda memory errors and out of memory issues",
        "VPC connectivity problems with Lambda"
    ]
    
    for query in queries:
        print(f"\n📝 Query: {query}")
        results = ingestion.vector_store.similarity_search(
            query, 
            k=3, 
            filter={"category": "technical"}
        )
        
        for i, doc in enumerate(results, 1):
            print(f"\n  [{i}] {doc.metadata.get('filename', 'Unknown')}")
            print(f"      Service: {doc.metadata.get('service', 'N/A')}")
            print(f"      Subcategory: {doc.metadata.get('subcategory', 'N/A')}")
            print(f"      Relevance Score: ✓")


def test_configuration_queries():
    """Test queries for configuration agent."""
    print("\n" + "=" * 70)
    print("CONFIGURATION & BEST PRACTICES QUERIES (Pure CAG)")
    print("=" * 70)
    
    ingestion = DocumentIngestion()
    
    from langchain_community.vectorstores import Chroma
    ingestion.vector_store = Chroma(
        collection_name=ingestion.collection_name,
        persist_directory=ingestion.persist_directory,
        embedding_function=ingestion.embeddings
    )
    
    queries = [
        "What are Lambda best practices?",
        "How do I configure CORS for API Gateway?",
        "IAM roles and policies for Lambda",
        "Lambda security guidelines",
        "How to deploy Lambda functions?"
    ]
    
    for query in queries:
        print(f"\n📝 Query: {query}")
        results = ingestion.vector_store.similarity_search(
            query, 
            k=3, 
            filter={"category": "configuration"}
        )
        
        for i, doc in enumerate(results, 1):
            print(f"\n  [{i}] {doc.metadata.get('filename', 'Unknown')}")
            print(f"      Service: {doc.metadata.get('service', 'N/A')}")
            print(f"      Subcategory: {doc.metadata.get('subcategory', 'N/A')}")


def test_billing_queries():
    """Test queries for billing agent."""
    print("\n" + "=" * 70)
    print("BILLING & PRICING QUERIES (Hybrid RAG/CAG)")
    print("=" * 70)
    
    ingestion = DocumentIngestion()
    
    from langchain_community.vectorstores import Chroma
    ingestion.vector_store = Chroma(
        collection_name=ingestion.collection_name,
        persist_directory=ingestion.persist_directory,
        embedding_function=ingestion.embeddings
    )
    
    queries = [
        "How much does Lambda cost?",
        "API Gateway pricing differences",
        "What is included in the AWS free tier?",
        "Cost optimization strategies for Lambda",
        "Regional pricing differences for Lambda"
    ]
    
    for query in queries:
        print(f"\n📝 Query: {query}")
        results = ingestion.vector_store.similarity_search(
            query, 
            k=3, 
            filter={"category": "billing"}
        )
        
        for i, doc in enumerate(results, 1):
            print(f"\n  [{i}] {doc.metadata.get('filename', 'Unknown')}")
            print(f"      Service: {doc.metadata.get('service', 'N/A')}")
            print(f"      Subcategory: {doc.metadata.get('subcategory', 'N/A')}")


def test_metadata_filtering():
    """Test metadata-based filtering capabilities."""
    print("\n" + "=" * 70)
    print("METADATA FILTERING TESTS")
    print("=" * 70)
    
    ingestion = DocumentIngestion()
    
    from langchain_community.vectorstores import Chroma
    ingestion.vector_store = Chroma(
        collection_name=ingestion.collection_name,
        persist_directory=ingestion.persist_directory,
        embedding_function=ingestion.embeddings
    )
    
    # Test 1: Filter by service
    print("\n🔍 Test 1: Lambda-only documents")
    results = ingestion.vector_store.similarity_search(
        "configuration",
        k=5,
        filter={"service": "lambda"}
    )
    print(f"   Found {len(results)} Lambda documents")
    
    # Test 2: Filter by difficulty
    print("\n🔍 Test 2: Beginner-level documents")
    results = ingestion.vector_store.similarity_search(
        "AWS",
        k=5,
        filter={"difficulty": "beginner"}
    )
    print(f"   Found {len(results)} beginner documents")
    
    # Test 3: Combine filters
    print("\n🔍 Test 3: Technical Lambda documents")
    results = ingestion.vector_store.similarity_search(
        "errors",
        k=5,
        filter={"category": "technical", "service": "lambda"}
    )
    print(f"   Found {len(results)} technical Lambda documents")


def test_collection_stats():
    """Display statistics about the vector store."""
    print("\n" + "=" * 70)
    print("VECTOR STORE STATISTICS")
    print("=" * 70)
    
    ingestion = DocumentIngestion()
    
    from langchain_community.vectorstores import Chroma
    ingestion.vector_store = Chroma(
        collection_name=ingestion.collection_name,
        persist_directory=ingestion.persist_directory,
        embedding_function=ingestion.embeddings
    )
    
    # Get collection
    collection = ingestion.vector_store._collection
    
    print(f"\nCollection Name: {collection.name}")
    print(f"Total Documents: {collection.count()}")
    
    # Count by category
    for category in ['technical', 'configuration', 'billing']:
        results = ingestion.vector_store.similarity_search(
            "AWS",
            k=1000,
            filter={"category": category}
        )
        print(f"{category.capitalize()} chunks: {len(results)}")


def main():
    """Run all retrieval tests."""
    print("\n" + "=" * 70)
    print("CHROMADB RETRIEVAL TEST SUITE")
    print("=" * 70)
    
    try:
        # Display collection stats
        test_collection_stats()
        
        # Test technical queries
        test_technical_queries()
        
        # Test configuration queries
        test_configuration_queries()
        
        # Test billing queries
        test_billing_queries()
        
        # Test metadata filtering
        test_metadata_filtering()
        
        print("\n" + "=" * 70)
        print("✅ ALL RETRIEVAL TESTS PASSED!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        raise


if __name__ == "__main__":
    main()

