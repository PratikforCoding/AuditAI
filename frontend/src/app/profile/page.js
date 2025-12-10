"use client";
import React, { useState } from "react";
import DashboardHeader from "@/components/dashboard-components/DashboardHeader";
import UserInfo from "@/components/profile/UserInfo";
import SecurityCard from "@/components/profile/SecurityCard";
import ApiKeysManager from "@/components/profile/ApiKeysManager";
import GcpCredentialsManager from "@/components/profile/GcpCredentialsManager";

export default function ProfilePage() {
    const [isRefreshing, setIsRefreshing] = useState(false);

    const handleRefresh = async () => {
        setIsRefreshing(true);
        await new Promise((resolve) => setTimeout(resolve, 1000));
        setIsRefreshing(false);
    };

    return (
        <div className="min-h-screen bg-background p-4 md:p-8 font-sans">
            <div className="max-w-7xl mx-auto">
                <DashboardHeader
                    title="Profile Settings"
                    userName="Audit User"
                    onRefresh={handleRefresh}
                    isRefreshing={isRefreshing}
                />

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Main Info Column */}
                    <div className="lg:col-span-2 space-y-8">
                        <UserInfo />
                    </div>

                    {/* Side Column */}
                    <div className="lg:col-span-1">
                        <SecurityCard />
                    </div>
                </div>

                <ApiKeysManager />
                <GcpCredentialsManager />
            </div>
        </div>
    );
}
