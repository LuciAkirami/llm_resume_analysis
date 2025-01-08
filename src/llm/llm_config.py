from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm():
    """
    Returns a LangChain LLM Runnable
    """
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
