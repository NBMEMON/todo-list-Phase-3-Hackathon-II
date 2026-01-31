'use client';

import { motion } from 'framer-motion';
import TaskList from '@/components/task-list';

export default function TasksPage() {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="space-y-6"
        >
            <div className="mb-8">
                <h2 className="text-3xl font-heading font-bold text-white">All Tasks</h2>
                <p className="text-slate-400">View and manage all your to-dos in one place</p>
            </div>

            <div className="bg-slate-800/30 backdrop-blur-lg rounded-2xl border border-white/10 p-6 shadow-xl">
                <TaskList />
            </div>
        </motion.div>
    );
}
