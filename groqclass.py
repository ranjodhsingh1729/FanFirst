import env
from groq import Groq

__all__ = ['GroqApiClass', ]


client = Groq(
    api_key=env.GROQ_API_KEY
)

class GroqApiClass:
    def __init__(self, model="llama-3.3-70b-versatile", temprature=1, max_completion_tokens=8192, top_p=1, stop=None, max_messages=4):
        self.model = model
        self.temperature = temprature
        self.max_completion_tokens = max_completion_tokens
        self.top_p = top_p
        self.stop = stop
        self.max_messages = max_messages
        self.messages = []

    def add_message(self, role, content):
        """Add a message to the conversation history and maintain message limit."""
        self.messages.append({
            "role": role,
            "content": content
        })
        
        # Keep only the last max_messages messages
        if len(self.messages) > self.max_messages * 2:  # *2 because each exchange has 2 messages (user + assistant)
            self.messages = self.messages[-self.max_messages * 2:]
    
    def get_completion(self, content=None):
        """Get completion from Groq API using conversation history."""
        if content:
            self.add_message("user", content)
            
        response = client.chat.completions.create(
            messages=self.messages,
            model=self.model,
            temperature=self.temperature,
            max_completion_tokens=self.max_completion_tokens,
            top_p=self.top_p,
            stop=self.stop,
        )
        
        # Save the assistant's response to message history
        assistant_message = response.choices[0].message.content
        self.add_message("assistant", assistant_message)
        
        return response

    def clear_history(self):
        """Clear the conversation history."""
        self.messages = []


if __name__ == "__main__":
    # Initialize GroqApi with default settings
    groq = GroqApiClass()
    
    print("Chat with Groq AI (type 'quit' to exit, 'clear' to reset conversation)")
    while True:
        prompt = input("\nYou: ").strip()
        
        if prompt.lower() == 'quit':
            break
        elif prompt.lower() == 'clear':
            groq.clear_history()
            print("Conversation history cleared.")
            continue
        elif not prompt:
            continue
            
        try:
            response = groq.get_completion(prompt)
            print("\nAI:", response.choices[0].message.content)
        except Exception as e:
            print(f"\nError: {str(e)}")
