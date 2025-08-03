import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
import threading
import queue
import time
import os
import json
from huggingface_hub import InferenceClient
from typing import List, Dict, Optional
import platform

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class EnhancedChatInterface:
    def __init__(self, api_key: str):
        self.client = InferenceClient(
            provider="together",
            api_key=api_key
        )
        self.chat_history: List[Dict] = []
        self.conversation_context = []
        self.data_queue = queue.Queue()
        self.running = False

        # Define agent models in order as class attribute
        self.agents = [
            {"name": "DeepSeek-R1", "model": "deepseek-ai/DeepSeek-R1"},
            {"name": "Llama 3.3", "model": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"},
            {"name": "Qwen 2.5 Coder", "model": "Qwen/Qwen2.5-Coder-32B-Instruct"}
        ]

        self.setup_gui()

    def setup_gui(self):
        """Configure CustomTkinter GUI"""
        self.root = ctk.CTk()
        self.root.title("Pyramid Model Conference ◭")
        self.root.geometry("800x600")

        # Configure grid weight
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Welcome label
        self.welcome_label = ctk.CTkLabel(
            self.main_frame,
            text="Pyramid Model Conference ◭ v1.0.0 - Pilot Release",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.welcome_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        # Output area (CTkTextbox for streaming)
        self.text_area = ctk.CTkTextbox(
            self.main_frame,
            wrap="word",
            width=600,
            height=300,
            font=ctk.CTkFont(size=12),
            state='disabled'
        )
        self.text_area.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Input frame
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        # Input entry
        self.input_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Type your message here...",
            font=ctk.CTkFont(size=12),
            height=40
        )
        self.input_entry.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="ew")
        self.input_entry.bind("<Return>", lambda event: self.send_message())

        # Send button
        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="Send",
            command=self.send_message,
            width=80,
            height=40
        )
        self.send_button.grid(row=0, column=1, pady=5)

        # Control buttons frame
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="ew")

        # Control buttons
        buttons = [
            ("Clear", self.clear_screen),
            ("History", self.show_history),
            ("Save", self.save_conversation_to_file),
            ("Load", self.load_conversation),
            ("Exit", self.on_closing)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = ctk.CTkButton(
                self.button_frame,
                text=text,
                command=command,
                width=100,
                height=32
            )
            btn.grid(row=0, column=i, padx=5, pady=10)

        # Configure button frame columns
        for i in range(len(buttons)):
            self.button_frame.grid_columnconfigure(i, weight=1)

        # Check mobile device for display optimization
        self.is_mobile = 'ANDROID_ROOT' in os.environ or 'Pydroid' in platform.platform()
        self.wrap_width = 55 if self.is_mobile else 95

        # Start queue checking
        self.check_queue()

        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def check_queue(self):
        """Check the queue for new data and update the text area"""
        # This method is simplified since we're using direct text appending
        # Keep it for any future queue-based operations
        try:
            while True:
                data = self.data_queue.get_nowait()
                self.append_text(data)
        except queue.Empty:
            pass
        # Schedule the next check
        self.root.after(100, self.check_queue)

    def send_message(self):
        """Handle sending a user message and getting chat completion"""
        user_input = self.input_entry.get().strip()
        if not user_input:
            return

        if user_input.lower() == 'exit':
            self.on_closing()
            return

        if user_input.lower() == 'h':
            self.show_history()
            return

        if user_input.lower() == 'clear':
            self.clear_screen()
            return

        if user_input.lower() == 'save':
            self.save_conversation_to_file()
            return

        if user_input.lower().startswith('load '):
            filename = user_input[5:].strip()
            self.load_conversation_from_file(filename)
            return

        # Display user input immediately
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.append_text(f"\n{timestamp} | You: {user_input}\n")
        self.input_entry.delete(0, "end")

        # Add user input to conversation context
        self.conversation_context.append({"role": "user", "content": user_input})

        # Disable send button and show processing
        self.send_button.configure(state="disabled", text="Processing...")

        # Start chat completion
        self.running = True
        threading.Thread(target=self.get_chat_completion, args=(user_input,), daemon=True).start()

    def append_text(self, text):
        """Safely append text to the text area"""
        self.text_area.configure(state='normal')
        self.text_area.insert("end", text)
        self.text_area.see("end")
        self.text_area.configure(state='disabled')
        self.root.update_idletasks()

    def get_chat_completion(self, user_input):
        """Get chat completion and display response"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        try:
            # Show that we're getting a response
            self.append_text(f"\n{timestamp} | Assistant: ")

            # Use the last 10 messages for context
            messages = self.conversation_context[-10:]

            # Track if we got any successful response
            successful_response = False
            combined_response = ""

            for i, agent in enumerate(self.agents):
                display_name = agent["name"]
                model_name = agent["model"]
                self.append_text(f"\n\n--- Using {display_name} ({model_name}) ---\n")

                try:
                    completion_stream = self.client.chat.completions.create(
                        model=model_name,
                        messages=messages,
                        max_tokens=2048,
                        temperature=0.7,
                        stream=True,
                    )

                    response_text = ""
                    for chunk in completion_stream:
                        if not self.running:
                            break

                        if hasattr(chunk, 'choices') and chunk.choices:
                            if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
                                content = chunk.choices[0].delta.content
                                if content:
                                    # Append each chunk directly to the text area
                                    self.append_text(content)
                                    response_text += content

                    # Add separator between agent responses
                    self.append_text(f"\n--- End of {display_name} response ---\n")

                    # Track successful responses
                    if response_text.strip():
                        successful_response = True
                        combined_response += f"\n\n--- {display_name} ---\n{response_text.strip()}"

                except Exception as e:
                    error_msg = f"\n❌ Error with {display_name}: {str(e)}\n"
                    self.append_text(error_msg)
                    # Continue to next agent instead of breaking

            # Save to chat history if we got any successful response
            if successful_response:
                self.save_chat(user_input, combined_response.strip())
                self.conversation_context.append({"role": "assistant", "content": combined_response.strip()})
            else:
                self.append_text("\n❌ All agents failed to respond. Please try again.\n")

        except Exception as e:
            error_msg = f"\n❌ Error getting chat completion: {str(e)}\n"
            self.append_text(error_msg)

        finally:
            # Re-enable send button
            self.running = False
            self.send_button.configure(state="normal", text="Send")

    def format_dataframe(self, df: pd.DataFrame, max_rows: Optional[int] = None,
                         max_cols: Optional[int] = None, precision: int = 2) -> str:
        """Format DataFrame for display"""
        with pd.option_context(
                'display.max_rows', max_rows or len(df),
                'display.max_columns', max_cols or len(df.columns),
                'display.max_colwidth', None,
                'display.precision', precision,
                'display.float_format', lambda x: f'{{:.{precision}f}}'.format(x)
        ):
            return str(df)

    def save_chat(self, user: str, response: str):
        """Save chat history with timestamps"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.chat_history.append({
            'timestamp': timestamp,
            'user': user,
            'response': response
        })

    def show_history(self):
        """Display formatted chat history"""
        if not self.chat_history:
            self.append_text("\nNo chat history available.\n")
            return

        chat_df = pd.DataFrame(self.chat_history)
        if 'user' in chat_df.columns:
            chat_df['user'] = chat_df['user'].apply(
                lambda x: (x[:97] + '...') if isinstance(x, str) and len(x) > 100 else x
            )
        if 'response' in chat_df.columns:
            chat_df['response'] = chat_df['response'].apply(
                lambda x: (x[:97] + '...') if isinstance(x, str) and len(x) > 100 else x
            )

        formatted_df_str = self.format_dataframe(chat_df)
        self.append_text("\n=== Chat History ===\n" + formatted_df_str + "\n")

    def save_conversation_to_file(self, filename=None):
        """Save the entire conversation to a JSON file"""
        if not filename:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialname=f"deepseek_chat_{time.strftime('%Y%m%d_%H%M%S')}.json"
            )

        if not filename:
            return

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'history': self.chat_history,
                    'context': self.conversation_context
                }, f, indent=2)
            self.append_text(f"\nConversation saved to {filename}\n")
        except Exception as e:
            error_msg = f"\nError saving conversation: {str(e)}\n"
            self.append_text(error_msg)
            messagebox.showerror("Save Error", f"Error saving conversation: {str(e)}")

    def load_conversation(self):
        """Open file dialog to load a conversation"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.load_conversation_from_file(filename)

    def load_conversation_from_file(self, filename):
        """Load a conversation from a JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.chat_history = data.get('history', [])
                self.conversation_context = data.get('context', [])
            msg_count = len(self.conversation_context) // 2
            self.append_text(f"\nConversation loaded from {filename}\n")
            self.append_text(f"Loaded {msg_count} message exchanges\n")
        except Exception as e:
            error_msg = f"\nError loading conversation: {str(e)}\n"
            self.append_text(error_msg)
            messagebox.showerror("Load Error", f"Error loading conversation: {str(e)}")

    def clear_screen(self):
        """Clear the text area"""
        self.text_area.configure(state='normal')
        self.text_area.delete("1.0", "end")
        self.text_area.configure(state='disabled')

    def on_closing(self):
        """Handle window closing"""
        self.running = False
        self.root.quit()
        self.root.destroy()

    def run(self):
        """Start the CustomTkinter event loop"""
        self.root.mainloop()


if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable not set")
    chat_interface = EnhancedChatInterface(api_key)
    chat_interface.run()