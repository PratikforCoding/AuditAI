import { CheckCircle2 } from "lucide-react";

export default function HowItWorks() {
    return (
        <section className="bg-black py-24 sm:py-32">
            <div className="mx-auto max-w-7xl px-6 lg:px-8">
                <div className="grid grid-cols-1 gap-y-16 lg:grid-cols-2 lg:gap-x-16">
                    <div className="relative flex flex-col justify-center">
                        <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
                            From Chaos to Clarity in <span className="text-[var(--color-accent-light)]">Three Steps</span>
                        </h2>
                        <p className="mt-4 text-lg text-neutral-400">
                            AuditAI simplifies cloud management by streamlining the discovery, analysis, and resolution workflow.
                        </p>

                        <div className="mt-10 space-y-8">
                            <div className="flex gap-4">
                                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#1e1e1e] border border-white/10 text-white font-bold">1</div>
                                <div>
                                    <h3 className="text-lg font-semibold text-white">Connect your Organization</h3>
                                    <p className="mt-2 text-neutral-400">Grant AuditAI read-only access to your GCP projects via a service account. We auto-discover all assets in minutes.</p>
                                </div>
                            </div>
                            <div className="flex gap-4">
                                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#1e1e1e] border border-white/10 text-white font-bold">2</div>
                                <div>
                                    <h3 className="text-lg font-semibold text-white">Run AI Audits</h3>
                                    <p className="mt-2 text-neutral-400">Our engine checks for over-provisioning, zombie assets, and open ports. Gemini analyzes the context of every finding.</p>
                                </div>
                            </div>
                            <div className="flex gap-4">
                                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[var(--color-accent-light)] text-black font-bold">3</div>
                                <div>
                                    <h3 className="text-lg font-semibold text-white">Apply Risk-Free Fixes</h3>
                                    <p className="mt-2 text-neutral-400">Review prioritized recommendations. Copy formatted gcloud commands or Terraform blocks to remediate instantly.</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="relative rounded-2xl border border-white/10 bg-[#0e0e0e] p-8 lg:p-12">
                        <div className="absolute top-0 right-0 -z-10 h-full w-full bg-[radial-gradient(#1a1a1a_1px,transparent_1px)] [background-size:16px_16px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_70%,transparent_100%)]"></div>

                        {/* Code Snippet Look for "Remediation" */}
                        <div className="rounded-lg bg-black/80 p-4 font-mono text-sm text-neutral-300 border border-white/10 shadow-2xl">
                            <div className="mb-2 flex items-center gap-2 border-b border-white/10 pb-2">
                                <span className="text-[var(--color-accent-light)] font-bold">Gemini Suggestion:</span>
                                <span>Delete Unused IP</span>
                            </div>
                            <div className="space-y-1">
                                <p className="text-neutral-500"># This static IP has been unattached for 30+ days</p>
                                <p className="text-purple-400">gcloud<span className="text-white"> compute addresses delete</span> example-ip-1</p>
                                <p className="pl-4 text-white">--region<span className="text-green-400"> us-central1</span></p>
                                <p className="pl-4 text-white">--quiet</p>
                            </div>
                            <div className="mt-4 flex gap-2">
                                <button className="rounded bg-[var(--color-accent-light)] px-3 py-1 text-xs font-bold text-black hover:bg-opacity-90">Copy Command</button>
                                <button className="rounded bg-white/10 px-3 py-1 text-xs text-white hover:bg-white/20">Ignore</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}
