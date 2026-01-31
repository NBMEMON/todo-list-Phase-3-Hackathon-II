import { Inter, Outfit } from 'next/font/google';
import { ThemeProvider } from '@/providers/theme-provider';
import { AuthProvider } from '@/contexts/AuthContext';
import '@/styles/globals.css';
import type { Metadata } from 'next';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });
const outfit = Outfit({ subsets: ['latin'], variable: '--font-outfit' });

export const metadata: Metadata = {
  title: 'FlowForge - Premium Todo Application',
  description: 'Elevate your productivity with our premium todo list experience',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${outfit.variable} font-sans antialiased bg-[#020617] text-slate-200 selection:bg-indigo-500/30`}>
        <ThemeProvider>
          <AuthProvider>
            <div className="fixed inset-0 z-[-1] bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.3),rgba(255,255,255,0))]pointer-events-none" />
            {children}
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}