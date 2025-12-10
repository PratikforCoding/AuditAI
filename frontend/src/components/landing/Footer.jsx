import Link from "next/link";
import { Github, Twitter, Linkedin } from "lucide-react";

export default function Footer() {
    return (
        <footer className="border-t border-white/10 bg-black">
            <div className="mx-auto max-w-7xl overflow-hidden px-6 py-12 sm:py-16 lg:px-8">
                <div className="flex justify-center space-x-10">
                    <Link href="#" className="text-neutral-400 hover:text-white">
                        <span className="sr-only">GitHub</span>
                        <Github className="h-6 w-6" aria-hidden="true" />
                    </Link>
                    <Link href="#" className="text-neutral-400 hover:text-white">
                        <span className="sr-only">Twitter</span>
                        <Twitter className="h-6 w-6" aria-hidden="true" />
                    </Link>
                    <Link href="#" className="text-neutral-400 hover:text-white">
                        <span className="sr-only">LinkedIn</span>
                        <Linkedin className="h-6 w-6" aria-hidden="true" />
                    </Link>
                </div>
                <div className="mt-8 text-center">
                    <p className="text-xs leading-5 text-neutral-500">
                        &copy; {new Date().getFullYear()} AuditAI, Inc. All rights reserved.
                    </p>
                    <p className="mt-2 text-xs text-neutral-600">
                        Not affiliated with Google Cloud Platform.
                    </p>
                </div>
            </div>
        </footer>
    );
}
