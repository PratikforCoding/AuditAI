"use client";
import Link from "next/link";
import { ArrowRight, Sparkles } from "lucide-react";
import { useEffect, useState } from "react";

export default function HeroSection() {
    const [featuresSection, setFeaturesSection] = useState(null);

    useEffect(() => {
        setFeaturesSection(document.querySelector("#features"));
    }, []);

    const handleScroll = () => {
        if (featuresSection) {
            featuresSection.scrollIntoView({ behavior: "smooth" });
        }
    };

    return (
        <section className="relative flex min-h-[90vh] flex-col items-center justify-center overflow-hidden bg-black px-4 pt-20 text-center sm:px-6 lg:px-8">
            {/* Background Effects */}
            <div className="absolute top-0 left-1/2 -z-10 h-[600px] w-[600px] -translate-x-1/2 transform rounded-full bg-accent-dark opacity-10 blur-[120px]" />
            <div className="absolute top-1/2 left-1/4 -z-10 h-[400px] w-[400px] -translate-x-1/2 transform rounded-full bg-blue-900/20 blur-[100px]" />

            <div className="mx-auto max-w-5xl">
                <div className="mb-8 flex items-center justify-center">
                    <span className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1 text-sm text-accent-light backdrop-blur-sm transition-colors hover:bg-white/10 select-none">
                        <Sparkles className="h-4 w-4" />
                        <span className="text-foreground">
                            Powered by{" "}
                        </span>{" "}
                        <span>Gemini AI</span>
                    </span>
                </div>

                <h1 className="mb-6 bg-linear-to-r from-white to-white/70 bg-clip-text text-5xl font-bold tracking-tight text-transparent sm:text-7xl">
                    Stop Cloud Waste. <br />
                    <span className="bg-linear-to-r from-accent-dark via-accent-light to-pink-200 bg-clip-text text-transparent">
                        Eliminate Cloud Risk.
                    </span>
                </h1>

                <p className="mx-auto mb-10 max-w-2xl text-lg text-neutral-400 sm:text-xl">
                    AuditAI connects to your GCP infrastructure to continuously
                    discover resources, detect misconfigurations, and fix cost
                    inefficiencies with AI-driven precision.
                </p>

                <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
                    <Link
                        href="/auth"
                        className="group inline-flex items-center justify-center gap-2 rounded-lg bg-linear-to-r from-accent-light to-pink-300 px-8 py-3.5 text-base font-semibold text-black transition-all hover:bg-accent-dark hover:ring-1 hover:ring-accent-light hover:ring-offset-2 hover:ring-offset-black"
                    >
                        Get Started
                        <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                    </Link>
                    <button
                        onClick={handleScroll}
                        className="group inline-flex items-center justify-center gap-2 rounded-lg border border-white/10 bg-white/5 px-8 py-3.5 text-base font-semibold text-white transition-all hover:bg-white/10"
                    >
                        View Features
                    </button>
                </div>
            </div>

            {/* UI Preview / Dashboard Mockup Placeholder */}
            <div className="relative mt-20 w-full max-w-5xl rounded-t-xl border border-white/10 bg-card/50 backdrop-blur-xl p-2 shadow-2xl">
                <div className="absolute inset-0 -z-10 bg-linear-to-b from-white/5 to-transparent rounded-t-xl" />
                <div className="flex items-center gap-2 border-b border-white/10 px-4 py-3">
                    <div className="flex gap-1.5">
                        <div className="h-3 w-3 rounded-full bg-red-500/50 hover:bg-red-500 duration-150" />
                        <div className="h-3 w-3 rounded-full bg-yellow-500/50 hover:bg-yellow-500 duration-150" />
                        <div className="h-3 w-3 rounded-full bg-green-500/50 hover:bg-green-500 duration-150" />
                    </div>
                </div>
                <div className="grid aspect-video w-full place-items-center object-contain rounded-b-lg bg-card">
                    {/* <div className="text-">
                        <p className="text-neutral-500 text-sm">
                            Interactive Dashboard Preview
                        </p>
                        <div className="mt-4 grid grid-cols-3 gap-4 opacity-50">
                            <div className="h-32 w-48 rounded-lg border border-white/5 bg-white/5" />
                            <div className="h-32 w-48 rounded-lg border border-white/5 bg-white/5" />
                            <div className="h-32 w-48 rounded-lg border border-white/5 bg-white/5" />
                        </div>
                    </div> */}

                    <img
                        src="/Dashboard.jpg"
                        alt="dashboard-sample"
                        className="rounded-b-xl w-full h-full border border-white/5"
                    />
                </div>
            </div>
        </section>
    );
}
