import React from 'react';
import ReactMarkdown from 'react-markdown';
import { User, Bot } from 'lucide-react';
import { cn } from '../lib/utils';

const MessageBubble = ({ message }) => {
    const isAi = message.role === 'assistant';

    return (
        <div className={cn(
            "flex w-full gap-6 p-6 rounded-2xl transition-all duration-500 hover:bg-white/[0.02]",
            isAi ? "bg-gradient-to-r from-white/[0.03] to-transparent border border-white/5" : "bg-transparent flex-row-reverse"
        )}>
            {/* Avatar */}
            <div className="flex-shrink-0">
                <div className={cn(
                    "w-10 h-10 rounded-xl flex items-center justify-center ring-1 ring-white/20 shadow-lg relative overflow-hidden",
                    isAi
                        ? "bg-gradient-to-br from-cyan-600 to-blue-700 shadow-cyan-500/20"
                        : "bg-gradient-to-br from-indigo-500 to-purple-600 shadow-purple-500/20"
                )}>
                    <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent" />
                    {isAi
                        ? <Bot className="w-6 h-6 text-white relative z-10" />
                        : <User className="w-6 h-6 text-white relative z-10" />
                    }
                </div>
            </div>

            {/* Content */}
            <div className={cn("flex-1 overflow-hidden", !isAi && "text-right")}>
                <div className={cn("flex items-center gap-2 mb-2", !isAi && "justify-end")}>
                    <span className="text-sm font-bold tracking-wide text-slate-200">
                        {isAi ? 'Genorai Cortex' : 'You'}
                    </span>
                    <span className="text-[10px] text-slate-500 uppercase tracking-widest font-medium">
                        {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                </div>

                <div className={cn(
                    "prose prose-invert prose-p:leading-relaxed prose-pre:bg-[#0a0a15] prose-pre:border prose-pre:border-white/10 max-w-none text-slate-300",
                    !isAi && "bg-blue-600/10 inline-block px-5 py-3 rounded-2xl rounded-tr-none border border-blue-500/10 text-left"
                )}>
                    <ReactMarkdown components={{
                        code({ node, inline, className, children, ...props }) {
                            return !inline ? (
                                <div className="relative group">
                                    <div className="absolute -inset-2 bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-lg blur opacity-0 group-hover:opacity-100 transition duration-500"></div>
                                    <code className={className} {...props}>
                                        {children}
                                    </code>
                                </div>
                            ) : (
                                <code className="bg-white/10 px-1.5 py-0.5 rounded text-cyan-200 font-mono text-xs" {...props}>
                                    {children}
                                </code>
                            )
                        }
                    }}>
                        {message.content}
                    </ReactMarkdown>
                </div>

                {/* Metadata / Footer (only for AI) */}
                {isAi && message.metadata && (
                    <div className="mt-4 pt-3 border-t border-white/5 flex flex-wrap gap-4 text-xs font-medium text-slate-500">
                        {message.confidence && (
                            <div className="flex items-center gap-1.5 px-2 py-1 rounded-full bg-green-500/10 border border-green-500/20 text-green-400">
                                <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                                <span>{(message.confidence * 100).toFixed(0)}% Confidence</span>
                            </div>
                        )}
                        {message.time_taken && (
                            <div className="flex items-center gap-1.5 px-2 py-1 rounded-full bg-slate-800 border border-white/5">
                                <div className="w-1.5 h-1.5 rounded-full bg-slate-400" />
                                <span>{message.time_taken.toFixed(2)}s processing</span>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

export default MessageBubble;
