"""
This module initializes and creates a new vector store from a `.docx` file.

Note:
- This script is intended to be run **only once** to create a fresh vector store.
- For adding or updating information in an existing vector store,
  use `update_vector_store.py` instead.
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from typing import List, Dict, Optional, Any
from langchain_core.documents import Document
import tiktoken
import torch

from config import settings

def app_document_loader(file_name: str):
    """
    Load and parse a Word document using the UnstructuredWordDocumentLoader.
    This function accepts a `.doc` file path and leverages the
    `UnstructuredWordDocumentLoader` to extract and structure the document
    content for downstream processing (e.g., text chunking, embedding,
    and vector store ingestion).

    Args:
        file_path (str): Absolute or relative path to the `.doc` file.

    Returns:
        List[Document]: A list of LangChain `Document` objects containing
        the extracted and structured text.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        ValueError: If the provided file is not a valid `.doc` file.
    """

    # Reading .docx file using UnstructuredWordDocumentLoader
    # Use mode="elements" to see the individual paragraph formatting
    file_loader = UnstructuredWordDocumentLoader(
        file_path=file_name,
        mode= "elements",
        strategy = "high_res",
        # strategy = "fast",
    )
    
    return file_loader.load()

# Handler function to get token size
def get_token_count(text: str) -> int:
    # 'cl100k_base' is the standard for modern embedding models
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    return len(tokens)  

# Enrichment to Metadata for efficient chunk retrieval
def chunk_and_enrich_hierarchy(elements: List[Document]):
    """
    Pass 1: Corrects categories based on visual formatting (bold/caps/numbered).
    Pass 2: Creates Contexual hierarchy Title -> Header -> Subheader.
    Pass 3: Combine Smaller but related chunks of same hierarchy
    Pass 4: Flattens the document into contextualized chunks with metadata inheritance
    """
    final_chunks = []
    sections = {}

    # Creating Text text_splitter for document chunking
    chunk_size = settings.CHUNK_WARNING_THRESHOLD
    chunk_overlap = settings.CHUNK_OVERLAP_SIZE

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,       
        chunk_overlap=chunk_overlap,     
        length_function=get_token_count,  # Or use 'len' for simplification
        is_separator_regex=False,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
 
    # State tracking for the hierarchy
    current_title = "Unknown Title"
    current_header = ""
    current_subheader = ""

    for el in elements:
        text = el.page_content.strip()
        if not text:
            continue
            
        # --- PASS 1: CATEGORY CORRECTION ---
        category = el.metadata.get("category")
        
        # Identify visual cues for misclassified headers
        # emphasized_text_contents usually catches bold runs from Unstructured
        is_bold = el.metadata.get("emphasized_text_contents") == [text]
        is_all_caps = text.isupper() and len(text) > 3
        is_numbered = text[0].isdigit() if len(text) > 0 else False

        # Apply Correction Logic
        if category != "Title":
            # All caps with numbers often acts as a Header
            if is_bold or (is_all_caps and is_numbered):
                category = "Header"

            # All caps without numbers often acts as a Subheader
            elif is_all_caps: 
                category = "Subheader"
        
        # --- PASS 2: HIERARCHY TRACKING & CHUNKING ---
        current_source = el.metadata.get('filename', 'Unknown Source')

        if category == "Title":
            current_title = text.strip()
            # Reset levels below
            current_header, current_subheader = "" , ""     

        elif category == "Header":
            current_header = text.strip()
            current_subheader = ""   # Reset levels below

        elif category == "Subheader":
            current_subheader = text.strip()

        # --- 3. Combine Smaller but related chunks of same hierarchy ---
        else:
            path = (current_source, current_title, current_header, current_subheader)
            if path not in sections:
                sections[path] = []
            sections[path].append(text)

    # --- 4. Creating contextualized chunks with metadata inheritance ---
    for path, full_text in sections.items():
        source, title, head, sub = path
        # Join all paragraphs in this section with double newlines
        full_section_text = "\n\n".join(full_text)

        if len(full_section_text) < chunk_size: 
            sub_chunks = [full_section_text]
        else:
            # Only use the overlap splitter for long paragraphs
            sub_chunks = text_splitter.split_text(full_section_text)

        for chunk in sub_chunks:
            # Create the 'Context Path' for LLM to see
            full_content = (
                f"Source: {source} > Context: {title} > Section: {head} > Sub-Section: {sub}\n"
                f"Content: {chunk}"
            )
    
            # Audit the token count
            token_size = get_token_count(full_content)

            # Create enriched Metadata
            enriched_doc = Document(
                page_content=full_content,
                metadata={
                    "title": title,
                    "header": head,
                    "subheader": sub,
                    "source": source,
                    "original_category": el.metadata.get("category"),
                    "tokens": token_size,
                }
            )
            final_chunks.append(enriched_doc)
            
    return final_chunks

# Creating Embeddings for Vector Store
# Setting Up nomic-embedding
class NomicEmbedding(HuggingFaceEmbeddings):
    def __init__(self,
                 model_name: str,
                #  model_dim: str,
                 model_kwargs: Dict[str, Any],
                 encode_kwargs: Dict[str, Any],
                 **kwargs,
                 ):
        # 1. Update hardware device in model_kwargs before passing to super
        if torch.backends.mps.is_available():
            target_device = "mps"
        elif torch.cuda.is_available():
            target_device = "cuda"
        else:
            target_device = "cpu"
            
        model_kwargs['device'] = target_device

        # 2. Call the parent constructor properly
        super().__init__(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
            **kwargs
        )
        
        print(f"✅ Success: NomicEmbedding initialized on [{target_device.upper()}]")

       
    def embed_query(self, text: str):
        query = f"search_query: {text}"
        return super().embed_query(query)
    
    def embed_documents(self, texts: List[str]):
        docs = [f"search_document: {text}" for text in texts]
        return super().embed_documents(docs)
    
    @classmethod
    def create_embedding(cls, 
                         model_name: Optional[str] = None, 
                         model_kwargs: Optional[Dict] = None, 
                         encode_kwargs: Optional[Dict] = None,
                         **kwargs):
        """
        Static factory method to build the embedder using global settings.
        Call this directly on the Class, not on an instance.
        """
        return cls(
            model_name=model_name,
            model_kwargs=model_kwargs or {'trust_remote_code': True},
            encode_kwargs=encode_kwargs or {"normalize_embeddings": True},
            **kwargs
        )

def main():
    file_name = settings.RESUME_FILE
    file_data = app_document_loader(file_name)

    enriched_chunks = chunk_and_enrich_hierarchy(file_data.copy())

    app_embeddings = NomicEmbedding.create_embedding(
        model_name=settings.EMBEDDING_MODEL,
        model_kwargs={'trust_remote_code': True, 'revision': 'main'},
        encode_kwargs={"normalize_embeddings": False,},
        show_progress=True,
    )

    # Creating Vector Store using FAISS
    app_vectorstore = FAISS.from_documents(enriched_chunks, app_embeddings)

    # Saving Vector Store for local Use
    vector_store_path = settings.VECTOR_STORE_PATH
    app_vectorstore.save_local(folder_path= vector_store_path)

if __name__ == "__main__":
    main()