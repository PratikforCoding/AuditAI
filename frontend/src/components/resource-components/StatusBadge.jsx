"use client";
import { X, AlertCircle, CheckCircle2, Clock } from "lucide-react";
// --- COMPONENT: STATUS BADGE ---
const StatusBadge = ({ status }) => {
    let colorVar = "text-text-muted";
    let icon = <Clock className="w-3 h-3 mr-1" />;
    let bgClass = "bg-neutral-900/50";
    let borderClass = "border-neutral-800";

    switch (status) {
        case "Running":
            colorVar = "text-[var(--color-status-running)]";
            icon = <CheckCircle2 className="w-3 h-3 mr-1" />;
            bgClass = "bg-green-900/20";
            borderClass = "border-green-900/30";
            break;
        case "Idle":
            colorVar = "text-[var(--color-status-idle)]";
            icon = <Clock className="w-3 h-3 mr-1" />;
            bgClass = "bg-yellow-900/20";
            borderClass = "border-yellow-900/30";
            break;
        case "Error":
            colorVar = "text-[var(--color-status-error)]";
            icon = <AlertCircle className="w-3 h-3 mr-1" />;
            bgClass = "bg-red-900/20";
            borderClass = "border-red-900/30";
            break;
        case "Stopped":
            colorVar = "text-text-muted";
            icon = <X className="w-3 h-3 mr-1" />;
            bgClass = "bg-neutral-900/50";
            borderClass = "border-neutral-800";
            break;
    }

    return (
        <span
            className={`flex items-center w-fit px-2.5 py-0.5 rounded-full text-xs font-medium border ${bgClass} ${borderClass} ${colorVar}`}
        >
            {icon}
            {status}
        </span>
    );
};

export default StatusBadge;
