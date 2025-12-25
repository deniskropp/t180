from klipper_sdk.memory import SpatialMemory

def test_semantics():
    mem = SpatialMemory()
    if not mem.model:
        print("Skipping test: No model")
        return

    # Ingest concepts
    n1 = mem.ingest_entry("Python programming function")
    n2 = mem.ingest_entry("Database SQL query")
    n3 = mem.ingest_entry("def foo(): pass")
    
    # Check similarity
    print(f"Checking similarity for '{n3.content}'...")
    similar = mem.find_similar(n3.content)
    for node in similar:
        # Should match n1 (Python) closer than n2 (SQL)
        print(f" -> {node.content}")

if __name__ == "__main__":
    test_semantics()
