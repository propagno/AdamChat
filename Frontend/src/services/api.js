const API_URL = "https://api.adamchat.com";

export async function login(username, password) {
    const response = await fetch(`${API_URL}/api/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });
    return response.json();
}

export async function sendMessageToChat(message) {
    const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
    });
    return response.json();
}
