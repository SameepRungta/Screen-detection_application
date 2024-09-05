let socket;
let openTabs = new Set();

function connectWebSocket() {
    socket = new WebSocket('ws://localhost:8080');

    socket.onopen = function() {
        console.log("Connected to WebSocket server");
        sendUpdatedTabs(); // Send initial data
    };

    socket.onclose = function() {
        console.log("Disconnected from WebSocket server. Reconnecting...");
        setTimeout(connectWebSocket, 5000); // Try to reconnect after 5 seconds
    };

    socket.onerror = function(error) {
        console.error("WebSocket error: " + error.message);
    };
}

function sendUpdatedTabs() {
    chrome.tabs.query({}, function(tabs) {
        let currentTabs = new Set(tabs.map(tab => tab.title));
        
        // Determine newly opened and closed tabs
        let newTabs = [...currentTabs].filter(tab => !openTabs.has(tab));
        let closedTabs = [...openTabs].filter(tab => !currentTabs.has(tab));
        
        if (newTabs.length > 0 || closedTabs.length > 0) {
            openTabs = currentTabs;  // Update current tabs state
            
            let tabsData = tabs.map(tab => ({ url: tab.url, title: tab.title }));
            if (socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify(tabsData));
            }
        }
    });
}

// Listen for tab changes and update the WebSocket server
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    sendUpdatedTabs();
});

chrome.tabs.onRemoved.addListener(function(tabId, removeInfo) {
    sendUpdatedTabs();
});

chrome.tabs.onCreated.addListener(function(tab) {
    sendUpdatedTabs();
});

chrome.tabs.onActivated.addListener(function(activeInfo) {
    sendUpdatedTabs();
});

// Initialize WebSocket connection
connectWebSocket();
