from typing import Dict, List, Optional, Any
import uuid
import numpy as np
try:
    from sentence_transformers import SentenceTransformer
    HAS_EMBEDDINGS = True
except ImportError:
    HAS_EMBEDDINGS = False

class MemoryNode:
    """A node in the spatial memory graph."""
    def __init__(self, content: str, node_type: str = "concept", vector: Optional[np.ndarray] = None):
        self.id = str(uuid.uuid4())
        self.content = content
        self.node_type = node_type
        self.vector = vector
        self.metadata = {}
        
    def __repr__(self):
        return f"<Node({self.node_type}): {self.content[:20]}...>"

class MemoryEdge:
    """A relationship between two nodes."""
    def __init__(self, source_id: str, target_id: str, relation: str, weight: float = 1.0):
        self.source_id = source_id
        self.target_id = target_id
        self.relation = relation
        self.weight = weight

class SpatialMemory:
    """
    Gen 8: The Spatial Layer (Topology + Semantics).
    Maps relationships between data points in a persistent graph using Vector Embeddings.
    """
    def __init__(self):
        self.nodes: Dict[str, MemoryNode] = {}
        self.edges: List[MemoryEdge] = []
        
        self.model = None
        if HAS_EMBEDDINGS:
            print("[SpatialMemory] Loading embedding model (all-MiniLM-L6-v2)...")
            try:
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception as e:
                print(f"[SpatialMemory] Failed to load model: {e}")
        else:
            print("[SpatialMemory] 'sentence-transformers' not found. Semantic features disabled.")
        
    def add_node(self, content: str, node_type: str = "fact") -> MemoryNode:
        vector = None
        if self.model:
            vector = self.model.encode(content)
            
        node = MemoryNode(content, node_type, vector)
        self.nodes[node.id] = node
        return node
        
    def find_similar(self, text: str, top_k: int = 3) -> List[MemoryNode]:
        """Finds semantically similar nodes."""
        if not self.model or not self.nodes:
            return []
            
        query_vector = self.model.encode(text)
        
        results = []
        for node in self.nodes.values():
            if node.vector is not None:
                # Cosine similarity
                similarity = np.dot(query_vector, node.vector) / (
                    np.linalg.norm(query_vector) * np.linalg.norm(node.vector)
                )
                results.append((similarity, node))
                
        # Sort by similarity desc
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:top_k]]

    def ingest_entry(self, entry_text: str):
        """
        Parses an entry and creates a node.
        Also finds and links to similar existing nodes.
        """
        new_node = self.add_node(entry_text, "entry")
        
        # Auto-link to similar concepts
        similar = self.find_similar(entry_text, top_k=2)
        for node in similar:
            if node.id != new_node.id:
                # Create an edge
                self.add_edge(new_node, node, "semantically_related", weight=0.8)
                print(f"  [Space] Linked '{new_node.content[:15]}...' to '{node.content[:15]}...'")
        
        return new_node

    def add_edge(self, source: MemoryNode, target: MemoryNode, relation: str, weight: float = 1.0):
        edge = MemoryEdge(source.id, target.id, relation, weight)
        self.edges.append(edge)
