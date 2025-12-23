import os
import sys
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field, ConfigDict
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from logger.logging import logger
from exception.exception_handling import CustomException

# Load environment variables at module level
load_dotenv()

class ConfigLoader:
    def __init__(self):
        logger.info("Loading configuration...")
        self.config = load_config()
    
    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    model_provider: Literal["groq", "groq2", "openai"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    def load_llm(self):
        """
        Load and return the LLM model.
        """
        try:
            logger.info("Starting LLM loading process...")
            logger.info(f"Loading model from provider: {self.model_provider}")
            
            if self.model_provider in ["groq", "groq2"]:
                logger.info(f"Loading LLM from {self.model_provider.upper()}")
                groq_api_key = os.getenv("GROQ_API_KEY")
                if not groq_api_key:
                    raise ValueError("GROQ_API_KEY not found in environment variables")
                
                model_name = self.config["llm"][self.model_provider]["model_name"]
                logger.info(f"Using model: {model_name}")
                return ChatGroq(model=model_name, api_key=groq_api_key)
                
            elif self.model_provider == "openai":
                logger.info("Loading LLM from OpenAI")
                openai_api_key = os.getenv("OPENAI_API_KEY")
                if not openai_api_key:
                    raise ValueError("OPENAI_API_KEY not found in environment variables")
                
                model_name = self.config["llm"]["openai"]["model_name"]
                logger.info(f"Using model: {model_name}")
                return ChatOpenAI(model_name=model_name, api_key=openai_api_key)
            
            else:
                raise ValueError(f"Unsupported model provider: {self.model_provider}")
                
        except Exception as e:
            logger.error(f"Error loading LLM: {str(e)}")
            raise CustomException(e, sys)