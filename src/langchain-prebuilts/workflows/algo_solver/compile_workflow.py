from typing import Any, TypedDict#, Optional, Sequence, Union
from langgraph.graph import StateGraph, END
#import agents
from util_funcs import format_feedback, save_graph_state
from langchain_core.runnables import RunnableLambda

# from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer


from langgraph import StateGraph, AgentNode, ToolNode, AgentState
from typing import TypedDict, Any
import faiss
import numpy as np



#Agent State
class AgentState(TypedDict):
    #core outputs#
    context:  str | None #dict[str, Any]
    messages: list[dict[str, Any]]
    routing: str
    search_results: list[str]

# Tools
class VectorSearchTool:
    def __init__(self, embeddings: np.ndarray, texts: list[str]):
        self.embeddings = embeddings.astype('float32')
        self.texts = texts
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(self.embeddings)

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> list[str]:
        query_embedding = query_embedding.astype('float32').reshape(1, -1)
        D, I = self.index.search(query_embedding, top_k)
        results = [self.texts[i] for i in I[0]]
        return results
    
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# model = SentenceTransformer("Qwen/Qwen3-Embedding-8B")
# query_embeddings = model.encode(queries, prompt_name="query")
# document_embeddings = model.encode(documents)

vector_tool = VectorSearchTool(query_embedding, vector_store)