"""Dynamic Context Engine for merging user queries with business context."""
from typing import Dict, Optional
from datetime import datetime
import json


class ContextEngine:
    """Engine that merges user queries with dynamic business context."""
    
    def __init__(self, default_context: Optional[Dict] = None):
        """Initialize the context engine with optional default context."""
        self.current_context: Dict = default_context or {}
        self.context_history: list = []
        
    def update_context(self, context: Dict, merge: bool = True) -> None:
        """
        Update the business context dynamically.
        
        Args:
            context: Dictionary containing context information
            merge: If True, merge with existing context. If False, replace.
        """
        if merge:
            self.current_context.update(context)
        else:
            self.current_context = context
            
        # Log context update
        self.context_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "context": self.current_context.copy()
        })
    
    def get_context(self) -> Dict:
        """Get the current business context."""
        return self.current_context.copy()
    
    def clear_context(self) -> None:
        """Clear all context."""
        self.current_context = {}
    
    def build_prompt(self, user_query: str, context_override: Optional[Dict] = None) -> str:
        """
        Build a structured prompt by merging user query with business context.
        
        Args:
            user_query: The user's question/request
            context_override: Optional context that temporarily overrides current context
            
        Returns:
            Structured prompt string ready for LLM
        """
        # Use override context if provided, otherwise use current context
        active_context = context_override if context_override else self.current_context
        
        # Build structured prompt
        prompt_parts = []
        
        # Business context section
        if active_context:
            prompt_parts.append("## Business Context")
            
            # Add role/persona if specified
            if "role" in active_context:
                prompt_parts.append(f"**Role:** {active_context['role']}")
            
            # Add mode/preset if specified
            if "mode" in active_context:
                prompt_parts.append(f"**Mode:** {active_context['mode']}")
            
            # Add instructions
            if "instructions" in active_context:
                instructions = active_context["instructions"]
                if isinstance(instructions, list):
                    instructions = "\n".join(f"- {inst}" for inst in instructions)
                prompt_parts.append(f"**Instructions:**\n{instructions}")
            
            # Add additional context fields
            for key, value in active_context.items():
                if key not in ["role", "mode", "instructions"]:
                    if isinstance(value, (dict, list)):
                        value = json.dumps(value, indent=2)
                    prompt_parts.append(f"**{key.title()}:** {value}")
            
            prompt_parts.append("")  # Empty line
        
        # User query section
        prompt_parts.append("## User Query")
        prompt_parts.append(user_query)
        prompt_parts.append("")
        
        # Response instructions
        prompt_parts.append("## Response Instructions")
        prompt_parts.append("Please provide a helpful, accurate response based on the business context and user query above.")
        prompt_parts.append("Do not mention that you are an AI, model name, tokens, or any technical details.")
        prompt_parts.append("Respond as if you are the SmartAdvisor system itself.")
        
        return "\n".join(prompt_parts)
    
    def build_chat_messages(self, user_query: str, context_override: Optional[Dict] = None, 
                           conversation_history: Optional[list] = None) -> list:
        """
        Build chat messages for LLM API that supports conversation history.
        
        Args:
            user_query: The user's question/request
            context_override: Optional context that temporarily overrides current context
            conversation_history: Previous messages in the conversation
            
        Returns:
            List of message dictionaries formatted for LLM API
        """
        messages = []
        
        # Add system message with context
        active_context = context_override if context_override else self.current_context
        system_message_parts = []
        
        if active_context:
            system_message_parts.append("You are SmartAdvisor, an internal business assistant.")
            
            if "role" in active_context:
                system_message_parts.append(f"You are operating in the role of: {active_context['role']}")
            
            if "mode" in active_context:
                system_message_parts.append(f"You are in {active_context['mode']} mode.")
            
            if "instructions" in active_context:
                instructions = active_context["instructions"]
                if isinstance(instructions, list):
                    instructions = "\n".join(inst for inst in instructions)
                system_message_parts.append(f"Follow these instructions:\n{instructions}")
            
            # Add other context fields
            for key, value in active_context.items():
                if key not in ["role", "mode", "instructions"]:
                    if isinstance(value, (dict, list)):
                        value = json.dumps(value, indent=2)
                    system_message_parts.append(f"{key.title()}: {value}")
        else:
            system_message_parts.append("You are SmartAdvisor, an internal business assistant.")
        
        system_message_parts.append("\nImportant: Do not mention that you are an AI, model name, tokens, or any technical details. Respond as SmartAdvisor itself.")
        
        messages.append({
            "role": "system",
            "content": "\n".join(system_message_parts)
        })
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current user query
        messages.append({
            "role": "user",
            "content": user_query
        })
        
        return messages

