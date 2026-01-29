# api/compare.py
"""
Comparison logic wrapper for the Laptop Battle API.
Runs pipeline for two laptops and determines the winner.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline import LaptopAnalysisPipeline


def run_single_analysis(laptop_name: str) -> Dict[str, Any]:
    """
    Run the full pipeline for a single laptop.
    
    Args:
        laptop_name: Name of the laptop to analyze
        
    Returns:
        Analysis result dictionary
    """
    try:
        pipeline = LaptopAnalysisPipeline(laptop_name)
        results = pipeline.run_full_pipeline(
            force_refresh_search=False,  # Use cached if available
            scrape_delay=1.5,
            skip_chromadb=False,
            skip_llm=False
        )
        
        analysis = results.get("analysis", {})
        
        return {
            "laptop_name": laptop_name,
            "sentiment_score": analysis.get("sentiment_score", 0),
            "pros": analysis.get("pros", []),
            "cons": analysis.get("cons", []),
            "key_themes": analysis.get("key_themes", []),
            "sentiment_explanation": analysis.get("sentiment_explanation", ""),
            "user_recommendation": analysis.get("user_recommendation", ""),
            "posts_analyzed": results.get("unique_urls", 0),
            "error": analysis.get("error", None)
        }
    except Exception as e:
        return {
            "laptop_name": laptop_name,
            "sentiment_score": 0,
            "pros": [],
            "cons": [],
            "key_themes": [],
            "sentiment_explanation": "",
            "user_recommendation": "",
            "posts_analyzed": 0,
            "error": str(e)
        }


async def compare_laptops(laptop1: str, laptop2: str) -> Dict[str, Any]:
    """
    Compare two laptops by running analysis pipeline for both.
    
    Args:
        laptop1: First laptop name
        laptop2: Second laptop name
        
    Returns:
        Comparison result with both analyses and winner
    """
    # Run both analyses in parallel using ThreadPoolExecutor
    loop = asyncio.get_event_loop()
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        # Submit both tasks
        future1 = loop.run_in_executor(executor, run_single_analysis, laptop1)
        future2 = loop.run_in_executor(executor, run_single_analysis, laptop2)
        
        # Wait for both to complete
        analysis1, analysis2 = await asyncio.gather(future1, future2)
    
    # Determine winner
    score1 = analysis1.get("sentiment_score", 0) or 0
    score2 = analysis2.get("sentiment_score", 0) or 0
    
    if score1 > score2:
        winner = "laptop1"
    elif score2 > score1:
        winner = "laptop2"
    else:
        winner = "tie"
    
    return {
        "laptop1": analysis1,
        "laptop2": analysis2,
        "winner": winner,
        "score_difference": abs(score1 - score2)
    }


def compare_laptops_sync(laptop1: str, laptop2: str) -> Dict[str, Any]:
    """
    Synchronous version of compare_laptops for testing.
    """
    analysis1 = run_single_analysis(laptop1)
    analysis2 = run_single_analysis(laptop2)
    
    score1 = analysis1.get("sentiment_score", 0) or 0
    score2 = analysis2.get("sentiment_score", 0) or 0
    
    if score1 > score2:
        winner = "laptop1"
    elif score2 > score1:
        winner = "laptop2"
    else:
        winner = "tie"
    
    return {
        "laptop1": analysis1,
        "laptop2": analysis2,
        "winner": winner,
        "score_difference": abs(score1 - score2)
    }


if __name__ == "__main__":
    # Test comparison
    result = compare_laptops_sync("Lenovo Legion Y540", "MacBook M4 Pro")
    print(f"Winner: {result['winner']}")
    print(f"Score difference: {result['score_difference']}")
