import env
from groq import Groq

__all__ = [
    "GroqApiClass",
]


client = Groq(api_key=env.GROQ_API_KEY)


class GroqApiClass:
    def __init__(
        self,
        model="llama-3.3-70b-versatile",
        temprature=1,
        max_completion_tokens=8192,
        top_p=1,
        stop=None,
        max_messages=4,
    ):
        self.model = model
        self.temperature = temprature
        self.max_completion_tokens = max_completion_tokens
        self.top_p = top_p
        self.stop = stop
        self.max_messages = max_messages
        self.messages = [
            {
                "role": "user",
                "content": "You are a navigation assistant for the FanFirst website. Your only job is to help users navigate through the site and understand how to use its features.\nKey Pages and Navigation Flow:\nHome Page (Not Logged In):\nGet Started → Signs up the user\nSign Up → Signs up the user\nSign In → Signs in the user\nAbout → Opens the About page\nAfter Sign Up/Sign In:\nUser is logged in and redirected to the main home page\nNavbar now shows:\nSign Out button\nDashboard Icon\nDashboard Button (Logged In Navbar):\nClicking it redirects to the Dashboard\nDashboard shows user’s connected music platforms and stats\nBehavior Rules:\nOnly help users with navigating the FanFirst website\nIf asked an unrelated question, reply:\n\"I'm here only to help you with navigating the FanFirst website. Please refer to a general assistant for anything else.\"\nBe brief, helpful, and always stay within the FanFirst website's context",
            }
        ]

    def add_message(self, role, content):
        """Add a message to the conversation history and maintain message limit."""
        self.messages.append({"role": role, "content": content})

        # Keep only the last max_messages messages except the first one
        if (
            len(self.messages)+1 > self.max_messages * 2
        ):  # *2 because each exchange has 2 messages (user + assistant)
            self.messages = self.messages[1:][-self.max_messages * 2 :]

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

        if prompt.lower() == "quit":
            break
        elif prompt.lower() == "clear":
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
