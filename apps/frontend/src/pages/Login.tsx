import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

export default function Login() {
	const navigate = useNavigate();
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [error, setError] = useState<string | null>(null);
	async function onSubmit(e: React.FormEvent) {
		e.preventDefault();
		setError(null);
		try {
			const res = await fetch("/api/auth/login", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ email, password }),
			});
			if (!res.ok) throw new Error("Login failed");
			const data = await res.json();
			localStorage.setItem("token", data.token);
			navigate("/projects");
		} catch (err) {
			setError((err as Error).message);
		}
	}
	return (
		<div className="max-w-md mx-auto">
			<h1 className="text-xl font-semibold mb-4">Login</h1>
			<form onSubmit={onSubmit} className="space-y-3">
				<input className="w-full border px-3 py-2 rounded" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
				<input className="w-full border px-3 py-2 rounded" placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
				{error && <div className="text-red-600 text-sm">{error}</div>}
				<button className="bg-blue-600 text-white px-4 py-2 rounded" type="submit">Login</button>
				<p className="text-sm">No account? <Link className="underline" to="/register">Register</Link></p>
			</form>
		</div>
	);
}