import openai
from config import settings

def summarize_transcript(transcript: str, title: str) -> str:
    """
    Sends the transcript to MIMO API for summarization.
    """
    client = openai.OpenAI(
        api_key=settings.MIMO_API_KEY,
        base_url=settings.MIMO_API_BASE
    )

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
