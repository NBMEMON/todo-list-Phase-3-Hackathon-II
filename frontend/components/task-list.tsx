'use client';

import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import TaskCard from './task-card';
import { Task, taskApi } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';

export default function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [sort, setSort] = useState<'newest' | 'oldest' | 'priority'>('newest');
  const { user } = useAuth();

  // Fetch tasks for the user
  const fetchTasks = useCallback(async (pageNum: number = 1, append: boolean = false) => {
    if (!user?.id) return;

    try {
      setLoading(true);
      const response = await taskApi.getUserTasks(user.id);

      if (response.data) {
        if (append) {
          setTasks(prev => [...prev, ...response.data]);
        } else {
          setTasks(response.data);
        }
        setHasMore(response.data.length > 0);
      }
    } catch (err) {
      setError('Failed to fetch tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  }, [user?.id]);

  // Apply filters and sorting to tasks
  useEffect(() => {
    let result = [...tasks];

    // Apply search filter
    if (searchTerm) {
      result = result.filter(task =>
        task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (task.description && task.description.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    // Apply status filter
    if (filter === 'active') {
      result = result.filter(task => !task.completed);
    } else if (filter === 'completed') {
      result = result.filter(task => task.completed);
    }

    // Apply sorting
    if (sort === 'newest') {
      result.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
    } else if (sort === 'oldest') {
      result.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
    } else if (sort === 'priority') {
      // Sort by priority: higher priority (lower number) first, then by newest
      result.sort((a, b) => {
        if (a.priority !== b.priority) {
          return a.priority - b.priority; // Lower number = higher priority
        }
        // If priorities are the same, sort by newest
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
      });
    }

    setFilteredTasks(result);
  }, [tasks, searchTerm, filter, sort]);

  // Load tasks on mount and when user changes
  useEffect(() => {
    if (user?.id) {
      fetchTasks();
    }
  }, [user?.id, fetchTasks]);

  // Handle infinite scroll
  useEffect(() => {
    const handleScroll = () => {
      if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight - 1000 || !hasMore || loading) {
        return;
      }
      setPage(prev => prev + 1);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [hasMore, loading]);

  // Load more tasks when page changes
  useEffect(() => {
    if (page > 1) {
      fetchTasks(page, true);
    }
  }, [page, fetchTasks]);

  const handleUpdate = async (updatedTask: Task) => {
    if (!user?.id) return;

    try {
      // Optimistically update the task in the UI
      setTasks(prev => prev.map(t => t.id === updatedTask.id ? updatedTask : t));

      const response = await taskApi.updateTask(user.id, updatedTask.id, updatedTask);

      if (response.data) {
        // Update with the server response in case there are any changes
        setTasks(prev => prev.map(t => t.id === updatedTask.id ? response.data as Task : t));
      }
    } catch (error) {
      // Revert the optimistic update if the API call fails
      setTasks(prev => prev.map(t => t.id === updatedTask.id ? { ...t } : t));
      console.error('Error updating task:', error);
    }
  };

  const handleDelete = async (taskId: string) => {
    if (!user?.id) return;

    try {
      // Optimistically remove the task from the UI
      setTasks(prev => prev.filter(t => t.id !== taskId));

      const response = await taskApi.deleteTask(user.id, taskId);

      if (response.error) {
        // Re-add the task if the API call fails
        console.error('Error deleting task:', response.error);
      }
    } catch (error) {
      // This shouldn't happen since the API call would fail, but just in case
      console.error('Error deleting task:', error);
    }
  };

  const handleToggleComplete = async (taskId: string, completed: boolean) => {
    if (!user?.id) return;

    try {
      // Optimistically update the task in the UI
      setTasks(prev => prev.map(t =>
        t.id === taskId ? { ...t, completed, updated_at: new Date().toISOString() } : t
      ));

      const response = await taskApi.toggleTaskCompletion(user.id, taskId, completed);

      if (response.data) {
        // Update with the server response in case there are any changes
        const updatedTaskData = response.data as Task;
        setTasks(prev => prev.map(t =>
          t.id === taskId ? { ...t, completed: updatedTaskData.completed, updated_at: updatedTaskData.updated_at } : t
        ));
      }
    } catch (error) {
      // Revert the optimistic update if the API call fails
      setTasks(prev => prev.map(t =>
        t.id === taskId ? { ...t, completed: !completed } : t
      ));
      console.error('Error toggling task completion:', error);
    }
  };

  if (loading && tasks.length === 0) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: i * 0.1 }}
            className="rounded-2xl border border-slate-800/50 p-6 bg-slate-900/40 backdrop-blur-lg shadow-xl"
          >
            <div className="animate-pulse flex items-start gap-4">
              <div className="w-6 h-6 rounded-full bg-slate-800 mt-1"></div>
              <div className="flex-1 space-y-3">
                <div className="h-5 bg-slate-800 rounded w-1/2"></div>
                <div className="h-4 bg-slate-800/60 rounded w-3/4"></div>
                <div className="flex gap-2 mt-2">
                  <div className="h-4 w-16 bg-slate-800 rounded"></div>
                  <div className="h-4 w-20 bg-slate-800 rounded"></div>
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-20 bg-slate-900/50 rounded-2xl border border-red-500/10">
        <p className="text-rose-400 mb-4">{error}</p>
        <button
          onClick={() => fetchTasks()}
          className="px-6 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg transition-colors border border-slate-700"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col xl:flex-row gap-4 p-2 bg-slate-900/40 backdrop-blur-xl rounded-2xl border border-slate-800/60 sticky top-4 z-10 shadow-2xl shadow-black/20">
        {/* Search */}
        <div className="flex-1 relative group">
          <svg className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500 group-focus-within:text-indigo-500 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            placeholder="Search tasks..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-12 pr-4 py-3 bg-slate-950/50 border border-transparent rounded-xl text-white placeholder-slate-500 focus:outline-none focus:bg-slate-950 focus:border-indigo-500/30 focus:ring-1 focus:ring-indigo-500/30 transition-all shadow-inner"
          />
        </div>

        {/* Filters & Sort */}
        <div className="flex flex-col sm:flex-row gap-2">
          <div className="flex bg-slate-950/50 p-1 rounded-xl border border-slate-800/50">
            {['all', 'active', 'completed'].map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f as any)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all capitalize ${filter === f
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/20'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                  }`}
              >
                {f}
              </button>
            ))}
          </div>

          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg className="h-4 w-4 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
              </svg>
            </div>
            <select
              value={sort}
              onChange={(e) => setSort(e.target.value as 'newest' | 'oldest' | 'priority')}
              className="h-full pl-10 pr-8 py-2 bg-slate-950/50 border border-slate-800/50 rounded-xl text-slate-300 text-sm font-medium focus:outline-none focus:border-indigo-500/30 focus:ring-1 focus:ring-indigo-500/30 transition-all appearance-none cursor-pointer hover:bg-slate-900/80"
            >
              <option value="newest">Newest First</option>
              <option value="oldest">Oldest First</option>
              <option value="priority">By Priority</option>
            </select>
            <div className="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
              <svg className="w-4 h-4 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <AnimatePresence mode='popLayout'>
        {filteredTasks.length > 0 ? (
          filteredTasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              onUpdate={handleUpdate}
              onDelete={handleDelete}
              onToggleComplete={handleToggleComplete}
            />
          ))
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="flex flex-col items-center justify-center py-20 text-center"
          >
            {searchTerm || filter !== 'all' ? (
              <>
                <div className="w-16 h-16 bg-slate-800/50 rounded-full flex items-center justify-center mb-4">
                  <svg className="w-8 h-8 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <h3 className="text-xl font-heading font-medium text-slate-200">No matches found</h3>
                <p className="text-slate-500 mt-2 max-w-xs mx-auto">Try adjusting your filters or search terms to find what you're looking for.</p>
                <button
                  onClick={() => { setSearchTerm(''); setFilter('all'); }}
                  className="mt-6 px-4 py-2 text-sm text-indigo-400 hover:text-indigo-300 transition-colors"
                >
                  Clear all filters
                </button>
              </>
            ) : (
              <>
                <div className="w-20 h-20 bg-gradient-to-tr from-indigo-500/20 to-purple-500/20 rounded-2xl flex items-center justify-center mb-6 ring-1 ring-inset ring-white/10">
                  <svg className="w-10 h-10 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                </div>
                <h3 className="text-2xl font-heading font-semibold text-white">No tasks yet</h3>
                <p className="text-slate-400 mt-2 max-w-sm mx-auto">Your productivity journey begins here. Create your first task to get started.</p>
              </>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {loading && page > 1 && (
        <div className="flex justify-center py-6">
          <div className="w-8 h-8 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin"></div>
        </div>
      )}

      {!hasMore && filteredTasks.length > 0 && (
        <div className="text-center py-8">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-900/50 border border-slate-800 text-slate-500 text-xs font-medium">
            <span>All tasks loaded</span>
            <div className="w-1 h-1 rounded-full bg-slate-500"></div>
            <span>{filteredTasks.length} total</span>
          </div>
        </div>
      )}
    </div>
  );
}