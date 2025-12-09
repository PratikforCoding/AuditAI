"use client";
import React, { useState, useMemo } from "react";
import {
    Search,
    Filter,
    ChevronLeft,
    ChevronRight,
    Server,
    Database,
    HardDrive,
    Cpu,
    Activity,
    ArrowUpDown,
    MoreHorizontal,
} from "lucide-react";
import ExportButton from "@/components/resource-components/ExportButton";
import ResourceDetailModal from "@/components/resource-components/ResourceDetailModal";
import StatusBadge from "@/components/resource-components/StatusBadge";

// --- MOCK DATA GENERATOR ---
const generateMockResources = (count) => {
    const types = ["Compute", "Storage", "Database", "Network"];
    const statuses = ["Running", "Idle", "Stopped", "Error"];
    const zones = ["us-east-1a", "us-east-1b", "us-west-2a", "eu-central-1"];

    return Array.from({ length: count }, (_, i) => {
        const type = types[Math.floor(Math.random() * types.length)];
        const status = statuses[Math.floor(Math.random() * statuses.length)];

        return {
            id: `res-${i + 1}`,
            name: `${type.toLowerCase()}-instance-${i + 100}`,
            type,
            status,
            zone: zones[Math.floor(Math.random() * zones.length)],
            cpu_utilization:
                status === "Running" ? Math.floor(Math.random() * 80) + 10 : 0,
            memory_utilization:
                status === "Running" ? Math.floor(Math.random() * 90) + 10 : 0,
            cost: Math.floor(Math.random() * 500) + 50,
            disk_size: `${Math.floor(Math.random() * 1000)} GB`,
            last_active: new Date(
                Date.now() - Math.floor(Math.random() * 1000000000),
            ).toISOString(),
        };
    });
};

const MOCK_RESOURCES = generateMockResources(65); // Generate enough for pagination

// --- MAIN PAGE COMPONENT ---
const ResourcesPage = () => {
    const [searchTerm, setSearchTerm] = useState("");
    const [typeFilter, setTypeFilter] = useState("All");
    const [statusFilter, setStatusFilter] = useState("All");
    const [sortConfig, setSortConfig] = useState({
        key: "name",
        direction: "asc",
    });
    const [currentPage, setCurrentPage] = useState(1);
    const [selectedResource, setSelectedResource] = useState(null);
    const itemsPerPage = 20;

    // Filter Logic
    const filteredResources = useMemo(() => {
        return MOCK_RESOURCES.filter((resource) => {
            const matchesSearch =
                resource.name
                    .toLowerCase()
                    .includes(searchTerm.toLowerCase()) ||
                resource.id.toLowerCase().includes(searchTerm.toLowerCase());
            const matchesType =
                typeFilter === "All" || resource.type === typeFilter;
            const matchesStatus =
                statusFilter === "All" || resource.status === statusFilter;
            return matchesSearch && matchesType && matchesStatus;
        });
    }, [searchTerm, typeFilter, statusFilter]);

    // Sort Logic
    const sortedResources = useMemo(() => {
        let sortableItems = [...filteredResources];
        if (sortConfig.key) {
            sortableItems.sort((a, b) => {
                if (a[sortConfig.key] < b[sortConfig.key]) {
                    return sortConfig.direction === "asc" ? -1 : 1;
                }
                if (a[sortConfig.key] > b[sortConfig.key]) {
                    return sortConfig.direction === "asc" ? 1 : -1;
                }
                return 0;
            });
        }
        return sortableItems;
    }, [filteredResources, sortConfig]);

    // Pagination Logic
    const totalPages = Math.ceil(sortedResources.length / itemsPerPage);
    const paginatedResources = sortedResources.slice(
        (currentPage - 1) * itemsPerPage,
        currentPage * itemsPerPage,
    );

    const handleSort = (key) => {
        let direction = "asc";
        if (sortConfig.key === key && sortConfig.direction === "asc") {
            direction = "desc";
        }
        setSortConfig({ key, direction });
    };

    return (
        <div className="min-h-screen bg-background p-4 md:p-8 font-sans">
            <div className="max-w-7xl mx-auto space-y-6">
                {/* Header */}
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                    <div>
                        <h1 className="text-3xl font-extrabold text-foreground">
                            <span className="text-accent-dark">Cloud</span>{" "}
                            Resources
                        </h1>
                        <p className="text-text-secondary mt-1">
                            Manage and monitor your infrastructure assets.
                        </p>
                    </div>
                    <ExportButton data={filteredResources} />
                </div>

                {/* Filters Bar */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 bg-card p-4 rounded-xl border border-border-dark">
                    {/* Search */}
                    <div className="relative md:col-span-2">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-text-muted" />
                        <input
                            type="text"
                            placeholder="Search resources by name or ID..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="w-full pl-10 pr-4 py-2 bg-neutral-900/90 border border-border-dark rounded-md text-sm text-foreground placeholder-text-mtext-text-muted focus:outline-none focus:border-accent-darktext-accent-dark transition-colors"
                        />
                    </div>

                    {/* Type Filter */}
                    <div className="relative">
                        <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-text-muted" />
                        <select
                            value={typeFilter}
                            onChange={(e) => {
                                setTypeFilter(e.target.value);
                                setCurrentPage(1);
                            }}
                            className="w-full pl-10 pr-4 py-2 bg-neutral-800/70 border border-border-dark rounded-md text-sm text-foreground appearance-none focus:outline-none focus:border-accent-darktext-accent-dark cursor-pointer"
                        >
                            <option value="All">All Types</option>
                            <option value="Compute">Compute</option>
                            <option value="Storage">Storage</option>
                            <option value="Database">Database</option>
                            <option value="Network">Network</option>
                        </select>
                    </div>

                    {/* Status Filter */}
                    <div className="relative">
                        <Activity className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-text-muted" />
                        <select
                            value={statusFilter}
                            onChange={(e) => {
                                setStatusFilter(e.target.value);
                                setCurrentPage(1);
                            }}
                            className="w-full pl-10 pr-4 py-2 bg-neutral-800/70 border border-border-dark rounded-md text-sm text-foreground appearance-none focus:outline-none focus:border-accent-darktext-accent-dark cursor-pointer"
                        >
                            <option value="All">All Statuses</option>
                            <option value="Running">Running</option>
                            <option value="Idle">Idle</option>
                            <option value="Stopped">Stopped</option>
                            <option value="Error">Error</option>
                        </select>
                    </div>
                </div>

                {/* Resources Table */}
                <div className="bg-card rounded-xl border border-border-dark overflow-hidden">
                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-border-darkborder-border-dark">
                            <thead className="bg-[#1A1A1A]">
                                <tr>
                                    {[
                                        "Name",
                                        "Type",
                                        "Status",
                                        "Zone",
                                        "Cost",
                                        "Utilization",
                                    ].map((header) => (
                                        <th
                                            key={header}
                                            onClick={() =>
                                                handleSort(header.toLowerCase())
                                            }
                                            className="px-6 py-4 text-left text-xs font-medium text-text-secondary uppercase tracking-wider cursor-pointer hover:text-accent-light transition-colors select-none"
                                        >
                                            <div className="flex items-center gap-1">
                                                {header}
                                                <ArrowUpDown className="w-3 h-3 opacity-50" />
                                            </div>
                                        </th>
                                    ))}
                                    <th className="px-6 py-4 text-right text-xs font-medium text-text-secondary uppercase tracking-wider">
                                        Actions
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-border-darkborder-border-dark">
                                {paginatedResources.map((resource) => (
                                    <tr
                                        key={resource.id}
                                        onClick={() =>
                                            setSelectedResource(resource)
                                        }
                                        className="group hover:bg-card-light transition-colors cursor-pointer"
                                    >
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <div className="flex items-center">
                                                <div className="p-2 rounded-full bg-card border border-border-light mr-3">
                                                    {resource.type ===
                                                    "Database" ? (
                                                        <Database className="w-4 h-4 text-teal-400" />
                                                    ) : resource.type ===
                                                      "Storage" ? (
                                                        <HardDrive className="w-4 h-4 text-blue-400" />
                                                    ) : resource.type ===
                                                      "Compute" ? (
                                                        <Cpu className="w-4 h-4 text-accent-dark" />
                                                    ) : (
                                                        <Server className="w-4 h-4 text-indigo-400" />
                                                    )}
                                                </div>
                                                <div>
                                                    <div className="text-sm font-medium text-foreground group-hover:text-accent-lightbg-accent-light transition-colors">
                                                        {resource.name}
                                                    </div>
                                                    <div className="text-xs text-text-muted">
                                                        {resource.id}
                                                    </div>
                                                </div>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-text-secondary">
                                            {resource.type}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <StatusBadge
                                                status={resource.status}
                                            />
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-text-secondary">
                                            {resource.zone}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-foreground">
                                            ${resource.cost.toFixed(2)}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <div className="flex items-center gap-2">
                                                <div className="w-24 bg-background rounded-full h-1.5 overflow-hidden">
                                                    <div
                                                        className={`h-1.5 rounded-full ${
                                                            resource.cpu_utilization >
                                                            80
                                                                ? "bg-status-error"
                                                                : "bg-status-running text-accent-dark"
                                                        }`}
                                                        style={{
                                                            width: `${resource.cpu_utilization}%`,
                                                        }}
                                                    ></div>
                                                </div>
                                                <span className="text-xs text-text-muted">
                                                    {resource.cpu_utilization}%
                                                </span>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                            <button className="text-text-muted hover:text-foreground p-1 rounded-full hover:bg-border-darkborder-border-dark transition-all">
                                                <MoreHorizontal className="w-4 h-4" />
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    {/* Pagination Footer */}
                    <div className="px-6 py-4 border-t border-border-dark bg-[#1A1A1A] flex items-center justify-between">
                        <span className="text-sm text-text-muted">
                            Showing{" "}
                            <span className="font-medium text-foreground">
                                {(currentPage - 1) * itemsPerPage + 1}
                            </span>{" "}
                            to{" "}
                            <span className="font-medium text-foreground">
                                {Math.min(
                                    currentPage * itemsPerPage,
                                    filteredResources.length,
                                )}
                            </span>{" "}
                            of{" "}
                            <span className="font-medium text-foreground">
                                {filteredResources.length}
                            </span>{" "}
                            results
                        </span>
                        <div className="flex items-center gap-2">
                            <button
                                onClick={() =>
                                    setCurrentPage((prev) =>
                                        Math.max(prev - 1, 1),
                                    )
                                }
                                disabled={currentPage === 1}
                                className="p-2 rounded-md border border-border-dark text-text-secondary hover:bg-background disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                            >
                                <ChevronLeft className="w-4 h-4" />
                            </button>
                            <button
                                onClick={() =>
                                    setCurrentPage((prev) =>
                                        Math.min(prev + 1, totalPages),
                                    )
                                }
                                disabled={currentPage === totalPages}
                                className="p-2 rounded-md border border-border-dark text-text-secondary hover:bg-background disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                            >
                                <ChevronRight className="w-4 h-4" />
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* Detail Modal */}
            {selectedResource && (
                <ResourceDetailModal
                    resource={selectedResource}
                    onClose={() => setSelectedResource(null)}
                />
            )}
        </div>
    );
};

export default ResourcesPage;
