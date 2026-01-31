'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';
import { useRouter } from 'next/navigation';
import { taskApi } from '@/lib/api';

export default function AnalyticsPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [analyticsData, setAnalyticsData] = useState({
    totalTasks: 0,
    completedTasks: 0,
    pendingTasks: 0,
    completionRate: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalyticsData = async () => {
      if (!user?.id) return;

      try {
        const response = await taskApi.getUserTasks(user.id);

        if (response.data) {
          const tasks = response.data;

          const totalTasks = tasks.length;
          const completedTasks = tasks.filter((task: any) => task.completed).length;
          const pendingTasks = totalTasks - completedTasks;
          const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

          setAnalyticsData({
            totalTasks,
            completedTasks,
            pendingTasks,
            completionRate,
          });
        }
      } catch (error) {
        console.error('Error fetching analytics data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalyticsData();
  }, [user]);

  if (loading) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-transparent">
          <div className="flex items-center justify-center min-h-[calc(100vh-80px)]">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-cyan-500"></div>
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-transparent">
        <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="mb-8 text-center">
              <h2 className="text-3xl font-bold text-white mb-2">Analytics</h2>
              <p className="text-slate-400">Track your productivity and progress</p>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="bg-slate-800/30 backdrop-blur-lg rounded-2xl border border-white/10 p-6 shadow-xl"
              >
                <div className="flex items-center">
                  <div className="p-3 bg-cyan-500/10 rounded-lg">
                    <svg className="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-slate-400">Total Tasks</p>
                    <p className="text-2xl font-bold text-white">{analyticsData.totalTasks}</p>
                  </div>
                </div>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="bg-slate-800/30 backdrop-blur-lg rounded-2xl border border-white/10 p-6 shadow-xl"
              >
                <div className="flex items-center">
                  <div className="p-3 bg-green-500/10 rounded-lg">
                    <svg className="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-slate-400">Completed</p>
                    <p className="text-2xl font-bold text-white">{analyticsData.completedTasks}</p>
                  </div>
                </div>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="bg-slate-800/30 backdrop-blur-lg rounded-2xl border border-white/10 p-6 shadow-xl"
              >
                <div className="flex items-center">
                  <div className="p-3 bg-yellow-500/10 rounded-lg">
                    <svg className="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-slate-400">Pending</p>
                    <p className="text-2xl font-bold text-white">{analyticsData.pendingTasks}</p>
                  </div>
                </div>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="bg-slate-800/30 backdrop-blur-lg rounded-2xl border border-white/10 p-6 shadow-xl"
              >
                <div className="flex items-center">
                  <div className="p-3 bg-purple-500/10 rounded-lg">
                    <svg className="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-slate-400">Completion Rate</p>
                    <p className="text-2xl font-bold text-white">{analyticsData.completionRate}%</p>
                  </div>
                </div>
              </motion.div>
            </div>

            {/* Charts Section */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="bg-slate-800/30 backdrop-blur-lg rounded-2xl border border-white/10 p-6 shadow-xl"
              >
                <h3 className="text-lg font-medium text-white mb-4">Task Distribution</h3>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-slate-300">Personal</span>
                      <span className="text-slate-400">60%</span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-2">
                      <div className="bg-cyan-500 h-2 rounded-full" style={{ width: '60%' }}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-slate-300">Work</span>
                      <span className="text-slate-400">30%</span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-2">
                      <div className="bg-purple-500 h-2 rounded-full" style={{ width: '30%' }}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-slate-300">Shopping</span>
                      <span className="text-slate-400">10%</span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-2">
                      <div className="bg-green-500 h-2 rounded-full" style={{ width: '10%' }}></div>
                    </div>
                  </div>
                </div>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
                className="bg-slate-800/30 backdrop-blur-lg rounded-2xl border border-white/10 p-6 shadow-xl"
              >
                <h3 className="text-lg font-medium text-white mb-4">Weekly Progress</h3>
                <div className="space-y-2">
                  {[70, 65, 80, 75, 90, 85, 95].map((value, index) => (
                    <div key={index} className="flex items-center">
                      <div className="w-12 text-sm text-slate-400">{['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][index]}</div>
                      <div className="flex-1 ml-2">
                        <div className="w-full bg-slate-700 rounded-full h-2">
                          <div className="bg-gradient-to-r from-cyan-500 to-purple-500 h-2 rounded-full" style={{ width: `${value}%` }}></div>
                        </div>
                      </div>
                      <div className="w-10 text-right text-sm text-slate-400">{value}%</div>
                    </div>
                  ))}
                </div>
              </motion.div>
            </div>

            <div className="mt-8 text-center">
              <button
                onClick={() => router.back()}
                className="px-6 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors"
              >
                Back to Dashboard
              </button>
            </div>
          </motion.div>
        </main>
      </div>
    </ProtectedRoute>
  );
}