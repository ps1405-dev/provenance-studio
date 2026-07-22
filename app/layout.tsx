import "./globals.css";
import "./fixes.css";
import type { Metadata } from "next";
export const metadata: Metadata = { title: "Provenance Studio", description: "Generate, trace, and safely reuse AI media." };
export default function RootLayout({ children }: { children: React.ReactNode }) { return <html lang="en"><body>{children}</body></html>; }
