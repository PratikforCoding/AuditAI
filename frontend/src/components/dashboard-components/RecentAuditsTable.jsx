import { ChevronDown, ChevronUp } from "lucide-react";
import { useMemo, useState } from "react";

const RecentAuditsTable = ({ audits }) => {
    const [sortConfig, setSortConfig] = useState({
        key: "date",
        direction: "descending",
    });

    const sortedAudits = useMemo(() => {
        let sortableItems = [...audits];
        if (sortConfig.key) {
            sortableItems.sort((a, b) => {
                const aVal = a[sortConfig.key];
                const bVal = b[sortConfig.key];

                if (aVal < bVal)
                    return sortConfig.direction === "ascending" ? -1 : 1;
                if (aVal > bVal)
                    return sortConfig.direction === "ascending" ? 1 : -1;
                return 0;
            });
        }
        return sortableItems;
    }, [audits, sortConfig]);

    const requestSort = (key) => {
        let direction = "ascending";
        if (sortConfig.key === key && sortConfig.direction === "ascending") {
            direction = "descending";
        }
        setSortConfig({ key, direction });
    };

    const getSortIcon = (key) => {
        if (sortConfig.key !== key) return null;
        return sortConfig.direction === "ascending" ? (
            <ChevronUp className="w-4 h-4 ml-1" />
        ) : (
            <ChevronDown className="w-4 h-4 ml-1" />
        );
    };

    const headers = [
        { key: "date", label: "Date" },
        { key: "resources_scanned", label: "Resources Scanned" },
        { key: "issues_found", label: "Issues Found" },
        { key: "savings", label: "Potential Savings" },
    ];

    return (
        <div className="mt-8 bg- p-6 rounded-xl border border-neutral-900 overflow-x-auto">
            <h2 className="text-xl font-semibold text-white mb-4">
                Recent Audits
            </h2>
            <table className="min-w-full divide-y divide-border-light">
                <thead>
                    <tr>
                        {headers.map((header) => (
                            <th
                                key={header.key}
                                onClick={() => requestSort(header.key)}
                                className="px-4 py-3 text-left text-xs font-medium text-accent-light uppercase tracking-wider cursor-pointer hover:text-accent-dark transition-duration-200 whitespace-nowrap"
                            >
                                <div className="flex items-center">
                                    {header.label}
                                    {getSortIcon(header.key)}
                                </div>
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody className="divide-y divide-neutral-900">
                    {sortedAudits.map((audit) => (
                        <tr
                            key={audit.id}
                            className="text-sm text-neutral-300 hover:bg-[#1A1A1A] transition-duration-200"
                        >
                            <td className="px-4 py-4 whitespace-nowrap">
                                {new Date(audit.date).toLocaleDateString()}
                            </td>
                            <td className="px-4 py-4 whitespace-nowrap">
                                {audit.resources_scanned}
                            </td>
                            <td
                                className={`px-4 py-4 whitespace-nowrap ${
                                    audit.issues_found > 0
                                        ? "text-status-error font-semibold"
                                        : "text-status-running"
                                }`}
                            >
                                {audit.issues_found}
                            </td>
                            <td className="px-4 py-4 whitespace-nowrap text-status-running">
                                ${audit.savings.toLocaleString()}
                                <span className="text-foreground"> /mo</span>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
            {audits.length === 0 && (
                <p className="text-center text-text-muted py-8">
                    No recent audit history found.
                </p>
            )}
        </div>
    );
};

export default RecentAuditsTable;
