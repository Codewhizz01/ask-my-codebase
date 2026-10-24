import { Component, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface Source { file: string; start_line: number; end_line: number; access: string; text: string; }

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  question = signal('');
  role = signal('guest');
  roles = ['guest', 'staff', 'admin'];
  answer = signal('');
  sources = signal<Source[]>([]);
  loading = signal(false);
  error = signal('');
  searched = signal(false);
  copied = signal(-1);
  examples = [
    'How does login work?',
    'Where is the password hashed?',
    'How is a document created?',
    'Where is the database configured?',
  ];

  constructor(private http: HttpClient) {}

  useExample(q: string) {
    this.question.set(q);
    this.ask();
  }

  changeRole(r: string) {
    this.role.set(r);
  }

  copy(text: string, i: number) {
    navigator.clipboard.writeText(text);
    this.copied.set(i);
    setTimeout(() => this.copied.set(-1), 1500);
  }

  ask() {
    const q = this.question().trim();
    if (!q) return;
    this.loading.set(true);
    this.error.set('');
    this.http
      .get<{ answer: string; sources: Source[] }>('http://127.0.0.1:8000/ask', {
        params: { q, k: 5, role: this.role() },
      })
      .subscribe({
        next: (res) => {
          this.answer.set((res.answer || '').replace(/\*\*/g, ''));
          this.sources.set(res.sources);
          this.searched.set(true);
          this.loading.set(false);
        },
        error: () => {
          this.error.set('Could not reach the API. Is uvicorn running?');
          this.loading.set(false);
        },
      });
  }
}