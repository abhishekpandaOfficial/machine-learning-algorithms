import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Machine Learning Knowledge Academy | Abhishek Panda",
  description:
    "A practical, searchable machine learning knowledge base: fundamentals, algorithms, real-world scenarios, and runnable notebooks.",
  metadataBase: new URL("https://abhishekpanda.com"),
  openGraph: {
    title: "Machine Learning Knowledge Academy",
    description: "Learn ML from fundamentals to production with practical Q&A and experiments.",
    type: "website",
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
