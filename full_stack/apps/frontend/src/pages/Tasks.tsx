import { useEffect, useState } from "react";

type Task = { id: number; title: string; status: "TODO" | "IN_PROGRESS" | "DONE" };

export default function Tasks() {
	const [tasks, setTasks] = useState<Task[]>([]);
	const token = localStorage.getItem("token");
	useEffect(() => {
		fetch("/api/tasks", { headers: { Authorization: `Bearer ${token}` } })
			.then(r => r.json()).then(setTasks).catch(() => setTasks([]));
	}, []);
	return (
		<div className="space-y-4">
			<h1 className="text-xl font-semibold">Tasks</h1>
			<ul className="divide-y bg-white rounded border">
				{tasks.map(t => (
					<li key={t.id} className="p-3 flex justify-between"><span>{t.title}</span><span className="text-sm text-gray-600">{t.status}</span></li>
				))}
			</ul>
		</div>
	);
}