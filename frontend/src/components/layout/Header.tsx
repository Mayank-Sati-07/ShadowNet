import { Search, Bell } from "lucide-react";

interface HeaderProps {
  onSearch: (value: string) => void;
  title?: string;
}

export default function Header({ onSearch, title = "Dashboard" }: HeaderProps) {
  return (
    <header className="fixed left-64 right-0 top-0 z-30 h-20 bg-[#0E0417] px-8">
      <div className="flex h-full items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-[var(--color-primary)] tracking-wide">
            {title}
          </h2>
          <p className="text-xs text-[var(--color-muted-foreground)] uppercase tracking-wider mt-1">
            ShadowNet / {title}
          </p>
        </div>

        <div className="flex items-center gap-4">
          <div className="relative">
            <Search
              size={17}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-muted-foreground)]"
            />
            <input
              onChange={(e) => onSearch(e.target.value)}
              placeholder="Search person ID..."
              className="
                w-72 border border-[var(--color-border)]
                bg-[var(--color-card)]/50 py-2.5 pl-10 pr-4
                text-sm text-[var(--color-foreground)] outline-none
                placeholder:text-[var(--color-muted-foreground)]
                focus:border-[var(--color-primary)] focus:ring-2 focus:ring-[var(--color-primary)]/20
                transition-all duration-300 rounded-lg shadow-sm backdrop-blur-md
              "
            />
          </div>

          <button className="border border-[var(--color-border)] bg-[var(--color-card)]/50 p-2.5 text-[var(--color-muted-foreground)] hover:text-[var(--color-primary)] rounded-lg transition-all duration-300 hover:border-[var(--color-primary)]/50 hover:shadow-md shadow-sm backdrop-blur-md">
            <Bell size={18} />
          </button>
        </div>
      </div>
    </header>
  );
}