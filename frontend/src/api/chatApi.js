const API_URL = import.meta.env.VITE_API_URL;

function getApiUrl() {
    if (!API_URL) {
        throw new Error(
            "VITE_API_URL is not configured. Check the frontend .env file."
        );
    }

    return API_URL.replace(/\/$/, "");
}

async function parseErrorResponse(response) {
    const defaultMessage =
        "Unable to communicate with the backend. Please try again.";

    try {
        const errorData = await response.json();

        if (typeof errorData.detail === "string") {
            return errorData.detail;
        }

        if (typeof errorData.message === "string") {
            return errorData.message;
        }

        if (Array.isArray(errorData.detail)) {
            return errorData.detail
                .map((error) => error.msg)
                .filter(Boolean)
                .join(", ");
        }
    } catch {
        return defaultMessage;
    }

    return defaultMessage;
}


export async function sendMessage(message, messages = [], signal) {
    const apiUrl = getApiUrl();
    const history = messages
        .filter((item) => item.text && item.text.trim() !== "")
        .map((item) => ({
            role: item.sender === "assistant" ? "assistant" : "user",
            content: item.text,
        }));
    const response = await fetch(`${apiUrl}/chat/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            message,
            history,
        }),
        signal,
    });

    if (!response.ok) {
        throw new Error(await parseErrorResponse(response));
    }

    const data = await response.json();

    return data.answer;
}

export async function generateBookImage(prompt, signal) {
    const apiUrl = getApiUrl();
    const response = await fetch(`${apiUrl}/images/generate`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt }),
        signal,
    });

    if (!response.ok) {
        throw new Error(await parseErrorResponse(response));
    }

    const data = await response.json();
    return data.image;
}
