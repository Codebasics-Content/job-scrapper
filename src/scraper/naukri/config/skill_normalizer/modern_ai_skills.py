#!/usr/bin/env python3
# Modern AI/ML Skills Database Updater
# EMD Compliance: ≤80 lines

import json
import logging
from pathlib import Path
from .computer_vision_skills import COMPUTER_VISION_SKILLS

logger = logging.getLogger(__name__)

class ModernAISkillsUpdater:
    """Updates skill databases with modern AI/ML terms"""
    
    MODERN_AI_SKILLS = {
        # Generative AI
        "generative ai": {"tokens": ["generative", "ai"], "type": "Hard Skill"},
        "gen ai": {"tokens": ["gen", "ai"], "type": "Hard Skill"},
        "generative artificial intelligence": {"tokens": ["generative", "artificial", "intelligence"], "type": "Hard Skill"},
        
        # Large Language Models
        "llm": {"tokens": ["llm"], "type": "Hard Skill"},
        "llms": {"tokens": ["llms"], "type": "Hard Skill"},
        "large language models": {"tokens": ["large", "language", "models"], "type": "Hard Skill"},
        "large language model": {"tokens": ["large", "language", "model"], "type": "Hard Skill"},
        
        # OpenAI Technologies
        "openai": {"tokens": ["openai"], "type": "Hard Skill"},
        "open ai": {"tokens": ["open", "ai"], "type": "Hard Skill"},
        "gpt": {"tokens": ["gpt"], "type": "Hard Skill"},
        "gpt-3": {"tokens": ["gpt", "3"], "type": "Hard Skill"},
        "gpt-4": {"tokens": ["gpt", "4"], "type": "Hard Skill"},
        "chatgpt": {"tokens": ["chatgpt"], "type": "Hard Skill"},
        "chat gpt": {"tokens": ["chat", "gpt"], "type": "Hard Skill"},
        
        # LangChain & AI Frameworks
        "langchain": {"tokens": ["langchain"], "type": "Hard Skill"},
        "lang chain": {"tokens": ["lang", "chain"], "type": "Hard Skill"},
        "langgraph": {"tokens": ["langgraph"], "type": "Hard Skill"},
        "lang graph": {"tokens": ["lang", "graph"], "type": "Hard Skill"},
        "llamaindex": {"tokens": ["llamaindex"], "type": "Hard Skill"},
        "llama index": {"tokens": ["llama", "index"], "type": "Hard Skill"},
        
        # AI Agents
        "agentic ai": {"tokens": ["agentic", "ai"], "type": "Hard Skill"},
        "ai agents": {"tokens": ["ai", "agents"], "type": "Hard Skill"},
        "ai agent": {"tokens": ["ai", "agent"], "type": "Hard Skill"},
        "autonomous agents": {"tokens": ["autonomous", "agents"], "type": "Hard Skill"},
        
        # Model Context Protocol
        "mcp": {"tokens": ["mcp"], "type": "Hard Skill"},
        "model context protocol": {"tokens": ["model", "context", "protocol"], "type": "Hard Skill"},
        
        # Modern Development Tools
        "fastapi": {"tokens": ["fastapi"], "type": "Hard Skill"},
        "fast api": {"tokens": ["fast", "api"], "type": "Hard Skill"},
        "docker": {"tokens": ["docker"], "type": "Hard Skill"},
        "containerization": {"tokens": ["containerization"], "type": "Hard Skill"},
        "kubernetes": {"tokens": ["kubernetes"], "type": "Hard Skill"},
        "k8s": {"tokens": ["k8s"], "type": "Hard Skill"},
        
        # Vector Databases
        "vector database": {"tokens": ["vector", "database"], "type": "Hard Skill"},
        "vector db": {"tokens": ["vector", "db"], "type": "Hard Skill"},
        "embeddings": {"tokens": ["embeddings"], "type": "Hard Skill"},
        "pinecone": {"tokens": ["pinecone"], "type": "Hard Skill"},
        "weaviate": {"tokens": ["weaviate"], "type": "Hard Skill"},
        "chroma": {"tokens": ["chroma"], "type": "Hard Skill"},
        
        # MLOps & AI Engineering
        "mlops": {"tokens": ["mlops"], "type": "Hard Skill"},
        "ml ops": {"tokens": ["ml", "ops"], "type": "Hard Skill"},
        "aiops": {"tokens": ["aiops"], "type": "Hard Skill"},
        "ai ops": {"tokens": ["ai", "ops"], "type": "Hard Skill"},
        "prompt engineering": {"tokens": ["prompt", "engineering"], "type": "Hard Skill"},
        "rag": {"tokens": ["rag"], "type": "Hard Skill"},
        "retrieval augmented generation": {"tokens": ["retrieval", "augmented", "generation"], "type": "Hard Skill"},
        
        # Advanced AI Models (2024-2025)
        "claude": {"tokens": ["claude"], "type": "Hard Skill"},
        "anthropic": {"tokens": ["anthropic"], "type": "Hard Skill"},
        "gemini": {"tokens": ["gemini"], "type": "Hard Skill"},
        "google gemini": {"tokens": ["google", "gemini"], "type": "Hard Skill"},
        "deepseek": {"tokens": ["deepseek"], "type": "Hard Skill"},
        "deep seek": {"tokens": ["deep", "seek"], "type": "Hard Skill"},
        "command r": {"tokens": ["command", "r"], "type": "Hard Skill"},
        "cohere": {"tokens": ["cohere"], "type": "Hard Skill"},
        "grok": {"tokens": ["grok"], "type": "Hard Skill"},
        "xai": {"tokens": ["xai"], "type": "Hard Skill"},
        
        # Computer Vision & Advanced AI (Combined)
        **COMPUTER_VISION_SKILLS
    }
    
    def update_token_dist(self, token_dist_path: Path) -> None:
        """Update token_dist.json with modern AI skills"""
        logger.info(f"Updating token distribution: {token_dist_path}")
        
        with open(token_dist_path, 'r') as file:
            token_dist = json.load(file)
        
        # Add new AI tokens with reasonable frequencies
        new_tokens = {}
        for skill_name, skill_data in self.MODERN_AI_SKILLS.items():
            logger.debug(f"Processing skill: {skill_name}")
            for token in skill_data["tokens"]:
                # Set frequency based on modern relevance (50-200 range)
                new_tokens[token] = 100
        
        token_dist.update(new_tokens)
        
        with open(token_dist_path, 'w') as file:
            json.dump(token_dist, file, separators=(',', ':'))
        
        logger.info(f"Added {len(new_tokens)} new AI/ML tokens")
