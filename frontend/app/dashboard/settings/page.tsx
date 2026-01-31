'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';
import { useRouter } from 'next/navigation';

export default function SettingsPage() {
  const { user } = useAuth();
  const router = useRouter();
  const [notifications, setNotifications] = useState(true);
  const [theme, setTheme] = useState('dark');

  const handleSaveSettings = () => {
    // In a real app, you would save these settings to the backend
    alert('Settings saved successfully!');
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-transparent">
        <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="mb-8 text-center">
              <h2 className="text-3xl font-bold text-white mb-2">Settings</h2>
              <p className="text-slate-400">Configure your account preferences</p>
            </div>

            <div className="bg-slate-800/30 backdrop-blur-lg rounded-2xl border border-white/10 p-6 shadow-xl">
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-medium text-white mb-4">Account Settings</h3>

                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="text-sm font-medium text-slate-300">Email Notifications</h4>
                        <p className="text-xs text-slate-400">Receive notifications via email</p>
                      </div>
                      <button
                        onClick={() => setNotifications(!notifications)}
                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${notifications ? 'bg-cyan-500' : 'bg-slate-600'
                          }`}
                      >
                        <span
                          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${notifications ? 'translate-x-6' : 'translate-x-1'
                            }`}
                        />
                      </button>
                    </div>

                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="text-sm font-medium text-slate-300">Theme</h4>
                        <p className="text-xs text-slate-400">Choose your preferred theme</p>
                      </div>
                      <select
                        value={theme}
                        onChange={(e) => setTheme(e.target.value)}
                        className="px-3 py-1 bg-slate-700 border border-slate-600 rounded text-white text-sm"
                      >
                        <option value="light">Light</option>
                        <option value="dark">Dark</option>
                        <option value="auto">Auto</option>
                      </select>
                    </div>
                  </div>
                </div>

                <div className="border-t border-slate-700 pt-6">
                  <h3 className="text-lg font-medium text-white mb-4">Security</h3>

                  <div className="space-y-4">
                    <button className="w-full text-left px-4 py-3 bg-slate-700/50 hover:bg-slate-700 rounded-lg transition-colors">
                      <div className="font-medium text-white">Change Password</div>
                      <div className="text-sm text-slate-400">Update your account password</div>
                    </button>

                    <button className="w-full text-left px-4 py-3 bg-slate-700/50 hover:bg-slate-700 rounded-lg transition-colors">
                      <div className="font-medium text-white">Two-Factor Authentication</div>
                      <div className="text-sm text-slate-400">Add an extra layer of security</div>
                    </button>
                  </div>
                </div>

                <div className="flex justify-end space-x-4 pt-6">
                  <button
                    onClick={() => router.back()}
                    className="px-6 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleSaveSettings}
                    className="px-6 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg transition-colors"
                  >
                    Save Settings
                  </button>
                </div>
              </div>
            </div>
          </motion.div>
        </main>
      </div>
    </ProtectedRoute>
  );
}