import chromadb
from chromadb.utils import embedding_functions


print("ChromaDB store module loaded.")

def store_markdown_in_chroma(md_path: str, collection_name="laptop_knowledge"):
    client = chromadb.Client(
        chromadb.config.Settings(
            persist_directory="./chroma"
        )
    )


    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    collection.add(
        documents=[content],
        metadatas=[{"source": md_path}],
        ids=[md_path]
    )

    print(f"Stored in ChromaDB: {md_path}")
    print("Documents in collection:", collection.count())




def main() -> None:
    store_markdown_in_chroma("knowledge/reddit/my-legion-y540-still-serving-me-after-5-years.md")
    

if __name__ == "__main__":
    main()