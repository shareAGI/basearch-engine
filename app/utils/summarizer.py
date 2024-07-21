from typing import Tuple
from .agents.article_summarizer_agent import ArticleSummarizerAgent
from .agents.article_summarizer_short_agent import ArticleSummarizerShortAgent

def summarize(content: str, short: bool = False) -> Tuple[bool, str]:
    # breakpoint()
    if short:
        summary_agent = ArticleSummarizerShortAgent()
    else:
        summary_agent = ArticleSummarizerAgent()
    return summary_agent(content)
