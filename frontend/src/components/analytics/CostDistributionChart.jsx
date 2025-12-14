"use client";
import React from "react";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts";

const data = [
    { name: "Compute", value: 1470, color: "#db2777" }, // Pink
    { name: "Storage", value: 612, color: "#8b5cf6" }, // Violet
    { name: "Network", value: 245, color: "#3b82f6" }, // Blue
    { name: "Other", value: 123, color: "#10b981" }, // Emerald
];

const renderCustomLabel = ({
    cx,
    cy,
    midAngle,
    innerRadius,
    outerRadius,
    percent,
}) => {
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
        <text
            x={x}
            y={y}
            fill="white"
            textAnchor={x > cx ? "start" : "end"}
            dominantBaseline="central"
            className="text-xs font-bold"
        >
            {`${(percent * 100).toFixed(0)}%`}
        </text>
    );
};

const CostDistributionChart = () => {
    return (
        <div className="bg-card border border-border-light rounded-xl p-6 shadow-sm flex flex-col">
            <h3 className="text-lg font-semibold text-foreground mb-4">
                Cost by Resource Type
            </h3>
            <div className="flex-1 min-h-[300px] w-full relative">
                <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                        <Pie
                            data={data}
                            cx="50%"
                            cy="50%"
                            labelLine={false}
                            label={renderCustomLabel}
                            outerRadius={100}
                            fill="#8884d8"
                            dataKey="value"
                            stroke="none"
                        >
                            {data.map((entry, index) => (
                                <Cell
                                    key={`cell-${index}`}
                                    fill={entry.color}
                                />
                            ))}
                        </Pie>
                        <Tooltip
                            contentStyle={{
                                backgroundColor: "#0e0e0e",
                                border: "1px solid #333",
                                borderRadius: "8px",
                            }}
                            itemStyle={{ color: "#fff" }}
                            formatter={(value) => `$${value}`}
                        />
                        <Legend
                            verticalAlign="bottom"
                            height={36}
                            iconType="circle"
                        />
                    </PieChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default CostDistributionChart;
