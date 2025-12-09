import { Download } from "lucide-react";

// --- COMPONENT: EXPORT BUTTON ---
const ExportButton = ({ data }) => {
    const handleExport = () => {
        const headers = [
            "ID",
            "Name",
            "Type",
            "Status",
            "Zone",
            "CPU %",
            "Cost",
            "Last Active",
        ];
        const csvContent = [
            headers.join(","),
            ...data.map((row) =>
                [
                    row.id,
                    row.name,
                    row.type,
                    row.status,
                    row.zone,
                    row.cpu_utilization,
                    row.cost,
                    row.last_active,
                ].join(","),
            ),
        ].join("\n");

        const blob = new Blob([csvContent], {
            type: "text/csv;charset=utf-8;",
        });
        const link = document.createElement("a");
        const url = URL.createObjectURL(blob);
        link.setAttribute("href", url);
        link.setAttribute("download", "auditai_resources.csv");
        link.style.visibility = "hidden";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <button
            onClick={handleExport}
            className="flex items-center px-4 py-2 text-sm font-medium text-foreground bg-accent-dark/40 border border-accent-dark/50 rounded-lg hover:border-accent-dark/80
            hover:bg-accent-dark/70 transition-colors duration-200"
        >
            <Download className="w-4 h-4 mr-2" />
            Export CSV
        </button>
    );
};

export default ExportButton;
