from app.utils.agents import BaseAgent
from app.utils import get_llm_output

class ArticleSummarizerShortAgent(BaseAgent):
    def __init__(self, model_name: str = None):
        super().__init__()
        self.agent_name = "ArticleSummarizerShortAgent"
        self.agent_desc = "Summarize article within 30 words"
        self.model = get_llm_output
        
        instruction = (
            "1. Summarize the article content within 30 words."
            "2. Ignore any text not related to the topic of this article. "
            "3. The summary must be in the language type of the article. "
            "\nArticle content: {input}\n\n(just give summary, no any other text)"
        )
        self.agent_llm_config = {
            "instruction": instruction,
            "temperature": 0.7,
            "max_tokens": 60,
        }
        
    def generate_summary(self, article_content: str) -> str:
        input_text = self.agent_llm_config["instruction"].format(input=article_content)
        return self.model(
            input_text,
            **self.agent_llm_config,
        )
    
    def run(self, text: str) -> str:
        return self.generate_summary(text)
    