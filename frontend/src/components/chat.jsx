import { useEffect, useRef, useState } from "react";
import { BookOpen, Check, Eraser, Sparkles } from "lucide-react";

import { sendMessage } from "../api/chatApi";
import ChatInput from "./chatInput";
import ChatMessage from "./chatMessage";

const QUICK_PROMPTS = [
    { emoji: "✦", title: "Fantasy", description: "A world to get lost in", text: "Recommend a fantasy novel" },
    { emoji: "⌕", title: "Mystery", description: "A clever case to unravel", text: "Suggest a mystery book" },
    { emoji: "♡", title: "Romance", description: "A story with heart", text: "Recommend a romance novel" },
    { emoji: "▦", title: "Historical", description: "A journey through time", text: "I like historical fiction" },
];

function Chat() {
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, loading]);

    async function handleSend(message) {
        const userMessage = { id: crypto.randomUUID(), sender: "user", text: message };
        setMessages((previous) => [...previous, userMessage]);
        setLoading(true);
        try {
            const answer = await sendMessage(message, messages);
            setMessages((previous) => [...previous, {
                id: crypto.randomUUID(),
                sender: "assistant",
                text: answer,
                imageContext: `User request: ${message}\nAssistant response: ${answer}`,
            }]);
        } catch (error) {
            setMessages((previous) => [...previous, { id: crypto.randomUUID(), sender: "assistant", text: error.message || "Something went wrong. Please try again.", isError: true }]);
        } finally {
            setLoading(false);
        }
    }

    function handleClearChat() {
        if (loading || messages.length === 0) return;
        setMessages([]);
        inputRef.current?.focus();
    }

    return (
        <section className="flex h-full min-h-0 flex-col">
            <div className="flex items-center justify-between border-b border-stone-200 bg-[#fffdf8] px-5 py-4 sm:px-8 sm:py-5">
                <div className="flex items-center gap-3">
                    <div className="rounded-xl bg-amber-100 p-3 text-amber-800"><BookOpen size={21} aria-hidden="true" /></div>
                    <div><h2 className="font-serif text-xl font-semibold text-stone-950 sm:text-2xl">The recommendation desk</h2><p className="hidden text-sm text-stone-500 sm:block">Tell me what you want to read next.</p></div>
                </div>
                <div className="flex items-center gap-3">
                    <span className="hidden items-center gap-1.5 text-xs font-semibold text-emerald-700 sm:flex"><Check size={14} aria-hidden="true" /> Ready to browse</span>
                    <button type="button" onClick={handleClearChat} disabled={loading || messages.length === 0} aria-label="Clear conversation" className="flex items-center gap-2 rounded-full border border-stone-200 px-3 py-2 text-xs font-semibold text-stone-600 transition hover:border-amber-300 hover:bg-amber-50 focus:outline-none focus:ring-2 focus:ring-amber-500 disabled:cursor-not-allowed disabled:opacity-40"><Eraser size={14} aria-hidden="true" /><span className="hidden sm:inline">Clear chat</span></button>
                </div>
            </div>
            <div className={`flex min-h-0 flex-1 flex-col bg-[#f8f5ee] px-4 py-5 sm:px-8 sm:py-6 ${messages.length > 0 ? "overflow-y-auto" : "overflow-hidden"}`}>
                {messages.length === 0 && (
                    <div className="m-auto flex w-full max-w-5xl flex-col items-center justify-center text-center">
                        <div className="mb-4 rounded-full border border-amber-200 bg-amber-100 p-4 text-amber-800 shadow-sm"><Sparkles size={32} aria-hidden="true" /></div>
                        <h2 className="font-serif text-3xl font-semibold text-stone-950 sm:text-4xl">Where shall we wander?</h2>
                        <p className="mt-2 max-w-lg leading-7 text-stone-600">Share a mood, a favorite author, or a world you want to disappear into. I’ll find a fitting next chapter.</p>
                        <div className="mt-6 grid w-full grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
                            {QUICK_PROMPTS.map((prompt) => <button key={prompt.text} type="button" onClick={() => handleSend(prompt.text)} disabled={loading} className="group flex min-h-20 items-center gap-3 rounded-2xl border border-stone-200 bg-[#fffdf8] px-4 py-3 text-left shadow-sm transition hover:-translate-y-1 hover:border-amber-300 hover:bg-amber-50/70 hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-amber-500 active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-60"><span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-amber-50 font-serif text-xl text-amber-800 transition-colors group-hover:bg-amber-100">{prompt.emoji}</span><span><span className="block font-semibold text-stone-800">{prompt.title}</span><span className="mt-1 block text-xs leading-5 text-stone-500">{prompt.description}</span></span></button>)}
                        </div>
                    </div>
                )}
                {messages.map((message) => <ChatMessage key={message.id} sender={message.sender} text={message.text} imageContext={message.imageContext} isError={message.isError} />)}
                {loading && <ChatMessage sender="assistant" loading />}
                <div ref={messagesEndRef} />
            </div>
            <div className="border-t border-stone-200 bg-[#fffdf8] p-4 sm:p-5"><ChatInput onSend={handleSend} disabled={loading} inputRef={inputRef} /></div>
        </section>
    );
}

export default Chat;
