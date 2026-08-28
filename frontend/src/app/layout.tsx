import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Alpha | Rewards and spending",
  description: "A personal spending and rewards dashboard.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
