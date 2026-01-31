'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import ConfettiAnimation from './confetti-animation';
import { Task } from '@/lib/api';

interface TaskCardProps {
  task: Task;
  onUpdate: (updatedTask: Task) => void;
  onDelete: (taskId: string) => void;
  onToggleComplete: (taskId: string, completed: boolean) => void;
}

export default function TaskCard({ task, onUpdate, onDelete, onToggleComplete }: TaskCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');
  const [editPriority, setEditPriority] = useState(task.priority);
  const [showConfetti, setShowConfetti] = useState(false);

  const handleSave = () => {
    const updatedTask = {
      ...task,
      title: editTitle,
      description: editDescription,
      priority: editPriority,
    };
    onUpdate(updatedTask);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditTitle(task.title);
    setEditDescription(task.description || '');
    setIsEditing(false);
  };

  const handleToggleComplete = () => {
    const newCompleted = !task.completed;
    if (newCompleted && !task.completed) {
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 1000);
    }
    onToggleComplete(task.id, newCompleted);
  };

  const getPriorityColor = (priority: number) => {
    switch (priority) {
      case 1: return 'text-rose-400 bg-rose-400/10 border-rose-400/20';
      case 2: return 'text-orange-400 bg-orange-400/10 border-orange-400/20';
      case 3: return 'text-amber-400 bg-amber-400/10 border-amber-400/20';
      case 4: return 'text-blue-400 bg-blue-400/10 border-blue-400/20';
      default: return 'text-slate-400 bg-slate-400/10 border-slate-400/20';
    }
  };

  const getPriorityLabel = (priority: number) => {
    switch (priority) {
      case 1: return 'High';
      case 2: return 'Med-High';
      case 3: return 'Medium';
      case 4: return 'Low-Med';
      default: return 'Low';
    }
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      whileHover={{ y: -2 }}
      className={`group relative rounded-2xl p-6 backdrop-blur-xl border transition-all duration-300 ${task.completed
          ? 'bg-slate-900/30 border-slate-800/50 hover:border-slate-700/50'
          : 'bg-slate-900/60 border-slate-800/80 hover:border-indigo-500/30 hover:shadow-lg hover:shadow-indigo-500/10'
        }`}
    >
      {isEditing ? (
        <div className="space-y-4">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="w-full px-4 py-3 bg-slate-950/50 border border-slate-700/50 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all font-heading"
            autoFocus
            placeholder="Task title"
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className="w-full px-4 py-3 bg-slate-950/50 border border-slate-700/50 rounded-xl text-slate-300 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all resize-none"
            placeholder="Add description..."
            rows={3}
          />

          <div className="flex flex-wrap items-center justify-between gap-4 pt-2">
            <div className="flex gap-2">
              {[1, 2, 3, 4, 5].map((level) => (
                <button
                  key={level}
                  type="button"
                  onClick={() => setEditPriority(level)}
                  className={`w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold transition-all ${editPriority === level
                      ? getPriorityColor(level).replace('bg-opacity-10', 'bg-opacity-100') + ' ring-2 ring-offset-2 ring-offset-slate-900'
                      : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                    }`}
                  aria-label={`Priority ${level}`}
                >
                  {level}
                </button>
              ))}
            </div>

            <div className="flex gap-3">
              <button
                onClick={handleCancel}
                className="px-4 py-2 text-sm font-medium text-slate-400 hover:text-white transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                className="px-4 py-2 text-sm font-medium bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg shadow-lg shadow-indigo-500/20 transition-all"
              >
                Save Changes
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div className="flex items-start gap-4">
          <button
            onClick={handleToggleComplete}
            className={`mt-1 flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all duration-300 ${task.completed
                ? 'bg-indigo-500 border-indigo-500 scale-100'
                : 'border-slate-600 hover:border-indigo-400 scale-95 hover:scale-100'
              }`}
          >
            {task.completed && (
              <motion.svg
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                className="w-3.5 h-3.5 text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth="3"
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </motion.svg>
            )}
          </button>

          <div className="flex-1 min-w-0">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h3
                  className={`text-lg font-heading font-semibold tracking-tight transition-all duration-300 ${task.completed ? 'text-slate-500 line-through' : 'text-slate-100'
                    }`}
                >
                  {task.title}
                </h3>
                {task.description && (
                  <p className={`mt-1 text-sm leading-relaxed ${task.completed ? 'text-slate-600' : 'text-slate-400'
                    }`}>
                    {task.description}
                  </p>
                )}
              </div>
            </div>

            <div className="mt-4 flex items-center gap-3">
              <span className={`px-2.5 py-1 rounded-md text-xs font-medium border ${getPriorityColor(task.priority)}`}>
                {getPriorityLabel(task.priority)}
              </span>
              <span className="text-xs text-slate-500">
                {new Date(task.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
              </span>
            </div>
          </div>

          <div className="flex flex-col gap-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
            <button
              onClick={() => setIsEditing(true)}
              className="p-2 text-slate-400 hover:text-indigo-400 hover:bg-slate-800/50 rounded-lg transition-colors"
              title="Edit"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
            </button>
            <button
              onClick={() => onDelete(task.id)}
              className="p-2 text-slate-400 hover:text-rose-400 hover:bg-slate-800/50 rounded-lg transition-colors"
              title="Delete"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      )}
      <ConfettiAnimation isActive={showConfetti} />
    </motion.div>
  );
}