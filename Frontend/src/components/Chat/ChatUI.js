import React, { useState } from "react";
import { sendMessageToChat } from "../services/api";

function ChatUI() {
    const [message, setMessage] = useState("");
    const [response, setResponse] = useState("");

    const sendMessage = async () => {
        const res = await sendMessageToChat(message);
        setResponse(res.response);
    };

    return (
        <div>
            <h2>Chat AI</h2>
            <input type="text" value={message} onChange={(e) => setMessage(e.target.value)} />
            <button onClick={sendMessage}>Enviar</button>
            <p>Resposta: {response}</p>
        </div>
    );
}

export default ChatUI;
