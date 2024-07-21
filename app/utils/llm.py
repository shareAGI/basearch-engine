from openai import OpenAI
from app.core.config import settings

API_KEY = settings.OPENAI_API_KEY
BASE_URL = settings.OPENAI_BASE_URL
LLM_MODEL = settings.OPENAI_LLM_MODEL

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def get_llm_output(
    input_text: str, 
    system_prompt: str = "You are a helpful assistant",
    model_name: str = LLM_MODEL, 
    temperature: float = 1.0,
    max_tokens: int = 4096,
    **kwargs
) -> str:
    """
    Get output from LLM.

    :param input_text: The text input to LLM.
    :param system_prompt: The system prompt to guide the LLM.
    :param model_name: Model name, such as 'deepseek-chat'.
    :param temperature: Temperature of generation.
    :param max_tokens: Maximum number of tokens.
    :return: The output text from LLM.
    """
    if not input_text:
        raise ValueError("Input text cannot be empty")
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_text}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False,
        )
        
        output_text = response.choices[0].message.content
        return output_text
    
    except Exception as e:
        raise RuntimeError(f"Failed to get LLM output: {e}")
