import React from 'react';
import { Bot, FileText, Settings, History, Plus } from 'lucide-react';
import { cn } from '../lib/utils';

const Sidebar = () => {
    const [active, setActive] = React.useState('chat');

    const navItems = [
        { id: 'chat', icon: Bot, label: 'Cortex Chat' },
        { id: 'history', icon: History, label: 'History' },
        { id: 'files', icon: FileText, label: 'Knowledge Base' },
        { id: 'settings', icon: Settings, label: 'Settings' },
    ];

    return (
        <div className="w-16 md:w-64 h-full border-r border-white/5 bg-black/20 backdrop-blur-xl flex flex-col transition-all duration-300">
            {/* Brand */}
            <div className="h-16 flex items-center justify-center md:justify-start md:px-6 border-b border-white/5">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
                    <Bot className="w-5 h-5 text-white" />
                </div>
                <span className="hidden md:block ml-3 font-bold text-lg tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
                    Genorai
                </span>
            </div>

            {/* New Chat Button */}
            <div className="p-4">
                <button className="w-full flex items-center justify-center md:justify-start gap-3 px-0 md:px-4 py-3 bg-primary/10 hover:bg-primary/20 text-primary rounded-xl transition-all border border-primary/20 group">
                    <Plus className="w-5 h-5" />
                    <span className="hidden md:block font-medium">New Analysis</span>
                </button>
            </div>

            {/* Navigation */}
            <nav className="flex-1 px-3 py-6 space-y-1">
                {navItems.map((item) => (
                    <button
                        key={item.id}
                        onClick={() => setActive(item.id)}
                        className={cn(
                            "w-full flex items-center justify-center md:justify-start gap-4 px-0 md:px-4 py-3.5 rounded-xl transition-all duration-300 relative group",
                            active === item.id
                                ? "bg-gradient-to-r from-blue-600/10 to-cyan-600/10 text-white shadow-[0_0_20px_rgba(59,130,246,0.15)] border border-blue-500/20"
                                : "text-slate-400 hover:text-white hover:bg-white/5"
                        )}
                    >
                        {active === item.id && (
                            <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-cyan-400 rounded-r-full shadow-[0_0_10px_cyan]" />
                        )}
                        <item.icon className={cn(
                            "w-5 h-5 transition-all duration-300",
                            active === item.id ? "text-cyan-400 scale-110" : "text-slate-500 group-hover:text-slate-300"
                        )} />
                        <span className={cn(
                            "hidden md:block font-medium tracking-wide text-sm",
                            active === item.id ? "text-cyan-50" : ""
                        )}>{item.label}</span>
                    </button>
                ))}
            </nav>
            {/* User / Footer */}
            <div className="p-4 border-t border-white/5">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-purple-500 to-pink-500 ring-2 ring-white/10" />
                    <div className="hidden md:block">
                        <p className="text-sm font-medium text-white">Elite User</p>
                        <p className="text-xs text-gray-500">Pro Plan</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Sidebar;
