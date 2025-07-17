# Malfunctional Website: An Interactive Learning Tool

This project is an intentionally "malfunctional" website designed to serve as an interactive, educational tool for web developers. It demonstrates common website errors in a controlled environment, turning error pages into learning opportunities. Each page explains why a specific error occurs and provides best practices to prevent it, all within a modern and clean user interface.

## Tech Stack

This project is built using the **MERN** stack:

-   **Frontend:** **React** (with Create React App)
    -   **Routing:** React Router
    -   **Styling:** CSS with a modern, dark theme
-   **Backend:** **Node.js** with **Express.js**
    -   **API:** A simple REST API to serve intentional errors.
-   **Database:** Not currently used, but can be extended with MongoDB if needed.

## Features

-   **Interactive Error Demonstrations:** Navigate to different endpoints to experience common web errors firsthand.
-   **Educational Content:** Each error page includes a detailed explanation of the error, its common causes, and how to prevent it.
-   **Modern UI:** A clean, dark-themed, and responsive design.

### Implemented Error Pages

-   **404 Not Found:** Demonstrates a classic "page not found" error.
-   **500 Internal Server Error:** Shows how a backend failure can impact the user experience.
-   **Broken Images:** Illustrates what happens when image links are incorrect.
-   **Unresponsive UI:** Simulates a button that becomes unresponsive after being clicked.

## Getting Started

Follow these instructions to get the project running on your local machine.

### Prerequisites

-   Node.js and npm (or yarn) installed on your system.

### Installation

1.  **Clone the repository (or download the source code).**

2.  **Install backend dependencies:**
    ```bash
    cd malfunctional_website/backend
    npm install
    ```

3.  **Install frontend dependencies:**
    ```bash
    cd malfunctional_website/frontend
    npm install
    ```

### Running the Application

You need to run both the backend and frontend servers simultaneously in separate terminals.

1.  **Start the backend server:**
    ```bash
    cd malfunctional_website/backend
    node server.js
    ```
    The backend will be running at `http://localhost:5001`.

2.  **Start the frontend development server:**
    ```bash
    cd malfunctional_website/frontend
    npm start
    ```
    The frontend application will open automatically in your browser at `http://localhost:3000`.

Once both servers are running, you can navigate the website and explore the different error pages.
