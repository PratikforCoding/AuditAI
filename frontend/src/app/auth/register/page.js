"use client";
import React, { useState } from "react";
import { Mail, Lock, UserPlus, Building, X, ArrowRight } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import CustomInput from "@/components/CustomInput";
import useAuthStore from "@/store/useAuthStore";

const RegisterPage = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [companyName, setCompanyName] = useState("");
    const [error, setError] = useState("");

    const router = useRouter();
    const { register, isRegistering } = useAuthStore();

    const handleRegister = async (e) => {
        e.preventDefault();

        if (!email || !password || !confirmPassword || !companyName) {
            setError("All fields are required");
            return;
        }

        if (password !== confirmPassword) {
            setError("Passwords do not match");
            return;
        }

        setError("");

        try {
            await register({
                email,
                password,
                confirm_password: confirmPassword,
                company_name: companyName
            });
            // Redirect to onboarding as requested
            router.push("/onboarding");
        } catch (err) {
            const errorMsg = err.response?.data?.detail || "Registration failed. Please try again.";
            setError(errorMsg);
        }
    };

    const handleGoogleSignIn = () => {
        console.log("Redirecting to Google OAuth...");
    };

    return (
        // Pure Black background
        <div className="min-h-screen bg-background flex items-center justify-center p-4">
            {/* The background blur ball */}
            {/*  !!!! IF REMOVED ==> Remove the backdrop filter blur from the card below */}
            <div className="rounded-md size-10 bg-white shadow-[0_0_50px_40px_white] absolute top-[25%] right-[45%]"></div>

            {/* Near Black Card background, no heavy shadow */}
            <div className="w-full max-w-md bg-linear-to-br from-card via-card/90 to-white/10 border border-white/5 text-foreground p-8 md:p-10 rounded-xl [backdrop-filter:blur(10px)]">
                {/* AuditAI Logo */}
                <div className="text-center mb-8">
                    <h1 className="text-4xl font-extrabold text-accent-dark tracking-wider mb-2">
                        <span className="text-foreground">Audit</span>AI
                    </h1>
                    <p className="text-text-secondary text-xl font-light mt-4">
                        Create your account
                    </p>
                </div>

                {/* OAuth2 - Sign in with Google */}
                <button
                    onClick={handleGoogleSignIn}
                    // Near Black button background, no shadow
                    className="w-full flex items-center justify-center py-2.5 space-x-3 px-4 mb-8 text-background font-semibold bg-foreground rounded-md transition duration-150  group cursor-pointer active:scale-99 hover:shadow-xl shadow-white/10"
                    disabled={isRegistering}
                >
                    <Image
                        src={"/search.png"}
                        width={22}
                        height={22}
                        alt="Google-logo"
                    ></Image>
                    <span>Sign up with Google</span>
                </button>

                <div className="relative flex items-center justify-center mb-8">
                    {/* Darker separator */}
                    <div className="grow border-t border-text-muted"></div>
                    <span className="shrink mx-4 text-text-muted text-xs uppercase">
                        or register with email
                    </span>
                    <div className="grow border-t border-text-muted"></div>
                </div>

                {/* Registration Form */}
                <form onSubmit={handleRegister} className="w-full">
                    {error && (
                        <div className="mb-4 px-3 flex items-center justify-between py-2.5 bg-red-900/20 hover:bg-red-900/25 duration-200 text-red-100 border border-red-800 rounded-md text-sm w-full">
                            <span>{error}</span>
                            <button type="button">
                                <X
                                    size={15}
                                    onClick={() => setError("")}
                                    className="text-foreground"
                                />
                            </button>
                        </div>
                    )}

                    <CustomInput
                        Icon={Mail}
                        placeholder="Email Address"
                        type="email"
                        value={email}
                        onChange={(e) => {
                            setEmail(e.target.value);
                            setError("");
                        }}
                    />

                    <CustomInput
                        Icon={Building}
                        placeholder="Company Name"
                        type="text"
                        value={companyName}
                        onChange={(e) => {
                            setCompanyName(e.target.value);
                            setError("");
                        }}
                    />

                    <CustomInput
                        Icon={Lock}
                        placeholder="Password"
                        type="password"
                        value={password}
                        onChange={(e) => {
                            setPassword(e.target.value);
                            setError("");
                        }}
                    />

                    <CustomInput
                        Icon={Lock}
                        placeholder="Confirm Password"
                        type="password"
                        value={confirmPassword}
                        onChange={(e) => {
                            setConfirmPassword(e.target.value);
                            setError("");
                        }}
                    />

                    {/* Sign Up Button */}
                    <button
                        type="submit"
                        className="w-full flex items-center justify-center text-[16px] py-2.5 px-4 mt-6 text-white border border-accent-dark/50 bg-accent-dark/40 rounded-md transition duration-200 hover:bg-accent-dark hover:shadow-lg shadow-pink-400/10 focus:outline-none disabled:opacity-50 cursor-pointer"
                        disabled={isRegistering}
                    >
                        {isRegistering ? (
                            <svg
                                className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 24 24"
                            >
                                <circle
                                    className="opacity-25"
                                    cx="12"
                                    cy="12"
                                    r="10"
                                    stroke="currentColor"
                                    strokeWidth="4"
                                ></circle>
                                <path
                                    className="opacity-75"
                                    fill="currentColor"
                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                                ></path>
                            </svg>
                        ) : (
                            <>
                                <UserPlus className="w-5 h-5 mr-2" />
                                Create Account
                            </>
                        )}
                    </button>
                </form>

                {/* Footer Links */}
                <div className="mt-8 pt-6 border-t border-border-muted/40 text-center text-sm space-y-2">
                    Already have an account?
                    <Link
                        href="/auth"
                        className="text-text-muted hover:text-accent-light transition duration-150 flex items-center justify-center"
                    >
                        <span className="ml-1">Sign in instead</span>
                        <ArrowRight className="w-3 h-3 ml-1" />
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default RegisterPage;
