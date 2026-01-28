# Laptop AI Project – Architecture & Execution Plan

## Goal
Build an AI system that:
- Scrapes Reddit laptop discussions
- Extracts pros & cons
- Scores laptops (1–100)
- Compares two laptops
- Supports YouTube review scoring

---

## Current Progress
✅ Reddit search-based scraper  
✅ Extracts relevant post URLs  
✅### Stage 2 — Extract Post Content
✅ Scrape post title
✅ Scrape post body
- Scrape top comments
✅ Convert scraped content into `.md`
✅ Store embeddings in ChromaDB

---

## System Pipeline

### Stage 1 — Discover Posts
- Reddit search scraper
- Finds relevant post links

### Stage 2 — Extract Post Content
- Scrape post title
- Scrape post body
- Scrape top comments

### Stage 3 — Knowledge Storage
- Convert scraped content into `.md`
- Store embeddings in ChromaDB

### Stage 4 — LLM Analysis
- Extract pros
- Extract cons
- Generate sentiment score (1–100)

### Stage 5 — Comparison Engine
- Compare two laptops
- Output pros/cons differences
- Generate recommendation

### Stage 6 — Frontend
- User inputs laptop names
- Displays ratings, summaries, and comparison

---

## 2-Day Execution Plan

### Day 1
- Build Reddit post content scraper
- Generate `.md` files per laptop
- Run LLM pros/cons extractor
- Store in ChromaDB

### Day 2
- Build FastAPI backend
- Add laptop search endpoint
- Add two-laptop comparison mode
- Build simple frontend UI
- Bonus: YouTube transcript scoring

---

## Long-Term Extensions
- YouTube transcript review scoring
- Performance benchmark graphs
- More data sources (LaptopMedia, forums)

---

## Project Vision
AI-powered laptop research and comparison assistant
