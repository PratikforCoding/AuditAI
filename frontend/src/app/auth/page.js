"use client";
import React, { useState } from "react";
import { Mail, Lock, LogIn, Chrome, ArrowRight, X } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import CustomInput from "@/components/CustomInput";

const LoginPage = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");

    const handleEmailSignIn = (e) => {
        e.preventDefault();
        if (!email || !password) {
            setError("Please enter both email and password");
            return;
        }
        setError("");
        setIsLoading(true);

        // --- MOCK API CALL for /api/auth/session ---
        setTimeout(() => {
            console.log("Attempting sign in with:", { email, password });
            setIsLoading(false);
            // For this mock, we'll just show success/fail based on a dummy check
            if (password === "password123") {
                console.log("Login successful! Redirecting...");
            } else {
                setError("Invalid credentials. Please try again.");
            }
        }, 1500);
    };

    const handleGoogleSignIn = () => {
        console.log("Redirecting to Google OAuth...");
        console.log("Initiating Google Sign-In (OAuth flow would start here).");
    };

    return (
        // Pure Black background
        <div className="min-h-screen bg-background flex items-center justify-center p-4">
            {/* The background blur ball */}
            {/*  !!!! IF REMOVED ==> Remove the backdrop filter blur from the card below */}
            <div className="rounded-md size-10 bg-white shadow-[0_0_50px_40px_white] absolute top-[25%] left-[45%]"></div>

            {/* Near Black Card background, no heavy shadow */}
            <div className="w-full max-w-md bg-linear-to-br from-card via-card/90 to-white/10 border border-white/5 text-foreground p-8 md:p-10 rounded-xl [backdrop-filter:blur(10px)]">
                {/* AuditAI Logo */}
                <div className="text-center mb-8">
                    <h1 className="text-4xl font-extrabold text-accent-dark tracking-wider mb-2">
                        <span className="text-foreground">Audit</span>AI
                    </h1>
                    <p className="text-text-secondary text-xl font-light mt-4">
                        Sign in to AuditAI
                    </p>
                </div>

                {/* OAuth2 - Sign in with Google */}
                <button
                    onClick={handleGoogleSignIn}
                    // Near Black button background, no shadow
                    className="w-full flex items-center justify-center py-2.5 space-x-3 px-4 mb-8 text-background font-semibold bg-foreground rounded-md transition duration-150  group cursor-pointer active:scale-99 hover:shadow-xl shadow-white/10"
                    disabled={isLoading}
                >
                    {/* <Chrome className="w-5 h-5 mr-3 text-white group-hover:text-white" /> */}
                    <Image
                        src={"/search.png"}
                        width={22}
                        height={22}
                        alt="Google-logo"
                    ></Image>
                    <span>Sign in with Google</span>
                </button>

                <div className="relative flex items-center justify-center mb-8">
                    {/* Darker separator */}
                    <div className="grow border-t border-text-muted"></div>
                    <span className="shrink mx-4 text-text-muted text-xs uppercase">
                        or continue with
                    </span>
                    <div className="grow border-t border-text-muted"></div>
                </div>

                {/* Email/Password Form */}
                <form onSubmit={handleEmailSignIn} className="w-full">
                    {error && (
                        <div className="mb-4 px-3 flex items-center justify-between py-2.5 bg-red-900/20 hover:bg-red-900/25 duration-200 text-red-100 border border-red-800 rounded-md text-sm w-full">
                            <span>{error}</span>
                            <button>
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
                        Icon={Lock}
                        placeholder="Password"
                        type="password"
                        value={password}
                        onChange={(e) => {
                            setPassword(e.target.value);
                            setError("");
                        }}
                    />

                    <Link
                        href="#"
                        className="text-neutral-500 text-sm hover:text-pink-300 w-max transition duration-200 block"
                        onClick={(e) => {
                            console.log("Forgot Password clicked");
                        }}
                    >
                        Forgot Password?
                    </Link>

                    {/* Sign In Button */}
                    <button
                        type="submit"
                        // Accent Pink button, no shadow/glow
                        className="w-full flex items-center justify-center text-[16px] py-2.5 px-4 mt-6 text-white border border-accent-dark/50 bg-accent-dark/40 rounded-md transition duration-200 hover:bg-accent-dark hover:shadow-lg shadow-pink-400/10 focus:outline-none disabled:opacity-50 cursor-pointer"
                        disabled={isLoading}
                    >
                        {isLoading ? (
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
                                <LogIn className="w-5 h-5 mr-2" />
                                Sign In
                            </>
                        )}
                    </button>
                </form>

                {/* Footer Links */}
                <div className="mt-8 pt-6 border-t border-border-muted/40 text-center text-sm space-y-2">
                    Don't have an account?
                    <Link
                        href="#"
                        className="text-text-muted hover:text-accent-light transition duration-150 flex items-center justify-center"
                        onClick={(e) => {
                            console.log("Sign Up clicked");
                        }}
                    >
                        <span className="ml-1">Create an account</span>
                        <ArrowRight className="w-3 h-3 ml-1" />
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;
