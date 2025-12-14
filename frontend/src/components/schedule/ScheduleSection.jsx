"use client";
import React from "react";
import { Calendar, Clock, Globe } from "lucide-react";

export default function ScheduleSection() {
    return (
        <div className="bg-card border border-border-light rounded-xl p-6 shadow-sm">
            <h3 className="text-xl font-semibold text-foreground mb-6 flex items-center gap-2">
                <Calendar className="w-5 h-5 text-accent-light" />
                Audit Schedule
            </h3>

            <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Frequency */}
                    <div className="space-y-2">
                        <label className="block text-sm font-medium text-neutral-400">
                            Frequency
                        </label>
                        <select className="w-full bg-[#1a1a1a] border border-neutral-800 rounded-lg px-4 py-2.5 text-foreground focus:ring-2 focus:ring-accent-dark focus:border-transparent outline-none transition-all">
                            <option value="daily">Daily</option>
                            <option value="weekly">Weekly</option>
                            <option value="monthly">Monthly</option>
                        </select>
                    </div>

                    {/* Time */}
                    <div className="space-y-2">
                        <label className="block text-sm font-medium text-neutral-400">
                            Time (UTC)
                        </label>
                        <div className="relative">
                            <Clock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-neutral-500" />
                            <select className="w-full bg-[#1a1a1a] border border-neutral-800 rounded-lg pl-10 pr-4 py-2.5 text-foreground focus:ring-2 focus:ring-accent-dark focus:border-transparent outline-none transition-all">
                                <option value="00:00">00:00 AM</option>
                                <option value="01:00">01:00 AM</option>
                                <option value="02:00">02:00 AM</option>
                                <option value="03:00">03:00 AM</option>
                                <option value="04:00">04:00 AM</option>
                                <option value="12:00">12:00 PM</option>
                            </select>
                        </div>
                    </div>

                    {/* Timezone */}
                    <div className="space-y-2 md:col-span-2">
                        <label className="block text-sm font-medium text-neutral-400">
                            Timezone
                        </label>
                        <div className="relative">
                            <Globe className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-neutral-500" />
                            <select className="w-full bg-[#1a1a1a] border border-neutral-800 rounded-lg pl-10 pr-4 py-2.5 text-foreground focus:ring-2 focus:ring-accent-dark focus:border-transparent outline-none transition-all">
                                <option value="UTC">UTC (Coordinated Universal Time)</option>
                                <option value="Asia/Kolkata">Asia/Kolkata (IST)</option>
                                <option value="America/New_York">America/New_York (EST)</option>
                                <option value="Europe/London">Europe/London (GMT)</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div className="flex items-center space-x-3 pt-2">
                    <input
                        type="checkbox"
                        id="enable-schedule"
                        className="w-4 h-4 rounded border-neutral-700 bg-neutral-800 text-accent-dark focus:ring-accent-dark/50"
                        defaultChecked
                    />
                    <label
                        htmlFor="enable-schedule"
                        className="text-sm font-medium text-foreground"
                    >
                        Enable Automatic Audits
                    </label>
                </div>

                <div className="p-4 bg-accent-dark/10 border border-accent-dark/20 rounded-lg flex items-center justify-between">
                    <span className="text-sm text-accent-light">Next Scheduled Audit:</span>
                    <span className="text-sm font-semibold text-foreground">Dec 11, 2025 at 3:00 AM UTC</span>
                </div>
            </div>
        </div>
    );
}
