import React from 'react';
import Sidebar from './Sidebar';
import Header from './Header';

const Layout = ({ children }) => {
    return (
        <div className="flex h-screen w-full bg-[#050510] text-foreground overflow-hidden font-sans selection:bg-cyan-500/30">
            <div className="fixed inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 pointer-events-none mix-blend-soft-light"></div>
            <div className="fixed inset-0 bg-gradient-to-br from-indigo-900/20 via-background to-cyan-900/10 pointer-events-none"></div>
            <Sidebar />
            <div className="flex-1 flex flex-col h-full min-w-0 relative z-10">
                <Header />
                <main className="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8 relative scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent">
                    {children}
                </main>
            </div>
        </div>
    );
};

export default Layout;
