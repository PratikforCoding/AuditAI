"use client";
import React, { useState } from "react";
import { Cloud, Plus, Trash2, Eye, EyeOff, CheckCircle2, AlertCircle } from "lucide-react";

export default function GcpCredentialsManager() {
    // Mock Data
    const [credentials, setCredentials] = useState([
        { id: "gcp_1", name: "Prod Analytics", projectId: "audit-ai-prod", status: "Verified", added: "2025-11-10" },
    ]);

    // Form State
    const [isAdding, setIsAdding] = useState(false);
    const [formData, setFormData] = useState({ name: "", projectId: "", key: "" });
    const [showKey, setShowKey] = useState(false);
    const [isVerifying, setIsVerifying] = useState(false);

    const handleAddClick = () => {
        setIsAdding(true);
        setFormData({ name: "", projectId: "", key: "" });
    };

    const handleCancel = () => {
        setIsAdding(false);
        setShowKey(false);
    };

    const handleSave = async () => {
        if (!formData.name || !formData.projectId || !formData.key) {
            alert("Please fill in all fields.");
            return;
        }

        setIsVerifying(true);
        // Simulate API verification
        await new Promise(resolve => setTimeout(resolve, 1500));
        setIsVerifying(false);

        const newCred = {
            id: `gcp_${Date.now()}`,
            name: formData.name,
            projectId: formData.projectId,
            status: "Verified", // Assuming verification passes
            added: new Date().toISOString().split('T')[0]
        };

        setCredentials([...credentials, newCred]);
        setIsAdding(false);
    };

    const handleDelete = (id) => {
        if (confirm("Are you sure you want to remove these credentials? AuditAI will lose access to analyze this project.")) {
            // Simulate deletion
            setCredentials(credentials.filter(c => c.id !== id));
        }
    };

    return (
        <div className="bg-card border border-border-light rounded-xl p-6 shadow-sm mt-8">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
                <div>
                    <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
                        <Cloud className="w-5 h-5 text-blue-400" />
                        GCP Service Account Credentials
                    </h3>
                    <p className="text-sm text-neutral-400 mt-1">
                        Provide Service Account keys to allow AuditAI to analyze your Google Cloud resources.
                    </p>
                </div>
                {!isAdding && (
                    <button
                        onClick={handleAddClick}
                        className="flex items-center px-4 py-2 bg-neutral-800 hover:bg-neutral-700 text-white rounded-lg text-sm font-medium transition-all border border-neutral-700 hover:border-neutral-600"
                    >
                        <Plus className="w-4 h-4 mr-2" />
                        Add Credentials
                    </button>
                )}
            </div>

            {isAdding && (
                <div className="mb-8 p-6 bg-[#1a1a1a] border border-neutral-800 rounded-xl animate-in fade-in slide-in-from-top-2">
                    <h4 className="text-base font-semibold text-foreground mb-4">Add New Service Account Key</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                        <div>
                            <label className="block text-xs font-medium text-neutral-500 mb-1">Friendly Name</label>
                            <input
                                type="text"
                                placeholder="e.g. Staging Cluster"
                                value={formData.name}
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                className="w-full bg-neutral-900 border border-neutral-800 rounded-lg px-3 py-2 text-sm text-foreground focus:ring-1 focus:ring-blue-500 outline-none"
                            />
                        </div>
                        <div>
                            <label className="block text-xs font-medium text-neutral-500 mb-1">GCP Project ID</label>
                            <input
                                type="text"
                                placeholder="e.g. my-project-id-123"
                                value={formData.projectId}
                                onChange={(e) => setFormData({ ...formData, projectId: e.target.value })}
                                className="w-full bg-neutral-900 border border-neutral-800 rounded-lg px-3 py-2 text-sm text-foreground focus:ring-1 focus:ring-blue-500 outline-none"
                            />
                        </div>
                    </div>
                    <div className="mb-6">
                        <label className="block text-xs font-medium text-neutral-500 mb-1">
                            Service Account JSON Key
                            <span className="ml-1 text-neutral-600">(Content of the JSON file)</span>
                        </label>
                        <div className="relative">
                            <textarea
                                placeholder='{"type": "service_account", "project_id": "..."}'
                                rows={4}
                                value={formData.key}
                                onChange={(e) => setFormData({ ...formData, key: e.target.value })}
                                className="w-full bg-neutral-900 border border-neutral-800 rounded-lg px-3 py-2 text-sm text-foreground font-mono focus:ring-1 focus:ring-blue-500 outline-none resize-none"
                            />
                        </div>
                    </div>

                    <div className="flex justify-end gap-3">
                        <button
                            onClick={handleCancel}
                            className="px-4 py-2 text-sm font-medium text-neutral-400 hover:text-white transition-colors"
                        >
                            Cancel
                        </button>
                        <button
                            onClick={handleSave}
                            disabled={isVerifying}
                            className={`flex items-center px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm font-medium transition-all ${isVerifying ? "opacity-70 cursor-not-allowed" : ""}`}
                        >
                            {isVerifying ? (
                                <>
                                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></div>
                                    Verifying...
                                </>
                            ) : (
                                "Verify & Save"
                            )}
                        </button>
                    </div>
                </div>
            )}

            <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="border-b border-neutral-800 text-xs text-neutral-500 uppercase tracking-wider">
                            <th className="pb-3 pl-2">Name</th>
                            <th className="pb-3">Project ID</th>
                            <th className="pb-3">Status</th>
                            <th className="pb-3">Added On</th>
                            <th className="pb-3 pr-2 text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-neutral-800">
                        {credentials.length > 0 ? (
                            credentials.map((cred) => (
                                <tr key={cred.id} className="group hover:bg-[#1a1a1a] transition-colors">
                                    <td className="py-3 pl-2 text-sm font-medium text-foreground">{cred.name}</td>
                                    <td className="py-3 text-sm font-mono text-neutral-400">{cred.projectId}</td>
                                    <td className="py-3">
                                        <span className="flex items-center gap-1.5 text-green-500 text-xs font-medium bg-green-500/10 px-2 py-0.5 rounded border border-green-500/20 w-fit">
                                            <CheckCircle2 className="w-3 h-3" /> {cred.status}
                                        </span>
                                    </td>
                                    <td className="py-3 text-sm text-neutral-500">{cred.added}</td>
                                    <td className="py-3 pr-2 text-right">
                                        <button
                                            onClick={() => handleDelete(cred.id)}
                                            className="text-xs font-medium text-neutral-500 hover:text-red-400 transition-colors"
                                            title="Delete Credentials"
                                        >
                                            <Trash2 className="w-4 h-4" />
                                        </button>
                                    </td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan={5} className="py-8 text-center text-neutral-500 text-sm">
                                    No GCP credentials added yet. Add one to start analyzing.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
