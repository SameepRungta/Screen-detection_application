# Screen-detection_application

**Author:** Sameep Rungta

## Project Description

The Open Windows Detector is a Python application that monitors and detects changes in open windows and browser tabs on your system. It provides real-time updates on newly opened and closed windows and tabs. The application uses a graphical interface built with Tkinter for displaying open windows and historical events. Additionally, it includes a WebSocket server for tracking browser tabs.

## Features

- **Window Detection:** Monitors and displays currently open windows.
- **Tab Tracking:** Tracks and logs browser tabs opened and closed through a WebSocket server.
- **Real-Time Updates:** Displays real-time changes in open windows and tabs.
- **Event Logging:** Logs events with timestamps for historical reference.
- **Chrome Extension Integration:** Tracks browser tabs using a Chrome extension.

## Installation

### Prerequisites

- Python 3.7 or higher
- A virtual environment (optional but recommended)
- Google Chrome or Chromium browser

### Setup

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/SameepRungta/open-windows-detector.git
    cd open-windows-detector
    ```

2. **Create and Activate a Virtual Environment (optional):**

    - On Windows:

        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3. **Install Python Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Load the Chrome Extension:**

    - Open Google Chrome and navigate to `chrome://extensions/`.
    - Enable "Developer mode" using the toggle switch in the top right corner.
    - Click on "Load unpacked" and select the `extension` folder within the project directory.
    - The extension should now be loaded, and it will start sending tab data to the WebSocket server.

5. **Run the Python Application:**

    ```bash
    python main.py
    ```

    This will start the application, and it will begin monitoring open windows and browser tabs.

## Usage

- The Tkinter application window will display a list of currently open windows and a history of detected events.
- The WebSocket server listens on `ws://localhost:8080` for connections from clients sending tab data.
- The Chrome extension will send data to the WebSocket server when tabs are opened or closed.

## WebSocket Protocol

- **Messages:** The WebSocket server expects JSON-formatted messages with an array of tab objects.
- **Example Message:**

    ```json
    [
        {"title": "Example Tab 1"},
        {"title": "Example Tab 2"}
    ]
    ```

## Chrome Extension

The Chrome extension is included in the `extension` folder. This extension collects data about the currently open tabs and sends it to the WebSocket server. Ensure you have the extension properly loaded and running in Chrome for the tab tracking to work.

## Contribution

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. **Fork the Repository:**
    
    Click the "Fork" button on the top right of the repository page.

2. **Create a New Branch:**

    ```bash
    git checkout -b feature-branch
    ```

3. **Make Your Changes and Commit:**

    ```bash
    git add .
    git commit -m "Add new feature"
    ```

4. **Push Your Changes:**

    ```bash
    git push origin feature-branch
    ```

5. **Create a Pull Request:**

    Go to the repository page on GitHub and create a pull request with a description of your changes.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Contact

For any questions or issues, please open an issue on GitHub or contact [sameeprungta2002@gmail.com](mailto:sameeprungta2002@gmail.com).
