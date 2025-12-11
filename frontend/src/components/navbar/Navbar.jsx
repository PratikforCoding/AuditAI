import Link from "next/link";
import { usePathname } from "next/navigation";
import React from "react";

const Navbar = () => {
    const pathname = usePathname();

    const navItems = [
        { name: "Overview", href: "/dashboard" },
        { name: "Resources", href: "/resources" },
        { name: "Analytics", href: "/analytics" },
        { name: "Audits", href: "/audits" },
        { name: "Recommendations", href: "/recommendations" },
        { name: "Settings", href: "/schedule" },
    ];

    return (
        <nav className="flex items-center gap-6 mt-4 border-b border-white/5">
            {navItems.map((item) => {
                const isActive = pathname === item.href;
                return (
                    <Link
                        key={item.href}
                        href={item.href}
                        className={`pb-3 text-sm font-medium transition-colors relative ${
                            isActive
                                ? "text-accent-light"
                                : "text-neutral-400 hover:text-neutral-200"
                        }`}
                    >
                        {item.name}
                        {isActive && (
                            <span className="absolute bottom-0 left-0 w-full h-0.5 bg-accent-light rounded-t-full" />
                        )}
                    </Link>
                );
            })}
        </nav>
    );
};

export default Navbar;
