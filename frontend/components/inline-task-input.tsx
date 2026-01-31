'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface InlineTaskInputProps {
    onAddTask: (title: string) => Promise<void>;
}

export default function InlineTaskInput({ onAddTask }: InlineTaskInputProps) {
    const [title, setTitle] = useState('');
    const [isFocused, setIsFocused] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!title.trim() || loading) return;

        setLoading(true);
        try {
            await onAddTask(title);
            setTitle('');
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="mb-6 relative z-20">
            <div
                className={`relative flex items-center bg-slate-800/50 border rounded-xl overflow-hidden transition-all duration-300 ${isFocused
                        ? 'border-indigo-500 shadow-lg shadow-indigo-500/10 ring-1 ring-indigo-500/20'
                        : 'border-slate-700 hover:border-slate-600'
                    }`}
            >
                <div className="pl-4 pr-3 text-slate-400">
                    <motion.div
                        animate={{ rotate: isFocused ? 90 : 0 }}
                        className={isFocused ? "text-indigo-400" : ""}
                    >
                        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                        </svg>
                    </motion.div>
                </div>

                <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    onFocus={() => setIsFocused(true)}
                    onBlur={() => setIsFocused(false)}
                    placeholder="Add a new task..."
                    className="w-full bg-transparent py-4 text-white placeholder-slate-400 focus:outline-none"
                    disabled={loading}
                />

                <div className="pr-4">
                    <AnimatePresence>
                        {(title.trim() || isFocused) && (
                            <motion.button
                                initial={{ opacity: 0, scale: 0.8 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.8 }}
                                type="submit"
                                disabled={!title.trim() || loading}
                                className={`text-xs font-semibold px-2 py-1 rounded border transition-colors ${title.trim()
                                        ? 'bg-indigo-600 border-indigo-500 text-white shadow-sm'
                                        : 'bg-slate-700 border-slate-600 text-slate-400'
                                    }`}
                            >
                                {loading ? 'Adding...' : 'Enter ↵'}
                            </motion.button>
                        )}
                    </AnimatePresence>
                </div>
            </div>
        </form>
    );
}
