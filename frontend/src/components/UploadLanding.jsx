import React, { useRef, useState } from 'react';
import axios from 'axios';
import { Upload, FileUp, Loader2, Sparkles } from 'lucide-react';
import { cn } from '../lib/utils';

const UploadLanding = ({ onUploadSuccess }) => {
    const fileInputRef = useRef(null);
    const [isDragging, setIsDragging] = useState(false);
    const [uploading, setUploading] = useState(false);

    const handleFile = async (file) => {
        if (!file) return;

        setUploading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://127.0.0.1:8000/api/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            // Delay slightly for effect
            setTimeout(() => {
                onUploadSuccess(response.data);
            }, 800);
        } catch (error) {
            console.error(error);
            alert("Upload failed. Please check the backend.");
        } finally {
            setUploading(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        handleFile(e.dataTransfer.files[0]);
    };

    return (
        <div className="min-h-screen w-full flex flex-col items-center justify-center relative overflow-hidden bg-[#050510] text-white">
            {/* Background Effects */}
            <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 pointer-events-none mix-blend-soft-light"></div>
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-600/20 rounded-full blur-[120px] pointer-events-none animate-pulse-slow"></div>

            {/* Content */}
            <div className="relative z-10 text-center space-y-8 max-w-2xl px-4">
                <div className="space-y-2">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 backdrop-blur-md mb-4">
                        <Sparkles className="w-4 h-4 text-cyan-400" />
                        <span className="text-xs font-medium tracking-wider text-cyan-100 uppercase">Genorai Cortex v3.0</span>
                    </div>
                    <h1 className="text-5xl md:text-6xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-b from-white to-white/60">
                        Analyze Your Data
                    </h1>
                    <p className="text-lg text-slate-400 max-w-lg mx-auto leading-relaxed">
                        Upload your documents to unlock elite-tier insights, visualizations, and predictive analytics.
                    </p>
                </div>

                {/* Upload Zone */}
                <div
                    onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                    onDragLeave={() => setIsDragging(false)}
                    onDrop={handleDrop}
                    onClick={() => fileInputRef.current?.click()}
                    className={cn(
                        "group relative w-full h-64 rounded-3xl border-2 border-dashed transition-all duration-300 cursor-pointer flex flex-col items-center justify-center gap-4 bg-white/[0.02]",
                        isDragging
                            ? "border-cyan-500 bg-cyan-500/10 scale-[1.02]"
                            : "border-white/10 hover:border-white/20 hover:bg-white/5"
                    )}
                >
                    <input
                        type="file"
                        ref={fileInputRef}
                        onChange={(e) => handleFile(e.target.files[0])}
                        className="hidden"
                        accept=".csv,.xlsx,.parquet"
                    />

                    {uploading ? (
                        <div className="flex flex-col items-center gap-4 animate-in fade-in zoom-in">
                            <div className="relative">
                                <div className="w-16 h-16 rounded-full border-4 border-white/10 border-t-cyan-500 animate-spin"></div>
                                <div className="absolute inset-0 flex items-center justify-center">
                                    <FileUp className="w-6 h-6 text-white/50" />
                                </div>
                            </div>
                            <p className="text-sm font-medium text-cyan-400 animate-pulse">Processing Document...</p>
                        </div>
                    ) : (
                        <>
                            <div className="w-20 h-20 rounded-full bg-gradient-to-br from-cyan-500/10 to-blue-600/10 flex items-center justify-center group-hover:scale-110 transition-transform duration-300 ring-1 ring-white/10">
                                <Upload className="w-10 h-10 text-cyan-400 group-hover:text-cyan-300" />
                            </div>
                            <div className="space-y-1">
                                <p className="text-lg font-medium text-white group-hover:text-cyan-100">
                                    Click to upload or drag and drop
                                </p>
                                <p className="text-sm text-slate-500">
                                    Supports CSV, Excel, Parquet (Max 50MB)
                                </p>
                            </div>
                        </>
                    )}
                </div>

                {/* Footer */}
                <div className="flex items-center justify-center gap-8 text-xs text-slate-600 font-medium uppercase tracking-widest">
                    <span>Secure Encryption</span>
                    <span>•</span>
                    <span>Local Processing</span>
                    <span>•</span>
                    <span>Instant Analysis</span>
                </div>
            </div>
        </div>
    );
};

export default UploadLanding;
