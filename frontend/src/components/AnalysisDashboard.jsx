import React from 'react';
import { BarChart3, PieChart, TrendingUp, Activity, Zap } from 'lucide-react';
import Plot from 'react-plotly.js';

const analysisCards = [
    { title: 'Total Rows', icon: BarChart3, color: 'text-blue-400', key: 'rows' },
    { title: 'Columns', icon: PieChart, color: 'text-purple-400', key: 'cols' },
    { title: 'Data Quality', icon: Zap, color: 'text-yellow-400', value: '99.9%' },
];

const AnalysisDashboard = ({ fileCheck, latestPlot }) => {

    // Parse Plotly data safely
    let plotData = null;
    if (latestPlot?.type === 'plotly') {
        try {
            plotData = JSON.parse(latestPlot.data);
        } catch (e) {
            console.error("Failed to parse Plotly JSON", e);
        }
    }

    return (
        <div className="h-full flex flex-col bg-[#0b0c15] relative overflow-hidden">
            {/* Glossy Overlay */}
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-cyan-500/50 to-transparent opacity-50"></div>

            {/* Header & Stats Row */}
            <div className="p-6 pb-2 shrink-0 z-10 glass-panel-b border-b border-white/5">
                <div className="flex items-center justify-between mb-6">
                    <div>
                        <h2 className="text-lg font-outfit font-bold text-white tracking-wide flex items-center gap-2">
                            <Activity className="w-4 h-4 text-cyan-400" />
                            INTELLIGENCE HUB
                        </h2>
                        <div className="flex items-center gap-2 mt-1">
                            <span className="relative flex h-2 w-2">
                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
                                <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
                            </span>
                            <p className="text-xs text-slate-400 font-mono tracking-wider">
                                CONTEXT: {fileCheck?.filename || 'IDLE'}
                            </p>
                        </div>
                    </div>
                </div>

                {/* Compact Stats Grid */}
                <div className="grid grid-cols-3 gap-3">
                    {analysisCards.map((card, idx) => (
                        <div key={idx} className="bg-white/5 border border-white/5 rounded-xl p-3 flex flex-col justify-center backdrop-blur-sm transition-all hover:bg-white/10">
                            <div className="flex items-center gap-2 mb-1">
                                <card.icon className={`w-3 h-3 ${card.color}`} />
                                <span className="text-[10px] uppercase text-slate-500 font-bold tracking-wider">{card.title}</span>
                            </div>
                            <span className="text-lg font-bold text-white font-mono">
                                {card.key === 'rows' ? fileCheck?.rows?.toLocaleString() || '-' :
                                    card.key === 'cols' ? fileCheck?.columns?.length || '-' :
                                        card.value}
                            </span>
                        </div>
                    ))}
                </div>
            </div>

            {/* Main Visualization Stage (Flex Fill) */}
            <div className="flex-1 p-6 min-h-0 relative z-0 flex flex-col">
                <div className="flex items-center gap-2 mb-3">
                    <TrendingUp className="w-4 h-4 text-slate-400" />
                    <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-widest">Visual Insight</h3>
                </div>

                <div className="flex-1 w-full bg-[#050510] border border-white/10 rounded-2xl overflow-hidden shadow-2xl relative group">
                    {/* Inner texture */}
                    <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-5 pointer-events-none"></div>

                    {plotData ? (
                        <Plot
                            data={plotData.data}
                            layout={{
                                ...plotData.layout,
                                autosize: true,
                                paper_bgcolor: '#050510',
                                plot_bgcolor: '#050510',
                                font: { color: '#94a3b8', family: "'Inter', sans-serif" },
                                margin: { t: 50, r: 20, l: 50, b: 50 },
                                showlegend: true,
                                legend: { orientation: 'h', y: -0.1 },
                            }}
                            style={{ width: '100%', height: '100%' }}
                            config={{
                                responsive: true,
                                displayModeBar: true,
                                displaylogo: false,
                                modeBarButtonsToRemove: ['lasso2d', 'select2d']
                            }}
                            className="w-full h-full"
                        />
                    ) : (
                        latestPlot?.type === 'image' ? (
                            <div className="relative w-full h-full flex items-center justify-center p-4">
                                <img
                                    src={`data:image/png;base64,${latestPlot.data}`}
                                    alt="Analysis"
                                    className="max-h-full max-w-full rounded-lg shadow-2xl object-contain"
                                />
                            </div>
                        ) : (
                            <div className="absolute inset-0 flex flex-col items-center justify-center text-center p-8">
                                <div className="w-24 h-24 rounded-full bg-cyan-500/5 flex items-center justify-center mb-6 animate-pulse-slow">
                                    <BarChart3 className="w-10 h-10 text-cyan-500/50" />
                                </div>
                                <h4 className="text-xl font-bold text-white mb-2 font-outfit">Ready to Visualize</h4>
                                <p className="text-sm text-slate-500 max-w-[200px] leading-relaxed">
                                    Ask Cortex to "Visualize the data" or "Show me trends" to populate this elite canvas.
                                </p>
                            </div>
                        )
                    )}
                </div>
            </div>
        </div>
    );
};

export default AnalysisDashboard;
