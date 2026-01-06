import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Loader2, BarChart3, PieChart, TrendingUp, ScatterChart, Activity, Box, LayoutGrid } from 'lucide-react';
import MessageBubble from './MessageBubble';

// --- internal ChartSelector Component ---
const ChartSelector = ({ onSelect, onClose }) => {
    const chartTypes = [
        { name: 'Bar Chart', icon: BarChart3, type: 'bar chart' },
        { name: 'Line Chart', icon: TrendingUp, type: 'line chart' },
        { name: 'Pie Chart', icon: PieChart, type: 'pie chart' },
        { name: 'Area Chart', icon: Activity, type: 'area chart' },
        { name: 'Scatter Plot', icon: ScatterChart, type: 'scatter plot' },
        { name: 'Histogram', icon: BarChart3, type: 'histogram' },
        { name: 'Box Plot', icon: Box, type: 'box plot' },
        { name: 'Heatmap', icon: LayoutGrid, type: 'heatmap' },
    ];

    return (
        <div className="absolute inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-[#0b0c15] border border-white/10 rounded-2xl p-6 w-full max-w-lg shadow-2xl relative animate-in fade-in zoom-in duration-300">
                <div className="mb-6 text-center">
                    <h3 className="text-xl font-bold text-white mb-2">Select Visualization Style</h3>
                    <p className="text-sm text-slate-400">Choose how you want to see the data.</p>
                </div>

                <div className="grid grid-cols-4 gap-4">
                    {chartTypes.map((chart) => (
                        <button
                            key={chart.name}
                            onClick={() => onSelect(chart.type)}
                            className="flex flex-col items-center justify-center gap-3 p-4 rounded-xl bg-white/5 border border-white/5 hover:bg-cyan-500/10 hover:border-cyan-500/30 transition-all group"
                        >
                            <div className="p-3 rounded-full bg-white/5 group-hover:bg-cyan-500/20 text-slate-400 group-hover:text-cyan-400 transition-colors">
                                <chart.icon className="w-6 h-6" />
                            </div>
                            <span className="text-xs font-medium text-slate-300 group-hover:text-white text-center">
                                {chart.name}
                            </span>
                        </button>
                    ))}
                </div>

                <div className="mt-6 text-center">
                    <button
                        onClick={onClose}
                        className="text-xs text-slate-500 hover:text-white underline"
                    >
                        Cancel / Let AI Decide
                    </button>
                </div>
            </div>
        </div>
    );
};

const ChatInterface = ({ isWorkspaceMode, onPlotGenerated }) => {
    const [messages, setMessages] = useState([
        {
            role: 'assistant',
            content: "Hello! I am ready to analyze your loaded document. Ask me anything about the data."
        }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [showPicker, setShowPicker] = useState(false);
    const [pendingQuery, setPendingQuery] = useState('');

    const bottomRef = useRef(null);

    const scrollToBottom = () => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (overrideInput = null) => {
        const textToSend = overrideInput || input;

        if (!textToSend.trim() || loading) return;

        // Intent Detection for Visualization
        // If it contains 'visualize', 'plot', 'graph', 'chart' AND DOES NOT specify a type, show picker.
        // Simple heuristic: if it mentions 'visualize' but not 'bar', 'line', 'pie' etc.
        const lowerInput = textToSend.toLowerCase();
        const visualizationKeywords = ['visualize', 'plot', 'graph', 'chart', 'trend'];
        const chartTypes = ['bar', 'line', 'pie', 'scatter', 'box', 'area', 'hist', 'heat'];

        const isVizRequest = visualizationKeywords.some(kw => lowerInput.includes(kw));
        const hasSpecificType = chartTypes.some(type => lowerInput.includes(type));

        // If user is just asking to visualize and hasn't picked, show picker.
        // We check overrideInput to prevent loop if calling recursively.
        if (isVizRequest && !hasSpecificType && !overrideInput && !showPicker) {
            setPendingQuery(textToSend);
            setShowPicker(true);
            return;
        }

        // Proceed to send
        const userMessage = { role: 'user', content: textToSend };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        try {
            // Call API
            const response = await axios.post('http://127.0.0.1:8000/api/analyze', {
                query: textToSend
            });

            const data = response.data;

            const aiMessage = {
                role: 'assistant',
                content: data.result,
                confidence: data.confidence,
                metadata: data.metadata,
                time_taken: data.time_taken
            };

            if (data.metadata?.plot) {
                onPlotGenerated && onPlotGenerated(data.metadata.plot);
            } else if (data.metadata?.image) {
                // Fallback for older image format (if any)
                onPlotGenerated && onPlotGenerated({ type: 'image', data: data.metadata.image });
            }

            setMessages(prev => [...prev, aiMessage]);

        } catch (error) {
            console.error(error);
            const errorMessage = {
                role: 'assistant',
                content: "> ⚠️ **System Error**\n\nI encountered an issue connecting to the Cortex Core. Please ensure the backend is running."
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    const handleChartSelect = (chartType) => {
        setShowPicker(false);
        const finalQuery = `${pendingQuery} as a ${chartType}`;
        handleSend(finalQuery); // Recursively call with modified query
        setPendingQuery('');
    };

    const handleCancelPicker = () => {
        setShowPicker(false);
        handleSend(pendingQuery); // Send original query
        setPendingQuery('');
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="flex flex-col h-full mx-auto relative px-4 md:px-8 max-w-4xl">

            {showPicker && (
                <ChartSelector onSelect={handleChartSelect} onClose={handleCancelPicker} />
            )}

            {/* Messages Area */}
            <div className="flex-1 space-y-6 pb-4 pt-6 overflow-y-auto scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent pr-4">
                {messages.map((msg, idx) => (
                    <MessageBubble key={idx} message={msg} />
                ))}

                {loading && (
                    <div className="flex w-full gap-6 p-6 rounded-2xl bg-white/5 border border-white/5 animate-pulse items-center">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-cyan-900/50 to-blue-900/50 ring-1 ring-white/10" />
                        <div className="flex-1 space-y-3 py-2">
                            <div className="flex gap-2">
                                <div className="w-2 h-2 rounded-full bg-cyan-500 animate-bounce" style={{ animationDelay: '0ms' }} />
                                <div className="w-2 h-2 rounded-full bg-cyan-500 animate-bounce" style={{ animationDelay: '150ms' }} />
                                <div className="w-2 h-2 rounded-full bg-cyan-500 animate-bounce" style={{ animationDelay: '300ms' }} />
                            </div>
                            <div className="text-xs text-cyan-500 font-medium">Cortex is thinking...</div>
                        </div>
                    </div>
                )}
                <div ref={bottomRef} />
            </div>

            {/* Input Area */}
            <div className="sticky bottom-0 pb-6 pt-6 bg-gradient-to-t from-[#050510] via-[#050510] to-transparent">
                <div className="relative group">
                    <div className="absolute -inset-0.5 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-2xl opacity-20 group-hover:opacity-40 transition duration-500 blur"></div>
                    <div className="relative flex items-end gap-3 p-2 md:p-3 rounded-2xl bg-black/40 backdrop-blur-xl border border-white/10 shadow-2xl">

                        {/* Text Input */}
                        <textarea
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder="Ask Genorai Cortex to analyze..."
                            className="flex-1 bg-transparent border-none focus:ring-0 text-slate-100 placeholder-slate-500 resize-none max-h-32 py-3 px-4 md:text-base text-sm font-medium"
                            rows={1}
                            style={{ minHeight: '44px' }}
                        />

                        {/* Send Button */}
                        <button
                            onClick={() => handleSend()}
                            disabled={loading || !input.trim()}
                            className="p-3 bg-gradient-to-br from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white rounded-xl transition-all disabled:opacity-50 disabled:grayscale shadow-lg shadow-cyan-500/20 group-hover:shadow-cyan-500/40"
                        >
                            {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
                        </button>
                    </div>
                </div>
                <div className="text-center mt-3">
                    <p className="text-[10px] text-slate-500 tracking-wider uppercase font-medium">
                        Genorai Cortex v3.0 • Elite Tier Analytics
                    </p>
                </div>
            </div>
        </div>
    );
};

export default ChatInterface;
