'use client';

import { motion } from 'framer-motion';

export default function CalendarPage() {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const dates = Array.from({ length: 35 }, (_, i) => i + 1); // Simple simulation

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="space-y-6"
        >
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-3xl font-heading font-bold text-white">Calendar</h2>
                    <p className="text-slate-400">View your schedule and deadlines</p>
                </div>
                <div className="flex gap-2">
                    <button className="px-3 py-1.5 text-sm bg-slate-800 text-slate-300 rounded-lg hover:bg-slate-700">Month</button>
                    <button className="px-3 py-1.5 text-sm bg-slate-900 text-slate-500 rounded-lg hover:bg-slate-800">Week</button>
                </div>
            </div>

            <div className="p-6 rounded-2xl bg-slate-900/50 backdrop-blur-xl border border-slate-800">
                <div className="grid grid-cols-7 mb-4">
                    {days.map(day => (
                        <div key={day} className="text-center text-sm font-medium text-slate-500 py-2">
                            {day}
                        </div>
                    ))}
                </div>
                <div className="grid grid-cols-7 gap-px bg-slate-800 rounded-lg border border-slate-800 overflow-hidden">
                    {dates.map((date, i) => (
                        <div key={i} className="bg-slate-900/50 min-h-[100px] p-2 hover:bg-slate-800/50 transition-colors cursor-pointer group relative">
                            <span className={`text-sm ${i === 14 ? 'text-indigo-400 font-bold bg-indigo-500/10 w-6 h-6 flex items-center justify-center rounded-full' : 'text-slate-400'}`}>
                                {(i % 30) + 1}
                            </span>

                            {/* Simulated Events */}
                            {i === 14 && (
                                <div className="mt-2 text-xs p-1 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 truncate">
                                    Project Review
                                </div>
                            )}
                            {i === 18 && (
                                <div className="mt-2 text-xs p-1 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 truncate">
                                    Ship Update
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </motion.div>
    );
}
