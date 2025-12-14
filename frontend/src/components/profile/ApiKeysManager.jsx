"use client";
import React, { useState } from "react";
import { Key, Plus, Trash2, Copy, Check } from "lucide-react";

export default function ApiKeysManager() {
    // Mock Data
    const [keys, setKeys] = useState([
        { id: "key_1", name: "Prod CI/CD", prefix: "pk_live_...", created: "2025-10-15", lastUsed: "2 mins ago" },
        { id: "key_2", name: "Dev Local", prefix: "pk_test_...", created: "2025-12-01", lastUsed: "1 day ago" },
    ]);
    const [isGenerating, setIsGenerating] = useState(false);
    const [copiedId, setCopiedId] = useState(null);

    const handleGenerate = async () => {
        setIsGenerating(true);
        await new Promise(resolve => setTimeout(resolve, 800));
        const newKey = {
            id: `key_${Date.now()}`,
            name: "New API Key",
            prefix: "pk_test_" + Math.random().toString(36).substring(7),
            created: new Date().toISOString().split('T')[0],
            lastUsed: "Never"
        };
        setKeys([newKey, ...keys]);
        setIsGenerating(false);
    };

    const handleRevoke = (id) => {
        if (confirm("Are you sure you want to revoke this API key? This action cannot be undone.")) {
            setKeys(keys.filter(k => k.id !== id));
        }
    };

    const handleCopy = (text, id) => {
        navigator.clipboard.writeText(text).then(() => {
            setCopiedId(id);
            setTimeout(() => setCopiedId(null), 2000);
        });
    };

    return (
        <div className="bg-card border border-border-light rounded-xl p-6 shadow-sm mt-8">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
                <div>
                    <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
                        <Key className="w-5 h-5 text-accent-light" />
                        API Keys
                    </h3>
                    <p className="text-sm text-neutral-400 mt-1">
                        Manage API keys for accessing the AuditAI API programmatically.
                    </p>
                </div>
                <button
                    onClick={handleGenerate}
                    disabled={isGenerating}
                    className="flex items-center px-4 py-2 bg-accent-dark hover:bg-accent-light text-white rounded-lg text-sm font-medium transition-all shadow-lg hover:shadow-accent-dark/20"
                >
                    {isGenerating ? <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2" /> : <Plus className="w-4 h-4 mr-2" />}
                    Generate New Key
                </button>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="border-b border-neutral-800 text-xs text-neutral-500 uppercase tracking-wider">
                            <th className="pb-3 pl-2">Name</th>
                            <th className="pb-3">Token Prefix</th>
                            <th className="pb-3">Created</th>
                            <th className="pb-3">Last Used</th>
                            <th className="pb-3 pr-2 text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-neutral-800">
                        {keys.length > 0 ? (
                            keys.map((key) => (
                                <tr key={key.id} className="group hover:bg-[#1a1a1a] transition-colors">
                                    <td className="py-3 pl-2 text-sm font-medium text-foreground">{key.name}</td>
                                    <td className="py-3 text-sm font-mono text-neutral-400 flex items-center gap-2">
                                        {key.prefix}
                                        <button
                                            onClick={() => handleCopy(key.prefix, key.id)}
                                            className="opacity-0 group-hover:opacity-100 transition-opacity text-neutral-500 hover:text-white"
                                            title="Copy"
                                        >
                                            {copiedId === key.id ? <Check className="w-3 h-3 text-green-500" /> : <Copy className="w-3 h-3" />}
                                        </button>
                                    </td>
                                    <td className="py-3 text-sm text-neutral-500">{key.created}</td>
                                    <td className="py-3 text-sm text-neutral-500">{key.lastUsed}</td>
                                    <td className="py-3 pr-2 text-right">
                                        <button
                                            onClick={() => handleRevoke(key.id)}
                                            className="text-xs font-medium text-red-500 hover:text-red-400 hover:underline"
                                        >
                                            Revoke
                                        </button>
                                    </td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan={5} className="py-8 text-center text-neutral-500 text-sm">
                                    No active API keys found.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
