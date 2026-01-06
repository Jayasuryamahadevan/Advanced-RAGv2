import React, { useState } from 'react';
import ChatInterface from './ChatInterface';
import AnalysisDashboard from './AnalysisDashboard';
import { ArrowLeft, FileText, LayoutDashboard } from 'lucide-react';

const Workspace = ({ fileData, onBack }) => {
    const [latestPlot, setLatestPlot] = useState(null);

    return (
        <div className="h-screen w-full bg-[#050510] flex overflow-hidden relative font-sans">
            {/* Background */}
            <div className="fixed inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 pointer-events-none mix-blend-soft-light"></div>

            {/* Left: Chat (60%) */}
            <div className="flex-1 flex flex-col h-full border-r border-white/5 relative z-10">
                {/* Minimal Header */}
                <div className="h-16 border-b border-white/5 flex items-center justify-between px-6 bg-black/20 backdrop-blur-sm">
                    <div className="flex items-center gap-4">
                        <button
                            onClick={onBack}
                            className="p-2 -ml-2 rounded-full hover:bg-white/5 text-slate-400 hover:text-white transition-colors"
                        >
                            <ArrowLeft className="w-5 h-5" />
                        </button>
                        <div>
                            <h1 className="text-sm font-bold text-white flex items-center gap-2">
                                <FileText className="w-4 h-4 text-cyan-400" />
                                {fileData?.filename}
                            </h1>
                            <p className="text-[10px] text-slate-500 uppercase tracking-widest">Active Session</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-green-500/10 border border-green-500/20">
                        <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                        <span className="text-xs font-medium text-green-400">Cortex Online</span>
                    </div>
                </div>

                <div className="flex-1 overflow-hidden">
                    <ChatInterface
                        isWorkspaceMode={true}
                        onPlotGenerated={setLatestPlot}
                    />
                </div>
            </div>

            {/* Right: Dashboard (45%) */}
            <div className="w-[45%] hidden xl:block h-full bg-black relative z-10 border-l border-white/5">
                <AnalysisDashboard fileCheck={fileData} latestPlot={latestPlot} />
            </div>
        </div>
    );
};

export default Workspace;
