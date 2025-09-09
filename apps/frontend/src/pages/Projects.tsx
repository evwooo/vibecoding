import { useEffect, useState } from "react";

type Project = { id: number; name: string; description?: string };

export default function Projects() {
	const [projects, setProjects] = useState<Project[]>([]);
	const [name, setName] = useState("");
	const [description, setDescription] = useState("");
	const token = localStorage.getItem("token");
	useEffect(() => {
		fetch("/api/projects", { headers: { Authorization: `Bearer ${token}` } })
			.then(r => r.json()).then(setProjects).catch(() => setProjects([]));
	}, []);
	async function onCreate(e: React.FormEvent) {
		e.preventDefault();
		const res = await fetch("/api/projects", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${token}`,
			},
			body: JSON.stringify({ name, description }),
		});
		if (res.ok) {
			const p = await res.json();
			setProjects([p, ...projects]);
			setName("");
			setDescription("");
		}
	}
	return (
		<div className="space-y-4">
			<h1 className="text-xl font-semibold">Projects</h1>
			<form onSubmit={onCreate} className="flex gap-2">
				<input className="border px-3 py-2 rounded w-56" placeholder="Name" value={name} onChange={e => setName(e.target.value)} />
				<input className="border px-3 py-2 rounded flex-1" placeholder="Description" value={description} onChange={e => setDescription(e.target.value)} />
				<button className="bg-green-600 text-white px-3 py-2 rounded" type="submit">Add</button>
			</form>
			<ul className="divide-y bg-white rounded border">
				{projects.map(p => (
					<li key={p.id} className="p-3"><span className="font-medium">{p.name}</span> <span className="text-gray-500">{p.description}</span></li>
				))}
			</ul>
		</div>
	);
}