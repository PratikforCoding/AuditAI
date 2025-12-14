import React from "react";
import { PiggyBank, ArrowRight, CheckCircle2 } from "lucide-react";

const SavingsCard = () => {
    return (
        <div className="bg-gradient-to-br from-[#1a1a1a] to-[#0e0e0e] border border-border-light rounded-xl p-6 shadow-sm relative overflow-hidden">
            {/* Background decoration */}
            <div className="absolute top-0 right-0 p-4 opacity-5">
                <PiggyBank className="w-32 h-32" />
            </div>

            <h3 className="text-lg font-semibold text-foreground mb-6 flex items-center gap-2">
                <PiggyBank className="w-5 h-5 text-green-400" />
                Savings Potential
            </h3>

            <div className="space-y-4 relative z-10">
                <div className="flex justify-between items-center py-2 border-b border-neutral-800">
                    <span className="text-neutral-400">Current Monthly</span>
                    <span className="text-xl font-bold text-foreground">
                        $2,450
                    </span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-neutral-800">
                    <span className="text-neutral-400">
                        If recommendations applied
                    </span>
                    <span className="text-xl font-bold text-green-400">
                        $1,670
                    </span>
                </div>

                <div className="mt-6 p-4 bg-green-500/10 border border-green-500/20 rounded-lg">
                    <div className="flex justify-between items-end mb-1">
                        <span className="text-sm text-green-400 font-medium uppercase tracking-wider">
                            Potential Savings
                        </span>
                        <span className="text-3xl font-extrabold text-green-400">
                            $780<span className="text-lg text-green-500/70 font-normal ml-1">/mo</span>
                        </span>
                    </div>
                    <div className="w-full bg-neutral-800 rounded-full h-2 mt-2">
                        <div
                            className="bg-green-500 h-2 rounded-full"
                            style={{ width: "32%" }}
                        ></div>
                    </div>
                    <p className="text-right text-xs text-green-500/70 mt-1">32% reduction</p>
                </div>

                <div className="flex justify-between items-center pt-2">
                    <span className="text-neutral-400">Annual Projected</span>
                    <span className="text-lg font-bold text-foreground">
                        $9,360
                    </span>
                </div>
            </div>

            <button className="w-full mt-6 py-3 bg-neutral-800 hover:bg-neutral-700 text-white rounded-lg font-medium transition-colors flex items-center justify-center gap-2 group">
                Apply Recommendations
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </button>
        </div>
    );
};

export default SavingsCard;
