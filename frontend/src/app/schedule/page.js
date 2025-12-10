"use client";
import React, { useState } from "react";
import DashboardHeader from "@/components/dashboard-components/DashboardHeader";
import ScheduleSection from "@/components/schedule/ScheduleSection";
import NotificationsSettings from "@/components/schedule/NotificationsSettings";
import ThresholdsSettings from "@/components/schedule/ThresholdsSettings";
import ExportSettings from "@/components/schedule/ExportSettings";
import DangerZone from "@/components/schedule/DangerZone";
import ProfileSettings from "@/components/schedule/ProfileSettings";
import { Save } from "lucide-react";

export default function SchedulePage() {
    const [isSaving, setIsSaving] = useState(false);
    const [isRefreshing, setIsRefreshing] = useState(false);

    const handleRefresh = async () => {
        setIsRefreshing(true);
        await new Promise((resolve) => setTimeout(resolve, 1000));
        setIsRefreshing(false);
    };

    const handleSaveSettings = async () => {
        setIsSaving(true);
        // Simulate API call
        await new Promise((resolve) => setTimeout(resolve, 2000));
        setIsSaving(false);
        alert("Settings saved successfully!");
    };

    return (
        <div className="min-h-screen bg-background p-4 md:p-8 font-sans">
            <div className="max-w-7xl mx-auto">
                <DashboardHeader
                    title="Settings & Preferences"
                    userName="Audit User"
                    onRefresh={handleRefresh}
                    isRefreshing={isRefreshing}
                />

                <div className="space-y-8 pb-20">
                    <p className="text-neutral-400 -mt-4 mb-4">
                        Manage your audit schedules, notification preferences, and account security.
                    </p>

                    {/* Main Settings Sections */}
                    <ProfileSettings />
                    <ScheduleSection />

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <NotificationsSettings />
                        <div className="space-y-8">
                            <ThresholdsSettings />
                            <ExportSettings />
                        </div>
                    </div>

                    <DangerZone />
                </div>

                {/* Floating Save Bar */}
                <div className="fixed bottom-6 left-0 right-0 mx-auto max-w-5xl px-4 md:px-8 z-50">
                    <div className="bg-[#141414]/90 backdrop-blur-md border border-border-light rounded-xl p-4 shadow-2xl flex items-center justify-between">
                        <span className="text-sm text-neutral-400 hidden sm:block">
                            Unsaved changes needed? Don&apos;t forget to save.
                        </span>
                        <div className="flex gap-4 w-full sm:w-auto justify-end">
                            <button className="px-5 py-2.5 text-sm font-medium text-neutral-300 hover:text-white transition-colors">
                                Cancel
                            </button>
                            <button
                                onClick={handleSaveSettings}
                                disabled={isSaving}
                                className={`flex items-center px-6 py-2.5 bg-accent-dark hover:bg-accent-light text-white rounded-lg font-medium shadow-lg hover:shadow-accent-dark/20 transition-all ${isSaving ? "opacity-70 cursor-not-allowed" : ""
                                    }`}
                            >
                                {isSaving ? (
                                    <>
                                        <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></div>
                                        Saving...
                                    </>
                                ) : (
                                    <>
                                        <Save className="w-4 h-4 mr-2" />
                                        Save Changes
                                    </>
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
