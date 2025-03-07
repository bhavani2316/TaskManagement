from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse
import sqlite3
from datetime import datetime

class TaskServer(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        if self.path == '/api/tasks':
            conn = sqlite3.connect('tasks.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks')
            tasks = cursor.fetchall()
            conn.close()
            
            tasks_list = [
                {
                    'id': task[0],
                    'text': task[1],
                    'priority': task[2],
                    'completed': bool(task[3]),
                    'created_at': task[4]
                }
                for task in tasks
            ]
            
            self._set_headers()
            self.wfile.write(json.dumps(tasks_list).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def do_POST(self):
        if self.path == '/api/tasks':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            task_data = json.loads(post_data)

            conn = sqlite3.connect('tasks.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (text, priority, completed, created_at)
                VALUES (?, ?, ?, ?)
            ''', (
                task_data['text'],
                task_data['priority'],
                task_data['completed'],
                datetime.now().isoformat()
            ))
            conn.commit()
            task_id = cursor.lastrowid
            conn.close()

            self._set_headers()
            self.wfile.write(json.dumps({
                'id': task_id,
                **task_data,
                'created_at': datetime.now().isoformat()
            }).encode())

    def do_PUT(self):
        if self.path.startswith('/api/tasks/'):
            task_id = int(self.path.split('/')[-1])
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            task_data = json.loads(post_data)

            conn = sqlite3.connect('tasks.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tasks
                SET completed = ?
                WHERE id = ?
            ''', (task_data['completed'], task_id))
            conn.commit()
            conn.close()

            self._set_headers()
            self.wfile.write(json.dumps({'success': True}).encode())

    def do_DELETE(self):
        if self.path.startswith('/api/tasks/'):
            task_id = int(self.path.split('/')[-1])
            
            conn = sqlite3.connect('tasks.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            conn.close()

            self._set_headers()
            self.wfile.write(json.dumps({'success': True}).encode())

def init_database():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            priority TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_database()
    server = HTTPServer(('localhost', 8000), TaskServer)
    print('Server running on port 8000...')
    server.serve_forever()