import React, { useState, useEffect } from 'react';
import { Wifi, Bell, Search, Zap } from 'lucide-react';
import axios from 'axios';

const Header = () => {
    const [isConnected, setIsConnected] = useState(false);

    useEffect(() => {
        const checkHealth = async () => {
            try {
                // In production, use env var. Here hardcoded to API port.
                await axios.get('http://127.0.0.1:8000/health');
                setIsConnected(true);
            } catch (error) {
                setIsConnected(false);
            }
        };

        checkHealth();
        const interval = setInterval(checkHealth, 30000); // Check every 30s
        return () => clearInterval(interval);
    }, []);

    return (
        <header className="h-16 px-6 flex items-center justify-between border-b border-white/5 bg-background/50 backdrop-blur-md sticky top-0 z-10">
            {/* Left: Breadcrumbs or Title */}
            <div className="flex items-center gap-4">
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/5 border border-white/5">
                    <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
                    <span className="text-xs font-medium text-gray-400 uppercase tracking-wider">
                        {isConnected ? 'System Online' : 'System Offline'}
                    </span>
                </div>
            </div>

            {/* Right: Actions */}
            <div className="flex items-center gap-4">
                <div className="relative hidden sm:block">
                    <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
                    <input
                        type="text"
                        placeholder="Search knowledge base..."
                        className="bg-black/20 border border-white/10 text-sm text-white pl-9 pr-4 py-2 rounded-full focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all w-64"
                    />
                </div>

                <button className="p-2 rounded-full hover:bg-white/5 text-gray-400 hover:text-white transition-colors relative">
                    <Bell className="w-5 h-5" />
                    <span className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full ring-2 ring-background" />
                </button>
            </div>
        </header>
    );
};

export default Header;
