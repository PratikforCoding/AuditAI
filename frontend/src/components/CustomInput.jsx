const CustomInput = ({ Icon, placeholder, type = "text", value, onChange }) => (
    <div className="relative w-full mb-4">
        <Icon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-accent-light" />
        <input
            type={type}
            placeholder={placeholder}
            value={value}
            onChange={onChange}
            className="w-full pl-10 pr-4 py-2.5 bg-[#1A1A1A] border border-neutral-800 text-foreground rounded-md focus:border-accent-light transition duration-200 placeholder-text-muted outline-none"
        />
    </div>
);

export default CustomInput;
