"use client";
import React from "react";
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
} from "recharts";

const data = [
    { name: "Dec", cost: 2100 },
    { name: "Jan", cost: 2200 },
    { name: "Feb", cost: 2150 },
    { name: "Mar", cost: 2300 },
    { name: "Apr", cost: 2250 },
    { name: "May", cost: 2400 },
    { name: "Jun", cost: 2450 },
];

const CostTrendChart = () => {
    return (
        <div className="bg-card border border-border-light rounded-xl p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-foreground mb-4">
                Cost Trend
            </h3>
            <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart
                        data={data}
                        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                    >
                        <CartesianGrid
                            strokeDasharray="3 3"
                            stroke="#333"
                            vertical={false}
                        />
                        <XAxis
                            dataKey="name"
                            stroke="#737373"
                            tick={{ fill: "#737373" }}
                            axisLine={{ stroke: "#333" }}
                        />
                        <YAxis
                            stroke="#737373"
                            tick={{ fill: "#737373" }}
                            axisLine={{ stroke: "#333" }}
                            tickFormatter={(value) => `$${value}`}
                        />
                        <Tooltip
                            contentStyle={{
                                backgroundColor: "#0e0e0e",
                                border: "1px solid #333",
                                borderRadius: "8px",
                            }}
                            itemStyle={{ color: "#fff" }}
                        />
                        <Line
                            type="monotone"
                            dataKey="cost"
                            stroke="#db2777" // Pink-600 to match accent
                            strokeWidth={3}
                            dot={{ fill: "#db2777", r: 4 }}
                            activeDot={{ r: 6, fill: "#fff" }}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default CostTrendChart;
