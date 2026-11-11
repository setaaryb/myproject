// 🔗 URL Web App Google Apps Script
const GAS_URL = 'https://script.google.com/macros/s/AKfycbxzidanLsDE6_FaUPWGFDsPifV9IkH73Tg7D_u8YiIbxSY5Oin-VhR7Gu_BVod3dQ6U/exec';

let DATA = null;
const $ = id => document.getElementById(id);
const rp = n => new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(Number(n) || 0);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const isAdmin = () => { try { return localStorage.getItem('isAdminLoggedIn') === 'true'; } catch { return false; } };
const fmtDate = d => { const t = new Date(d); return isNaN(t) ? esc(d) : t.toLocaleDateString('id-ID', { day: '2-digit', month: 'short', year: 'numeric' }); };

/* ---------- API ---------- */
async function callApi(action, payload = {}) {
    try {
        if (action === 'getInitialData') return await (await fetch(`${GAS_URL}?action=getInitialData`)).json();
        return await (await fetch(GAS_URL, { method: 'POST', body: JSON.stringify({ action, ...payload }) })).json();
    } catch (e) { toast('Koneksi ke server gagal. Coba lagi.', 'bad'); return null; }
}
async function busy(btn, fn) {
    const label = btn.textContent; btn.disabled = true; btn.textContent = 'Memproses…';
    try { return await fn(); } finally { btn.disabled = false; btn.textContent = label; }
}

/* ---------- UI helper ---------- */
function toast(msg, type = 'ok') {
    const t = document.createElement('div'); t.className = 'toast ' + type; t.textContent = msg;
    $('toasts').appendChild(t); t.onclick = () => t.remove();
    setTimeout(() => { t.classList.add('bye'); setTimeout(() => t.remove(), 250); }, 3000);
}
function confirmBox(msg, yesLabel = 'Ya, hapus') {
    return new Promise(res => {
        $('confirmMsg').textContent = msg; $('confirmYes').textContent = yesLabel;
        $('confirmBox').classList.remove('hidden'); $('confirmYes').focus();
        const done = v => { $('confirmBox').classList.add('hidden'); $('confirmYes').onclick = $('confirmNo').onclick = null; res(v); };
        $('confirmYes').onclick = () => done(true); $('confirmNo').onclick = () => done(false);
    });
}

/* ---------- Helper v2 ---------- */
let mFilter = '';
const curUser = () => DATA && DATA.users.find(u => u.id === $('txUserId').value);
function loginErr(msg) {
    const e = $('loginErr'), c = document.querySelector('.login-card');
    e.textContent = msg; e.classList.remove('hidden');
    c.classList.remove('shake'); void c.offsetWidth; c.classList.add('shake');
}
function animateNumbers() {
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    document.querySelectorAll('[data-n]').forEach(el => {
        const to = Number(el.dataset.n) || 0;
        if (reduce || !to) { el.textContent = rp(to); return; }
        const t0 = performance.now(), dur = 900;
        (function f(t) {
            const p = Math.min((t - t0) / dur, 1), e = 1 - Math.pow(1 - p, 3);
            el.textContent = rp(to * e); if (p < 1) requestAnimationFrame(f);
        })(t0);
    });
}
function updateHints() {
    const u = curUser(), masuk = $('txTipe').value === 'MASUK';
    $('userHint').textContent = masuk && u
        ? (u.totalTerkumpul >= u.targetSaldo ? 'Sudah lunas ✓' : `Kurang ${rp(u.targetSaldo - u.totalTerkumpul)} dari target ${rp(u.targetSaldo)}`) : '';
    const j = Number($('txJumlah').value); $('jumlahHint').textContent = j > 0 ? '= ' + rp(j) : '';
}
function renderExtras(d) {
    const n = d.users.length, ok = d.users.filter(u => u.totalTerkumpul >= u.targetSaldo).length, tg = d.summary.totalTargetKeseluruhan;
    const pct = tg > 0 ? Math.min(100, Math.round(d.summary.totalKasTerkumpul / tg * 100)) : 0;
    $('overall').innerHTML = `<div style="display:flex;justify-content:space-between;gap:10px;font-weight:900"><span>Progres kas keseluruhan</span><span>${pct}%</span></div>
    <div class="progress big ${pct >= 100 ? 'full' : ''}"><i style="width:${pct}%"></i></div><div class="muted">${ok} dari ${n} anggota sudah lunas</div>`;
    const list = d.transactions.slice(0, 8);
    const items = list.map(t => { const m = t.tipe === 'MASUK'; return `<span>${m ? '🟢' : '🟠'} ${esc(m ? t.namaUser : t.keterangan)} <b>${m ? '+' : '−'}${rp(t.jumlah)}</b></span>`; }).join('');
    $('ticker').classList.toggle('hidden', !list.length);
    const g = items.repeat(Math.ceil(8 / Math.max(list.length, 1)));
    $('tickerTrack').innerHTML = g + g;
}

/* ---------- Routing (hash) ---------- */
function route() {
    const h = location.hash.replace('#/', '').replace('#', '');
    const page = h === 'admin' ? 'admin' : h === 'login' ? 'login' : 'public';
    if (page === 'admin' && !isAdmin()) { location.hash = '#/login'; return; }
    if (page === 'login' && isAdmin()) { location.hash = '#/admin'; return; }
    $('viewPublic').classList.toggle('hidden', page !== 'public');
    $('viewLogin').classList.toggle('hidden', page !== 'login');
    $('viewAdmin').classList.toggle('hidden', page !== 'admin');
    const cur = $({ public: 'viewPublic', login: 'viewLogin', admin: 'viewAdmin' }[page]);
    cur.classList.remove('enter'); void cur.offsetWidth; cur.classList.add('enter');
    $('btnToLogin').style.display = isAdmin() ? 'none' : 'inline-flex';
    $('btnToAdmin').style.display = isAdmin() ? 'inline-flex' : 'none';
    if (page === 'login') $('inputPass').focus();
    window.scrollTo(0, 0);
}
document.addEventListener('click', e => {
    const g = e.target.closest('[data-go]'); if (!g) return;
    location.hash = g.dataset.go === 'public' ? '#/' : '#/' + g.dataset.go;
});
window.addEventListener('hashchange', route);

/* ---------- Render ---------- */
function statsHtml(s) {
    return `<div class="stat"><small>💰 Kas terkumpul</small><b data-n="${s.totalKasTerkumpul}">${rp(s.totalKasTerkumpul)}</b></div>
    <div class="stat"><small>🎯 Target keseluruhan</small><b data-n="${s.totalTargetKeseluruhan}">${rp(s.totalTargetKeseluruhan)}</b></div>
    <div class="stat"><small>💸 Total pengeluaran</small><b data-n="${s.totalPengeluaran}">${rp(s.totalPengeluaran)}</b></div>`;
}
function txHtml(list, empty = 'Belum ada transaksi.') {
    if (!list.length) return `<li class="empty" style="display:block">${empty}</li>`;
    return list.map(t => {
        const masuk = t.tipe === 'MASUK';
        return `<li><span class="d">${fmtDate(t.tanggal)}</span>
      <span class="n">${esc(masuk ? t.namaUser : t.keterangan)}<small><span class="tag ${masuk ? 'in' : 'out'}">${masuk ? 'Masuk' : 'Keluar'}</span>${masuk && t.keterangan ? ' ' + esc(t.keterangan) : ''}</small></span>
      <span class="a ${masuk ? 'in' : 'out'}">${masuk ? '+' : '−'}${rp(t.jumlah)}</span></li>`;
    }).join('');
}
function memberCard(u, i = 0, anim = false) {
    const pct = u.targetSaldo > 0 ? Math.min(Math.round(u.totalTerkumpul / u.targetSaldo * 100), 100) : 0;
    const lunas = u.totalTerkumpul >= u.targetSaldo;
    return `<article class="member ${anim ? 'pop' : ''}" style="--i:${Math.min(i, 10)}"><h3>${esc(u.nama)}</h3>
    <div class="muted">Terbayar <b style="color:#000">${rp(u.totalTerkumpul)}</b> dari ${rp(u.targetSaldo)}</div>
    <div class="progress ${lunas ? 'full' : ''}"><i style="width:${pct}%"></i></div>
    <span class="tag ${lunas ? 'ok' : 'no'}">${lunas ? 'Lunas' : pct + '%'}</span></article>`;
}
function renderMembers(anim) {
    const q = $('searchMember').value.trim().toLowerCase();
    let list = DATA.users.filter(u => u.nama.toLowerCase().includes(q));
    if (mFilter) list = list.filter(u => (u.totalTerkumpul >= u.targetSaldo) === (mFilter === 'lunas'));
    $('pubMembers').innerHTML = list.length ? list.map((u, i) => memberCard(u, i, anim)).join('') : '<div class="empty">Anggota tidak ditemukan.</div>';
}
function renderAdminTx() {
    const f = $('txFilter').value;
    $('admTx').innerHTML = txHtml(DATA.transactions.filter(t => !f || t.tipe === f));
}
function render(d) {
    DATA = d;
    const s = d.settings, title = s.kasTitle || 'Sistem Kas';
    document.title = title;
    $('pubTitle').textContent = title; $('admLogo').textContent = title;
    $('pubPay').textContent = s.paymentInfo || '-';
    $('cfgTitle').value = s.kasTitle || ''; $('cfgPayment').value = s.paymentInfo || '';
    $('pubStats').innerHTML = $('admStats').innerHTML = statsHtml(d.summary);
    renderMembers(true);
    renderExtras(d);
    $('pubTx').innerHTML = txHtml(d.transactions);
    $('admRecent').innerHTML = txHtml(d.transactions.slice(0, 6));
    renderAdminTx();

    const unpaid = d.users.filter(u => u.totalTerkumpul < u.targetSaldo);
    $('admUnpaid').innerHTML = unpaid.length
        ? unpaid.map(u => `<div class="list-row"><div><b>${esc(u.nama)}</b><div class="muted">Kurang ${rp(u.targetSaldo - u.totalTerkumpul)}</div></div></div>`).join('')
        : '<div class="empty">Semua anggota sudah lunas 🎉</div>';

    $('txUserId').innerHTML = d.users.map(u => `<option value="${esc(u.id)}">${esc(u.nama)}</option>`).join('');
    $('admMembers').innerHTML = d.users.length
        ? d.users.map(u => `<div class="list-row"><div><b>${esc(u.nama)}</b><div class="muted">Target ${rp(u.targetSaldo)} · Terbayar ${rp(u.totalTerkumpul)}</div></div>
        <button class="btn red sm" data-del="${esc(u.id)}" data-name="${esc(u.nama)}">Hapus</button></div>`).join('')
        : '<div class="empty">Belum ada anggota. Tambahkan lewat form di samping.</div>';
}
async function load() {
    const d = await callApi('getInitialData');
    if (d && d.settings) { render(d); animateNumbers(); updateHints(); }
    else if (d) toast('Data dari server tidak sesuai format.', 'bad');
}

/* ---------- Event ---------- */
$('searchMember').addEventListener('input', () => DATA && renderMembers());
$('txFilter').addEventListener('change', () => DATA && renderAdminTx());
$('showPass').addEventListener('change', e => $('inputPass').type = e.target.checked ? 'text' : 'password');
$('inputPass').addEventListener('keydown', e => e.key === 'Enter' && $('btnLogin').click());

$('admNav').addEventListener('click', e => {
    const b = e.target.closest('button[data-tab]'); if (!b) return;
    document.querySelectorAll('#admNav button').forEach(x => x.classList.toggle('on', x === b));
    document.querySelectorAll('.tab').forEach(x => x.classList.toggle('on', x.id === b.dataset.tab));
});
$('txTipe').addEventListener('change', e => $('groupUser').classList.toggle('hidden', e.target.value !== 'MASUK'));

$('btnLogin').onclick = () => busy($('btnLogin'), async () => {
    const password = $('inputPass').value; const err = $('loginErr');
    if (!password) { loginErr('Password wajib diisi.'); return; }
    const res = await callApi('loginAdmin', { password });
    if (res && res.success) {
        try { localStorage.setItem('isAdminLoggedIn', 'true'); } catch { }
        err.classList.add('hidden'); $('inputPass').value = ''; toast('Login berhasil'); location.hash = '#/admin';
    } else { loginErr((res && res.message) || 'Password salah. Coba lagi.'); }
});
$('btnLogout').onclick = () => { try { localStorage.removeItem('isAdminLoggedIn'); } catch { } toast('Kamu sudah keluar'); location.hash = '#/'; route(); };

$('btnTx').onclick = () => busy($('btnTx'), async () => {
    const tipe = $('txTipe').value, jumlah = $('txJumlah').value;
    if (!jumlah || Number(jumlah) <= 0) return toast('Isi jumlah dengan benar.', 'bad');
    if (tipe === 'MASUK' && !$('txUserId').value) return toast('Pilih anggota dulu.', 'bad');
    const u = DATA.users.find(x => x.id === $('txUserId').value);
    const payload = {
        tipe, userId: tipe === 'MASUK' ? $('txUserId').value : '-',
        namaUser: tipe === 'MASUK' && u ? u.nama : 'PENGELUARAN KAS',
        jumlah, tanggal: $('txTanggal').value, keterangan: $('txKet').value
    };
    const res = await callApi('addTransaction', { payload });
    if (res && res.success) { toast(res.message || 'Transaksi disimpan'); $('txJumlah').value = ''; $('txKet').value = ''; load(); }
    else if (res) toast(res.message || 'Gagal menyimpan', 'bad');
});

$('btnUser').onclick = () => busy($('btnUser'), async () => {
    const nama = $('usrNama').value.trim(), targetSaldo = $('usrTarget').value;
    if (!nama) return toast('Nama wajib diisi.', 'bad');
    const res = await callApi('addUser', { payload: { nama, targetSaldo } });
    if (res && res.success) { toast(res.message || 'Anggota ditambahkan'); $('usrNama').value = ''; load(); }
    else if (res) toast(res.message || 'Gagal menambah anggota', 'bad');
});

$('admMembers').addEventListener('click', async e => {
    const b = e.target.closest('[data-del]'); if (!b) return;
    if (!await confirmBox(`Hapus anggota "${b.dataset.name}"?`)) return;
    const res = await callApi('deleteUser', { userId: b.dataset.del });
    if (res && res.success) { toast(res.message || 'Anggota dihapus'); load(); }
    else if (res) toast(res.message || 'Gagal menghapus', 'bad');
});

$('btnSettings').onclick = () => busy($('btnSettings'), async () => {
    const payload = { kasTitle: $('cfgTitle').value, paymentInfo: $('cfgPayment').value, newPassword: $('cfgPass').value };
    const res = await callApi('updateSettings', { payload });
    if (res && res.success) { toast(res.message || 'Pengaturan disimpan'); $('cfgPass').value = ''; load(); }
    else if (res) toast(res.message || 'Gagal menyimpan', 'bad');
});

$('chips').addEventListener('click', e => {
    const b = e.target.closest('.chip'); if (!b || !DATA) return;
    mFilter = b.dataset.f;
    document.querySelectorAll('#chips .chip').forEach(x => x.classList.toggle('on', x === b));
    renderMembers(true);
});
$('quick').addEventListener('click', e => {
    const b = e.target.closest('.chip'); if (!b) return;
    if (b.dataset.amt) $('txJumlah').value = b.dataset.amt;
    else { const u = curUser(); if (u && u.totalTerkumpul < u.targetSaldo) $('txJumlah').value = u.targetSaldo - u.totalTerkumpul; else return toast('Tidak ada sisa tagihan.', 'bad'); }
    updateHints();
});
['txTipe', 'txUserId'].forEach(id => $(id).addEventListener('change', updateHints));
$('txJumlah').addEventListener('input', updateHints);
$('btnRefresh').onclick = () => busy($('btnRefresh'), async () => { await load(); toast('Data diperbarui'); });
document.addEventListener('keydown', e => { if (e.key === 'Escape' && !$('confirmBox').classList.contains('hidden')) $('confirmNo').click(); });

/* ---------- Init ---------- */
$('txTanggal').valueAsDate = new Date();
route(); load();
