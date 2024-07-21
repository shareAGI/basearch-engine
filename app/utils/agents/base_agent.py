from typing import Any, Dict, Tuple, TypedDict
import logging
import uuid
from enum import Enum
from time import time

# Initialize the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    FREE = "free"
    RUNNING = "running"
    FINISHED = "finished"
    FAILED = "failed"

class LLMConfig(TypedDict, total=False):
    model_name: str
    instruction: str
    system_prompt: str
    temperature: float
    max_tokens: int
    top_k: int
    top_p: float

class BaseAgent:
    def __init__(self):
        self.agent_id: str = str(uuid.uuid4())
        self.agent_name: str = None
        self.agent_desc: str = None
        self.agent_status: AgentStatus = AgentStatus.FREE
        self.agent_llm_config: LLMConfig = None
        
    def run(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("You should implement this method.")
    
    def stop(self):
        raise NotImplementedError("You should implement this method.")
    
    def get_id(self) -> str:
        return self.agent_id
    
    def get_name(self) -> str:
        return self.agent_name
    
    def get_desc(self) -> str:
        return self.agent_desc
    
    def get_status(self) -> AgentStatus:
        return self.agent_status
    
    def get_info(self) -> Dict[str, Any]:
        return {
            "id": self.agent_id,
            "name": self.agent_name,
            "desc": self.agent_desc,
            "status": self.agent_status.value,
            "llm_config": self.agent_llm_config,
        }
    
    def __call__(self, *args: Any, **kwargs: Any) -> Tuple[bool, Any]:
        logger.info("##########################")
        logger.info(f"Agent {self.agent_name} is called.")
        logger.info("##########################")
        self.agent_status = AgentStatus.RUNNING
        
        try:
            logger.info(f"Agent {self.agent_name} id {self.agent_id} is running...")
            time_start = time()
            agent_out = self.run(*args, **kwargs)
            self.agent_status = AgentStatus.FINISHED
        except Exception as e:
            logger.info("##########################")
            logger.error(f"Agent {self.agent_name} has failed, id: {self.agent_id}. Error: {e}", exc_info=True)
            logger.info("##########################")
            agent_out = None
            self.agent_status = AgentStatus.FAILED
        
        logger.info("##########################")
        time_stop = time()
        logger.info(f"Agent {self.agent_name} has finished. Time: {(time_stop - time_start):0.2f}s")
        logger.info("##########################")
        
        if agent_out is None:
            return False, agent_out
        
        return True, agent_out
    
    def __str__(self) -> str:
        return f"Agent info: {self.get_info()}"
