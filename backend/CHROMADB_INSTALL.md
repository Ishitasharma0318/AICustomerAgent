# ChromaDB Installation Notes

## Issue
ChromaDB installation fails on MacOS due to compilation error in `chroma-hnswlib` dependency:
```
clang: error: the clang compiler does not support '-march=native'
```

## Solution Options

### Option 1: Install Pre-compiled Wheel (Recommended)
```bash
# Activate virtual environment
source venv/bin/activate

# Install chromadb with pre-compiled wheels
pip install chromadb --no-build-isolation
```

### Option 2: Use Docker
Run ChromaDB in a Docker container:
```bash
docker run -p 8000:8000 chromadb/chroma
```

Then update your code to connect to the Docker instance instead of using the embedded version.

### Option 3: Install with Conda
```bash
conda install -c conda-forge chromadb
```

### Option 4: Use Alternative Vector Database
Consider using:
- FAISS (Facebook AI Similarity Search)
- Pinecone
- Weaviate
- Qdrant

## Next Steps
1. Try Option 1 first (pre-compiled wheel)
2. If that fails, use Option 2 (Docker) for development
3. Update the code to support the chosen solution

## When to Install
Install ChromaDB when you're ready to implement **Stage 3: Data Ingestion Pipeline**.

