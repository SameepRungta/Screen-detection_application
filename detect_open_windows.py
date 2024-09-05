import tkinter as tk
from tkinter import scrolledtext, font
from datetime import datetime
import threading
import pygetwindow as gw
import time
import json
import asyncio
import websockets

class ModernWindowDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Open Windows Detector")
        self.root.geometry("800x600")

        # UI Styling
        self.title_font = font.Font(family='Helvetica', size=18, weight='bold')
        self.bg_color = '#2E2E2E'
        self.header_color = '#4A90E2'
        self.text_area_bg = '#1E1E1E'
        self.text_color = '#F5F5F5'

        # Header
        self.header_frame = tk.Frame(root, bg=self.header_color, pady=10)
        self.header_frame.pack(fill=tk.X)
        self.header_label = tk.Label(self.header_frame, text="Open Windows Detector", font=self.title_font, bg=self.header_color, fg='white')
        self.header_label.pack()

        # Content Frame
        self.content_frame = tk.Frame(root, bg=self.bg_color)
        self.content_frame.pack(fill=tk.BOTH, padx=20, pady=10, expand=True)

        # Scrolled Text Areas
        self.text_area = scrolledtext.ScrolledText(self.content_frame, wrap=tk.WORD, bg=self.text_area_bg, fg=self.text_color, font=('Arial', 12))
        self.text_area.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.history_area = scrolledtext.ScrolledText(self.content_frame, wrap=tk.WORD, bg=self.text_area_bg, fg=self.text_color, font=('Arial', 12))
        self.history_area.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        # Configure Grid Layout
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Initialize Variables
        self.previous_windows = set()
        self.open_tabs = set()  # Track open tabs by title
        self.running = True

        # Start Threads
        self.update_thread = threading.Thread(target=self.update_window_list)
        self.update_thread.start()

        # Start WebSocket Server
        self.websocket_server_thread = threading.Thread(target=self.start_websocket_server)
        self.websocket_server_thread.start()

    def update_window_list(self):
        while self.running:
            try:
                open_windows = self.get_open_windows()
                current_windows = set(open_windows)

                # Detect new and closed windows
                new_windows = current_windows - self.previous_windows
                closed_windows = self.previous_windows - current_windows

                if new_windows or closed_windows:  # Update UI only when there are changes
                    # Record events
                    for window in new_windows:
                        self.record_event(f"Opened: {window}")
                    for window in closed_windows:
                        self.record_event(f"Closed: {window}")

                    # Update previous windows
                    self.previous_windows = current_windows

                    # Update UI
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, "Open windows:\n" + "\n".join(open_windows))

                self.root.update_idletasks()
                time.sleep(1)
            except Exception as e:
                self.record_event(f"Error updating window list: {e}")

    def get_open_windows(self):
        try:
            windows = gw.getAllTitles()  # Get all window titles
            open_windows = [title for title in windows if title.strip()]  # Filter out empty titles
            return open_windows
        except Exception as e:
            self.record_event(f"Error fetching open windows: {e}")
            return []

    def record_event(self, event):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history_area.insert(tk.END, f"{timestamp} - {event}\n")
        self.history_area.yview(tk.END)

    async def handle_client(self, websocket, path):
        self.record_event("Client connected")
        try:
            async for message in websocket:
                try:
                    tabs_data = json.loads(message)  # Expecting JSON formatted data
                    current_tabs = set(tab['title'] for tab in tabs_data)
                    
                    # Determine newly opened and closed tabs
                    new_tabs = current_tabs - self.open_tabs
                    closed_tabs = self.open_tabs - current_tabs
                    
                    # Log only new opened or closed tabs
                    for tab_title in new_tabs:
                        self.record_event(f"Opened: {tab_title}")
                    
                    for tab_title in closed_tabs:
                        self.record_event(f"Closed: {tab_title}")

                    # Update the list of open tabs
                    self.open_tabs = current_tabs

                except json.JSONDecodeError as e:
                    self.record_event(f"Error decoding JSON data: {e}")
        except Exception as e:
            self.record_event(f"Error handling client: {e}")

    def start_websocket_server(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(self.handle_client, "localhost", 8080)
        self.record_event("WebSocket server listening on ws://localhost:8080")
        loop.run_until_complete(start_server)
        loop.run_forever()

    def on_closing(self):
        self.running = False
        self.update_thread.join()
        self.websocket_server_thread.join()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ModernWindowDetectorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
