import os
import re
from config import settings

def save_to_obsidian(title: str, summary: str, transcript: str):
    """
    Saves the summary and transcript into a Markdown file in the Obsidian Knowledge-Base.
    """
    # Sanitize title for filename
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    filename = f"{safe_title}.md"
    filepath = os.path.join(settings.KNOWLEDGE_BASE_DIR, filename)

    content = f"{summary}\n\n## 📝 完整逐字稿\n\n```text\n{transcript}\n```\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Saved to Obsidian: {filepath}")
    return filepath
