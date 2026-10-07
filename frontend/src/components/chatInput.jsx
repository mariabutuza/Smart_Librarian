import { useEffect, useRef, useState } from "react";
import { LoaderCircle, Mic, MicOff, SendHorizontal } from "lucide-react";

function ChatInput({ onSend, disabled, inputRef }) {
    const [message, setMessage] = useState("");
    const [isListening, setIsListening] = useState(false);
    const voiceSupported = typeof window !== "undefined" && Boolean(
        window.SpeechRecognition || window.webkitSpeechRecognition
    );
    const textareaRef = useRef(null);
    const recognitionRef = useRef(null);
    const voiceTranscriptRef = useRef("");

    useEffect(() => {
        if (!textareaRef.current) return;
        textareaRef.current.style.height = "0px";
        textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }, [message]);

    useEffect(() => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            return undefined;
        }

        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = "ro-RO";

        recognition.onstart = () => setIsListening(true);
        recognition.onresult = (event) => {
            const transcript = Array.from(event.results)
                .map((result) => result[0].transcript)
                .join("");

            voiceTranscriptRef.current = transcript;
            setMessage(transcript);
        };
        recognition.onerror = () => {
            setIsListening(false);
            voiceTranscriptRef.current = "";
        };
        recognition.onend = () => {
            const transcript = voiceTranscriptRef.current.trim();
            setIsListening(false);
            voiceTranscriptRef.current = "";

            if (!transcript || disabled) return;

            onSend(transcript);
            setMessage("");
        };

        recognitionRef.current = recognition;

        return () => {
            recognition.abort();
            recognitionRef.current = null;
        };
    }, [disabled, onSend]);

    function handleRef(element) {
        textareaRef.current = element;
        if (inputRef) inputRef.current = element;
    }

    function handleSubmit(event) {
        event.preventDefault();
        const trimmed = message.trim();
        if (!trimmed || disabled) return;
        onSend(trimmed);
        setMessage("");
    }

    function handleKeyDown(event) {
        if (event.key !== "Enter" || event.shiftKey) return;
        event.preventDefault();
        handleSubmit(event);
    }

    function handleVoiceToggle() {
        if (!voiceSupported || disabled) return;

        if (isListening) {
            recognitionRef.current?.stop();
            return;
        }

        voiceTranscriptRef.current = "";
        setMessage("");
        recognitionRef.current?.start();
    }

    return (
        <form onSubmit={handleSubmit} aria-label="Send a book request" className="mx-auto flex w-full max-w-4xl items-end gap-3">
            <textarea ref={handleRef} rows={1} value={message} disabled={disabled || isListening} aria-label="Your book request" placeholder={isListening ? "Ascult... vorbește acum" : "Ask about a book, genre, or favorite author..."} onChange={(event) => setMessage(event.target.value)} onKeyDown={handleKeyDown} className="max-h-40 min-h-[56px] flex-1 resize-none overflow-y-auto rounded-3xl border border-stone-200 bg-white px-4 py-4 text-stone-700 shadow-sm outline-none transition focus:border-amber-500 focus:ring-4 focus:ring-amber-100 disabled:bg-stone-100 placeholder:text-stone-400" />
            <button type="button" onClick={handleVoiceToggle} disabled={disabled || !voiceSupported} aria-label={isListening ? "Oprește modul vocal" : "Pornește modul vocal"} title={voiceSupported ? (isListening ? "Oprește modul vocal" : "Pornește modul vocal") : "Recunoașterea vocală nu este suportată în acest browser"} className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-full border transition focus:outline-none focus:ring-4 focus:ring-amber-200 disabled:cursor-not-allowed disabled:opacity-40 ${isListening ? "border-red-200 bg-red-100 text-red-700 hover:bg-red-200" : "border-stone-200 bg-white text-stone-600 hover:border-amber-300 hover:bg-amber-50 hover:text-amber-800"}`}>{isListening ? <MicOff size={20} aria-hidden="true" /> : <Mic size={20} aria-hidden="true" />}</button>
            <button type="submit" disabled={disabled || !message.trim()} aria-label={disabled ? "Waiting for response" : "Send message"} className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-amber-800 text-white shadow-lg transition hover:scale-105 hover:bg-amber-900 focus:outline-none focus:ring-4 focus:ring-amber-200 active:scale-95 disabled:cursor-not-allowed disabled:bg-stone-300 disabled:shadow-none">{disabled ? <LoaderCircle size={20} className="animate-spin" aria-hidden="true" /> : <SendHorizontal size={20} aria-hidden="true" />}</button>
        </form>
    );
}

export default ChatInput;
