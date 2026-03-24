<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

type Book = {
  title: string
  author: string
  isbn: string
  pages: number
  available: boolean
}

const allBooks = ref<Book[]>([])
const searchQuery = ref('')
const statusFilter = ref<'all' | 'available' | 'borrowed'>('all')
const loading = ref(false)
const error = ref('')
const successMsg = ref('')

const title = ref('')
const author = ref('')
const isbn = ref('')
const pages = ref<number | null>(null)

const filteredBooks = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()
  return allBooks.value.filter((book) => {
    if (statusFilter.value === 'available' && !book.available) return false
    if (statusFilter.value === 'borrowed' && book.available) return false
    if (!query) return true
    return (
      book.title.toLowerCase().includes(query) ||
      book.author.toLowerCase().includes(query) ||
      book.isbn.toLowerCase().includes(query)
    )
  })
})

const canAdd = computed(
  () =>
    title.value.trim().length > 0 &&
    author.value.trim().length > 0 &&
    isbn.value.trim().length > 0 &&
    pages.value !== null &&
    pages.value > 0,
)

const flash = (msg: string, isError = false) => {
  if (isError) { error.value = msg; successMsg.value = '' }
  else { successMsg.value = msg; error.value = '' }
  setTimeout(() => { error.value = ''; successMsg.value = '' }, 3500)
}

const loadSampleBooks = () => {
  allBooks.value = [
    { title: 'The Hobbit', author: 'J.R.R. Tolkien', isbn: '978-0261103344', pages: 310, available: true },
    { title: '1984', author: 'George Orwell', isbn: '978-0451524935', pages: 328, available: false },
    { title: 'Clean Code', author: 'Robert C. Martin', isbn: '978-0132350884', pages: 464, available: true },
  ]
}

const getBooks = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await fetch('http://localhost:5000/books')
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
    const data = await res.json()
    allBooks.value = data.map((item: any, idx: number) => ({
      title: String(item.title ?? `Book ${idx + 1}`),
      author: String(item.author ?? 'Unknown'),
      isbn: String(item.isbn ?? `${idx}-${Date.now()}`),
      pages: Number(item.pages ?? 0),
      available: item.available === undefined ? true : Boolean(item.available),
    }))
    if (allBooks.value.length === 0) loadSampleBooks()
  } catch (e) {
    flash('Could not reach API — showing sample data.', true)
    loadSampleBooks()
  } finally {
    loading.value = false
  }
}

const addBook = async () => {
  if (!canAdd.value) return
  const newBook: Book = {
    title: title.value.trim(),
    author: author.value.trim(),
    isbn: isbn.value.trim(),
    pages: pages.value ?? 0,
    available: true,
  }
  try {
    const res = await fetch('http://localhost:5000/books', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newBook),
    })
    if (!res.ok) {
      const err = await res.json()
      throw new Error(err.error ?? `POST failed ${res.status}`)
    }
    await getBooks()
    title.value = ''; author.value = ''; isbn.value = ''; pages.value = null
    flash(`"${newBook.title}" added successfully.`)
  } catch (e: any) {
    flash(e.message ?? 'Failed to add book.', true)
    allBooks.value.unshift(newBook)
  }
}

const removeBook = async (book: Book) => {
  try {
    const res = await fetch(`http://localhost:5000/books/${encodeURIComponent(book.title)}`, {
      method: 'DELETE',
    })
    if (!res.ok) throw new Error(`DELETE failed ${res.status}`)
    await getBooks()
    flash(`"${book.title}" removed.`)
  } catch (e) {
    flash('Could not remove from API; removed locally.', true)
    allBooks.value = allBooks.value.filter((b) => b.isbn !== book.isbn)
  }
}

const clearFilters = () => { searchQuery.value = ''; statusFilter.value = 'all' }

onMounted(getBooks)
</script>

<template>
  <div class="page">
    <div class="card">
      <!-- Header -->
      <div class="card-header">
        <div class="header-left">
          <span class="header-icon">📚</span>
          <div>
            <h1>Library Manager</h1>
            <p class="subtitle">{{ allBooks.length }} book{{ allBooks.length !== 1 ? 's' : '' }} in collection</p>
          </div>
        </div>
        <button class="btn btn-ghost" @click="getBooks" :disabled="loading">
          <span :class="{ spin: loading }">↻</span> Refresh
        </button>
      </div>

      <!-- Toast -->
      <transition name="toast">
        <div v-if="successMsg" class="toast toast-success">✓ {{ successMsg }}</div>
        <div v-else-if="error" class="toast toast-error">⚠ {{ error }}</div>
      </transition>

      <!-- Add book form -->
      <div class="section-label">Add a book</div>
      <div class="add-form">
        <input v-model="title"         class="inp"        placeholder="Title"  aria-label="Title" />
        <input v-model="author"        class="inp"        placeholder="Author" aria-label="Author" />
        <input v-model="isbn"          class="inp inp-sm" placeholder="ISBN"   aria-label="ISBN" />
        <input v-model.number="pages"  class="inp inp-xs" placeholder="Pages" type="number" min="1" aria-label="Pages" />
        <button class="btn btn-primary" @click="addBook" :disabled="!canAdd">+ Add Book</button>
      </div>

      <!-- Filter bar -->
      <div class="filter-bar">
        <div class="search-wrap">
          <span class="search-icon">🔍</span>
          <input v-model="searchQuery" class="search-inp" placeholder="Search title, author or ISBN…" />
        </div>
        <div class="filter-pills">
          <button
            v-for="opt in (['all', 'available', 'borrowed'] as const)"
            :key="opt"
            class="pill"
            :class="{ active: statusFilter === opt }"
            @click="statusFilter = opt"
          >
            {{ opt.charAt(0).toUpperCase() + opt.slice(1) }}
          </button>
          <button v-if="searchQuery || statusFilter !== 'all'" class="pill pill-clear" @click="clearFilters">✕ Clear</button>
        </div>
      </div>

      <!-- Book count -->
      <div class="book-count">
        <span v-if="loading">Loading...</span>
        <span v-else>Showing {{ filteredBooks.length }} of {{ allBooks.length }} book{{ allBooks.length !== 1 ? 's' : '' }}</span>
      </div>

      <!-- Table -->
      <div class="table-wrap">
        <table class="book-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Author</th>
              <th>ISBN</th>
              <th class="num">Pages</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="6" class="center-cell">
                <span class="spinner"></span> Loading…
              </td>
            </tr>
            <tr v-else-if="filteredBooks.length === 0">
              <td colspan="6" class="center-cell muted">
                No books in the library yet.
              </td>
            </tr>
            <tr v-for="book in filteredBooks" :key="book.isbn">
              <td class="td-title">{{ book.title }}</td>
              <td>{{ book.author }}</td>
              <td class="muted mono">{{ book.isbn }}</td>
              <td class="num muted">{{ book.pages }}</td>
              <td>
                <span class="badge" :class="book.available ? 'badge-ok' : 'badge-out'">
                  {{ book.available ? 'Available' : 'Borrowed' }}
                </span>
              </td>
              <td>
                <button class="btn btn-danger" @click="removeBook(book)">Remove</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ── Reset / page ────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.page {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1f36 0%, #16213e 60%, #0f3460 100%);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 2.5rem 1rem;
  font-family: Inter, system-ui, -apple-system, Segoe UI, sans-serif;
}

/* ── Card ───────────────────────────────────────────────────── */
.card {
  width: 100%;
  max-width: 1050px;
  background: #ffffff;
  border-radius: 1.25rem;
  box-shadow: 0 24px 60px rgba(0,0,0,0.35);
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 2rem;
  background: linear-gradient(90deg, #1e3a5f 0%, #2d6bc4 100%);
  color: #fff;
}

.header-left { display: flex; align-items: center; gap: 1rem; }
.header-icon { font-size: 2rem; line-height: 1; }

h1 { font-size: 1.45rem; font-weight: 700; letter-spacing: -0.02em; color: #fff; }
.subtitle { font-size: 0.82rem; color: rgba(255,255,255,0.65); margin-top: 0.2rem; }

/* ── Toast ──────────────────────────────────────────────────── */
.toast {
  margin: 0.75rem 2rem 0;
  padding: 0.65rem 1rem;
  border-radius: 0.6rem;
  font-size: 0.9rem;
  font-weight: 500;
}
.toast-success { background: #ecfdf5; color: #065f46; border: 1px solid #6ee7b7; }
.toast-error   { background: #fef2f2; color: #991b1b; border: 1px solid #fca5a5; }

.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(-6px); }

/* ── Section label ──────────────────────────────────────────── */
.section-label {
  padding: 1.25rem 2rem 0.5rem;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #64748b;
}

/* ── Add form ───────────────────────────────────────────────── */
.add-form {
  display: flex;
  gap: 0.6rem;
  padding: 0 2rem 1.25rem;
  flex-wrap: nowrap;
  align-items: center;
}

.inp {
  flex: 2;
  min-width: 0;
  height: 2.4rem;
  padding: 0 0.75rem;
  border: 1.5px solid #e2e8f0;
  border-radius: 0.6rem;
  font-size: 0.9rem;
  color: #1e293b;
  background: #f8fafc;
  transition: border-color 0.15s;
}
.inp:focus { outline: none; border-color: #2d6bc4; background: #fff; }
.inp-sm { flex: 1.5; }
.inp-xs { flex: 1; }

/* ── Buttons ────────────────────────────────────────────────── */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0 1rem;
  height: 2.4rem;
  border: none;
  border-radius: 0.6rem;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.15s, background 0.15s;
  white-space: nowrap;
}
.btn:disabled { opacity: 0.45; cursor: not-allowed; }

.btn-primary { background: #2d6bc4; color: #fff; }
.btn-primary:not(:disabled):hover { background: #1e55a3; }

.btn-danger  { background: #fee2e2; color: #b91c1c; font-size: 0.82rem; height: 2rem; padding: 0 0.75rem; }
.btn-danger:hover { background: #fecaca; }

.btn-ghost   { background: rgba(255,255,255,0.15); color: #fff; border: 1px solid rgba(255,255,255,0.3); }
.btn-ghost:not(:disabled):hover { background: rgba(255,255,255,0.25); }

.link-btn { background: none; border: none; color: #2d6bc4; cursor: pointer; font-size: inherit; text-decoration: underline; padding: 0; }

/* ── Filter bar ─────────────────────────────────────────────── */
.filter-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0 2rem 1.25rem;
  flex-wrap: wrap;
}

.search-wrap {
  position: relative;
  flex: 1;
  min-width: 200px;
}
.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.85rem;
  pointer-events: none;
}
.search-inp {
  width: 100%;
  height: 2.4rem;
  padding: 0 0.75rem 0 2.25rem;
  border: 1.5px solid #e2e8f0;
  border-radius: 0.6rem;
  font-size: 0.9rem;
  background: #f8fafc;
  color: #1e293b;
  transition: border-color 0.15s;
}
.search-inp:focus { outline: none; border-color: #2d6bc4; background: #fff; }

.filter-pills { display: flex; gap: 0.4rem; }

.pill {
  padding: 0.35rem 0.9rem;
  border: 1.5px solid #e2e8f0;
  border-radius: 2rem;
  background: #fff;
  font-size: 0.82rem;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.15s;
}
.pill:hover { border-color: #2d6bc4; color: #2d6bc4; }
.pill.active { background: #2d6bc4; border-color: #2d6bc4; color: #fff; }
.pill-clear  { border-color: #fca5a5; color: #b91c1c; }
.pill-clear:hover { background: #fee2e2; border-color: #f87171; }

/* ── Table ──────────────────────────────────────────────────── */
.book-count {
  padding: 0 2rem 0.75rem;
  font-size: 0.82rem;
  font-weight: 600;
  color: #64748b;
}

.table-wrap { overflow-x: auto; }

.book-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.book-table th {
  padding: 0.75rem 1.25rem;
  background: #f1f5f9;
  color: #475569;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  border-bottom: 1.5px solid #e2e8f0;
  text-align: left;
}

.book-table td {
  padding: 0.9rem 1.25rem;
  border-bottom: 1px solid #f1f5f9;
  color: #1e293b;
  vertical-align: middle;
}

.book-table tbody tr:last-child td { border-bottom: none; }
.book-table tbody tr:hover td { background: #f8fafc; }

.td-title { font-weight: 600; }
.num      { text-align: right; }
.muted    { color: #94a3b8; }
.mono     { font-family: 'SF Mono', 'Fira Code', monospace; font-size: 0.82rem; }

.center-cell { text-align: center; padding: 2.5rem; color: #94a3b8; }

/* ── Badge ──────────────────────────────────────────────────── */
.badge {
  display: inline-block;
  padding: 0.2rem 0.65rem;
  border-radius: 2rem;
  font-size: 0.75rem;
  font-weight: 700;
}
.badge-ok  { background: #dcfce7; color: #166534; }
.badge-out { background: #fef3c7; color: #92400e; }

/* ── Spinner ────────────────────────────────────────────────── */
.spinner {
  display: inline-block;
  width: 1rem; height: 1rem;
  border: 2px solid #e2e8f0;
  border-top-color: #2d6bc4;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  vertical-align: middle;
  margin-right: 0.4rem;
}
.spin { display: inline-block; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>