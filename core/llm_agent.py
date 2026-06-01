import openai
from config import settings

def chunk_text(text: str, chunk_size: int = 4000) -> list[str]:
    """Splits text into chunks of roughly `chunk_size` characters."""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def map_summarize(client: openai.OpenAI, chunk: str, index: int, total: int) -> str:
    """Extracts key information from a specific chunk of the transcript."""
    print(f"[{index}/{total}] Mapping chunk (length: {len(chunk)})...")
    prompt = f"""
    这是一段播客逐字稿的第 {index}/{total} 部分。请你提取出这部分内容中的核心事实、重要观点、有价值的金句以及提及的工具/书籍。
    请尽量保留原文中的重要细节和时间线索，这是为了后续汇总使用。请用简明扼要的条目列出：
    
    原始文本部分：
    {chunk}
    """
    response = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[
            {"role": "system", "content": "你是一个高效的信息提取器，负责从长片段中无损脱水出核心事实与金句。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

def reduce_summarize(client: openai.OpenAI, summaries: list[str], title: str) -> str:
    """Synthesizes all mapped summaries into the final structured markdown."""
    print("Reducing all chunked summaries into final output...")
    combined_summaries = "\n\n---\n\n".join([f"第 {i+1} 部分脱水摘要:\n{s}" for i, s in enumerate(summaries)])
    
    prompt = f"""
    这是一期名为《{title}》的播客的全部脱水摘要（由多个部分提取组合而成）。
    请你根据这些摘要，生成一份全局的、高质量的结构化播客总结。
    
    请严格按照以下格式输出 Markdown：
    
    ## 🎯 一句话核心
    (用一句话概括这期播客最核心的价值)

    ## ⏱️ 时间轴大纲
    (根据话题切换列出带有逻辑的大纲)

    ## 💎 关键金句与实体
    (提取出里面非常有洞察力的金句，以及提到的重要人物、书籍、工具等)

    ---
    以下是全篇脱水摘要：
    {combined_summaries}
    """
    response = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[
            {"role": "system", "content": "你是一个专业的播客总结专家，擅长全局把控，能将零散的摘要重组为结构严谨的大纲。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

def summarize_transcript(transcript: str, title: str) -> str:
    """
    Sends the transcript to MIMO API for summarization, using Map-Reduce if the text is too long.
    """
    client = openai.OpenAI(
        api_key=settings.MIMO_API_KEY,
        base_url=settings.MIMO_API_BASE
    )

    # Threshold for chunking
    MAX_LENGTH = 6000
    
    if len(transcript) <= MAX_LENGTH:
        print(f"Transcript length ({len(transcript)}) is within limit. Running single-pass summarization...")
        prompt = f"""
        这是一期名为《{title}》的播客逐字稿。请你作为专业的播客总结助手，根据以下文本生成一份高质量的结构化总结。

        请严格按照以下格式输出 Markdown：
        
        ## 🎯 一句话核心
        (用一句话概括这期播客最核心的价值)

        ## ⏱️ 时间轴大纲
        (根据话题切换列出带时间戳的大纲)

        ## 💎 关键金句与实体
        (提取出里面非常有洞察力的金句，以及提到的重要人物、书籍、工具等)

        ---
        以下是原始逐字稿：
        {transcript}
        """

        print("Sending request to MIMO API...")
        response = client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {"role": "system", "content": "你是一个专业的播客总结专家，擅长从冗长的对话中提取高密度知识。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    else:
        print(f"Transcript length ({len(transcript)}) exceeds limit. Starting Map-Reduce chunking...")
        chunks = chunk_text(transcript, chunk_size=4000)
        total_chunks = len(chunks)
        mapped_summaries = []
        
        for i, chunk in enumerate(chunks):
            # Process sequentially to avoid hitting API rate limits
            summary = map_summarize(client, chunk, i+1, total_chunks)
            mapped_summaries.append(summary)
            
        final_result = reduce_summarize(client, mapped_summaries, title)
        return final_result
