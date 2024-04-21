import {useState} from "react";
import {Input} from "@/components/ui/input"
import {Button} from "@/components/ui/button"
import "./App.css";

function App() {
    const [count, setCount] = useState(0);

    return (
        <main className="flex h-screen w-full flex-col items-center justify-center bg-gray-900 px-4 text-white">
            <div className="flex flex-col items-center justify-center space-y-8">
                <div
                    className="flex h-32 w-32 items-center justify-center rounded-full bg-gray-800 transition-transform hover:scale-105">
                    <MicIcon className="h-16 w-16"/>
                </div>
                <div className="w-full max-w-md space-y-4">
                    <Input
                        className="w-full rounded-lg bg-gray-800 px-4 py-3 text-white placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-600"
                        placeholder="Enter your voice command or text prompt"
                        type="text"
                    />
                    <Button
                        className="w-full rounded-lg bg-indigo-600 py-3 font-medium transition-colors hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500">
                        Submit
                    </Button>
                </div>
            </div>
        </main>
    )
}

function MicIcon(props) {
    return (
        <svg
            {...props}
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
            <line x1="12" x2="12" y1="19" y2="22"/>
        </svg>
    )
}

export default App