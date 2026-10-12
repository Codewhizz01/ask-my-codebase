import { Component, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface Source { file: string; start_line: number; end_line: number; text: string; }

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  question = signal('');
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
      .get<{ sources: Source[] }>('http://127.0.0.1:8000/search', { params: { q, k: 5 } })
      .subscribe({
        next: (res) => {
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