# laptop-ai
# Reddit Scraping Attempts – Summary

## Goal
Attempt to extract data from Reddit posts, preferably via the `.json` endpoint, using Python in Google Colab.

---

## Initial Approach: requests + `.json`

### Method
- Used Python `requests`
- Added `User-Agent` and `Accept: application/json`
- Attempted to access:
https://www.reddit.com/r/.../.json
https://old.reddit.com/r/.../.json



### Result
- All requests returned **HTTP 403**
- Response body was HTML (block page), not JSON
- `.json()` raised `JSONDecodeError`

### Conclusion
Reddit blocks unauthenticated access to `.json` endpoints, especially from cloud IPs (Google Colab).

---

## Debugging Steps Taken
- Printed status codes and response text
- Checked for valid JSON before parsing
- Added delays between requests
- Switched to `old.reddit.com`
- Verified headers were correct

### Outcome
No change — consistent 403 responses.

---

## BeautifulSoup Evaluation

### Findings
- BeautifulSoup only parses HTML
- Reddit pages are JavaScript-heavy
- HTML scraping is fragile and unreliable

### Conclusion
BeautifulSoup is not suitable for Reddit scraping.

---

## PRAW (Python Reddit API Wrapper)

### Method
- Created Reddit app
- Installed and configured PRAW
- Attempted read-only access

### Result
- Reddit denied API access approval
- PRAW unusable without authorization

---

## Current Understanding

- Reddit `.json` endpoints are:
- Undocumented
- Actively restricted
- Not intended for public scraping

- Reddit uses:
- IP reputation
- Cloudflare
- Bot detection
- OAuth enforcement

---

## Alternative Technologies Considered

### Selenium / Playwright
- Can render Reddit pages
- Can scrape visible HTML
- Cannot access `.json` endpoints
- May still be blocked by IP reputation

### steel.dev
- Provides hosted browser automation
- Uses residential IPs
- Useful for HTML scraping
- Does NOT unlock Reddit JSON APIs

---

## Final Conclusion

There is no reliable, unauthenticated way to access Reddit `.json` endpoints in 2025+.

Possible paths forward:
- Use Playwright/Selenium to scrape rendered HTML
- Use officially approved Reddit API access
- Choose alternative platforms for scraping practice

## Problems above fixed using vs code instead of google colab
# Reddit subreddit scraping
Using beautifulsoup and requests I am able to scrape the frontpage of subreddits from a hardcoded list.  


## Scraping Strategy Update – Search-Based Reddit Scraping

### Problem
Scraping subreddit homepages does not return results for:
- old laptop models (e.g. Lenovo Legion Y540)
- low-activity topics
- historical discussions

### Root Cause
Subreddit front pages only show:
- hot
- trending
- recent posts

Older content is not linked.

### Solution
Switch from:
❌ Subreddit browsing  
to  
✅ Reddit search-based scraping

### Approach
1. Define search keywords (e.g. "lenovo legion y540")
2. Generate Reddit search URLs
3. Scrape post results instead of homepage content
4. Extract:
   - post title
   - post URL
   - subreddit
   - scrape timestamp

### Example Search URL
https://www.reddit.com/r/LenovoLegion/search/?q=y540&restrict_sr=1

### Benefits
- Finds older posts
- Higher relevance
- Matches user-driven laptop search UX
- Scales to any laptop model

### Next Steps
- Implement search-based scraper
- Save results as Markdown
- Embed into ChromaDB for LLM context


User types laptop name
↓
Search-based Reddit scraping
↓
Structured results
↓
Markdown files
↓
ChromaDB
↓
LLM context



## Reddit Search-Based Scraper

### Motivation
Scraping subreddit front pages does not surface:
- old laptop models
- niche issues
- historical discussions

### Solution
Use Reddit’s global search pages to scrape posts based on keywords.

### How It Works
1. Define search queries (e.g. "lenovo legion y540")
2. Generate Reddit search URLs
3. Fetch search result pages
4. Extract post titles and comment URLs
5. Save results to JSON and CSV

### Example Search URL

https://www.reddit.com/search/?q=lenovo+legion+y540


### Benefits
- Finds old and rare posts
- High relevance
- User-input driven
- Matches Laptop AI app flow

### Limitations
- Reddit is JS-heavy
- Requests-based scraping may break
- Playwright / Steel is the long-term solution




## Bug Fix – Reddit Search Scraper Invalid URL

### Problem
Running the search-based Reddit scraper resulted in:


### Root Cause
`requests.get()` was mistakenly called with:
- the raw search query string  
instead of:
- the constructed Reddit search URL

### Fix
Ensure `requests.get()` always receives the full URL:

```python
search_url = "https://www.reddit.com/search/?q=" + encoded_query
requests.get(search_url)



### Reddit link scraper --> reddit post scraper --> LLM 
I have a pipeline that first scrapes/finds the relevant reddit posts, then a separate scraper gets data from that post, then i  

[ Reddit Posts ]
        |
        v
[ Scraper ]
        |
        v
[ Structured Python dict ]
        |
        +--> [ Markdown Files (.md) ]  ← human / GitHub
        |
        +--> [ Embeddings ] → [ ChromaDB ] ← LLM context






## Stage 3 — Knowledge Storage

At this stage, the project transitions from raw data scraping to structured, persistent knowledge storage.

### Goals
- Convert scraped Reddit post content into human-readable Markdown files
- Store semantic embeddings in ChromaDB for future LLM retrieval

---

### Markdown Knowledge Base

Each scraped Reddit post is converted into a `.md` file with metadata:

- Source URL
- Scrape timestamp
- Clean post body text

This allows:
- Easy inspection and debugging
- GitHub version control
- Reuse across multiple stages (LLM, comparisons, frontend)

Each post is saved as: knowledge/reddit/<post-title-slug>.md


---

### ChromaDB Vector Storage

To enable semantic search and LLM grounding, each Markdown document is embedded and stored in ChromaDB.

ChromaDB runs locally and provides:
- Vector similarity search
- Persistent memory
- Scalable context retrieval for LLM prompts

Embeddings are generated using:
- `sentence-transformers/all-MiniLM-L6-v2`

Stored data includes:
- Document text
- Source metadata
- Unique IDs based on file paths

---

### Why ChromaDB?

Using ChromaDB allows the application to:
- Avoid sending all scraped text to the LLM
- Retrieve only relevant knowledge per query
- Reduce hallucinations
- Scale to many laptops and comparisons

This is a critical foundation for future features:
- Pros/cons extraction
- Laptop comparisons
- YouTube transcript integration
- Cached LLM outputs per comparison slug

---

### Status
✔ Reddit scraping complete  
✔ Markdown knowledge generation complete  
✔ Vector storage implemented  
⬜ LLM summarization (next stage)  
⬜ Frontend integration  





User Query
   |
   v
Reddit Search Scraper
   |
   v
List of Post URLs
   |
   v
Reddit Post Scraper
   |
   v
Structured Dict
   |
   v
Markdown Generator
   |
   v
.md Knowledge Files
   |
   v
ChromaDB Embeddings


## Markdown Knowledge Generation

This module converts scraped Reddit post data into persistent Markdown knowledge files.

### Input
A Python dictionary returned by the Reddit post scraper:
```python
{
  "url": str,
  "title": str,
  "body": str,
  "comments": list,
  "scraped_at": str
}

Output

A Markdown file stored at:
knowledge/reddit/<slugified-title>.md



## Stage 3 — Vector Knowledge Storage (ChromaDB)

Scraped Reddit content is converted into Markdown and embedded into a local ChromaDB vector store.

### Purpose
- Enable semantic search over scraped laptop knowledge
- Provide grounded context for LLM analysis
- Avoid hallucinations and token overload

### Implementation
- SentenceTransformer embeddings (`all-MiniLM-L6-v2`)
- Persistent local storage (`./chroma`)
- One document per Markdown file

Stored data includes:
- Vector embeddings
- Original text
- Source metadata

---

## Stage 4 — LLM Analysis (Completed)

### Description
This stage uses Google Gemini to analyze Reddit knowledge stored in ChromaDB.

### Workflow
1. Query ChromaDB for laptop-relevant Reddit content
2. Provide retrieved context to Gemini
3. Extract:
   - Pros
   - Cons
   - Sentiment score (1–100)

### Output
Structured JSON suitable for:
- Laptop comparison
- Frontend rendering
- Scoring logic

This completes the AI reasoning layer of the project.

