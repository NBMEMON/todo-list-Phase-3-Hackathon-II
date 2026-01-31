'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useTheme } from '@/providers/theme-provider';

export default function Sidebar() {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();
  const { theme } = useTheme();

  const navItems = [
    { name: 'Dashboard', href: '/dashboard', icon: '📊' },
    { name: 'Tasks', href: '/dashboard/tasks', icon: '✅' },
    { name: 'Projects', href: '/dashboard/projects', icon: '📁' },
    { name: 'Calendar', href: '/dashboard/calendar', icon: '📅' },
    { name: 'Analytics', href: '/dashboard/analytics', icon: '📈' },
    { name: 'Settings', href: '/dashboard/settings', icon: '⚙️' },
  ];

  return (
    <>
      {/* Mobile menu button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="md:hidden fixed top-20 left-4 z-40 p-2 rounded-lg bg-slate-800/80 backdrop-blur-lg border border-white/20 text-slate-300"
        aria-label="Toggle sidebar"
      >
        ☰
      </button>

      {/* Sidebar */}
      <AnimatePresence>
        {(isOpen || window.innerWidth >= 768) && (
          <>
            {/* Overlay for mobile */}
            {isOpen && window.innerWidth < 768 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 z-30 bg-black/50 md:hidden"
                onClick={() => setIsOpen(false)}
              />
            )}

            <motion.aside
              initial={{ x: '-100%' }}
              animate={{ x: 0 }}
              exit={{ x: '-100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className={`fixed top-16 left-0 z-30 h-[calc(100vh-4rem)] w-64 bg-slate-950/50 backdrop-blur-xl border-r border-slate-800/50 transform ${isOpen ? 'translate-x-0' : '-translate-x-full'
                } md:translate-x-0 md:static md:h-auto md:w-64`}
            >
              <div className="p-4">
                <h2 className="text-lg font-semibold text-white mb-6 pl-2">Navigation</h2>

                <nav>
                  <ul className="space-y-1">
                    {navItems.map((item) => (
                      <li key={item.name}>
                        <Link
                          href={item.href}
                          className={`flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors ${pathname === item.href
                            ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/20'
                            : theme === 'dark'
                              ? 'text-slate-300 hover:bg-white/10 hover:text-white'
                              : 'text-slate-700 hover:bg-gray-200 hover:text-gray-900'
                            }`}
                        >
                          <span className="mr-3 text-lg">{item.icon}</span>
                          <span>{item.name}</span>
                        </Link>
                      </li>
                    ))}
                  </ul>
                </nav>

                <div className="mt-8 pt-6 border-t border-white/10">
                  <h3 className="px-4 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">
                    Labels
                  </h3>
                  <ul className="space-y-1">
                    <li>
                      <a
                        href="#"
                        className={`flex items-center px-4 py-2 text-sm rounded-lg transition-colors ${theme === 'dark'
                          ? 'text-slate-400 hover:bg-white/10 hover:text-white'
                          : 'text-slate-700 hover:bg-gray-200 hover:text-gray-900'
                          }`}
                      >
                        <span className="w-3 h-3 rounded-full bg-cyan-500 mr-3"></span>
                        Personal
                      </a>
                    </li>
                    <li>
                      <a
                        href="#"
                        className={`flex items-center px-4 py-2 text-sm rounded-lg transition-colors ${theme === 'dark'
                          ? 'text-slate-400 hover:bg-white/10 hover:text-white'
                          : 'text-slate-700 hover:bg-gray-200 hover:text-gray-900'
                          }`}
                      >
                        <span className="w-3 h-3 rounded-full bg-purple-500 mr-3"></span>
                        Work
                      </a>
                    </li>
                    <li>
                      <a
                        href="#"
                        className={`flex items-center px-4 py-2 text-sm rounded-lg transition-colors ${theme === 'dark'
                          ? 'text-slate-400 hover:bg-white/10 hover:text-white'
                          : 'text-slate-700 hover:bg-gray-200 hover:text-gray-900'
                          }`}
                      >
                        <span className="w-3 h-3 rounded-full bg-green-500 mr-3"></span>
                        Important
                      </a>
                    </li>
                  </ul>
                </div>
              </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>
    </>
  );
}