import { BrowserRouter, Routes, Route, Navigate, Link } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Projects from "./pages/Projects";
import Tasks from "./pages/Tasks";

const queryClient = new QueryClient();

function App() {
	return (
		<QueryClientProvider client={queryClient}>
			<BrowserRouter>
				<div className="min-h-screen bg-gray-50 text-gray-900">
					<header className="border-b bg-white">
						<div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
							<Link to="/" className="font-semibold">Internship Demo</Link>
							<nav className="space-x-4 text-sm">
								<Link to="/projects" className="hover:underline">Projects</Link>
								<Link to="/tasks" className="hover:underline">Tasks</Link>
								<Link to="/login" className="hover:underline">Login</Link>
							</nav>
						</div>
					</header>
					<main className="max-w-5xl mx-auto px-4 py-6">
						<Routes>
							<Route path="/" element={<Home />} />
							<Route path="/login" element={<Login />} />
							<Route path="/register" element={<Register />} />
							<Route path="/projects" element={<Projects />} />
							<Route path="/tasks" element={<Tasks />} />
							<Route path="*" element={<Navigate to="/" />} />
						</Routes>
					</main>
				</div>
			</BrowserRouter>
			<ReactQueryDevtools initialIsOpen={false} />
		</QueryClientProvider>
	);
}

export default App;
