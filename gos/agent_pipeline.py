import json
import os
import sys
import datetime
import urllib.request
import ssl
import xml.etree.ElementTree as ET

# Ensure utf-8 stdout for Windows console
sys.stdout.reconfigure(encoding='utf-8')

STORE_FILE = "mentor_store.js"
USER_STATE_FILE = "mentor_user_state.json"
DATA_FILE = "mentor_data.json"

# 52-Week Industry & AI Research Curriculum
CURRICULUM = {
    1: {
        "title": "Week 1: Python Foundations & Git Version Control",
        "focus": "Product Engineering & Software Foundations (FAANG Benchmark)",
        "query": "cat:cs.CL+OR+cat:cs.AI",
        "youtube": [
            {
                "title": "CS50’s Introduction to Programming with Python",
                "url": "https://www.youtube.com/watch?v=nLRL_NcnK-4",
                "duration": "16 Hours",
                "channel": "Harvard CS50 / freeCodeCamp",
                "why_watch": "Gold standard Python introduction covering functions, variables, and conditionals."
            },
            {
                "title": "Git and GitHub for Beginners - Full Course",
                "url": "https://www.youtube.com/watch?v=RGOj5yH7evE",
                "duration": "1 Hour",
                "channel": "freeCodeCamp",
                "why_watch": "Learn how top engineering teams manage repositories, commits, and PRs."
            }
        ],
        "goals": [
            {"id": "w1_1", "category": "tech", "text": "Setup Developer Environment: VS Code + Python 3.12 + Git + GitHub SSH Keys", "difficulty": "Beginner", "impact": "Essential dev infrastructure for all software engineering"},
            {"id": "w1_2", "category": "tech", "text": "Complete CS50P Lecture 0 & 1 (Functions, Variables, Conditionals)", "difficulty": "Beginner", "impact": "Core computational thinking for coding interviews"},
            {"id": "w1_3", "category": "tech", "text": "Build & push first Python CLI script to GitHub with clean README", "difficulty": "Intermediate", "impact": "Demonstrates real version control habits from Year 1"},
            {"id": "w1_4", "category": "research", "text": "Read Jay Alammar's 'Illustrated Transformer' visual guide", "difficulty": "Intermediate", "impact": "Grasp intuition behind modern LLMs (ChatGPT, Gemini)"},
            {"id": "w1_5", "category": "fitness", "text": "30-min daily brisk walk + 20 pushups (Hostel Health Protocol)", "difficulty": "Beginner", "impact": "Maintains physical energy for long coding sessions"},
            {"id": "w1_6", "category": "finance", "text": "Track all hostel expenditures daily in budget spreadsheet", "difficulty": "Beginner", "impact": "Financial discipline & money management"}
        ]
    },
    2: {
        "title": "Week 2: Data Structures & Computational Complexity (Big-O)",
        "focus": "Algorithm Foundations & Code Efficiency",
        "query": "cat:cs.DS+OR+cat:cs.AI",
        "youtube": [
            {
                "title": "Data Structures and Algorithms for Beginners",
                "url": "https://www.youtube.com/watch?v=8hly31xKLI0",
                "duration": "5 Hours",
                "channel": "freeCodeCamp",
                "why_watch": "Essential breakdown of Arrays, Linked Lists, and Big-O notation."
            }
        ],
        "goals": [
            {"id": "w2_1", "category": "tech", "text": "Implement Linear Search & Binary Search from scratch in Python", "difficulty": "Beginner", "impact": "Foundational algorithmic thinking for DSA interviews"},
            {"id": "w2_2", "category": "tech", "text": "Solve 3 LeetCode Easy array problems (Two Sum, Contains Duplicate)", "difficulty": "Intermediate", "impact": "Build problem-solving confidence early"},
            {"id": "w2_3", "category": "research", "text": "Read Paper Summary: 'ResNet - Deep Residual Learning for Image Recognition'", "difficulty": "Intermediate", "impact": "Understand skip connections in deep neural networks"}
        ]
    }
}

def fetch_arxiv_papers(query="cat:cs.CL+OR+cat:cs.AI", max_results=2):
    """Fetch live AI research papers from arXiv API safely."""
    papers = []
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        url = f"https://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
        req = urllib.request.urlopen(url, context=ctx, timeout=8)
        xml_data = req.read()
        root = ET.fromstring(xml_data)
        
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            arxiv_id = entry.find('atom:id', ns).text.split('/abs/')[-1]
            summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')[:180] + "..."
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            summary_url = f"https://arxiv.org/abs/{arxiv_id}"
            
            papers.append({
                "title": title,
                "arxiv_id": arxiv_id,
                "pdf_url": pdf_url,
                "summary_url": summary_url,
                "key_takeaway": summary,
                "reading_guideline": "Read the abstract & conclusion to spot emerging AI trends."
            })
    except Exception as e:
        print(f"[!] arXiv API fetch warning: {e}. Using fallback paper curated list.")
        papers = [{
            "title": "Attention Is All You Need (Vaswani et al., 2017)",
            "arxiv_id": "1706.03762",
            "pdf_url": "https://arxiv.org/pdf/1706.03762.pdf",
            "summary_url": "https://jalammar.github.io/illustrated-transformer/",
            "key_takeaway": "Introduced Transformers - the foundational architecture behind modern AI & LLMs.",
            "reading_guideline": "Read Jay Alammar's Illustrated Transformer visual guide!"
        }]
    return papers

def run_agent_pipeline():
    print("[+] Running AI Mentor Agent Pipeline & Research Engine...")

    # 1. Read User State from Local JSON files
    user_state = {}
    if os.path.exists(USER_STATE_FILE):
        try:
            with open(USER_STATE_FILE, "r", encoding="utf-8") as f:
                user_state = json.load(f)
        except Exception:
            pass
    elif os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                user_state = json.load(f)
        except Exception:
            pass

    completed_goals = user_state.get("completed_goals", {})
    reflection = user_state.get("reflection_notes", "")
    week_num = user_state.get("week_num", 1)

    print(f"[+] Student Progress Analysis: Week {week_num} | Completed {sum(1 for v in completed_goals.values() if v)} goals.")
    if reflection:
        print(f"[+] Student Reflection: '{reflection}'")

    # Get curriculum for week
    curr = CURRICULUM.get(week_num, CURRICULUM[1])

    # 2. Live Research: Fetch ArXiv Papers
    print("[+] Performing live AI paper research via arXiv API...")
    papers = fetch_arxiv_papers(query=curr.get("query", "cat:cs.AI"), max_results=2)

    # 3. Process Goals (Carry over uncompleted tasks + Add new curriculum tasks)
    processed_goals = []
    for g in curr["goals"]:
        is_done = completed_goals.get(g["id"], False)
        processed_goals.append({
            "id": g["id"],
            "category": g["category"],
            "text": g["text"],
            "difficulty": g["difficulty"],
            "impact": g["impact"],
            "done": is_done
        })

    # Add adaptive warmup goal if student left reflection notes or missed tasks
    uncompleted_count = sum(1 for g in processed_goals if not g["done"])
    if uncompleted_count > 2 and reflection:
        processed_goals.insert(0, {
            "id": f"adaptive_recovery_{week_num}",
            "category": "mindset",
            "text": f"Agent Recovery Focus: Spend 20 mins reviewing missed topics based on notes: '{reflection[:40]}...'",
            "difficulty": "Beginner",
            "impact": "Prevents backlog accumulation and resets momentum",
            "done": False
        })

    # 4. Generate Mentor Assessment & Insights
    done_count = sum(1 for g in processed_goals if g["done"])
    total_count = len(processed_goals)
    
    assessment = (
        f"Week {week_num} Assessment: You have completed {done_count} out of {total_count} goals. "
        f"{'Great momentum! Keep shipping code daily.' if done_count >= 3 else 'Focus on finishing 1 small coding task today to build momentum.'}"
    )

    insights = [
        "Product Engineering Benchmark: FAANG & top AI startups evaluate candidates on Git cleanliness and basic Data Structures in Year 1.",
        "AI Trend: Reading 1 research paper abstract weekly builds technical depth that sets you apart from 99% of engineering students."
    ]

    warnings = [
        "Hostel Discipline: Do not sacrifice sleep for late-night gaming before 9 AM lectures.",
        "Coding Rule: Write code on VS Code daily — reading tutorials without coding yields zero skill growth."
    ]

    # 5. Build Complete Store Object
    store_payload = {
        "week_key": f"2026-08-10_w{week_num}",
        "week_title": curr["title"],
        "industry_focus": curr["focus"],
        "generated_at": datetime.datetime.now().isoformat(),
        "weekly_goals": processed_goals,
        "curated_resources": {
            "youtube_videos": curr["youtube"],
            "research_papers": papers
        },
        "report": {
            "overall_assessment": assessment,
            "industry_insights": insights,
            "warnings": warnings
        }
    }

    # Write mentor_store.js
    js_content = f"// Auto-generated by AI Agent Research Pipeline\nwindow.MENTOR_STORE = {json.dumps(store_payload, indent=2)};\n"
    with open(STORE_FILE, "w", encoding="utf-8") as f:
        f.write(js_content)

    # Update mentor_goals.json & mentor_report.json
    with open("mentor_goals.json", "w", encoding="utf-8") as f:
        json.dump(store_payload, f, indent=2)

    with open("mentor_report.json", "w", encoding="utf-8") as f:
        json.dump(store_payload["report"], f, indent=2)

    print("[+] Success: AI Agent Research Pipeline updated mentor_store.js, mentor_goals.json & mentor_report.json!")

if __name__ == "__main__":
    run_agent_pipeline()
