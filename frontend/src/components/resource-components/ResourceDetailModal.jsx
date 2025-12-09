import { X, Server } from "lucide-react";
import StatusBadge from "./StatusBadge";

// --- COMPONENT: RESOURCE DETAIL MODAL ---
const ResourceDetailModal = ({ resource, onClose }) => {
    if (!resource) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
            <div className="w-full max-w-2xl bg-card border border-border-dark rounded-xl shadow-2xl p-6 relative animate-in zoom-in-95 duration-200">
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 text-text-muted hover:text-foreground transition-colors"
                >
                    <X className="w-6 h-6" />
                </button>

                <div className="flex items-center gap-3 mb-6">
                    <div className="p-3 bg-[#1A1A1A] rounded-lg border border-border-dark">
                        <Server className="w-8 h-8 text-accent-dark" />
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold text-foreground">
                            {resource.name}
                        </h2>
                        <div className="flex items-center gap-2 mt-1">
                            <span className="text-text-muted text-sm uppercase tracking-wider">
                                {resource.id}
                            </span>
                            <span className="text-border-darkborder-border-dark">
                                |
                            </span>
                            <StatusBadge status={resource.status} />
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-4">
                        <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider border-b border-border-dark pb-2">
                            Configuration
                        </h3>
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <p className="text-xs text-text-muted">Type</p>
                                <p className="text-foreground font-medium">
                                    {resource.type}
                                </p>
                            </div>
                            <div>
                                <p className="text-xs text-text-muted">Zone</p>
                                <p className="text-foreground font-medium">
                                    {resource.zone}
                                </p>
                            </div>
                            <div>
                                <p className="text-xs text-text-muted">
                                    Disk Size
                                </p>
                                <p className="text-foreground font-medium">
                                    {resource.disk_size}
                                </p>
                            </div>
                            <div>
                                <p className="text-xs text-text-muted">
                                    Last Active
                                </p>
                                <p className="text-foreground font-medium">
                                    {new Date(
                                        resource.last_active,
                                    ).toLocaleDateString()}
                                </p>
                            </div>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider border-b border-border-dark pb-2">
                            Metrics
                        </h3>
                        <div className="space-y-4">
                            <div>
                                <div className="flex justify-between mb-1">
                                    <p className="text-xs text-text-muted">
                                        CPU Utilization
                                    </p>
                                    <p className="text-xs text-foreground">
                                        {resource.cpu_utilization}%
                                    </p>
                                </div>
                                <div className="w-full bg-[#1A1A1A] rounded-full h-1.5 overflow-hidden">
                                    <div
                                        className={`h-1.5 rounded-full ${
                                            resource.cpu_utilization > 80
                                                ? "bg-status-error"
                                                : "bg-status-running text-accent-dark"
                                        }`}
                                        style={{
                                            width: `${resource.cpu_utilization}%`,
                                        }}
                                    ></div>
                                </div>
                            </div>
                            <div>
                                <div className="flex justify-between mb-1">
                                    <p className="text-xs text-text-muted">
                                        Memory Utilization
                                    </p>
                                    <p className="text-xs text-foreground">
                                        {resource.memory_utilization}%
                                    </p>
                                </div>
                                <div className="w-full bg-[#1A1A1A] rounded-full h-1.5 overflow-hidden">
                                    <div
                                        className="bg-accent-light h-1.5 rounded-full"
                                        style={{
                                            width: `${resource.memory_utilization}%`,
                                        }}
                                    ></div>
                                </div>
                            </div>
                            <div className="p-4 bg-[#1A1A1A] rounded-lg border border-border-dark mt-2">
                                <p className="text-xs text-text-muted mb-1">
                                    Monthly Cost
                                </p>
                                <p className="text-2xl font-bold text-foreground">
                                    ${resource.cost.toFixed(2)}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ResourceDetailModal;
