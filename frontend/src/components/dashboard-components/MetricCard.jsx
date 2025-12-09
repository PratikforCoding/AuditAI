const MetricCard = ({
    title,
    value,
    icon: Icon,
    colorClass = "text-pink-500",
}) => (
    <div className="bg-card-light/60 hover:bg-card p-5 rounded-xl border border-border-dark duration-200 hover:border-accent-light/20 hover:shadow-2xl shadow-accent-light/15 select-none">
        <div className="flex items-center justify-between">
            <p className="text-sm font-medium text-neutral-400">{title}</p>
            <Icon className={`w-5 h-5 ${colorClass}`} />
        </div>
        <p className="mt-3 text-3xl font-bold text-foreground transition-duration-200">
            {value}
        </p>
    </div>
);

export default MetricCard;
