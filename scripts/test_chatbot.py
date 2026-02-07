#!/usr/bin/env python3
"""
Test script for chatbot functionality
Run this to test the chatbot without UI
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag_engine import RAGEngine
from src.chatbot import ProfileChatbot
from config import settings


def test_chatbot():
    """Test chatbot with sample queries"""
    print("=" * 60)
    print("Chatbot Test Suite")
    print("=" * 60)
    
    # Load RAG engine
    print("\n📖 Loading RAG engine...")
    try:
        rag_engine = RAGEngine()
        rag_engine.load()
        print("✅ Vector store loaded")
    except Exception as e:
        print(f"❌ Error loading vector store: {str(e)}")
        print("\nRun setup_vectordb.py first!")
        sys.exit(1)
    
    # Initialize chatbot
    print("\n🤖 Initializing chatbot...")
    try:
        chatbot = ProfileChatbot(rag_engine)
        print(f"✅ Chatbot initialized with {settings.MODEL_NAME}")
    except Exception as e:
        print(f"❌ Error initializing chatbot: {str(e)}")
        sys.exit(1)
    
    # Test queries
    test_queries = [
        "Hello!",
        "Tell me about your experience with AI and machine learning",
        "What projects have you worked on?",
        "What are your technical skills?",
        "What is your educational background?",
        "Tell me about your experience at TCS",
        "What awards have you received?",
        "Thank you!"
    ]
    
    print("\n" + "=" * 60)
    print("Running Test Queries")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[Query {i}]")
        print(f"User: {query}")
        
        try:
            response = chatbot.chat(query)
            print(f"Bot: {response[:200]}..." if len(response) > 200 else f"Bot: {response}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("-" * 60)
    
    # Display conversation history
    print("\n" + "=" * 60)
    print("Conversation History Summary")
    print("=" * 60)
    history = chatbot.get_history()
    print(f"Total exchanges: {len(history) // 2}")
    print("=" * 60)


def interactive_test():
    """Interactive chatbot test"""
    print("=" * 60)
    print("Interactive Chatbot Test")
    print("=" * 60)
    
    # Load RAG engine
    print("\n📖 Loading RAG engine...")
    try:
        rag_engine = RAGEngine()
        rag_engine.load()
        print("✅ Vector store loaded")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
    
    # Initialize chatbot
    print("\n🤖 Initializing chatbot...")
    try:
        chatbot = ProfileChatbot(rag_engine)
        print(f"✅ Chatbot ready!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
    
    # Greeting
    greeting = chatbot.get_greeting()
    print(f"\nBot: {greeting}")
    
    print("\n" + "=" * 60)
    print("Type 'quit' or 'exit' to end the conversation")
    print("=" * 60)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            farewell = chatbot.get_farewell()
            print(f"\nBot: {farewell}")
            break
        
        if not user_input:
            continue
        
        try:
            response = chatbot.chat(user_input)
            print(f"\nBot: {response}")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


def main():
    """Main test function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test chatbot functionality")
    parser.add_argument(
        '--mode',
        choices=['auto', 'interactive'],
        default='auto',
        help='Test mode: auto (run predefined queries) or interactive (manual testing)'
    )
    
    args = parser.parse_args()
    
    if args.mode == 'auto':
        test_chatbot()
    else:
        interactive_test()


if __name__ == "__main__":
    main()