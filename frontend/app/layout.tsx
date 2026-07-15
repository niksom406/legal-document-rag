import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ABC Matter Assistant — Internal AI Tool",
  description:
    "Internal AI assistant for ABC conveyancing staff. Upload a matter PDF and get source-grounded answers with clickable citations. Read-only. For staff review only.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,400&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
