"use client";
import React, { useState } from "react";
import { RefreshCw, User2, LogOut } from "lucide-react";

/**
 * Reusable Header for Dashboard pages (Overview, Analytics, etc.)
 * @param {Object} props
 * @param {string} props.title - The main title text (e.g., "Dashboard", "Analytics")
 * @param {string} props.userName - Name of the user to display greetings
 * @param {Function} props.onRefresh - Handler for refresh button
 * @param {boolean} props.isRefreshing - Loading state for refresh button
 */
const DashboardHeader = ({
    title = "Dashboard",
    userName = "User",
    onRefresh,
    isRefreshing = false,
}) => {
    return (
        <header className="flex justify-between items-center pb-6 border-b border-border-light mb-6">
            <h1 className="text-3xl font-extrabold text-foreground">
                Audit<span className="text-accent-dark mr-3">AI</span>
                {title}
            </h1>
            <div className="flex items-center space-x-4">
                <p className="hidden md:block text-lg font-medium text-foreground">
                    Hello, {userName}!
                </p>

                {/* Refresh Button */}
                {onRefresh && (
                    <button
                        onClick={onRefresh}
                        disabled={isRefreshing}
                        className={`p-2 rounded-full border border-neutral-800 bg-[#080808] text-pink-400 hover:bg-neutral-800 transition-duration-200 ${isRefreshing
                                ? "opacity-70 cursor-not-allowed"
                                : "hover:border-accent-light"
                            }`}
                        title="Refresh Data"
                    >
                        <RefreshCw
                            className={`w-5 h-5 ${isRefreshing ? "animate-spin" : ""
                                }`}
                        />
                    </button>
                )}

                {/* User Profile/Dropdown Placeholder */}
                <div className="relative group">
                    <button className="flex items-center p-2 rounded-full border border-border-light bg-accent-dark text-foreground hover:bg-accent-light duration-200">
                        <User2 className="w-5 h-5" />
                    </button>
                    {/* Mock Dropdown Menu */}
                    <div className="absolute right-0 mt-2 w-48 bg-[#1A1A1A] border border-neutral-800 rounded-lg shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-10">
                        <a
                            href="#"
                            onClick={(e) => {
                                e.preventDefault();
                                console.log("View Profile clicked");
                            }}
                            className="flex items-center px-4 py-2 text-neutral-300 hover:bg-neutral-800 rounded-t-lg"
                        >
                            <User2 className="w-4 h-4 mr-2" /> Profile
                        </a>
                        <a
                            href="#"
                            onClick={(e) => {
                                e.preventDefault();
                                console.log("Logout clicked");
                            }}
                            className="flex items-center px-4 py-2 text-red-400 hover:bg-red-900/30 rounded-b-lg border-t border-neutral-800"
                        >
                            <LogOut className="w-4 h-4 mr-2" /> Logout
                        </a>
                    </div>
                </div>
            </div>
        </header>
    );
};

export default DashboardHeader;
