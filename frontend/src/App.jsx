import { BookOpen, LibraryBig, Sparkles } from "lucide-react";

import Chat from "./components/chat";

function App() {
    return (
        <main className="min-h-screen bg-[#f3efe7] px-4 py-6 text-stone-900 sm:px-6 lg:px-10 lg:py-10">
            <div className="mx-auto flex w-full max-w-7xl flex-col gap-6">
                <header className="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
                    <div>
                        <div className="mb-4 flex items-center gap-3 text-amber-800">
                            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-amber-100 shadow-sm"><LibraryBig size={23} aria-hidden="true" /></div>
                            <span className="text-sm font-semibold uppercase tracking-[0.2em]">Your reading room</span>
                        </div>
                        <div className="flex items-center gap-3">
                            <h1 className="font-serif text-4xl font-semibold tracking-tight text-stone-950 sm:text-6xl">Smart Librarian</h1>
                            <Sparkles className="mt-2 text-amber-600" size={22} aria-hidden="true" />
                        </div>
                        <p className="mt-3 max-w-xl text-base leading-7 text-stone-600 sm:text-lg">A thoughtful AI companion for finding the stories that stay with you.</p>
                    </div>
                    <div className="flex flex-wrap gap-2 text-xs font-semibold uppercase tracking-wider text-stone-600">
                        <span className="rounded-full border border-stone-200 bg-white/70 px-3 py-2">Find your genre</span>
                        <span className="rounded-full border border-stone-200 bg-white/70 px-3 py-2">Popular picks</span>
                        <span className="rounded-full border border-stone-200 bg-white/70 px-3 py-2">Made for you</span>
                    </div>
                </header>
                <div className="h-[min(78vh,760px)] min-h-[560px] overflow-hidden rounded-[2rem] border border-stone-200 bg-[#fffdf8] shadow-[0_24px_70px_-32px_rgba(77,58,35,0.45)]"><Chat /></div>
                <footer className="flex items-center justify-center gap-2 text-center text-xs text-stone-500"><BookOpen size={14} aria-hidden="true" /><span>Made for curious readers · Dava.X · 2026</span></footer>
            </div>
        </main>
    );
}

export default App;
