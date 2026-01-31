'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/ProtectedRoute';
import { useTheme } from '@/providers/theme-provider';

// Simulated Icons
const Icons = {
  User: () => <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />,
  Mail: () => <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />,
  Shield: () => <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />,
  Bell: () => <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />,
  Moon: () => <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />,
  LogOut: () => <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />,
  Trash: () => <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />,
  Camera: () => <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
};

export default function ProfilePage() {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();

  // State for form fields
  const [name, setName] = useState(user?.name || user?.username || '');
  const [email, setEmail] = useState(user?.email || '');
  const [notifications, setNotifications] = useState(true);
  const [isEditing, setIsEditing] = useState(false);

  if (!user) return null;

  return (
    <ProtectedRoute>
      <div className="space-y-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="relative p-8 rounded-3xl bg-slate-900/50 backdrop-blur-xl border border-slate-800 overflow-hidden"
        >
          <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-r from-indigo-600/20 to-purple-600/20" />

          <div className="relative flex flex-col md:flex-row items-center md:items-end gap-6 pt-12">
            <div className="relative group">
              <div className="w-24 h-24 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 p-1 shadow-2xl">
                <div className="w-full h-full rounded-full bg-slate-900 flex items-center justify-center text-3xl font-bold text-white overflow-hidden">
                  {user.username?.charAt(0).toUpperCase()}
                </div>
              </div>
              <button className="absolute bottom-0 right-0 p-2 bg-slate-800 rounded-full border border-slate-700 text-slate-300 hover:text-white hover:border-indigo-500 transition-colors">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <Icons.Camera />
                </svg>
              </button>
            </div>

            <div className="flex-1 text-center md:text-left mb-2">
              <h1 className="text-3xl font-heading font-bold text-white">{user.username}</h1>
              <div className="flex items-center justify-center md:justify-start gap-4 mt-2 text-sm text-slate-400">
                <span className="flex items-center gap-1.5">
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><Icons.Mail /></svg>
                  {user.email}
                </span>
                <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium">
                  Active Account
                </span>
              </div>
            </div>

            <button
              onClick={() => setIsEditing(!isEditing)}
              className={`px-5 py-2.5 rounded-xl font-medium transition-all ${isEditing ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/20' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}
            >
              {isEditing ? 'Save Changes' : 'Edit Profile'}
            </button>
          </div>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8">
          {/* Left Column - Navigation/Settings */}
          <div className="space-y-6">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
              className="p-6 rounded-2xl bg-slate-900/50 backdrop-blur-xl border border-slate-800"
            >
              <h3 className="text-lg font-heading font-semibold text-white mb-4">Account Preferences</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 rounded-xl bg-slate-800/50 border border-slate-700/50">
                  <div className="flex items-center gap-3 text-slate-300">
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><Icons.Moon /></svg>
                    <span>Dark Mode</span>
                  </div>
                  <button
                    onClick={toggleTheme}
                    className={`w-11 h-6 rounded-full transition-colors relative ${theme === 'dark' ? 'bg-indigo-600' : 'bg-slate-700'}`}
                  >
                    <span className={`absolute top-1 left-1 w-4 h-4 rounded-full bg-white transition-transform ${theme === 'dark' ? 'translate-x-5' : 'translate-x-0'}`} />
                  </button>
                </div>

                <div className="flex items-center justify-between p-3 rounded-xl bg-slate-800/50 border border-slate-700/50">
                  <div className="flex items-center gap-3 text-slate-300">
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><Icons.Bell /></svg>
                    <span>Notifications</span>
                  </div>
                  <button
                    onClick={() => setNotifications(!notifications)}
                    className={`w-11 h-6 rounded-full transition-colors relative ${notifications ? 'bg-indigo-600' : 'bg-slate-700'}`}
                  >
                    <span className={`absolute top-1 left-1 w-4 h-4 rounded-full bg-white transition-transform ${notifications ? 'translate-x-5' : 'translate-x-0'}`} />
                  </button>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="p-6 rounded-2xl bg-slate-900/50 backdrop-blur-xl border border-slate-800"
            >
              <h3 className="text-lg font-heading font-semibold text-white mb-4">Account Metadata</h3>
              <div className="space-y-3 text-sm text-slate-400">
                <div className="flex justify-between">
                  <span>Joined</span>
                  <span className="text-slate-200">{new Date(user.created_at).toLocaleDateString()}</span>
                </div>
                <div className="flex justify-between">
                  <span>Last Login</span>
                  <span className="text-slate-200">Just now</span>
                </div>
                <div className="flex justify-between">
                  <span>ID</span>
                  <span className="font-mono text-xs">{user.id.substring(0, 8)}...</span>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Right Column - Forms */}
          <div className="md:col-span-2 space-y-6">
            {/* Personal Info */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="p-8 rounded-3xl bg-slate-900/50 backdrop-blur-xl border border-slate-800"
            >
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400">
                  <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><Icons.User /></svg>
                </div>
                <h3 className="text-xl font-heading font-semibold text-white">Personal Information</h3>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-400">Full Name</label>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    disabled={!isEditing}
                    className="w-full px-4 py-3 bg-slate-950/50 border border-slate-700/50 rounded-xl text-white focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-400">Email Address</label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    disabled={!isEditing}
                    className="w-full px-4 py-3 bg-slate-950/50 border border-slate-700/50 rounded-xl text-white focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                  />
                </div>
                <div className="col-span-full">
                  <label className="text-sm font-medium text-slate-400">Bio</label>
                  <textarea
                    rows={3}
                    placeholder="Tell us a little about yourself..."
                    disabled={!isEditing}
                    className="w-full px-4 py-3 bg-slate-950/50 border border-slate-700/50 rounded-xl text-white focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all resize-none"
                  />
                </div>
              </div>
            </motion.div>

            {/* Security */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="p-8 rounded-3xl bg-slate-900/50 backdrop-blur-xl border border-slate-800"
            >
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
                  <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><Icons.Shield /></svg>
                </div>
                <h3 className="text-xl font-heading font-semibold text-white">Security</h3>
              </div>

              <div className="space-y-6">
                <button className="flex items-center justify-between w-full p-4 rounded-xl bg-slate-800/30 border border-slate-700/50 hover:bg-slate-800/50 transition-colors group">
                  <div className="text-left">
                    <span className="block text-white font-medium">Change Password</span>
                    <span className="text-sm text-slate-400">Update your password to keep your account secure</span>
                  </div>
                  <svg className="w-5 h-5 text-slate-500 group-hover:text-indigo-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </button>

                <div className="flex items-center justify-between pt-4 border-t border-slate-800/50">
                  <div>
                    <h4 className="text-white font-medium">Log out of all devices</h4>
                    <p className="text-sm text-slate-400 mt-1">You will be logged out of your active sessions</p>
                  </div>
                  <button className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white border border-slate-700 hover:border-slate-600 rounded-lg transition-colors">
                    Log Out All
                  </button>
                </div>
              </div>
            </motion.div>

            {/* Danger Zone */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="p-8 rounded-3xl bg-rose-950/10 border border-rose-900/20"
            >
              <div className="flex items-center gap-3 mb-2">
                <div className="p-2 rounded-lg bg-rose-500/10 text-rose-500">
                  <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><Icons.Trash /></svg>
                </div>
                <h3 className="text-xl font-heading font-semibold text-rose-500">Danger Zone</h3>
              </div>
              <p className="text-slate-400 mb-6 pl-14">Permanently delete your account and all of your content.</p>

              <div className="flex justify-end">
                <button className="px-5 py-2.5 bg-rose-500/10 hover:bg-rose-500/20 text-rose-500 border border-rose-500/20 rounded-xl font-medium transition-colors">
                  Delete Account
                </button>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}