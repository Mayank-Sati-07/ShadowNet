interface StatCardProps {
  title: string;
  value: string | number;
  description?: string;
  icon: React.ReactNode;
}


export default function StatCard({
  title,
  value,
  description,
  icon,
}: StatCardProps) {

  return (
    <div className="
      rounded-xl
      border border-slate-800
      bg-[#0c1220]
      p-5
      transition
      hover:border-slate-700
    ">

      <div className="flex items-start justify-between">

        <div>

          <p className="text-sm text-slate-500">
            {title}
          </p>

          <p className="mt-2 text-3xl font-bold text-white">
            {value}
          </p>

          {description && (
            <p className="mt-2 text-xs text-slate-500">
              {description}
            </p>
          )}

        </div>

        <div className="rounded-lg bg-blue-500/10 p-3 text-blue-400">
          {icon}
        </div>

      </div>

    </div>
  );
}