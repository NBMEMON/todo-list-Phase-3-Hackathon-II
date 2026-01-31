'use client';

import Link from 'next/link';
import { redirect } from 'next/navigation';
import { getTokens } from '@/lib/auth';
import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';

// Icons (Simulated with SVG for zero-dependency)
const CheckIcon = () => (
  <svg className="w-5 h-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
  </svg>
);

const FeatureIcon = ({ path }: { path: string }) => (
  <div className="w-12 h-12 rounded-lg bg-indigo-500/10 flex items-center justify-center mb-4 text-indigo-400">
    <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={path} />
    </svg>
  </div>
);

export default function HomePage() {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="min-h-screen bg-[#020617] text-slate-200 selection:bg-indigo-500/30">
      {/* Navigation */}
      <header className={`fixed top-0 w-full z-50 transition-all duration-300 ${isScrolled ? 'bg-slate-950/80 backdrop-blur-xl border-b border-slate-800/50' : 'bg-transparent'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <span className="text-xl font-heading font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
              FlowForge
            </span>
            <div className="flex items-center gap-4">
              <Link href="/login" className="text-sm font-medium text-slate-300 hover:text-white transition-colors">
                Log in
              </Link>
              <Link href="/register">
                <button className="px-4 py-2 text-sm font-medium bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg shadow-lg shadow-indigo-500/20 transition-all">
                  Get Started
                </button>
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[500px] bg-indigo-500/10 blur-[120px] rounded-full pointer-events-none" />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="inline-block px-3 py-1 mb-6 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-medium tracking-wide">
              REIMAGINED PRODUCTIVITY
            </div>
            <h1 className="text-5xl md:text-7xl font-heading font-bold tracking-tight text-white mb-6">
              Organize your life <br />
              <span className="bg-gradient-to-r from-indigo-400 via-purple-400 to-indigo-400 bg-clip-text text-transparent bg-[length:200%_auto] animate-gradient">
                with elegant simplicity
              </span>
            </h1>
            <p className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
              Experience a task manager designed for focus. Beautifully crafted,
              intuitively structured, and powered by modern technology to keep you in flow.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link href="/register">
                <button className="px-8 py-4 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl shadow-xl shadow-indigo-500/25 transform transition hover:scale-105 active:scale-95">
                  Start for free
                </button>
              </Link>
              <Link href="#features">
                <button className="px-8 py-4 bg-slate-800 hover:bg-slate-700 text-white font-medium rounded-xl border border-slate-700 hover:border-slate-600 transition-colors">
                  How it works
                </button>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-24 bg-slate-950/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-heading font-bold text-white mb-4">Everything you need</h2>
            <p className="text-slate-400">Powerful features wrapped in a stunning interface.</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                title: 'Smart Organization',
                desc: 'Group tasks by project, priority, or tags. Keep your workspace clean and your mind clear.',
                icon: 'M4 6h16M4 12h16M4 18h7'
              },
              {
                title: 'Focus Mode',
                desc: 'Eliminate distractions with a dedicated focus view that highlights only what matters now.',
                icon: 'M13 10V3L4 14h7v7l9-11h-7z'
              },
              {
                title: 'Real-time Sync',
                desc: 'Access your tasks from anywhere. Your data flows seamlessly across all your devices.',
                icon: 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15'
              }
            ].map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="p-8 rounded-2xl bg-slate-900 border border-slate-800 hover:border-indigo-500/30 transition-colors group"
              >
                <FeatureIcon path={feature.icon} />
                <h3 className="text-xl font-semibold text-white mb-3 group-hover:text-indigo-400 transition-colors">{feature.title}</h3>
                <p className="text-slate-400 leading-relaxed">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Workflow Section */}
      <section className="py-24 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-heading font-bold text-white mb-6">
                Designed for the <br />
                <span className="text-indigo-400">modern workflow</span>
              </h2>
              <div className="space-y-6">
                {[
                  'Capture ideas instantly with Quick Add',
                  'Prioritize tasks with drag-and-drop',
                  'Track progress with visual analytics',
                  'Collaborate with team members seamlessly'
                ].map((item, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <div className="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-500/20 flex items-center justify-center">
                      <CheckIcon />
                    </div>
                    <span className="text-slate-300">{item}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-tr from-indigo-500/20 to-purple-500/20 blur-3xl rounded-full" />
              <div className="relative bg-slate-900/50 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-6 shadow-2xl">
                {/* Mock UI */}
                <div className="space-y-4">
                  {[1, 2, 3].map((i) => (
                    <div key={i} className="flex items-center gap-4 p-4 rounded-xl bg-slate-800/50 border border-slate-700/50">
                      <div className={`w-5 h-5 rounded-full border-2 ${i === 1 ? 'bg-indigo-500 border-indigo-500' : 'border-slate-600'}`} />
                      <div className="flex-1">
                        <div className={`h-4 rounded w-3/4 ${i === 1 ? 'bg-slate-600' : 'bg-slate-300'}`} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-indigo-600/10" />
        <div className="max-w-4xl mx-auto px-4 relative z-10 text-center">
          <h2 className="text-4xl font-heading font-bold text-white mb-6">Ready to regain control?</h2>
          <p className="text-xl text-slate-300 mb-10">
            Join thousands of productive individuals who trust FlowForge to manage their day.
          </p>
          <Link href="/register">
            <button className="px-10 py-5 bg-white text-indigo-600 font-bold rounded-xl shadow-xl transform transition hover:scale-105 active:scale-95">
              Get Started for Free
            </button>
          </Link>
          <p className="mt-4 text-sm text-slate-500">No credit card required • Free forever plan available</p>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-slate-800 bg-slate-950">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div className="col-span-1 md:col-span-2">
              <span className="text-xl font-heading font-bold text-white mb-4 block">FlowForge</span>
              <p className="text-slate-500 max-w-sm">
                The premium task management solution for professionals who demand excellence.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Product</h4>
              <ul className="space-y-2 text-slate-400">
                <li><Link href="#" className="hover:text-indigo-400">Features</Link></li>
                <li><Link href="#" className="hover:text-indigo-400">Pricing</Link></li>
                <li><Link href="#" className="hover:text-indigo-400">Changelog</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Company</h4>
              <ul className="space-y-2 text-slate-400">
                <li><Link href="#" className="hover:text-indigo-400">About</Link></li>
                <li><Link href="#" className="hover:text-indigo-400">Blog</Link></li>
                <li><Link href="#" className="hover:text-indigo-400">Contact</Link></li>
              </ul>
            </div>
          </div>
          <div className="pt-8 border-t border-slate-800 text-center text-slate-600 text-sm">
            © 2024 FlowForge. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}