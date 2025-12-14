"use client";
import React, { useState } from "react";
import { Upload, FileJson, CheckCircle, AlertTriangle, ArrowRight, Loader2 } from "lucide-react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import useOnboardingStore from "@/store/useOnboardingStore";

const OnboardingPage = () => {
    const router = useRouter();
    const {
        validateCredentials,
        uploadServiceAccount,
        isLoading,
        validationResult
    } = useOnboardingStore();

    const [file, setFile] = useState(null);
    const [projectId, setProjectId] = useState("");
    const [error, setError] = useState("");

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
            setError("");
            // Reset validation when file changes
        }
    };

    const handleValidate = async () => {
        if (!file || !projectId) {
            setError("Please provide both Project ID and Service Account File.");
            return;
        }
        await validateCredentials(projectId, file);
    };

    const handleUpload = async () => {
        if (!file || !projectId) {
            setError("Please provide both Project ID and Service Account File.");
            return;
        }

        // If not already validated (optional check), user can assume validate first or direct upload
        // The API flow suggests validate -> upload
        if (!validationResult?.is_valid) {
            setError("Please validate credentials successfully before uploading.");
            return;
        }

        const success = await uploadServiceAccount(projectId, file);
        if (success) {
            router.push("/dashboard");
        } else {
            setError("Failed to upload credentials. Please try again.");
        }
    };

    return (
        <div className="min-h-screen bg-background flex flex-col items-center justify-center p-4">
            <div className="w-full max-w-2xl bg-card border border-border/50 rounded-xl p-8 shadow-xl">
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-foreground mb-2">Connect Google Cloud</h1>
                    <p className="text-text-muted">Upload your Service Account Key to start auditing.</p>
                </div>

                <div className="space-y-6">
                    {/* Project ID Input */}
                    <div>
                        <label className="block text-sm font-medium text-text-secondary mb-2">Google Cloud Project ID</label>
                        <input
                            type="text"
                            className="w-full px-4 py-3 bg-background border border-border rounded-lg focus:ring-2 focus:ring-accent-dark focus:border-transparent outline-none text-foreground placeholder:text-text-muted/50"
                            placeholder="e.g. my-awesome-project-123"
                            value={projectId}
                            onChange={(e) => setProjectId(e.target.value)}
                        />
                    </div>

                    {/* File Upload Area */}
                    <div className="border-2 border-dashed border-border rounded-xl p-8 text-center hover:bg-white/5 transition-colors cursor-pointer relative">
                        <input
                            type="file"
                            accept=".json"
                            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                            onChange={handleFileChange}
                        />
                        <div className="flex flex-col items-center">
                            {file ? (
                                <FileJson className="w-12 h-12 text-accent-light mb-4" />
                            ) : (
                                <Upload className="w-12 h-12 text-text-muted mb-4" />
                            )}

                            <p className="text-lg font-medium text-foreground">
                                {file ? file.name : "Drop your service-account.json here"}
                            </p>
                            <p className="text-sm text-text-muted mt-2">
                                {file ? `${(file.size / 1024).toFixed(2)} KB` : "or click to browse"}
                            </p>
                        </div>
                    </div>

                    {/* Error Message */}
                    {error && (
                        <div className="p-3 bg-red-900/20 text-red-200 rounded-lg text-sm border border-red-800/50 flex items-center">
                            <AlertTriangle className="w-4 h-4 mr-2 shrink-0" />
                            {error}
                        </div>
                    )}

                    {/* Validation Results */}
                    {validationResult && (
                        <div className={`p-4 rounded-lg border ${validationResult.is_valid ? 'bg-green-900/10 border-green-800/50' : 'bg-yellow-900/10 border-yellow-800/50'}`}>
                            <div className="flex items-center mb-2">
                                {validationResult.is_valid ? (
                                    <CheckCircle className="w-5 h-5 text-green-400 mr-2" />
                                ) : (
                                    <AlertTriangle className="w-5 h-5 text-yellow-400 mr-2" />
                                )}
                                <h3 className={`font-semibold ${validationResult.is_valid ? 'text-green-400' : 'text-yellow-400'}`}>
                                    {validationResult.is_valid ? "Credentials Valid" : "Validation Issues Found"}
                                </h3>
                            </div>

                            {validationResult.issues?.length > 0 && (
                                <ul className="list-disc list-inside text-sm text-text-secondary space-y-1 ml-1">
                                    {validationResult.issues.map((issue, idx) => (
                                        <li key={idx}>{issue}</li>
                                    ))}
                                </ul>
                            )}
                        </div>
                    )}

                    {/* Actions */}
                    <div className="flex gap-4 pt-4">
                        <button
                            onClick={handleValidate}
                            disabled={isLoading || !file || !projectId}
                            className="flex-1 py-3 px-4 bg-transparent border border-accent-dark text-accent-light rounded-lg font-semibold hover:bg-accent-dark/10 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {isLoading ? <Loader2 className="w-5 h-5 animate-spin mx-auto" /> : "Validate Key"}
                        </button>

                        <button
                            onClick={handleUpload}
                            disabled={isLoading || !validationResult?.is_valid}
                            className="flex-1 py-3 px-4 bg-accent-dark text-white rounded-lg font-semibold hover:bg-accent-light transition-colors shadow-lg shadow-accent-dark/20 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                        >
                            {isLoading ? (
                                <Loader2 className="w-5 h-5 animate-spin" />
                            ) : (
                                <>
                                    Connect Project
                                    <ArrowRight className="w-5 h-5 ml-2" />
                                </>
                            )}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default OnboardingPage;
