# Task Management System

A full-stack task management application built with Python (backend) and JavaScript/HTML/CSS (frontend).

## Features

- Create, read, update, and delete tasks
- Set priority levels for tasks
- Filter tasks by status (All/Active/Completed)
- Persistent storage using SQLite
- Modern and responsive UI

## Tech Stack

- Frontend:
  - HTML5
  - CSS3
  - JavaScript (ES6+)
  - Vite (Build tool)
- Backend:
  - Python
  - SQLite
  - HTTP Server

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.6 or higher)
- npm or yarn

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/task-management-system.git
   cd task-management-system
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Start the Python backend server:
   ```bash
   python3 server.py
   ```

4. In a new terminal, start the frontend development server:
   ```bash
   npm run dev
   ```

5. Open your browser and visit `http://localhost:5173`

## Project Structure

```
task-management-system/
├── index.html
├── main.js
├── style.css
├── server.py
├── package.json
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.