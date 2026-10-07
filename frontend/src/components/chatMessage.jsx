import { BookOpen, ImagePlus, LoaderCircle, User, Volume2, VolumeX } from "lucide-react";
import { useId, useEffect, useState } from "react";

import { generateBookImage } from "../api/chatApi";

function ChatMessage({ sender, text, imageContext = "", loading = false, isError = false }) {
    const isAssistant = sender === "assistant";
    const imagePromptId = useId();
    const [isSpeaking, setIsSpeaking] = useState(false);
    const [imageUrl, setImageUrl] = useState("");
    const [isGeneratingImage, setIsGeneratingImage] = useState(false);
    const [imageError, setImageError] = useState("");
    const [imagePrompt, setImagePrompt] = useState("");
    const [isImagePromptOpen, setIsImagePromptOpen] = useState(false);

    useEffect(() => {
        return () => {
            if (isSpeaking && "speechSynthesis" in window) {
                window.speechSynthesis.cancel();
            }
        };
    }, [isSpeaking]);

    function handleSpeechEnd() {
        setIsSpeaking(false);
    }

    function handleSpeak() {
        if (!isAssistant || !text || !("speechSynthesis" in window)) return;

        if (isSpeaking) {
            window.speechSynthesis.cancel();
            setIsSpeaking(false);
            return;
        }

        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = /[ăâîșț]/i.test(text) ? "ro-RO" : "en-US";
        utterance.rate = 0.95;
        utterance.onend = handleSpeechEnd;
        utterance.onerror = handleSpeechEnd;

        window.speechSynthesis.speak(utterance);
        setIsSpeaking(true);
    }

    function handleOpenImagePrompt() {
        if (!isAssistant || isGeneratingImage) return;
        setImageError("");
        setIsImagePromptOpen(true);
    }

    function handleCancelImagePrompt() {
        if (isGeneratingImage) return;
        setImagePrompt("");
        setImageError("");
        setIsImagePromptOpen(false);
    }

    async function handleGenerateImage(event) {
        event.preventDefault();
        const prompt = imagePrompt.trim();

        if (!isAssistant || !prompt || isGeneratingImage) return;

        setIsGeneratingImage(true);
        setImageError("");

        try {
            const contextualPrompt = [
                `Image request from the user: ${prompt}`,
                imageContext ? `Conversation context to use as reference:\n${imageContext}` : "",
                "Follow the user's image request. Use the conversation context only to preserve the relevant book, characters, setting, mood, or themes.",
            ].filter(Boolean).join("\n\n");
            const generatedImage = await generateBookImage(contextualPrompt);
            setImageUrl(generatedImage);
            setImagePrompt("");
            setIsImagePromptOpen(false);
        } catch (error) {
            setImageError(error.message || "Imaginea nu a putut fi generată.");
        } finally {
            setIsGeneratingImage(false);
        }
    }

    return (
        <div className={`mb-6 flex items-start gap-3 sm:gap-4 ${isAssistant ? "" : "flex-row-reverse"}`}>
            <div aria-hidden="true" className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl shadow-sm sm:h-11 sm:w-11 ${isAssistant ? "bg-amber-800 text-amber-50" : "bg-stone-700 text-white"}`}>
                {isAssistant ? <BookOpen size={20} /> : <User size={20} />}
            </div>
            <div className={`flex max-w-[88%] flex-col sm:max-w-[75%] ${isAssistant ? "items-start" : "items-end"}`}>
                <span className="mb-1.5 text-[10px] font-semibold uppercase tracking-[0.18em] text-stone-500">{isAssistant ? "Smart Librarian" : "You"}</span>
                <div className={`rounded-3xl px-4 py-3.5 text-sm leading-7 shadow-sm transition-all duration-300 sm:px-5 sm:py-4 sm:text-base ${isAssistant ? "rounded-tl-md border border-stone-200 bg-[#fffdf8] text-stone-700" : "rounded-tr-md bg-stone-800 text-stone-50"}`}>
                    {loading ? <div className="flex items-center gap-2 py-1" role="status" aria-label="Smart Librarian is typing"><span className="h-2.5 w-2.5 animate-bounce rounded-full bg-amber-500" /><span className="h-2.5 w-2.5 animate-bounce rounded-full bg-amber-500 [animation-delay:150ms]" /><span className="h-2.5 w-2.5 animate-bounce rounded-full bg-amber-500 [animation-delay:300ms]" /></div> : <p className="whitespace-pre-wrap break-words">{text}</p>}
                </div>
                {imageUrl && <img src={imageUrl} alt="Ilustrație generată" className="mt-3 w-full max-w-sm rounded-2xl border border-stone-200 shadow-md" />}
                {isAssistant && !loading && !isError && <div className="mt-2 flex flex-wrap gap-1">
                    <button type="button" onClick={handleSpeak} aria-label={isSpeaking ? "Oprește redarea răspunsului" : "Ascultă răspunsul"} className="flex items-center gap-1.5 rounded-full px-2 py-1 text-xs font-medium text-stone-500 transition hover:bg-amber-100 hover:text-amber-800 focus:outline-none focus:ring-2 focus:ring-amber-500">{isSpeaking ? <VolumeX size={14} aria-hidden="true" /> : <Volume2 size={14} aria-hidden="true" />}{isSpeaking ? "Oprește" : "Ascultă"}</button>
                    <button type="button" onClick={handleOpenImagePrompt} disabled={isGeneratingImage} aria-label="Descrie imaginea pe care vrei să o generez" className="flex items-center gap-1.5 rounded-full px-2 py-1 text-xs font-medium text-stone-500 transition hover:bg-amber-100 hover:text-amber-800 focus:outline-none focus:ring-2 focus:ring-amber-500 disabled:cursor-not-allowed disabled:opacity-60"><ImagePlus size={14} aria-hidden="true" />{imageUrl ? "Generează din nou" : "Imagine"}</button>
                </div>}
                {isImagePromptOpen && <form onSubmit={handleGenerateImage} className="mt-3 w-full max-w-sm rounded-2xl border border-stone-200 bg-[#fffdf8] p-3 shadow-sm">
                    <label htmlFor={imagePromptId} className="block text-xs font-semibold text-stone-700">Ce imagine vrei să generez?</label>
                    <input id={imagePromptId} type="text" value={imagePrompt} onChange={(event) => setImagePrompt(event.target.value)} placeholder="Descrie imaginea..." autoFocus disabled={isGeneratingImage} className="mt-2 w-full rounded-xl border border-stone-200 bg-white px-3 py-2 text-sm text-stone-800 outline-none transition placeholder:text-stone-400 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 disabled:bg-stone-100" />
                    <div className="mt-2 flex justify-end gap-2">
                        <button type="button" onClick={handleCancelImagePrompt} disabled={isGeneratingImage} className="rounded-full px-3 py-1.5 text-xs font-semibold text-stone-600 transition hover:bg-stone-100 disabled:cursor-not-allowed disabled:opacity-60">Anulează</button>
                        <button type="submit" disabled={!imagePrompt.trim() || isGeneratingImage} className="flex items-center gap-1.5 rounded-full bg-amber-800 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-amber-900 disabled:cursor-not-allowed disabled:opacity-50">{isGeneratingImage && <LoaderCircle size={13} className="animate-spin" aria-hidden="true" />}{isGeneratingImage ? "Se generează" : "Generează"}</button>
                    </div>
                </form>}
                {imageError && <p role="alert" className="mt-2 text-xs text-red-700">{imageError}</p>}
            </div>
        </div>
    );
}

export default ChatMessage;
