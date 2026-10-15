html_content = '''<!DOCTYPE html>
<html lang="my">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
  <title>Sky Mother POS Pro</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
  <style>
    body { background: #0b0f19; color: #f8fafc; font-family: system-ui, sans-serif; -webkit-user-select: none; }
    .pos-card { background: #131b2e; border: 1px solid #1e293b; border-radius: 10px; }
    .item-card { background: #1a243b; border: 1px solid #2d3b55; border-radius: 8px; cursor: pointer; transition: 0.1s; }
    .item-card:active { transform: scale(0.96); border-color: #38bdf8; }
    .cat-scroll { display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; }
    .cat-btn { white-space: nowrap; border-radius: 20px; padding: 4px 12px; font-size: 13px; border: 1px solid #334155; background: #1e293b; color: #cbd5e1; }
    .cat-btn.active { background: #0284c7; color: white; border-color: #38bdf8; font-weight: bold; }
    .receipt-box { background: #fff; color: #000; font-family: monospace; padding: 15px; border-radius: 6px; font-size: 13px; }
    .dashed-line { border-top: 1px dashed #555; margin: 8px 0; }
  </style>
</head>
<body class="p-2">
  <!-- Top Bar -->
  <nav class="pos-card p-2 mb-2 d-flex justify-content-between align-items-center">
    <div class="d-flex align-items-center gap-2">
      <h6 class="fw-bold mb-0 text-info"><i class="fas fa-store"></i> Sky Mother POS <span class="badge bg-primary">Pro</span></h6>
      <span class="badge bg-dark border border-secondary" onclick="promptStaff()" style="cursor:pointer;"><i class="fas fa-user text-info"></i> <span id="lblStaff">Owner</span></span>
    </div>
    <div class="d-flex gap-1">
      <button class="btn btn-sm btn-outline-info py-1" onclick="printModal.show()"><i class="fas fa-print"></i> Printer</button>
      <a href="/api/export-csv" class="btn btn-sm btn-outline-warning py-1"><i class="fas fa-file-excel"></i> စာရင်း</a>
    </div>
  </nav>

  <!-- Floor & Table Filter -->
  <div class="pos-card p-2 mb-2 d-flex justify-content-between align-items-center flex-wrap gap-2">
    <div class="cat-scroll" id="floorBtns">
      <button class="cat-btn active" onclick="setFloor('all', this)">အားလုံး</button>
      <button class="cat-btn" onclick="setFloor('flr1', this)">၁ ထပ် (ဆိုင်)</button>
      <button class="cat-btn" onclick="setFloor('ktv', this)">KTV</button>
      <button class="cat-btn" onclick="setFloor('flr2', this)">၂ ထပ်</button>
      <button class="cat-btn" onclick="setFloor('flr3', this)">၃ ထပ်</button>
    </div>
    <div class="d-flex align-items-center gap-1">
      <span class="small text-secondary">ဝိုင်း:</span>
      <select id="selTable" class="form-select form-select-sm bg-dark text-white border-secondary" style="width:130px;" onchange="onTableSelect()"></select>
    </div>
  </div>

  <div class="row g-2">
    <!-- Menu Grid -->
    <div class="col-7">
      <div class="pos-card p-2">
        <input type="text" id="txtSearch" class="form-control form-control-sm bg-dark text-white border-secondary mb-2" placeholder="ရှာရန်..." oninput="renderItems()">
        <div class="cat-scroll mb-2" id="boxCats"></div>
        <div class="row g-2" id="gridItems" style="max-height: 58vh; overflow-y: auto;"></div>
      </div>
    </div>

    <!-- Active Ticket -->
    <div class="col-5">
      <div class="pos-card p-3">
        <div class="d-flex justify-content-between align-items-center border-bottom border-secondary pb-2 mb-2">
          <h6 class="mb-0 fw-bold text-info"><span id="lblTable">ဝိုင်း</span></h6>
          <div>
            <button class="btn btn-sm btn-outline-warning py-0 px-2" onclick="printKOT()"><i class="fas fa-utensils"></i> KOT</button>
            <button class="btn btn-sm btn-outline-danger py-0 px-2" onclick="clearCart()"><i class="fas fa-trash"></i></button>
          </div>
        </div>
        <div id="cartBox" style="max-height: 40vh; overflow-y: auto;">
          <p class="text-secondary text-center small my-4">အော်ဒါမရှိပါ</p>
        </div>
        <div class="border-top border-secondary pt-2 mt-2">
          <div class="d-flex justify-content-between mb-2">
            <span>ကျသင့်ငွေ:</span>
            <span class="fs-5 fw-bold text-warning" id="lblTotal">0 Ks</span>
          </div>
          <div class="d-grid gap-1 mb-2">
            <button class="btn btn-sm btn-outline-warning fw-bold" onclick="showPreview()"><i class="fas fa-eye"></i> ဘေလ်စစ်မည် (Preview)</button>
          </div>
          <div class="d-flex gap-2">
            <button class="btn btn-primary w-50 py-2 fw-bold" onclick="saveOrder()"><i class="fas fa-save"></i> အော်ဒါသိမ်း</button>
            <button class="btn btn-success w-50 py-2 fw-bold" onclick="checkoutModal.show(); calcBill();"><i class="fas fa-calculator"></i> ဘေလ်ရှင်း</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Printer Setting Modal (Direct Web Bluetooth / WebUSB / RawBT) -->
  <div class="modal fade" id="printModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content bg-dark text-white border-secondary">
        <div class="modal-header border-secondary p-2">
          <h6 class="modal-title text-info fw-bold"><i class="fas fa-print"></i> Thermal Printer ချိတ်ဆက်မှု</h6>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body small">
          <div class="d-grid gap-2 mb-3">
            <button class="btn btn-outline-info py-2 fw-bold" onclick="connectBT()">
              <i class="fab fa-bluetooth text-primary fs-5 me-2"></i> Bluetooth ဖြင့် တိုက်ရိုက်ချိတ်မည် (Printer001)
            </button>
            <button class="btn btn-outline-success py-2 fw-bold" onclick="connectUSB()">
              <i class="fas fa-usb text-success fs-5 me-2"></i> USB OTG ကြိုးဖြင့် တိုက်ရိုက်ချိတ်မည်
            </button>
          </div>
          <div class="p-2 mb-2 bg-secondary bg-opacity-25 rounded border border-secondary">
            <label class="text-secondary mb-1">ပုံနှိပ်မည့် ပုံစံ:</label>
            <select id="selPrintMode" class="form-select form-select-sm bg-black text-white border-secondary" onchange="setPrintMode(this.value)">
              <option value="rawbt" selected>RawBT App (အငြိမ်းချမ်းဆုံး ချိတ်ဆက်မှု)</option>
              <option value="direct_bt">Web Bluetooth (တိုက်ရိုက် - App မလို)</option>
              <option value="direct_usb">Web USB (OTG ကြိုးဖြင့် တိုက်ရိုက်)</option>
            </select>
          </div>
          <button class="btn btn-warning w-100 fw-bold" onclick="testPrint()"><i class="fas fa-bolt"></i> စမ်းသပ် Print ထုတ်မည်</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Screen Bill Preview Modal -->
  <div class="modal fade" id="previewModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content bg-transparent border-0">
        <div class="receipt-box shadow-lg">
          <div class="text-center">
            <h5 class="fw-bold mb-0">Sky Mother</h5>
            <small>Hotel &amp; Restaurant</small><br>
            <div class="badge bg-warning text-dark my-1">** PREVIEW ဘေလ်စစ်ရန် **</div><br>
            <small>Ph: 09-340339520</small>
          </div>
          <div class="dashed-line"></div>
          <div>ဝိုင်း: <strong id="pvTable"></strong> | တာဝန်ခံ: <span id="pvStaff"></span></div>
          <div class="dashed-line"></div>
          <div id="pvItems"></div>
          <div class="dashed-line"></div>
          <div class="d-flex justify-content-between fw-bold fs-6">
            <span>ကျသင့်ငွေ:</span>
            <span id="pvTotal">0 Ks</span>
          </div>
          <div class="mt-3 d-flex gap-2">
            <button class="btn btn-dark w-100 fw-bold" onclick="printSlip('preview')"><i class="fas fa-print"></i> စက္ကူ Print ထုတ်မည်</button>
            <button class="btn btn-secondary w-100" data-bs-dismiss="modal">ပိတ်မည်</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Checkout Modal -->
  <div class="modal fade" id="checkoutModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content bg-dark text-white border-secondary p-3">
        <h6 class="fw-bold text-success mb-2"><i class="fas fa-check-circle"></i> ဘေလ်ရှင်းခြင်း</h6>
        <div class="mb-2">ကျသင့်ငွေ: <span class="fs-5 fw-bold text-warning" id="chkTotal">0 Ks</span></div>
        <div class="row g-2 mb-2">
          <div class="col-6">
            <label class="small text-secondary">လျှော့ဈေး:</label>
            <input type="number" id="chkDiscount" class="form-control form-control-sm bg-black text-white border-secondary" value="0" oninput="calcBill()">
          </div>
          <div class="col-6">
            <label class="small text-secondary">ပေးချေငွေ:</label>
            <input type="number" id="chkPaid" class="form-control form-control-sm bg-black text-white border-secondary" oninput="calcBill()">
          </div>
        </div>
        <div class="mb-2">အကြွေးကျန်: <span class="fs-5 fw-bold text-danger" id="chkDue">0 Ks</span></div>
        <div class="mb-3">
          <label class="small text-secondary">ဧည့်သည်အမည် (ရွေးချယ်ရန်):</label>
          <input type="text" id="chkCust" class="form-control form-control-sm bg-black text-white border-secondary" placeholder="ဧည့်သည်အမည်">
        </div>
        <div class="d-flex gap-2">
          <button class="btn btn-success w-100 fw-bold py-2" onclick="confirmCheckout()"><i class="fas fa-print"></i> ဘေလ်ပိတ်ပြီး Print ထုတ်မည်</button>
          <button class="btn btn-secondary w-100" data-bs-dismiss="modal">မလုပ်တော့ပါ</button>
        </div>
      </div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  <script>
    const floors = {
      'flr1': ['A1', 'A2', 'Table 1', 'Table 2', 'Table 3', 'Table 4', 'Table 5', 'Table 6', 'Table 7', 'Table 8', 'Table 9', 'V1', 'V2'],
      'ktv': ['K2', 'K3'],
      'flr2': ['101', '102', '103', '104', '105', '106', '107', '108', '109', '110'],
      'flr3': ['201', '202', '203', '204', '205', '206', '207', '208', '209', '210']
    };
    let menu = [], cart = [], activeOrders = {}, activeFloor = 'all', curCat = 'All';
    let staff = localStorage.getItem('sm_staff') || 'Owner';
    let printMode = localStorage.getItem('sm_print_mode') || 'rawbt';
    let btDevice, btChar, usbDevice, usbEndpoint;

    const printModal = new bootstrap.Modal(document.getElementById('printModal'));
    const previewModal = new bootstrap.Modal(document.getElementById('previewModal'));
    const checkoutModal = new bootstrap.Modal(document.getElementById('checkoutModal'));

    function promptStaff() {
      const s = prompt("ဝန်ထမ်းအမည် ထည့်ပါ:", staff);
      if (s) { staff = s.trim(); localStorage.setItem('sm_staff', staff); document.getElementById('lblStaff').textContent = staff; }
    }

    async function init() {
      document.getElementById('lblStaff').textContent = staff;
      document.getElementById('selPrintMode').value = printMode;
      try {
        const res = await fetch('data.json');
        const db = await res.json();
        menu = db.items || [];
        renderCats(db.categories || ['All']);
        renderItems();
      } catch(e) {}
      await refreshOrders();
      buildTables();
      onTableSelect();
    }

    function renderCats(cats) {
      const b = document.getElementById('boxCats');
      b.innerHTML = '';
      cats.forEach((c, i) => {
        b.innerHTML += `<button class="cat-btn ${i===0?'active':''}" onclick="setCat('${c}', this)">${c}</button>`;
      });
    }

    function setCat(c, el) {
      curCat = c;
      document.querySelectorAll('#boxCats .cat-btn').forEach(b => b.classList.remove('active'));
      el.classList.add('active');
      renderItems();
    }

    function renderItems() {
      const q = document.getElementById('txtSearch').value.toLowerCase().trim();
      let list = (curCat === 'All') ? menu : menu.filter(m => m.category === curCat);
      if (q) list = list.filter(m => m.name.toLowerCase().includes(q));
      const g = document.getElementById('gridItems');
      g.innerHTML = '';
      list.forEach(it => {
        g.innerHTML += `
          <div class="col-6 col-sm-4">
            <div class="item-card p-2 text-center" onclick="addItem(${it.id})">
              ${it.image ? `<img src="${it.image}" style="width:100%;height:65px;object-fit:cover;border-radius:4px;" class="mb-1">` : ''}
              <div class="small fw-bold text-truncate">${it.name}</div>
              <span class="badge bg-primary" style="font-size:11px;">${it.price.toLocaleString()} Ks</span>
            </div>
          </div>`;
      });
    }

    function buildTables() {
      const sel = document.getElementById('selTable');
      const prev = sel.value;
      sel.innerHTML = '';
      let list = (activeFloor === 'all') ? [...floors.flr1, ...floors.ktv, ...floors.flr2, ...floors.flr3] : (floors[activeFloor] || []);
      list.forEach(t => {
        const has = activeOrders[t] && activeOrders[t].items && activeOrders[t].items.length > 0;
        sel.innerHTML += `<option value="${t}">${has ? '🔴' : '🟢'} ${t}</option>`;
      });
      if (prev && list.includes(prev)) sel.value = prev;
    }

    function setFloor(f, el) {
      activeFloor = f;
      document.querySelectorAll('#floorBtns .cat-btn').forEach(b => b.classList.remove('active'));
      el.classList.add('active');
      buildTables();
      onTableSelect();
    }

    function onTableSelect() {
      const t = document.getElementById('selTable').value;
      document.getElementById('lblTable').textContent = t || '-';
      if (t && activeOrders[t] && activeOrders[t].items) {
        cart = JSON.parse(JSON.stringify(activeOrders[t].items));
      } else {
        cart = [];
      }
      renderCart();
    }

    function addItem(id) {
      const it = menu.find(m => m.id === id);
      if (!it) return;
      const ex = cart.find(c => c.id === id);
      if (ex) ex.qty += 1;
      else cart.push({ id: it.id, name: it.name, price: it.price, qty: 1 });
      renderCart();
    }

    function renderCart() {
      const box = document.getElementById('cartBox');
      if (cart.length === 0) {
        box.innerHTML = '<p class="text-secondary text-center small my-4">အော်ဒါမရှိပါ</p>';
        document.getElementById('lblTotal').textContent = '0 Ks';
        return;
      }
      box.innerHTML = '';
      let total = 0;
      cart.forEach((it, i) => {
        const sub = it.price * it.qty;
        total += sub;
        box.innerHTML += `
          <div class="d-flex justify-content-between align-items-center mb-1 pb-1 border-bottom border-dark small">
            <div><strong>${it.name}</strong><br><span class="text-secondary">${it.price.toLocaleString()} x ${it.qty}</span></div>
            <div class="d-flex align-items-center gap-1">
              <span class="text-warning me-1">${sub.toLocaleString()} Ks</span>
              <button class="btn btn-sm btn-secondary py-0 px-1" onclick="cart[${i}].qty--; if(!cart[${i}].qty) cart.splice(${i},1); renderCart();">-</button>
              <button class="btn btn-sm btn-secondary py-0 px-1" onclick="cart[${i}].qty++; renderCart();">+</button>
            </div>
          </div>`;
      });
      document.getElementById('lblTotal').textContent = total.toLocaleString() + ' Ks';
    }

    function clearCart() {
      const t = document.getElementById('selTable').value;
      if (!confirm(`[${t}] အော်ဒါများကို ရှင်းမည်လား?`)) return;
      cart = [];
      if (activeOrders[t]) delete activeOrders[t];
      renderCart();
      buildTables();
    }

    async function saveOrder() {
      const t = document.getElementById('selTable').value;
      if (cart.length === 0) return alert("အော်ဒါမရှိပါ");
      activeOrders[t] = { table: t, waiter: staff, items: cart };
      try {
        await fetch('/api/active', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ table_name: t, waiter_name: staff, items: cart })
        });
      } catch(e) {}
      alert(`[${t}] တွင် အော်ဒါသိမ်းပြီးပါပြီ`);
      buildTables();
    }

    async function refreshOrders() {
      try {
        const res = await fetch('/api/active');
        activeOrders = await res.json();
      } catch(e) {}
    }

    // Direct Web Bluetooth
    async function connectBT() {
      try {
        btDevice = await navigator.bluetooth.requestDevice({
          acceptAllDevices: true,
          optionalServices: ['000018f0-0000-1000-8000-00805f9b34fb', '49535343-fe7d-4ae5-8fa9-9fafd205e455']
        });
        const server = await btDevice.gatt.connect();
        const svcs = await server.getPrimaryServices();
        for (let s of svcs) {
          const chars = await s.getCharacteristics();
          for (let c of chars) {
            if (c.properties.write || c.properties.writeWithoutResponse) { btChar = c; break; }
          }
        }
        alert("Bluetooth Printer ချိတ်ဆက်ပြီးပါပြီ");
      } catch(e) { alert("Bluetooth ချိတ်၍မရပါ: " + e.message); }
    }

    // Direct Web USB
    async function connectUSB() {
      try {
        usbDevice = await navigator.usb.requestDevice({ filters: [] });
        await usbDevice.open();
        await usbDevice.selectConfiguration(1);
        await usbDevice.claimInterface(0);
        usbEndpoint = usbDevice.configuration.interfaces[0].alternate.endpoints.find(e => e.direction === 'out');
        alert("USB Printer ချိတ်ဆက်ပြီးပါပြီ");
      } catch(e) { alert("USB ချိတ်၍မရပါ: " + e.message); }
    }

    function setPrintMode(m) {
      printMode = m;
      localStorage.setItem('sm_print_mode', m);
    }

    async function sendPrint(text) {
      if (printMode === 'direct_bt' && btChar) {
        await btChar.writeValue(new TextEncoder().encode(text));
      } else if (printMode === 'direct_usb' && usbDevice && usbEndpoint) {
        await usbDevice.transferOut(usbEndpoint.endpointNumber, new TextEncoder().encode(text));
      } else {
        window.location.href = "rawbt:data:text/plain;charset=utf-8;base64," + btoa(unescape(encodeURIComponent(text)));
      }
    }

    function makeSlipText(type, d) {
      let t = `Sky Mother\nHotel & Restaurant\nPh: 09-340339520\n--------------------------------\n`;
      if (type === 'preview') t += `** PREVIEW ဘေလ်စစ်ရန် **\n`;
      else if (type === 'kot') t += `** KITCHEN ORDER (မီးဖိုချောင်) **\n`;
      else t += `Order ID: ${d.id}\n`;
      t += `ဝိုင်း: ${d.table} | တာဝန်ခံ: ${d.staff}\n--------------------------------\n`;
      d.items.forEach(it => { t += `${it.name} x${it.qty}  ${(it.price*it.qty).toLocaleString()} Ks\n`; });
      t += `--------------------------------\n`;
      if (type !== 'kot') {
        t += `ကျသင့်ငွေ: ${d.total.toLocaleString()} Ks\n`;
        if (d.due > 0) t += `အကြွေးကျန်: ${d.due.toLocaleString()} Ks\n`;
      }
      t += `Have a wonderful day! Thank You\n\n\n`;
      return t;
    }

    function showPreview() {
      const t = document.getElementById('selTable').value;
      if (cart.length === 0) return alert("အော်ဒါမရှိပါ");
      document.getElementById('pvTable').textContent = t;
      document.getElementById('pvStaff').textContent = staff;
      let total = 0;
      const b = document.getElementById('pvItems');
      b.innerHTML = '';
      cart.forEach(it => {
        total += it.price * it.qty;
        b.innerHTML += `<div class="d-flex justify-content-between"><span>${it.name} x ${it.qty}</span><span>${(it.price*it.qty).toLocaleString()} Ks</span></div>`;
      });
      document.getElementById('pvTotal').textContent = total.toLocaleString() + ' Ks';
      previewModal.show();
    }

    function printSlip(type) {
      const t = document.getElementById('selTable').value;
      let total = 0; cart.forEach(it => total += it.price * it.qty);
      const txt = makeSlipText(type, { id: 'SM-'+Date.now().toString().slice(-4), table: t, staff: staff, items: cart, total: total, due: 0 });
      sendPrint(txt);
      previewModal.hide();
    }

    function printKOT() {
      const t = document.getElementById('selTable').value;
      if (cart.length === 0) return alert("မီးဖိုချောင်သို့ ပို့ရန် အော်ဒါမရှိပါ");
      const txt = makeSlipText('kot', { table: t, staff: staff, items: cart });
      sendPrint(txt);
    }

    function testPrint() {
      sendPrint(`Sky Mother POS\nTest Print အောင်မြင်ပါသည်!\nPrinter001 Ready\n\n\n`);
    }

    function calcBill() {
      let total = 0; cart.forEach(it => total += it.price * it.qty);
      const disc = parseInt(document.getElementById('chkDiscount').value) || 0;
      const net = Math.max(0, total - disc);
      document.getElementById('chkTotal').textContent = total.toLocaleString() + ' Ks';
      let paid = parseInt(document.getElementById('chkPaid').value);
      if (isNaN(paid)) { paid = net; document.getElementById('chkPaid').value = net; }
      const due = Math.max(0, net - paid);
      document.getElementById('chkDue').textContent = due.toLocaleString() + ' Ks';
    }

    async function confirmCheckout() {
      const t = document.getElementById('selTable').value;
      let total = 0; cart.forEach(it => total += it.price * it.qty);
      const disc = parseInt(document.getElementById('chkDiscount').value) || 0;
      const net = Math.max(0, total - disc);
      const paid = parseInt(document.getElementById('chkPaid').value) || net;
      const due = Math.max(0, net - paid);
      const cust = document.getElementById('chkCust').value.trim();

      const txt = makeSlipText('final', { id: 'SM-'+Date.now().toString().slice(-4), table: t, staff: staff, items: cart, total: net, due: due });
      sendPrint(txt);

      try {
        await fetch('/api/checkout', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ table_name: t, customer_name: cust, discount: disc, paid_amount: paid, waiter_name: staff })
        });
      } catch(e) {}

      checkoutModal.hide();
      cart = [];
      delete activeOrders[t];
      renderCart();
      buildTables();
      alert(`[${t}] ဘေလ်ရှင်းပြီးပါပြီ`);
    }

    init();
  </script>
</body>
</html>
'''

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("SUCCESS: Sky Mother POS Pro UI successfully generated!")
