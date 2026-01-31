'use client';

import { motion } from 'framer-motion';

export default function ProjectsPage() {
    const projects = [
        { id: 1, name: 'Website Redesign', progress: 75, status: 'In Progress', members: 3 },
        { id: 2, name: 'Mobile App Launch', progress: 45, status: 'In Progress', members: 5 },
        { id: 3, name: 'Marketing Campaign', progress: 10, status: 'Planning', members: 2 },
        { id: 4, name: 'Q4 Financial Review', progress: 100, status: 'Completed', members: 4 },
    ];

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="space-y-6"
        >
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-3xl font-heading font-bold text-white">Projects</h2>
                    <p className="text-slate-400">Manage your ongoing initiatives</p>
                </div>
                <button className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg shadow-lg shadow-indigo-500/20 transition-all font-medium">
                    + New Project
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {projects.map((project) => (
                    <div key={project.id} className="p-6 rounded-2xl bg-slate-900/50 backdrop-blur-xl border border-slate-800 hover:border-indigo-500/30 transition-colors group">
                        <div className="flex justify-between items-start mb-4">
                            <div className="p-3 rounded-xl bg-slate-800 text-indigo-400 group-hover:bg-indigo-500/20 group-hover:text-indigo-300 transition-colors">
                                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                                </svg>
                            </div>
                            <span className={`px-2 py-1 rounded-full text-xs font-medium border ${project.status === 'Completed' ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' :
                                    project.status === 'In Progress' ? 'bg-amber-500/10 border-amber-500/20 text-amber-400' :
                                        'bg-slate-700/50 border-slate-600 text-slate-400'
                                }`}>
                                {project.status}
                            </span>
                        </div>

                        <h3 className="text-xl font-bold text-white mb-2">{project.name}</h3>

                        <div className="mb-4">
                            <div className="flex justify-between text-xs text-slate-400 mb-1">
                                <span>Progress</span>
                                <span>{project.progress}%</span>
                            </div>
                            <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
                                <div
                                    className="h-full bg-indigo-500 rounded-full"
                                    style={{ width: `${project.progress}%` }}
                                />
                            </div>
                        </div>

                        <div className="flex items-center justify-between pt-4 border-t border-slate-800/50">
                            <div className="flex -space-x-2">
                                {[...Array(project.members)].map((_, i) => (
                                    <div key={i} className="w-8 h-8 rounded-full bg-slate-700 border-2 border-slate-900 flex items-center justify-center text-xs text-white font-medium">
                                        {String.fromCharCode(65 + i)}
                                    </div>
                                ))}
                            </div>
                            <span className="text-sm text-slate-400">{project.members} members</span>
                        </div>
                    </div>
                ))}
            </div>
        </motion.div>
    );
}
