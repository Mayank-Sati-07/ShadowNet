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
 
 border border-white/10
 bg-[#0c1220]
 p-5
 transition
 hover:border-white/10
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

 <div className="bg-transparent border border-emerald-500/30 rounded-xl bg-emerald-500/10 backdrop-blur-sm p-3 text-cyan-400">
 {icon}
 </div>

 </div>

 </div>
 );
}