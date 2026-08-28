"use client";

import { useEffect, useState } from "react";
import styles from "./page.module.css";

type Transaction = { id: string; occurred_at: string | null; merchant: string; category: string; amount: number; status: string; payment_method: string };
type Dashboard = { items: Transaction[]; total: number };
const api = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const money = new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 });

export default function Home() {
  const [data, setData] = useState<Dashboard | null>(null);
  const [balance, setBalance] = useState<number | null>(null);
  const [search, setSearch] = useState("");
  const [error, setError] = useState("");
  const [selected, setSelected] = useState<Transaction | null>(null);
  useEffect(() => { const timer = setTimeout(async () => { try { const [transactions, wallet] = await Promise.all([fetch(`${api}/api/transactions?search=${encodeURIComponent(search)}&page_size=12`), fetch(`${api}/api/rewards/balance`)]); if (!transactions.ok || !wallet.ok) throw Error("Dashboard data is unavailable."); setData(await transactions.json()); setBalance((await wallet.json()).balance); setError(""); } catch (e) { setError(e instanceof Error ? e.message : "Unable to load dashboard."); } }, 250); return () => clearTimeout(timer); }, [search]);
  return <main><header><a className={styles.brand} href="#top"><b>α</b> Alpha</a><nav>Overview&nbsp;&nbsp;&nbsp; Activity&nbsp;&nbsp;&nbsp; Rewards</nav><span className={styles.coins}>✦ {balance?.toLocaleString("en-IN") ?? "—"} coins</span></header><section className={styles.hero} id="top"><p>YOUR FINANCIAL PULSE</p><h1>Spend with<br/><em>clarity.</em></h1><span>₹</span><article>A considered view of every payment, your everyday habits, and the rewards you are earning along the way.</article></section><section className={styles.cards}><div><small>THIS PERIOD</small><strong>{data ? `${data.total.toLocaleString("en-IN")} payments` : "Loading…"}</strong><i>All matching transactions</i></div><div><small>COIN BALANCE</small><strong>{balance?.toLocaleString("en-IN") ?? "—"}</strong><i>Earned from successful payments</i></div><div><small>SMARTER SPENDING</small><strong>Stay in control</strong><i>Explore your transaction history</i></div></section><section className={styles.activity}><div className={styles.heading}><div><p>ALL ACTIVITY</p><h2>Every transaction, in one place.</h2></div><input value={search} onChange={e => setSearch(e.target.value)} placeholder="⌕  Search merchants" /></div>{error ? <div className={styles.error}>{error} Start PostgreSQL and the API, then refresh.</div> : <div className={styles.table}><table><thead><tr><th>Date</th><th>Merchant</th><th>Category</th><th>Amount</th><th>Status</th></tr></thead><tbody>{data?.items.map(item => <tr key={item.id} onClick={() => setSelected(item)}><td>{item.occurred_at ? new Date(item.occurred_at).toLocaleDateString("en-IN", {day:"numeric",month:"short",year:"numeric"}) : "—"}</td><td><b>{item.merchant}</b><small>{item.payment_method}</small></td><td><mark>{item.category}</mark></td><td><b>{money.format(item.amount)}</b></td><td><em className={styles[item.status.toLowerCase()]}>{item.status.toLowerCase()}</em></td></tr>)}</tbody></table>{!data && <div className={styles.loading}>Loading your activity…</div>}</div>}</section>{selected && <aside className={styles.drawer}><button onClick={()=>setSelected(null)}>×</button><p>TRANSACTION DETAILS</p><h2>{selected.merchant}</h2><strong>{money.format(selected.amount)}</strong><dl><dt>Category</dt><dd>{selected.category}</dd><dt>Method</dt><dd>{selected.payment_method}</dd><dt>Reference</dt><dd>{selected.id}</dd></dl></aside>}</main>;
}
