import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

export default function Register() {
	const navigate = useNavigate();
	const [name, setName] = useState("");
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [error, setError] = useState<string | null>(null);
	async function onSubmit(e: React.FormEvent) {
		e.preventDefault();
		setError(null);
		try {
			const res = await fetch("/api/auth/register", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ name, email, password }),
			});
			if (!res.ok) throw new Error("Register failed");
			const data = await res.json();
			localStorage.setItem("token", data.token);
			navigate("/projects");
		} catch (err) {
			setError((err as Error).message);
		}
	}
	return (
		<div className="max-w-md mx-auto">
			<h1 className="text-xl font-semibold mb-4">Register</h1>
			<form onSubmit={onSubmit} className="space-y-3">
				<input className="w-full border px-3 py-2 rounded" placeholder="Name" value={name} onChange={e => setName(e.target.value)} />
				<input className="w-full border px-3 py-2 rounded" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
				<input className="w-full border px-3 py-2 rounded" placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
				{error && <div className="text-red-600 text-sm">{error}</div>}
				<button className="bg-blue-600 text-white px-4 py-2 rounded" type="submit">Create account</button>
				<p className="text-sm">Have an account? <Link className="underline" to="/login">Login</Link></p>
			</form>
		</div>
	);
}