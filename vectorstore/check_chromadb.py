# check_chromadb.py
import chromadb
from chromadb.utils import embedding_functions

def check_all_collections():
    """Check what's actually in ChromaDB."""
    
    client = chromadb.Client(
        chromadb.config.Settings(
            persist_directory="./chroma"
        )
    )
    
    print("="*60)
    print("ChromaDB Diagnostic Report")
    print("="*60)
    
    # List all collections
    collections = client.list_collections()
    print(f"\nTotal collections: {len(collections)}")
    
    for col in collections:
        print(f"\n📁 Collection: {col.name}")
        print(f"   Documents: {col.count()}")
        
        if col.count() > 0:
            # Get a sample document
            result = col.get(limit=1)
            print(f"   Sample IDs: {result['ids']}")
            print(f"   Sample metadata: {result['metadatas']}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    check_all_collections()