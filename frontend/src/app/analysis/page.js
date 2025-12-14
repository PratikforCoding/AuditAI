"use client";
import React, { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Sparkles, AlertCircle, FileText } from "lucide-react";
import useAgentStore from "@/store/useAgentStore";
import DashboardHeader from "@/components/dashboard-components/DashboardHeader";

const AnalysisPage = () => {
    const {
        analyzeInfrastructure,
        interactiveChat,
        chatHistory,
        isLoading,
        analysisResult
    } = useAgentStore();

    const [query, setQuery] = useState("");
    // Use stored project ID or default
    const [projectId, setProjectId] = useState("my-project-123");
    // Ideally fetch from onboarding store if available
    // const { status } = useOnboardingStore(); 
    // useEffect(() => { if(status?.project_id) setProjectId(status.project_id) }, [status]);

    const chatEndRef = useRef(null);

    const scrollToBottom = () => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [chatHistory, analysisResult]);

    const handleAnalyze = async () => {
        if (!query.trim()) return;
        await analyzeInfrastructure(projectId, query);
        setQuery("");
    };

    const handleChat = async () => {
        if (!query.trim()) return;
        const currentQuery = query;
        setQuery("");
        await interactiveChat(currentQuery);
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleChat();
        }
    };

    return (
        <div className="min-h-screen bg-background text-foreground flex flex-col">
            <DashboardHeader title="Agent Analysis" userName="User" />

            <div className="flex-1 max-w-6xl w-full mx-auto p-4 flex flex-col md:flex-row gap-6 h-[calc(100vh-100px)]">

                {/* Main Analysis Panel - scrollable */}
                <div className="flex-1 bg-card border border-border/50 rounded-xl overflow-hidden flex flex-col shadow-lg">
                    <div className="p-4 border-b border-border/50 bg-white/5 flex justify-between items-center">
                        <h2 className="font-semibold flex items-center">
                            <Sparkles className="w-5 h-5 text-accent-light mr-2" />
                            Infrastructure Analysis
                        </h2>
                        {/* Example action to generate report */}
                        <button className="text-xs flex items-center bg-white/10 px-3 py-1.5 rounded-full hover:bg-white/20 transition-colors">
                            <FileText className="w-3 h-3 mr-1" />
                            Generate Report
                        </button>
                    </div>

                    <div className="flex-1 overflow-y-auto p-6 space-y-6">
                        {/* If no analysis yet, show empty state or intro */}
                        {!analysisResult && chatHistory.length === 0 && (
                            <div className="text-center text-text-muted mt-20">
                                <Bot className="w-16 h-16 mx-auto mb-4 opacity-20" />
                                <h3 className="text-xl font-medium mb-2">Ask AuditAI anything about your infrastructure</h3>
                                <p className="max-w-md mx-auto">
                                    "How can I reduce my compute costs?" <br />
                                    "Are there any security vulnerabilities?"
                                </p>
                            </div>
                        )}

                        {/* Display Analysis Result if exists */}
                        {analysisResult && (
                            <div className="bg-accent-dark/5 border border-accent-dark/20 rounded-lg p-6">
                                <h3 className="text-lg font-bold text-accent-light mb-4">Analysis Result</h3>
                                <div className="prose prose-invert max-w-none text-sm">
                                    {/* Ideally render Markdown here */}
                                    <pre className="whitespace-pre-wrap font-sans text-text-secondary">
                                        {analysisResult.analysis}
                                    </pre>
                                </div>
                            </div>
                        )}

                        {/* Chat History */}
                        {chatHistory.map((msg, idx) => (
                            <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                {msg.role !== 'user' && (
                                    <div className="w-8 h-8 rounded-full bg-accent-dark/20 flex items-center justify-center shrink-0">
                                        <Bot className="w-5 h-5 text-accent-light" />
                                    </div>
                                )}

                                <div className={`max-w-[80%] rounded-2xl px-5 py-3 ${msg.role === 'user'
                                    ? 'bg-accent-dark text-white rounded-br-sm'
                                    : 'bg-white/5 text-text-secondary border border-border/50 rounded-bl-sm'
                                    }`}>
                                    <p className="whitespace-pre-wrap text-sm">{msg.content}</p>
                                </div>

                                {msg.role === 'user' && (
                                    <div className="w-8 h-8 rounded-full bg-pink-500/20 flex items-center justify-center shrink-0">
                                        <User className="w-5 h-5 text-pink-400" />
                                    </div>
                                )}
                            </div>
                        ))}

                        {isLoading && (
                            <div className="flex items-center gap-2 text-text-muted text-sm ml-12">
                                <div className="w-2 h-2 bg-accent-light rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                <div className="w-2 h-2 bg-accent-light rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                <div className="w-2 h-2 bg-accent-light rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                            </div>
                        )}
                        <div ref={chatEndRef} />
                    </div>

                    {/* Input Area */}
                    <div className="p-4 border-t border-border/50 bg-background/50 backdrop-blur-sm">
                        <div className="relative">
                            <textarea
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                                onKeyDown={handleKeyDown}
                                placeholder="Type your query here..."
                                className="w-full bg-card border border-border rounded-xl pl-4 pr-12 py-3 focus:ring-2 focus:ring-accent-dark/50 focus:border-accent-dark outline-none resize-none h-[60px]"
                            />
                            <button
                                onClick={handleChat}
                                disabled={isLoading || !query.trim()}
                                className="absolute right-3 top-3 p-2 bg-accent-dark hover:bg-accent-light text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                <Send className="w-4 h-4" />
                            </button>
                        </div>
                    </div>
                </div>

                {/* Sidebar - could be suggestions or history */}
                <div className="hidden md:block w-80 space-y-4">
                    {/* Suggestions Panel */}
                    <div className="bg-card border border-border/50 rounded-xl p-4 shadow-lg h-full flex flex-col">
                        <h3 className="font-semibold text-text-secondary mb-4 flex items-center">
                            <Sparkles className="w-4 h-4 mr-2" />
                            Suggested Queries
                        </h3>
                        <div className="space-y-2 flex-1 overflow-y-auto">
                            {[
                                "Analyze my compute costs for last 30 days",
                                "Find idle instances in production",
                                "Check for security groups with open ports",
                                "Generate a cost optimization report"
                            ].map((suggestion, i) => (
                                <button
                                    key={i}
                                    onClick={() => {
                                        // setQuery(suggestion);
                                        // handleChat(suggestion); // simplified logic
                                    }}
                                    className="w-full text-left p-3 rounded-lg bg-white/5 hover:bg-white/10 text-sm text-text-muted hover:text-foreground transition-colors border border-transparent hover:border-border/50"
                                >
                                    {suggestion}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default AnalysisPage;
