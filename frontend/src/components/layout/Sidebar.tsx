import {
  LayoutDashboard,
  Users,
  Network,
  ArrowLeftRight,
  TriangleAlert,
  Search,
  FileText,
  Shield,
} from "lucide-react";
import { NavLink } from "react-router-dom";

const navigation = [
  { name: "Dashboard", path: "/", icon: LayoutDashboard },
  { name: "Network Explorer", path: "/network", icon: Network },
  { name: "Cases", path: "/cases", icon: Search },
  { name: "Persons", path: "/persons", icon: Users },
  { name: "Transactions", path: "/transactions", icon: ArrowLeftRight },
  { name: "Anomalies", path: "/anomalies", icon: TriangleAlert },
  { name: "Investigation", path: "/investigation", icon: Search },
  { name: "Documents", path: "/documents", icon: FileText },
];

export default function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 border-r border-[var(--color-border)] bg-[var(--color-background)]">
      <div className="flex h-20 items-center gap-3 border-b border-[var(--color-border)] px-6">
        <div className="flex h-10 w-10 items-center justify-center bg-[var(--color-primary)]/10 rounded-lg border border-[var(--color-primary)]/20 shadow-sm">
          <Shield className="text-[var(--color-primary)]" size={22} />
        </div>
        <div>
          <h1 className="font-bold tracking-wide text-[var(--color-foreground)]">CNAS</h1>
          <p className="text-xs text-[var(--color-muted-foreground)]">
            Investigation System
          </p>
        </div>
      </div>

      <nav className="space-y-1 p-4">
        {navigation.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === "/"}
              className={({ isActive }) =>
                `
                  flex items-center gap-3 px-4 py-3 
                  text-sm font-medium transition-all duration-300 rounded-lg
                  ${
                    isActive
                      ? "bg-[var(--color-card)] text-[var(--color-primary)] border border-[var(--color-primary)]/20 shadow-sm"
                      : "text-[var(--color-muted-foreground)] border border-transparent hover:bg-[var(--color-card)] hover:text-[var(--color-primary)] hover:border-[var(--color-border)] shadow-none"
                  }
                `
              }
            >
              <Icon size={18} />
              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}