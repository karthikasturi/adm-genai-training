# Day 14 Lab Guide: Building a React App One Feature at a Time

**Who this is for:** anyone who wants to walk the full arc of today's React session hands-on, end to end, starting from nothing — no team, no capstone API, no prior setup required. This is a companion to today's actual capstone hands-on activities (Modules 14A and 14B in the course content and slides), not a replacement for them: those exercises build against your team's real capstone UI and real capstone API; this lab builds the same skills — components, props, state, effects, axios, loading/error states, and reviewing AI-generated code — against a small, generic product-catalog app and a free public API, so every step here is exactly reproducible regardless of which team or capstone case study you're on. Module 4 continues past that core arc into the three topics Module 14C names at overview depth only — routing, writing data back, and a production build — self-paced practice for whichever of these your own team's core workflow actually needs; it isn't part of today's graded activities.

**Tech choices, and why:** this lab uses **Vite + JavaScript** throughout — the combination named on today's "Choosing Your Setup" slide as the fastest path to a first project. If your team standardized on TypeScript instead, every concept here still applies unchanged; only the file extensions (`.tsx`) and prop types would differ, and that's not covered further in this lab. The backend is the **[Fake Store API](https://fakestoreapi.com/)**, a free, public, no-authentication REST API built specifically for practicing exactly this kind of exercise — its products endpoint plays the same role here that JSONPlaceholder plays in Module 14A's own hands-on activity, except with product data instead of posts, which fits a product-catalog app more naturally.

**Source grounding:** `course-outline/Day14_Frontend_Development_React_Content.md` and `presentation/Day14_Slide_Content.md` (components, JSX, props, state, `useState`/`useEffect`, the virtual DOM and reconciliation, axios, loading/error states, and the AI-generated-code review discipline all come from there); [Vite: Getting Started](https://vite.dev/guide/) (project scaffolding); [Fake Store API](https://fakestoreapi.com/) (the practice backend); [axios documentation](https://axios.rest/) (the HTTP client swapped in during Module 3).

**Before you start:** a terminal, a code editor, and an AI coding assistant (the same one used in today's other hands-on activities). No account, API key, or team-specific setup is needed anywhere in this lab.

---

## Module 1: Environment Setup — Node.js, npm & Vite

### Exercise 1: Install Node.js and npm, and verify your environment
**Objective:**
by the end of this exercise, `node -v` and `npm -v` both print a version number, confirming a working local JavaScript runtime and package manager — the foundation every later exercise in this lab depends on.

**Prerequisites for this exercise:**
- None beyond the course prerequisites.

**Steps:**
1. Check whether Node.js and npm are already installed by running `node -v && npm -v` in a terminal — if both print version numbers, skip to Exercise 2.
2. If nothing printed, or npm is missing, install Node.js from the official installer at nodejs.org, choosing the current LTS release for your operating system, or, on Linux/macOS, install it via nvm with `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash`, restarting your terminal, then running `nvm install --lts`.
3. Re-run `node -v && npm -v` and confirm both now print a version number — Node 18 or newer is required for Vite's current tooling.
4. Confirm npm can reach the public registry by running `npm ping`, which should print `Ping success` — a lab machine behind a proxy or with no network access will fail here before it ever reaches Vite.

**Expected Result:**
`node -v` prints something like `v22.x.x` (any version 18 or newer is fine), `npm -v` prints something like `10.x.x`, and `npm ping` prints `Ping success`.

**Troubleshooting:**
- `node: command not found` right after installing → your terminal's PATH wasn't refreshed yet; close and reopen the terminal, or run `source ~/.bashrc` (or `~/.zshrc`), then retry.
- `npm ping` fails or times out → you're likely behind a network proxy or firewall; get this environment's npm proxy settings from your facilitator before continuing, since every later exercise in this lab needs npm's registry.
- Node version prints but is below 18 → reinstall using `nvm install --lts` rather than patching the existing install; Vite's current tooling requires Node 18 or newer.

### Exercise 2: Create a new Vite + React project
**Objective:**
a running local Vite development server serving a default React app, using the Vite + JavaScript combination named on today's tooling slide as the fastest path to a first project.

**Prerequisites for this exercise:**
- Exercise 1 completed — `node -v` and `npm -v` both succeed.

**Steps:**
1. From a folder where you keep coursework, run `npm create vite@latest product-catalog -- --template react` and wait for it to scaffold the project — this is the Vite+JS combination from today's tooling slide, not TypeScript, to keep this lab's syntax as close as possible to the plain JavaScript taught in class.
2. Move into the new project with `cd product-catalog`.
3. Install its dependencies with `npm install`, which should finish with no error and create a `node_modules` folder.
4. Start the development server with `npm run dev` and note the local URL it prints, typically `http://localhost:5173/`.
5. Open that URL in a browser and confirm you see Vite's default "Hello Vite + React" starter page with a clickable counter button.
6. Leave the dev server running in that terminal for the rest of this lab — Vite hot-reloads every file change automatically, so it never needs restarting between exercises.

**Expected Result:**
a browser tab showing Vite's default React starter page at `http://localhost:5173/`, with a working counter button that increments on click — confirming both the build tool and React are wired up correctly before any of this lab's own code is added.

**Troubleshooting:**
- Port `5173` is already in use → Vite automatically tries the next port (`5174`, ...) and prints whichever one it actually bound to; use the URL actually printed in your terminal, not always `5173`.
- The scaffold command still prompts for a framework or variant → answer `React` then `JavaScript` at the prompts if the `-- --template react` flag didn't fully suppress them, which varies slightly by npm version.
- A blank white page in the browser with a console error → check the terminal running `npm run dev` for the actual build error first; a blank page is almost always a JavaScript error, not a network issue.

---

## Module 2: Component Essentials — Building the Product Catalog

### Exercise 1: Scaffold the ProductCard and ProductList components with an AI coding assistant
**Objective:**
a small, working component tree — one parent component (`ProductList`) rendering several child components (`ProductCard`), each displaying one hardcoded product's title, price, and image — giving this lab a real UI to build every later feature onto.

**Prerequisites for this exercise:**
- Exercise 2 (Module 1) completed — the Vite dev server is running and showing the default starter page.

**Steps:**
1. Inside `src/`, create a new file `data/products.js` containing a hardcoded array of at least four product objects, each with `id`, `title`, `price`, and `image` fields — this stands in for the real API until Exercise 3.
2. Give your AI coding assistant this controlled prompt: `Create two React function components in src/components/: ProductCard.jsx, which takes a single "product" prop and renders its image, title, and price; and ProductList.jsx, which takes a "products" array prop and renders one ProductCard per item using product.id as the key. Do not add any state, any data fetching, any new npm dependency, any CSS or styling, or any PropTypes/comments beyond the code itself — these two components only render the props they're given, with plain unstyled markup.`
3. Read the AI assistant's generated code for both files line by line before accepting it, confirming neither file adds a dependency, a fetch call, a `useState`, or any styling beyond plain HTML tags — this exercise is components and props only, and extra polish just adds code you didn't write and won't recognize later.
4. Replace the contents of `src/App.jsx` with a version that imports `products` from `data/products.js` and `ProductList`, then renders `<ProductList products={products} />`.
5. Save all files and check the browser tab — Vite hot-reloads automatically — and confirm your four hardcoded products now render as cards.

**Expected Result:**
the browser shows four product cards, each with an image, a title, and a price, driven entirely by the hardcoded array in `data/products.js` flowing down through props — no network request has happened yet.

**Troubleshooting:**
- Cards render with `undefined` in place of a value → a field name in `products.js` (e.g. `title` vs. `name`) doesn't match exactly what `ProductCard.jsx` destructures; a prop name mismatch renders as `undefined`, not an error.
- React warns `Each child in a list should have a unique "key" prop` in the browser console → confirm step 2's result actually set `key={product.id}` on the mapped `ProductCard` elements, not left off entirely.
- The AI assistant added a `useState`, a fetch call, or CSS/styling anyway → reject that part of the diff and ask again, restating the controlled prompt's constraint explicitly — this exercise is deliberately components-and-props only; state and fetching are the next two exercises, and styling was never asked for.

### Exercise 2: Give ProductCard its own state — a per-card "favorite" toggle
**Objective:**
each `ProductCard` independently remembers whether it's been marked a favorite, demonstrating that state is private to each rendered copy of a component, never shared or passed down.

**Prerequisites for this exercise:**
- Exercise 1 (Module 2) completed — `ProductCard` and `ProductList` are rendering the hardcoded products.

**Steps:**
1. In `ProductCard.jsx`, import `useState` from `react`.
2. Add `const [isFavorite, setIsFavorite] = useState(false);` as the first line inside the component function.
3. Add a button below the existing price that toggles it: `<button onClick={() => setIsFavorite(!isFavorite)}>{isFavorite ? '★ Favorited' : '☆ Favorite'}</button>`.
4. Save the file, and in the browser click the favorite button on one card only.
5. Confirm the other three cards' buttons are unaffected — each still reads `☆ Favorite` — proving each `ProductCard` instance holds its own separate, isolated state.

**Expected Result:**
clicking one card's favorite button changes only that card's button text to `★ Favorited`; every other card's button remains `☆ Favorite`, confirming state is isolated per rendered component instance, not shared across them.

**Troubleshooting:**
- Clicking one card's button changes every card's text → `isFavorite` was likely hoisted into `ProductList` and passed down as a shared prop instead of living inside each `ProductCard`; move the `useState` call back into `ProductCard.jsx` itself.
- Nothing happens on click → confirm the `onClick` handler is a function (`() => setIsFavorite(...)`), not a direct call (`onClick={setIsFavorite(...)}`), which runs it immediately on every render instead of on click.
- No common pitfalls beyond the two above for this exercise.

### Exercise 3: Replace the hardcoded list with a live fetch from the Fake Store API
**Objective:**
`App`'s product data now comes from a real, live network request to the Fake Store API instead of the hardcoded array, using the exact `useEffect` data-fetching mechanic taught in today's session.

**Prerequisites for this exercise:**
- Exercise 2 (Module 2) completed.

**Steps:**
1. In `App.jsx`, import `useState` and `useEffect` from `react`.
2. Replace the hardcoded `products` import with `const [products, setProducts] = useState([]);`.
3. Add a `useEffect` with an empty dependency array that fetches `https://fakestoreapi.com/products` with the browser's built-in `fetch`, parses the JSON response, and calls `setProducts` with the result: `useEffect(() => { let ignore = false; fetch('https://fakestoreapi.com/products').then(res => res.json()).then(data => { if (!ignore) setProducts(data); }); return () => { ignore = true; }; }, []);`, matching the `ignore`-flag guard pattern from today's session exactly.
4. Save the file and confirm the browser now shows real, live product data (real titles like "Fjallraven - Foldsack No. 1 Backpack" and real prices) instead of your four hardcoded entries.
5. Open your browser's Network tab, refresh the page, and confirm a request to `fakestoreapi.com/products` actually appears and returns a `200` status.

**Expected Result:**
the page now renders around 20 real products fetched live from the Fake Store API, each still going through the same `ProductCard`/`ProductList` component tree built in Exercise 1, and the Network tab shows a successful `200` request to `fakestoreapi.com/products`.

**Troubleshooting:**
- The page shows nothing at all → check the browser console for a fetch error first; the Fake Store API is a public service and can occasionally be slow or briefly unavailable, in which case retry after a few seconds.
- The `ignore` flag seems to do nothing today → that's expected on a fast local fetch; the guard exists for when a component unmounts, or refetches, before a slow request resolves, which won't reliably show up in this simple exercise — keep it anyway, it's the pattern taught in class and Exercise 1 of Module 3 depends on it staying in place.
- `products.map is not a function` in the console → the fetch resolved to something other than an array (often an error object); add `console.log(data)` inside the `.then` before calling `setProducts` to see what actually came back.

---

## Module 3: Making the API Call Production-Honest

### Exercise 1: Add loading and error states around the fetch
**Objective:**
the screen now clearly shows one of three states — loading, error, or the real product list — instead of an ambiguous blank screen while the request is in flight or if it fails.

**Prerequisites for this exercise:**
- Exercise 3 (Module 2) completed.

**Steps:**
1. In `App.jsx`, add two more state values: `const [isLoading, setIsLoading] = useState(true);` and `const [error, setError] = useState(null);`.
2. At the very start of the `useEffect`'s body, before the fetch call, add `setIsLoading(true); setError(null);` so both reset on every run.
3. Chain `.catch(err => { if (!ignore) setError(err); })` onto the existing fetch promise, and add `.finally(() => { if (!ignore) setIsLoading(false); })` after it.
4. In the JSX returned by `App`, render one of three things: a `<p>Loading products...</p>` while `isLoading` is true, a `<p>Something went wrong: {error.message}</p>` if `error` is set, or the existing `<ProductList products={products} />` otherwise.
5. Confirm the loading message appears briefly on every page refresh before the real products render — open DevTools' Network tab and throttle to "Slow 3G" if it's too fast to see.
6. Deliberately break the request by changing the URL to `https://fakestoreapi.com/does-not-exist`, refresh, and confirm the error message now renders instead of a blank screen or a stuck loading message.
7. Revert the URL back to `https://fakestoreapi.com/products` and confirm the real product list renders normally again.

**Expected Result:**
with a throttled connection, the browser briefly shows "Loading products..." before showing the real product cards; with a broken URL, it shows a "Something went wrong" message instead of hanging or going blank; with the URL restored, it shows the real products again.

**Troubleshooting:**
- The loading message never disappears, even on success → `.finally()` was likely left off, or `setIsLoading(false)` was only added inside `.catch`, not on the success path too.
- The error message shows even when the request actually succeeds → `error` was probably never reset to `null` at the start of the effect, so a previous run's error state is stuck; confirm step 2's reset line runs before every fetch attempt.
- The broken-URL test shows a blank screen instead of the error message → a fetch to a `404` path still resolves successfully (`fetch` only rejects on a true network failure, not on an HTTP error status); check `res.ok` before calling `res.json()` and throw if it's false, so a `404` actually reaches the `.catch`.

### Exercise 2: Swap the fetch call for axios with an AI coding assistant, then review and correct the diff
**Objective:**
the same request now uses axios instead of the browser's native `fetch`, and the team has practiced reading an AI-generated diff line by line and catching a real issue before accepting it — the same review discipline used throughout this course's AI-assisted work.

**Prerequisites for this exercise:**
- Exercise 1 (Module 3) completed.

**Steps:**
1. Install axios with `npm install axios`.
2. Give your AI coding assistant this controlled prompt: `In src/App.jsx, replace the fetch() call to https://fakestoreapi.com/products with an equivalent axios.get() call. Preserve the existing ignore-flag cleanup pattern exactly. Preserve the existing isLoading and error state resets at the start of the effect exactly. Do not change any other part of the file.`
3. Before accepting anything, read the diff line by line and check specifically for the three things named in the prompt: the `ignore` flag is still present and still checked before every setter call, both `isLoading` and `error` still reset at the start of the effect, and the URL is unchanged.
4. Confirm the assistant correctly used `response.data` (axios's already-parsed body) rather than calling `.json()` on it, which would throw since axios doesn't return a raw `Response` object the way `fetch` does.
5. Deliberately re-run the broken-URL test from Exercise 1 (temporarily point the request at a nonexistent path), confirm the error message still renders, then revert the URL.
6. In the browser's Network tab, confirm the request now shows as an XHR request (axios's underlying transport) rather than a `fetch` request.

**Expected Result:**
the app behaves identically to before the swap (same loading, error, and success states), the Network tab shows the request going out as an XHR call instead of a `fetch`, and the diff review in step 3 turned up no dropped guard, no missing state reset, and no invented URL.

**Troubleshooting:**
- `res.json is not a function` (or similar) after the swap → the assistant left in a `.json()` call meant for `fetch`'s response object; axios already parses JSON into `response.data`, so that call must be removed, not adapted.
- The `ignore` flag or one of the two state resets is missing after the swap → this is exactly the kind of issue this exercise is designed to catch; reject that part of the diff and ask the assistant to add back the specific missing piece, rather than regenerating the whole change from scratch.
- The error branch stops distinguishing a bad response from a network failure → axios structures failures differently from `fetch` (`error.response` vs. `error.request` vs. `error.message`); if the assistant's diff collapsed these into one generic catch, ask it explicitly to preserve the three-way distinction.

### Exercise 3: Add a category filter
**Objective:**
a dropdown that filters the visible products by category, giving this lab one more real feature built entirely from state and props already covered — no new concepts and no new dependency.

**Prerequisites for this exercise:**
- Exercise 2 (Module 3) completed.

**Steps:**
1. In `App.jsx`, add `const [selectedCategory, setSelectedCategory] = useState('all');`.
2. Compute the list of unique categories present in `products` with `const categories = ['all', ...new Set(products.map(p => p.category))];`.
3. Add a `<select>` element bound to `selectedCategory`, with an `<option>` for each entry in `categories`, and an `onChange` that calls `setSelectedCategory(event.target.value)`.
4. Compute a filtered list just before rendering: `const visibleProducts = selectedCategory === 'all' ? products : products.filter(p => p.category === selectedCategory);`.
5. Pass `visibleProducts`, not the original `products`, into `<ProductList products={visibleProducts} />`.
6. Test it: pick a category from the dropdown and confirm only products from that category remain visible, then switch back to "all" and confirm every product returns.

**Expected Result:**
selecting a category from the dropdown immediately narrows the visible product cards to only that category, with no page reload and no new network request — the same data already fetched in Exercise 3 (Module 2) is simply filtered differently before rendering, the same reconciliation mechanism from today's session, just driven by dropdown state instead of newly fetched data.

**Troubleshooting:**
- The dropdown shows categories, but selecting one clears every product → `visibleProducts` was likely computed against the wrong field name; log `products[0].category` in the console to confirm the exact field name the Fake Store API actually returns.
- The dropdown's selected value doesn't visually update when changed → confirm the `<select>`'s `value` prop is bound to `selectedCategory` (a controlled input), not left unset.
- No common pitfalls beyond the two above for this exercise.

---

## Module 4: Beyond the Basics — Routing, Writing Data Back & Shipping a Build

This module is self-paced practice for the three topics Module 14C names at overview depth only in today's session — routing, writing data back, and a production build. None of it is graded today; do whichever exercises match what your own team's core workflow actually needs (a team whose workflow is a single screen may only need Exercise 3).

### Exercise 1: Add a product detail route with React Router
**Objective:**
navigating from the product list to a specific product's own URL (for example `/products/7`) renders a dedicated `ProductDetail` view reading that id via `useParams()`, giving this app its first real second screen instead of staying one unlinkable page.

**Prerequisites for this exercise:**
- Exercise 3 (Module 3) completed — the category filter is working.

**Steps:**
1. Install React Router with `npm install react-router`.
2. Give your AI coding assistant this controlled prompt: `Create a React function component ProductDetail.jsx in src/components/ that reads a productId route param with useParams() from react-router, fetches https://fakestoreapi.com/products/{productId} with axios in a useEffect with an empty dependency array, and renders the product's title, price, description, and image once loaded, showing "Loading..." while the request is in flight. Do not add routing setup itself — that belongs in App.jsx. Do not add error-state handling, a "not found" state, CSS or styling, PropTypes, extra sub-components, or a back-navigation link — just the fetch and the four fields listed above, nothing more.`
3. Read the diff before accepting it, confirming it imports `useParams` from `react-router` (not the separate `react-router-dom` package), reuses the same `axios.get` + `useEffect` pattern already in `App.jsx`, and adds nothing beyond the fetch and the four rendered fields — no styling, no extra state, no extra files.
4. In `App.jsx`, import `BrowserRouter`, `Routes`, and `Route` from `react-router`, and wrap the existing rendered content in `<BrowserRouter>`.
5. Replace the plain `<ProductList products={visibleProducts} />` render with `<Routes><Route path="/" element={<ProductList products={visibleProducts} />} /><Route path="/products/:productId" element={<ProductDetail />} /></Routes>`.
6. In `ProductCard.jsx`, import `Link` from `react-router` and wrap each card's title in `<Link to={\`/products/${product.id}\`}>` so clicking a title navigates to that product's own route.
7. Save all files, click a product's title in the browser, and confirm the URL bar changes to `/products/<id>` and the detail view renders that exact product's data.
8. Use the browser's Back button and confirm it returns to the product list without a full page reload.

**Expected Result:**
clicking any product title navigates to its own `/products/:id` URL and renders a detail view fetched specifically for that id; Back returns to the list, and no full-page reload happens at any point (the Network tab shows no new document load, only the one request for the detail data).

**Troubleshooting:**
- `useParams is not a function`, or a similar import error → confirm the import is from `react-router`, not `react-router-dom` — this app installs the newer unified package, which folds that separate package's exports in.
- Clicking a title reloads the whole page instead of navigating → confirm `ProductCard` uses react-router's `<Link>`, not a plain `<a href="...">`, which triggers a real browser navigation instead of a client-side route change.
- The detail route renders but shows the wrong product, or `undefined` → log the `productId` read from `useParams()` and confirm it matches the id used in the `axios.get` URL — a common slip is fetching `/products/undefined` because the param name in the route path (`:productId`) doesn't match the key destructured from `useParams()`.
- The AI assistant added error handling, styling, a back link, or split the component into several files anyway → reject that part of the diff and ask again, restating the constraint explicitly; Exercise 2 adds a form directly into this same file next, and extra structure here just makes that step harder to follow.

### Exercise 2: Submit a maintenance-style request with a controlled form and axios.post
**Objective:**
a controlled form writes data back to the Fake Store API for the first time in this lab — everything built so far has only read data down; submitting now calls `axios.post` and shows its response, the same write direction a real "submit maintenance requests" workflow needs.

**Prerequisites for this exercise:**
- Exercise 1 (Module 4) completed.

**Steps:**
1. In `ProductDetail.jsx`, add two controlled state values: `const [note, setNote] = useState(''); const [submitStatus, setSubmitStatus] = useState(null);`.
2. Add a small form with one text input bound to `note`: `<input value={note} onChange={e => setNote(e.target.value)} placeholder="Describe an issue with this product" />`, plus a submit button.
3. On the form's `onSubmit`, call `e.preventDefault()` first, then `axios.post('https://fakestoreapi.com/products', { title: note }).then(res => setSubmitStatus('sent: id ' + res.data.id)).catch(() => setSubmitStatus('failed'));`.
4. Render `submitStatus` beneath the form once it's set, so the result of the write is visible on screen, not just in the console.
5. Type a short note, submit it, and confirm a "sent: id ..." message renders — per the Fake Store API's own docs this write is simulated and never actually persisted, so it's safe to submit freely.
6. Refresh the page and confirm the note you just "sent" is nowhere in the product list — direct, hands-on confirmation that this practice API's writes never persist, unlike the team's real capstone API.

**Expected Result:**
typing into the input updates it live (a controlled input), submitting shows a "sent: id ..." response from the Fake Store API with no page reload, and a refresh afterward confirms nothing was actually saved — matching the practical safety note from today's slides exactly.

**Troubleshooting:**
- The page reloads on submit → `e.preventDefault()` is missing, or isn't the first line of the submit handler; add it before the `axios.post` call.
- Typing in the input does nothing → confirm both `value={note}` and `onChange={...}` are set together on the `<input>` — setting only one leaves it either frozen or uncontrolled.
- Nothing renders after submitting → confirm `submitStatus` is actually read somewhere in the JSX below the form, not only set in state.

### Exercise 3: Build for production and serve the static output
**Objective:**
a real `dist/` folder exists, produced by `npm run build`, and `npm run preview` proves it serves correctly as plain static files — the same kind of output an EC2 instance or an Azure App Service would serve for the actual capstone demo.

**Prerequisites for this exercise:**
- Exercise 2 (Module 4) completed.

**Steps:**
1. Stop the `npm run dev` server that's been running since Module 1 (Ctrl+C in its terminal) — it isn't needed for this exercise.
2. Run `npm run build` and confirm it completes with no error, printing a summary of the files it wrote into a new `dist/` folder.
3. List the contents of `dist/` and confirm it contains an `index.html` and an `assets/` folder holding `.js` and `.css` files — no `.jsx` files anywhere, since JSX only ever existed for the build step to compile away.
4. Run `npm run preview` and open the local URL it prints, typically `http://localhost:4173/`.
5. Click through the same product list → product detail → back → form-submit flow from Exercises 1 and 2, and confirm it all still works from this static build, not the dev server.
6. Reload the preview server's page directly at a product detail URL such as `http://localhost:4173/products/7` and note whether it loads correctly or shows a blank page — a static file server has no route for `/products/7` unless it's specifically configured to fall back to `index.html`, which is exactly the kind of deployment detail a real EC2 or Azure static-hosting setup has to handle, beyond this lab's scope.

**Expected Result:**
`npm run build` produces a `dist/` folder of plain HTML/JS/CSS with no JSX anywhere in it, `npm run preview` serves that exact folder locally, and the full app — list, detail route, and form submit — works identically to the dev server, confirming this build is genuinely what a real deployment would ship.

**Troubleshooting:**
- `npm run build` fails with a syntax or import error → this is the first time this code has actually been compiled for production instead of just hot-reloaded by the dev server; read the error's file and line number directly, it's usually a mistake dev mode never caught because dev mode is more permissive.
- `npm run preview` shows a blank page with a console error about a missing asset → confirm `npm run build` actually finished successfully first, and that the `dist/` folder being served isn't a stale one left over from an earlier failed build.
- Reloading directly at `/products/7` in preview shows a blank page instead of the detail view → this is the same underlying issue named in step 6, not a new bug — a static server that only serves `index.html` for `/` has nothing to fall back to on a direct hit to a nested route, and configuring that fallback is a deployment step beyond this lab.

---

**What this lab covered, end to end:** Node.js/npm verification → a scaffolded Vite+JS project → an AI-assisted component tree (props only) → a component's own isolated state → a live `useEffect` fetch replacing hardcoded data → loading and error states → an AI-assisted axios swap with a real diff review → one feature (category filtering) built from nothing but state and props already learned → routing to a second, linkable screen → a controlled form writing data back with axios.post → a production `npm run build` served and sanity-checked with `npm run preview`. Every controlled prompt in this lab named its file, its exact scope, and what not to touch — the same discipline this course has used in every AI-assisted exercise since Day 13.
