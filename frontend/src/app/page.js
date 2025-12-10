import HeroSection from "@/components/landing/HeroSection";
import FeaturesSection from "@/components/landing/FeaturesSection";
import HowItWorks from "@/components/landing/HowItWorks";
import Footer from "@/components/landing/Footer";

export default function Home() {
    return (
        <div className="min-h-screen bg-black text-white selection:bg-[var(--color-accent-light)] selection:text-black">
            <HeroSection />
            <FeaturesSection />
            <HowItWorks />
            <Footer />
        </div>
    );
}
