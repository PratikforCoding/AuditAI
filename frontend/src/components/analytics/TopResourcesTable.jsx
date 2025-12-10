import React from "react";
import { Database, Server, HardDrive, Wifi, Box } from "lucide-react";

const resources = [
    {
        name: "prod-db",
        type: "Database",
        cost: 450,
        percentage: 18,
        icon: Database,
    },
    {
        name: "prod-1",
        type: "Compute",
        cost: 320,
        percentage: 13,
        icon: Server,
    },
    {
        name: "backup-storage",
        type: "Storage",
        cost: 180,
        percentage: 7,
        icon: HardDrive,
    },
    {
        name: "analytics-vm",
        type: "Compute",
        cost: 150,
        percentage: 6,
        icon: Server,
    },
    {
        name: "cdn-config",
        type: "Network",
        cost: 120,
        percentage: 5,
        icon: Wifi,
    },
];

const TopResourcesTable = () => {
    return (
        <div className="bg-card border border-border-light rounded-xl overflow-hidden shadow-sm">
            <div className="p-6 border-b border-border-light">
                <h3 className="text-lg font-semibold text-foreground">
                    Top Expensive Resources
                </h3>
            </div>
            <div className="overflow-x-auto">
                <table className="w-full text-left text-sm text-neutral-400">
                    <thead className="bg-[#141414] text-neutral-200 uppercase text-xs">
                        <tr>
                            <th className="px-6 py-3">Resource Name</th>
                            <th className="px-6 py-3">Type</th>
                            <th className="px-6 py-3 text-right">Cost</th>
                            <th className="px-6 py-3 text-right">% of Total</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-neutral-800">
                        {resources.map((resource, index) => {
                            const Icon = resource.icon || Box;
                            return (
                                <tr
                                    key={index}
                                    className="hover:bg-neutral-900/50 transition-colors"
                                >
                                    <td className="px-6 py-4 font-medium text-foreground flex items-center gap-3">
                                        <div className="p-2 bg-neutral-800 rounded-md">
                                            <Icon className="w-4 h-4 text-accent-light" />
                                        </div>
                                        {resource.name}
                                    </td>
                                    <td className="px-6 py-4">{resource.type}</td>
                                    <td className="px-6 py-4 text-right text-foreground font-semibold">
                                        ${resource.cost}/mo
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        {resource.percentage}%
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default TopResourcesTable;
