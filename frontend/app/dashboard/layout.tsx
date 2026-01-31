import { ThemeProvider } from '@/providers/theme-provider';
import { AuthProvider } from '@/contexts/AuthContext';
import Sidebar from '@/components/sidebar';
import Header from '@/components/header';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ThemeProvider>
      <AuthProvider>
        <div className="flex h-screen bg-[#020617] overflow-hidden">
          <Sidebar />
          <div className="flex-1 flex flex-col overflow-hidden">
            <Header />
            <main className="flex-1 overflow-y-auto bg-slate-950/50 p-4 md:p-6 lg:p-8">
              {children}
            </main>
          </div>
        </div>
      </AuthProvider>
    </ThemeProvider>
  );
}