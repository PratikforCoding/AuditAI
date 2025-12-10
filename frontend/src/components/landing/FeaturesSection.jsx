import { Search, ShieldAlert, Zap } from "lucide-react";

const features = [
    {
        title: "Deep Discovery",
        description:
            "Instantly map your entire GCP footprint. See every project, bucket, and instance in one unified view.",
        icon: Search,
        color: "text-blue-400",
        bg: "bg-blue-400/10",
    },
    {
        title: "Intelligent Audits",
        description:
            "Detect security risks and cost anomalies before they become problems. Automated compliance checks run 24/7.",
        icon: ShieldAlert,
        color: "text-[var(--color-status-error)]",
        bg: "bg-[var(--color-status-error)]/10",
    },
    {
        title: "AI Remediation",
        description:
            "Don't just find problems—fix them. Gemini explains the issue and generates precise CLI commands or Terraform code.",
        icon: Zap,
        color: "text-[var(--color-status-idle)]",
        bg: "bg-[var(--color-status-idle)]/10",
    },
];

export default function FeaturesSection() {
    return (
        <section id="features" className="relative bg-[#050505] py-24 sm:py-32">
            <div className="mx-auto max-w-7xl px-6 lg:px-8">
                <div className="mx-auto max-w-2xl text-center">
                    <h2 className="text-lg font-semibold leading-8 text-accent-light">
                        Core Capabilities
                    </h2>
                    <p className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
                        Everything you need to master GCP
                    </p>
                    <p className="mt-6 text-lg leading-8 text-neutral-400">
                        An all-in-one platform to visualize, secure, and
                        optimize your cloud infrastructure with the power of AI.
                    </p>
                </div>

                <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
                    <div className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-3">
                        {features.map((feature) => (
                            <div
                                key={feature.title}
                                className="flex flex-col items-start rounded-2xl border border-white/5 bg-linear-to-br from-card to-white/10 p-8 transition-colors hover:border-accent-light/30 hover:bg-neutral-200/8 duration-200 select-none"
                            >
                                <div
                                    className={`mb-6 flex h-12 w-12 items-center justify-center rounded-lg ${feature.bg}`}
                                >
                                    <feature.icon
                                        className={`h-6 w-6 ${feature.color}`}
                                        aria-hidden="true"
                                    />
                                </div>
                                <dt className="text-xl font-semibold leading-7 text-white">
                                    {feature.title}
                                </dt>
                                <dd className="mt-1 flex flex-auto flex-col text-base leading-7 text-neutral-400">
                                    <p className="flex-auto">
                                        {feature.description}
                                    </p>
                                </dd>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}
