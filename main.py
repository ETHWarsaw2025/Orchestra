#!/usr/bin/env python3
"""
Golem-Powered Blockchain Audio Aggregator

This system aggregates blockchain data using Golem, analyzes it, and generates 
musical patterns in the Strudel language based on the analyzed data.

Data Flow:
Orchestra Table (Golem) -> Blockchain Data Retrieval -> Blockchain Data Storage (Golem) 
-> Data Analysis -> Strudel Audio Track Generation -> Strudel Audio Table (Golem)
"""

import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from orchestrator import BlockchainAudioOrchestrator

# Load environment variables
load_dotenv()

async def main():
    """Main function to run the complete pipeline"""
    print("🎵 Golem-Powered Blockchain Audio Aggregator")
    print("=" * 50)
    
    # Initialize the orchestrator
    orchestrator = BlockchainAudioOrchestrator()
    
    try:
        # Run the complete pipeline
        await orchestrator.run_pipeline()
        print("✅ Pipeline completed successfully!")
        
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())


