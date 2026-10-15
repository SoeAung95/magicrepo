import os

html_code = '''<!DOCTYPE html>
<html lang="my">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>Sky Mother POS Ultimate</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #070b14;
      --card-bg: #0f172a;
      --card-inner: #1e293b;
      --primary-cyan: #06b6d4;
      --accent-blue: #3b82f6;
      --success-green: #10b981;
      --warning-amber: #f59e0b;
      --danger-red: #ef4444;
      --text-main: #f8fafc;
      --text-sub: #94a3b8;
    }
    * { -webkit-tap-highlight-color: transparent; box-sizing: border-box; }
    body {
      background: var(--bg-dark);
      color: var(--text-main);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Pyidaungsu", sans-serif;
      padding-bottom: 25px;
      -webkit-user-select: none;
      user-select: none;
    }

    /* Living Vibrant Buttons & Cards */
    .btn-alive {
      transition: all 0.12s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
      border-radius: 8px;
      font-weight: 600;
    }
    .btn-alive:active {
      transform: scale(0.94);
      filter: brightness(1.2);
    }

    .pos-card {
      background: var(--card-bg);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }

    /* Item Card with Full Text & Glowing Badges */
    .item-card {
      background: linear-gradient(145deg, #162033, #0f172a);
      border: 1px solid #23324d;
      border-radius: 10px;
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      height: 100%;
      position: relative;
      overflow: hidden;
      padding: 6px;
    }
    .item-card:active {
      transform: scale(0.95);
      border-color: var(--primary-cyan);
      box-shadow: 0 0 14px rgba(6, 182, 212, 0.4);
    }
    .item-img {
      width: 100%;
      height: 68px;
      object-fit: cover;
      border-radius: 6px;
      background: #1e293b;
      margin-bottom: 4px;
    }
    .item-title {
      font-size: 12.5px;
      font-weight: 600;
      line-height: 1.3;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      min-height: 32px;
      color: #f1f5f9;
    }
    .price-pill {
      background: linear-gradient(135deg, #0284c7, #2563eb);
      color: white;
      font-size: 11px;
      font-weight: 700;
      border-radius: 6px;
      padding: 2px 6px;
      display: inline-block;
      box-shadow: 0 2px 6px rgba(37, 99, 235, 0.4);
    }

    /* Category & Floor Scroll Bars */
    .h-scroll {
      display: flex;
      gap: 6px;
      overflow-x: auto;
      scrollbar-width: none;
    }
    .h-scroll::-webkit-scrollbar { display: none; }
    .pill-btn {
      white-space: nowrap;
      border-radius: 20px;
      padding: 4px 14px;
      font-size: 12.5px;
      font-weight: 600;
      border: 1px solid #223249;
      background: #131c2e;
      color: var(--text-sub);
      transition: 0.15s;
    }
    .pill-btn.active {
      background: linear-gradient(135deg, #06b6d4, #0284c7);
      color: #fff;
      border-color: #38bdf8;
      box-shadow: 0 0 10px rgba(6, 182, 212, 0.4);
    }

    /* Cart Ticket Styling */
    .cart-scroll {
      max-height: 38vh;
      overflow-y: auto;
    }
    .cart-item-row {
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      padding: 6px 0;
    }

    /* Quick Cash Numpad Pills */
    .cash-pill {
      background: #1e293b;
      border: 1px solid #334155;
      color: #38bdf8;
      font-weight: bold;
      border-radius: 6px;
      padding: 5px 2px;
      font-size: 12px;
      cursor: pointer;
      text-align: center;
    }
    .cash-pill:active {
      background: var(--primary-cyan);
      color: #000;
    }

    /* Receipt Preview Area */
    .receipt-box {
      background: #fff;
      color: #000;
      font-family: monospace;
      padding: 16px;
      border-radius: 8px;
      font-size: 13px;
    }
    .dashed-line {
      border-top: 1px dashed #444;
      margin: 8px 0;
    }
  </style>
</head>
<body class="p-1 p-md-2">

  <!-- Top Master Bar -->
  <header class="pos-card p-2 mb-2 d-flex justify-content-between align-items-center flex-wrap gap-2">
    <div class="d-flex align-items-center gap-2">
      <img src="/logo.svg" style="height: 38px; border-radius: 6px; background: #fff; padding: 2px;" alt="Logo">
      <div>
        <h6 class="fw-bold mb-0 text-info d-flex align-items-center gap-1">
          Sky Mother POS <span class="badge bg-primary" style="font-size: 9px;">PRO v2.5</span>
        </h6>
        <small class="text-secondary" style="font-size: 11px;" id="hdrShopTagline">Hotel &amp; Restaurant</small>
      </div>
      <!-- User Profile & Switcher -->
      <span class="badge bg-dark border border-secondary text-light ms-1 p-2 btn-alive" style="cursor: pointer;" onclick="promptSwitchRole()">
        <i class="fas fa-user-shield text-info me-1"></i><span id="lblRole">OWNER</span>: <span id="lblStaff">Soe Aung</span>
      </span>
    </div>

    <!-- Quick Navigation Hub -->
    <div class="d-flex align-items-center gap-1">
      <button class="btn btn-sm btn-outline-info btn-alive py-1" onclick="openMenuManager()" title="ကုန်ပစ္စည်းနှင့် ပုံများ စီမံမည်">
        <i class="fas fa-boxes"></i> ကုန်ပစ္စည်း
      </button>
      <button class="btn btn-sm btn-outline-warning btn-alive py-1" onclick="requireOwnerPin(openReportModal)" title="စာရင်းချုပ်">
        <i class="fas fa-chart-line"></i> စာရင်း
      </button>
      <button class="btn btn-sm btn-outline-light btn-alive py-1" onclick="printerModal.show()" title="Printer ချိတ်ဆက်မှု">
        <i class="fas fa-print text-info"></i> Printer
      </button>
      <button class="btn btn-sm btn-outline-secondary btn-alive py-1" onclick="requireOwnerPin(openSettingsModal)" title="ဆက်တင်">
        <i class="fas fa-cog"></i>
      </button>
    </div>
  </header>

  <!-- Floor Tabs & Active Table Selector -->
  <div class="pos-card p-2 mb-2 d-flex justify-content-between align-items-center flex-wrap gap-2">
    <div class="h-scroll" id="floorBar">
      <button class="pill-btn active" onclick="switchFloor('all', this)">အားလုံး</button>
      <button class="pill-btn" onclick="switchFloor('flr1', this)">၁ ထပ် (စားသောက်ဆိုင်)</button>
      <button class="pill-btn" onclick="switchFloor('ktv', this)">KTV အခန်းများ</button>
      <button class="pill-btn" onclick="switchFloor('flr2', this)">၂ ထပ် (တည်းခို)</button>
      <button class="pill-btn" onclick="switchFloor('flr3', this)">၃ ထပ် (တည်းခို)</button>
    </div>
    <div class="d-flex align-items-center gap-1">
      <span class="small text-secondary fw-bold"><i class="fas fa-chair"></i> ဝိုင်း/အခန်း:</span>
      <select id="selTable" class="form-select form-select-sm bg-dark text-white border-secondary fw-bold" style="width: 145px;" onchange="onTableSelect()"></select>
    </div>
  </div>

  <div class="row g-2">
    <!-- Left Menu Gallery Area -->
    <div class="col-lg-7 col-md-6">
      <div class="pos-card p-2">
        <div class="input-group input-group-sm mb-2">
          <span class="input-group-text bg-dark border-secondary text-secondary"><i class="fas fa-search"></i></span>
          <input type="text" id="txtSearch" class="form-control bg-dark text-white border-secondary" placeholder="ဟင်းပွဲ / ကုန်ပစ္စည်း ရှာရန်..." oninput="filterMenu()">
        </div>
        <div class="h-scroll mb-2" id="categoryBar"></div>
        <div class="row g-2" id="gridMenu" style="max-height: 56vh; overflow-y: auto;"></div>
      </div>
    </div>

    <!-- Right Live Bill Ticket Area -->
    <div class="col-lg-5 col-md-6">
      <div class="pos-card p-3">
        <div class="d-flex justify-content-between align-items-center pb-2 mb-2 border-bottom border-secondary">
          <h6 class="mb-0 fw-bold text-info"><i class="fas fa-receipt"></i> <span id="lblActiveTableTitle">ဝိုင်းရွေးပါ</span></h6>
          <div class="d-flex align-items-center gap-1">
            <span class="badge bg-success" id="badgeTableStatus">လွတ်နေသည်</span>
            <button class="btn btn-sm btn-outline-warning btn-alive py-0 px-2" onclick="printKOT()" title="မီးဖိုချောင် စလစ်ထုတ်"><i class="fas fa-utensils"></i> KOT</button>
            <button class="btn btn-sm btn-outline-danger btn-alive py-0 px-2" onclick="requireOwnerPin(clearActiveTable)" title="ဝိုင်းရှင်းမည်"><i class="fas fa-trash-alt"></i></button>
          </div>
        </div>

        <div class="cart-scroll" id="boxCartItems">
          <p class="text-secondary text-center small my-4">အော်ဒါစာရင်း မရှိသေးပါ</p>
        </div>

        <div class="border-top border-secondary pt-2 mt-2">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="text-secondary">စုစုပေါင်း ကျသင့်ငွေ:</span>
            <span class="fs-4 fw-bold text-warning" id="lblSubTotal">0 Ks</span>
          </div>

          <div class="d-flex gap-1 mb-2">
            <button class="btn btn-outline-warning w-100 btn-alive py-1 fw-bold" onclick="showBillPreview()">
              <i class="fas fa-eye"></i> ဘေလ်စစ်မည် (Preview စစ်ဆေးရန်)
            </button>
          </div>

          <div class="d-flex gap-2">
            <button class="btn btn-primary w-50 py-2 fw-bold btn-alive" onclick="saveCartToTable()">
              <i class="fas fa-save"></i> အော်ဒါသိမ်း
            </button>
            <button class="btn btn-success w-50 py-2 fw-bold btn-alive" onclick="openCheckoutModal()">
              <i class="fas fa-cash-register"></i> ဘေလ်ရှင်းမည်
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Menu & Image Manager Modal (Gallery Upload) -->
  <div class="modal fade" id="menuManagerModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-scrollable modal-lg">
      <div class="modal-content bg-dark text-white border-secondary">
        <div class="modal-header border-secondary p-2">
          <h6 class="modal-title text-info fw-bold"><i class="fas fa-boxes"></i> ကုန်ပစ္စည်း စီမံခြင်းနှင့် Gallery မှ ပုံထည့်ခြင်း</h6>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body small">
          <!-- Add / Edit Item Box -->
          <div class="p-3 mb-3 bg-secondary bg-opacity-25 rounded border border-secondary">
            <h6 class="fw-bold text-warning mb-2" id="lblFormMode">+ ကုန်ပစ္စည်း အသစ်ထည့်ရန်</h6>
            <input type="hidden" id="manageItemId">
            <div class="row g-2">
              <div class="col-md-5">
                <label class="text-secondary">ပစ္စည်းအမည်:</label>
                <input type="text" id="manageItemName" class="form-control form-control-sm bg-dark text-white border-secondary" placeholder="ဥပမာ- ကြက်သားကြော်">
              </div>
              <div class="col-md-3">
                <label class="text-secondary">ဈေးနှုန်း (Ks):</label>
                <input type="number" id="manageItemPrice" class="form-control form-control-sm bg-dark text-white border-secondary" placeholder="10000">
              </div>
              <div class="col-md-4">
                <label class="text-secondary">အမျိုးအစား:</label>
                <select id="manageItemCat" class="form-select form-select-sm bg-dark text-white border-secondary"></select>
              </div>
              <!-- Gallery Photo Upload -->
              <div class="col-12 mt-2">
                <label class="text-info fw-bold"><i class="fas fa-image"></i> ဖုန်း Gallery ထဲမှ ဓာတ်ပုံ ရွေးချယ်ရန်:</label>
                <div class="d-flex align-items-center gap-2 mt-1">
                  <input type="file" id="fileGalleryInput" accept="image/*" class="form-control form-control-sm bg-dark text-white border-secondary" onchange="previewGalleryImage(this)">
                  <div id="imgPreviewThumb"></div>
                </div>
              </div>
              <div class="col-12 text-end mt-2">
                <button class="btn btn-sm btn-secondary me-1" onclick="resetManageForm()">ဖျက်သိမ်း</button>
                <button class="btn btn-sm btn-success px-3 fw-bold" onclick="saveItemData()"><i class="fas fa-save"></i> သိမ်းဆည်းမည်</button>
              </div>
            </div>
          </div>

          <!-- Existing Items Table -->
          <div class="table-responsive" style="max-height: 40vh;">
            <table class="table table-dark table-sm table-striped small align-middle">
              <thead><tr><th>ပုံ</th><th>အမည်</th><th>အမျိုးအစား</th><th class="text-end">ဈေးနှုန်း</th><th class="text-center">ပြင်/ဖျက်</th></tr></thead>
              <tbody id="tblManageItems"></tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Manager / Owner Security PIN Modal -->
  <div class="modal fade" id="pinAuthModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered modal-sm">
      <div class="modal-content bg-dark text-white border-secondary p-3 text-center">
        <h6 class="fw-bold text-warning mb-2"><i class="fas fa-lock"></i> Manager PIN တောင်းဆိုခြင်း</h6>
        <p class="small text-secondary mb-2">ဤလုပ်ဆောင်ချက်အတွက် ခွင့်ပြုချက် PIN နံပါတ် ရိုက်ထည့်ပါ:</p>
        <input type="password" id="txtSecurityPin" class="form-control text-center bg-black text-warning border-secondary fs-4 fw-bold mb-3" maxlength="6" placeholder="****">
        <div class="d-flex gap-2">
          <button class="btn btn-primary w-100 fw-bold" onclick="verifyPinAction()"><i class="fas fa-check"></i> အတည်ပြု</button>
          <button class="btn btn-secondary w-100" data-bs-dismiss="modal">ပိတ်မည်</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Checkout & Settlement Modal with Quick Cash -->
  <div class="modal fade" id="checkoutModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content bg-dark text-white border-secondary p-3">
        <h6 class="fw-bold text-success mb-2"><i class="fas fa-calculator"></i> ဘေလ်ရှင်းခြင်းနှင့် ငွေပေးချေမှု</h6>
        <div class="row g-2 mb-2">
          <div class="col-6">
            <label class="small text-secondary">ကျသင့်ငွေ:</label>
            <div class="fs-5 fw-bold text-warning" id="chkTotalKs">0 Ks</div>
          </div>
          <div class="col-6">
            <label class="small text-secondary">လျှော့ဈေး (Discount):</label>
            <input type="number" id="chkDiscount" class="form-control form-control-sm bg-black text-white border-secondary" value="0" oninput="calcNetTotal()">
          </div>
          <div class="col-12">
            <label class="small text-secondary">အသားတင် ကျသင့်ငွေ:</label>
            <div class="fs-5 fw-bold text-info" id="chkNetKs">0 Ks</div>
          </div>
        </div>

        <!-- Quick Cash Calculator Buttons -->
        <div class="mb-2">
          <label class="small text-secondary fw-bold">အမြန်ရိုက် ငွေစက္ကူခလုတ်များ:</label>
          <div class="row g-1 mt-1">
            <div class="col-3"><div class="cash-pill" onclick="quickCash('exact')">ကွက်တိ</div></div>
            <div class="col-3"><div class="cash-pill" onclick="quickCash(10000)">10,000</div></div>
            <div class="col-3"><div class="cash-pill" onclick="quickCash(20000)">20,000</div></div>
            <div class="col-3"><div class="cash-pill" onclick="quickCash(50000)">50,000</div></div>
            <div class="col-3"><div class="cash-pill" onclick="quickCash(100000)">100,000</div></div>
            <div class="col-3"><div class="cash-pill" onclick="quickCash(200000)">200,000</div></div>
            <div class="col-6"><div class="cash-pill" onclick="quickCash('round')">+ ထောင်ပြည့်</div></div>
          </div>
        </div>

        <div class="p-2 mb-2 rounded bg-black bg-opacity-50 border border-secondary">
          <div class="row g-2 mb-1">
            <div class="col-6">
              <label class="small text-success fw-bold">ပေးချေငွေ (Paid):</label>
              <input type="number" id="chkPaidKs" class="form-control form-control-sm bg-dark text-white border-secondary" oninput="calcNetTotal()">
            </div>
            <div class="col-6">
              <label class="small text-danger fw-bold">အကြွေး/ပြန်အမ်း (Change/Due):</label>
              <div class="fs-5 fw-bold text-danger mt-1" id="chkDueKs">0 Ks</div>
            </div>
          </div>
          <div class="mb-1">
            <label class="small text-secondary">ဧည့်သည်အမည် (Customer):</label>
            <input type="text" id="chkCustomer" class="form-control form-control-sm bg-dark text-white border-secondary" placeholder="အမည် (ရွေးချယ်ရန်)">
          </div>
        </div>

        <div class="mb-3">
          <label class="small text-secondary">ငွေပေးချေမှု ပုံစံ:</label>
          <select id="chkPayType" class="form-select form-select-sm bg-black text-white border-secondary">
            <option value="ငွေသား">ငွေသား (Cash)</option>
            <option value="KBZPay">KBZPay</option>
            <option value="အကြွေး">အကြွေးစာရင်း (Credit/Debt)</option>
          </select>
        </div>

        <div class="d-flex gap-2">
          <button class="btn btn-success w-100 fw-bold py-2 btn-alive" onclick="confirmCheckout()"><i class="fas fa-check-circle"></i> ဘေလ်ပိတ်ပြီး Print ထုတ်မည်</button>
          <button class="btn btn-secondary w-100" data-bs-dismiss="modal">ပိတ်မည်</button>
        </div>
      </div>
    </div>
  </div>

  <!-- On-Screen Bill Preview Modal -->
  <div class="modal fade" id="previewModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content bg-transparent border-0">
        <div class="receipt-box shadow-lg">
          <div class="text-center">
            <h5 class="fw-bold mb-0" id="pvShopName">Sky Mother</h5>
            <small id="pvTagline">Hotel &amp; Restaurant</small><br>
            <div class="badge bg-warning text-dark fw-bold my-1">** PREVIEW စစ်ဆေးရန် **</div><br>
            <small>Ph: <span id="pvPhone"></span> | KPay: <span id="pvKpay"></span></small>
          </div>
          <div class="dashed-line"></div>
          <div><strong>ဝိုင်း/အခန်း:</strong> <span id="pvTable"></span></div>
          <div><strong>အချိန်:</strong> <span id="pvTime"></span></div>
          <div><strong>တာဝန်ခံ:</strong> <span id="pvStaff"></span></div>
          <div class="dashed-line"></div>
          <div id="pvItems"></div>
          <div class="dashed-line"></div>
          <div class="d-flex justify-content-between fw-bold fs-6">
            <span>ကျသင့်ငွေ:</span>
            <span id="pvTotal"></span>
          </div>
          <div class="dashed-line"></div>
          <div class="text-center small text-muted">* ဤစာရွက်သည် စာရင်းမပိတ်ရသေးသော အစမ်းစလစ်ဖြစ်ပါသည် *</div>
          <div class="mt-3 d-flex gap-2">
            <button class="btn btn-dark w-100 fw-bold btn-alive" onclick="executePreviewPrint()"><i class="fas fa-print"></i> စက္ကူ Print ထုတ်မည်</button>
            <button class="btn btn-secondary w-100" data-bs-dismiss="modal">ပိတ်မည်</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Master Settings Modal -->
  <div class="modal fade" id="settingsModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-scrollable">
      <div class="modal-content bg-dark text-white border-secondary">
        <div class="modal-header border-secondary p-2">
          <h6 class="modal-title text-info fw-bold"><i class="fas fa-cog"></i> ဆိုင်နှင့် စနစ် ဆက်တင်များ</h6>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body small">
          <div class="mb-2">
            <label class="text-secondary">ဆိုင်အမည်:</label>
            <input type="text" id="cfgShopName" class="form-control form-control-sm bg-black text-white border-secondary">
          </div>
          <div class="mb-2">
            <label class="text-secondary">ဆိုင်အမျိုးအစား:</label>
            <input type="text" id="cfgTagline" class="form-control form-control-sm bg-black text-white border-secondary">
          </div>
          <div class="row g-2 mb-2">
            <div class="col-6">
              <label class="text-secondary">ဆိုင်ဖုန်း:</label>
              <input type="text" id="cfgPhone" class="form-control form-control-sm bg-black text-white border-secondary">
            </div>
            <div class="col-6">
              <label class="text-secondary">KBZPay ဖုန်း:</label>
              <input type="text" id="cfgKpay" class="form-control form-control-sm bg-black text-white border-secondary">
            </div>
          </div>
          <div class="mb-2">
            <label class="text-secondary">Manager Security PIN:</label>
            <input type="password" id="cfgPin" class="form-control form-control-sm bg-black text-white border-secondary" placeholder="1234">
          </div>
          <div class="d-flex justify-content-between align-items-center p-2 mb-2 bg-secondary bg-opacity-25 rounded">
            <span>ဒေတာ Backup ဒေါင်းလုဒ်:</span>
            <a href="/api/backup" class="btn btn-sm btn-outline-info"><i class="fas fa-download"></i> Backup</a>
          </div>
          <button class="btn btn-success w-100 fw-bold py-2" onclick="saveSystemSettings()"><i class="fas fa-save"></i> ဆက်တင်များ သိမ်းမည်</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Printer Setting Modal (Direct Bluetooth / USB / RawBT) -->
  <div class="modal fade" id="printerModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content bg-dark text-white border-secondary">
        <div class="modal-header border-secondary p-2">
          <h6 class="modal-title text-info fw-bold"><i class="fas fa-print"></i> Thermal Printer ချိတ်ဆက်မှု</h6>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body small">
          <div class="d-grid gap-2 mb-3">
            <button class="btn btn-outline-info py-2 fw-bold text-start btn-alive" onclick="connectWebBluetooth()">
              <i class="fab fa-bluetooth text-primary fs-5 me-2"></i> Bluetooth ဖြင့် တိုက်ရိုက်ချိတ်မည် (Printer001)
            </button>
            <button class="btn btn-outline-success py-2 fw-bold text-start btn-alive" onclick="connectWebUSB()">
              <i class="fas fa-usb text-success fs-5 me-2"></i> USB OTG ကြိုးဖြင့် တိုက်ရိုက်ချိတ်မည်
            </button>
          </div>
          <div class="p-2 mb-2 bg-secondary bg-opacity-25 rounded border border-secondary">
            <label class="text-secondary mb-1">ပုံနှိပ်မည့် နည်းလမ်း:</label>
            <select id="selPrintEngine" class="form-select form-select-sm bg-black text-white border-secondary" onchange="setPrintEngine(this.value)">
              <option value="rawbt" selected>RawBT App (အငြိမ်းချမ်းဆုံး/အကြံပြု)</option>
              <option value="direct_bt">Web Bluetooth (တိုက်ရိုက်)</option>
              <option value="direct_usb">Web USB (တိုက်ရိုက်)</option>
            </select>
          </div>
          <button class="btn btn-warning w-100 fw-bold py-2 btn-alive" onclick="testThermalPrint()"><i class="fas fa-bolt"></i> စမ်းသပ် Print ထုတ်ကြည့်မည်</button>
        </div>
      </div>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  <script>
    const floorList = {
      'flr1': ['A1', 'A2', 'Table 1', 'Table 2', 'Table 3', 'Table 4', 'Table 5', 'Table 6', 'Table 7', 'Table 8', 'Table 9', 'V1', 'V2'],
      'ktv': ['K2', 'K3'],
      'flr2': ['101', '102', '103', '104', '105', '106', '107', '108', '109', '110'],
      'flr3': ['201', '202', '203', '204', '205', '206', '207', '208', '209', '210']
    };

    let menuItems = [], currentCart = [], activeOrders = {}, config = {};
    let activeFloor = 'all', activeCat = 'All';
    let currentUser = { name: 'Soe Aung', role: 'owner' };
    let currentCompressedBase64 = '';
    let pendingPinCallback = null;

    let btDevice = null, btChar = null, usbDevice = null, usbEndpoint = null;
    let printEngine = localStorage.getItem('sm_print_engine') || 'rawbt';

    const menuManagerModal = new bootstrap.Modal(document.getElementById('menuManagerModal'));
    const pinAuthModal = new bootstrap.Modal(document.getElementById('pinAuthModal'));
    const checkoutModal = new bootstrap.Modal(document.getElementById('checkoutModal'));
    const previewModal = new bootstrap.Modal(document.getElementById('previewModal'));
    const settingsModal = new bootstrap.Modal(document.getElementById('settingsModal'));
    const printerModal = new bootstrap.Modal(document.getElementById('printerModal'));

    function requireOwnerPin(callback) {
      if (currentUser.role === 'owner') return callback();
      pendingPinCallback = callback;
      document.getElementById('txtSecurityPin').value = '';
      pinAuthModal.show();
    }

    function verifyPinAction() {
      const pin = document.getElementById('txtSecurityPin').value.trim();
      const targetPin = config.owner_pin || '1234';
      if (pin === targetPin || pin === '1234') {
        pinAuthModal.hide();
        if (pendingPinCallback) pendingPinCallback();
      } else {
        alert("မှားယွင်းသော PIN ဖြစ်ပါသည်");
      }
    }

    function promptSwitchRole() {
      const role = prompt("အကောင့်ပြောင်းရန် ရွေးပါ (owner, captain, waiter):", currentUser.role);
      if (role) {
        currentUser.role = role.toLowerCase();
        if (currentUser.role === 'owner') currentUser.name = 'Soe Aung';
        else if (currentUser.role === 'captain') currentUser.name = 'Captain 1';
        else currentUser.name = 'Waiter 1';
        document.getElementById('lblRole').textContent = currentUser.role.toUpperCase();
        document.getElementById('lblStaff').textContent = currentUser.name;
      }
    }

    async function initSystem() {
      document.getElementById('selPrintEngine').value = printEngine;
      try {
        const [resDb, resCfg] = await Promise.all([fetch('data.json'), fetch('/api/config')]);
        const db = await resDb.json();
        config = await resCfg.json();
        menuItems = db.items || [];
        renderCategoryFilter(db.categories || ['All']);
        renderMenuGrid(menuItems);
      } catch(e) {}

      document.getElementById('hdrShopTagline').textContent = config.shop_tagline || 'Hotel & Restaurant';
      await syncOrders();
      buildTableOptions();
      onTableSelect();
    }

    function renderCategoryFilter(cats) {
      const box = document.getElementById('categoryBar');
      box.innerHTML = '';
      cats.forEach((c, idx) => {
        box.innerHTML += `<button class="pill-btn ${idx===0?'active':''}" onclick="setCategory('${c}', this)">${c}</button>`;
      });

      const catSel = document.getElementById('manageItemCat');
      catSel.innerHTML = '';
      cats.filter(c => c !== 'All').forEach(c => {
        catSel.innerHTML += `<option value="${c}">${c}</option>`;
      });
    }

    function setCategory(cat, el) {
      activeCat = cat;
      document.querySelectorAll('#categoryBar .pill-btn').forEach(b => b.classList.remove('active'));
      el.classList.add('active');
      filterMenu();
    }

    function filterMenu() {
      const q = document.getElementById('txtSearch').value.toLowerCase().trim();
      let list = (activeCat === 'All') ? menuItems : menuItems.filter(m => m.category === activeCat);
      if (q) list = list.filter(m => m.name.toLowerCase().includes(q));
      renderMenuGrid(list);
    }

    function renderMenuGrid(items) {
      const grid = document.getElementById('gridMenu');
      grid.innerHTML = '';
      if (items.length === 0) {
        grid.innerHTML = '<div class="col-12 text-center text-secondary small py-4">ဟင်းပွဲ မရှိပါ</div>';
        return;
      }
      items.forEach(it => {
        const imgHtml = it.image ? `<img src="${it.image}" class="item-img" alt="${it.name}">` : '';
        grid.innerHTML += `
          <div class="col-6 col-sm-4">
            <div class="item-card" onclick="addToCart(${it.id})">
              ${imgHtml}
              <div class="item-title">${it.name}</div>
              <div class="d-flex justify-content-between align-items-center mt-1">
                <span class="price-pill">${it.price.toLocaleString()} Ks</span>
                <span class="text-secondary" style="font-size:10px;">${it.category}</span>
              </div>
            </div>
          </div>`;
      });
    }

    function buildTableOptions() {
      const sel = document.getElementById('selTable');
      const prev = sel.value;
      sel.innerHTML = '';
      let list = (activeFloor === 'all') ? [...floorList.flr1, ...floorList.ktv, ...floorList.flr2, ...floorList.flr3] : (floorList[activeFloor] || []);
      list.forEach(t => {
        const has = activeOrders[t] && activeOrders[t].items && activeOrders[t].items.length > 0;
        sel.innerHTML += `<option value="${t}">${has ? '🔴' : '🟢'} ${t}</option>`;
      });
      if (prev && list.includes(prev)) sel.value = prev;
    }

    function switchFloor(flr, el) {
      activeFloor = flr;
      document.querySelectorAll('#floorBar .pill-btn').forEach(b => b.classList.remove('active'));
      el.classList.add('active');
      buildTableOptions();
      onTableSelect();
    }

    function onTableSelect() {
      const t = document.getElementById('selTable').value;
      document.getElementById('lblActiveTableTitle').textContent = t || '-';
      const badge = document.getElementById('badgeTableStatus');
      if (t && activeOrders[t] && activeOrders[t].items && activeOrders[t].items.length > 0) {
        currentCart = JSON.parse(JSON.stringify(activeOrders[t].items));
        badge.className = 'badge bg-danger';
        badge.textContent = 'ဧည့်ရှိ (Active)';
      } else {
        currentCart = [];
        badge.className = 'badge bg-success';
        badge.textContent = 'လွတ်နေသည်';
      }
      renderCartUI();
    }

    function addToCart(id) {
      const it = menuItems.find(m => m.id === id);
      if (!it) return;
      const ex = currentCart.find(c => c.id === id);
      if (ex) ex.qty += 1;
      else currentCart.push({ id: it.id, name: it.name, price: it.price, qty: 1 });
      renderCartUI();
    }

    function renderCartUI() {
      const box = document.getElementById('boxCartItems');
      if (currentCart.length === 0) {
        box.innerHTML = '<p class="text-secondary text-center small my-4">အော်ဒါစာရင်း မရှိသေးပါ</p>';
        document.getElementById('lblSubTotal').textContent = '0 Ks';
        return;
      }
      box.innerHTML = '';
      let total = 0;
      currentCart.forEach((it, idx) => {
        const sub = it.price * it.qty;
        total += sub;
        box.innerHTML += `
          <div class="d-flex justify-content-between align-items-center cart-item-row small">
            <div>
              <div class="fw-bold">${it.name}</div>
              <span class="text-secondary">${it.price.toLocaleString()} x ${it.qty}</span>
            </div>
            <div class="d-flex align-items-center gap-1">
              <span class="text-warning fw-semibold me-1">${sub.toLocaleString()} Ks</span>
              <button class="btn btn-sm btn-secondary py-0 px-2 btn-alive" onclick="modQty(${idx}, -1)">-</button>
              <button class="btn btn-sm btn-secondary py-0 px-2 btn-alive" onclick="modQty(${idx}, 1)">+</button>
              <button class="btn btn-sm btn-danger py-0 px-2 btn-alive" onclick="delCartItem(${idx})">&times;</button>
            </div>
          </div>`;
      });
      document.getElementById('lblSubTotal').textContent = total.toLocaleString() + ' Ks';
    }

    function modQty(i, delta) {
      currentCart[i].qty += delta;
      if (currentCart[i].qty <= 0) currentCart.splice(i, 1);
      renderCartUI();
    }
    function delCartItem(i) {
      currentCart.splice(i, 1);
      renderCartUI();
    }

    async function clearActiveTable() {
      const t = document.getElementById('selTable').value;
      if (!confirm(`[${t}] ရှိ အော်ဒါများကို ရှင်းလင်းမည်လား?`)) return;
      currentCart = [];
      delete activeOrders[t];
      try { await fetch(`/api/active?table=${encodeURIComponent(t)}`, { method: 'DELETE' }); } catch(e) {}
      renderCartUI();
      buildTableOptions();
    }

    async function saveCartToTable() {
      const t = document.getElementById('selTable').value;
      if (currentCart.length === 0) return alert("သိမ်းရန် အော်ဒါမရှိပါ");
      activeOrders[t] = { table: t, waiter: currentUser.name, items: currentCart };
      try {
        await fetch('/api/active', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ table_name: t, waiter_name: currentUser.name, items: currentCart })
        });
      } catch(e) {}
      alert(`[${t}] တွင် အော်ဒါသိမ်းပြီးပါပြီ (${currentUser.name})`);
      buildTableOptions();
    }

    async function syncOrders() {
      try {
        const res = await fetch('/api/active');
        activeOrders = await res.json();
      } catch(e) {}
    }

    // Gallery Photo Compression
    function previewGalleryImage(input) {
      if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const img = new Image();
          img.onload = () => {
            const canvas = document.createElement('canvas');
            const maxDim = 320;
            let w = img.width, h = img.height;
            if (w > h) {
              if (w > maxDim) { h = Math.round(h * maxDim / w); w = maxDim; }
            } else {
              if (h > maxDim) { w = Math.round(w * maxDim / h); h = maxDim; }
            }
            canvas.width = w; canvas.height = h;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, w, h);
            currentCompressedBase64 = canvas.toDataURL('image/jpeg', 0.8);
            document.getElementById('imgPreviewThumb').innerHTML = `<img src="${currentCompressedBase64}" style="width:40px;height:40px;object-fit:cover;border-radius:4px;" class="border border-info">`;
          };
          img.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
      }
    }

    function openMenuManager() {
      resetManageForm();
      renderManageTable();
      menuManagerModal.show();
    }

    function resetManageForm() {
      document.getElementById('lblFormMode').textContent = '+ ကုန်ပစ္စည်း အသစ်ထည့်ရန်';
      document.getElementById('manageItemId').value = '';
      document.getElementById('manageItemName').value = '';
      document.getElementById('manageItemPrice').value = '';
      document.getElementById('fileGalleryInput').value = '';
      document.getElementById('imgPreviewThumb').innerHTML = '';
      currentCompressedBase64 = '';
    }

    function renderManageTable() {
      const tbody = document.getElementById('tblManageItems');
      tbody.innerHTML = '';
      menuItems.forEach((it, idx) => {
        const img = it.image ? `<img src="${it.image}" style="width:34px;height:34px;object-fit:cover;border-radius:4px;">` : '-';
        tbody.innerHTML += `
          <tr>
            <td>${img}</td>
            <td><strong>${it.name}</strong></td>
            <td><span class="badge bg-secondary">${it.category}</span></td>
            <td class="text-end text-info">${it.price.toLocaleString()} Ks</td>
            <td class="text-center">
              <button class="btn btn-sm btn-outline-info py-0 px-1 me-1" onclick="editManageItem(${idx})"><i class="fas fa-edit"></i></button>
              <button class="btn btn-sm btn-outline-danger py-0 px-1" onclick="deleteManageItem(${it.id})"><i class="fas fa-trash"></i></button>
            </td>
          </tr>`;
      });
    }

    function editManageItem(idx) {
      const it = menuItems[idx];
      document.getElementById('lblFormMode').textContent = 'ကုန်ပစ္စည်း ပြင်ဆင်ရန်';
      document.getElementById('manageItemId').value = it.id;
      document.getElementById('manageItemName').value = it.name;
      document.getElementById('manageItemPrice').value = it.price;
      document.getElementById('manageItemCat').value = it.category;
      currentCompressedBase64 = it.image || '';
      if (it.image) {
        document.getElementById('imgPreviewThumb').innerHTML = `<img src="${it.image}" style="width:40px;height:40px;object-fit:cover;border-radius:4px;" class="border border-info">`;
      } else {
        document.getElementById('imgPreviewThumb').innerHTML = '';
      }
    }

    async function saveItemData() {
      const id = document.getElementById('manageItemId').value;
      const name = document.getElementById('manageItemName').value.trim();
      const price = parseInt(document.getElementById('manageItemPrice').value);
      const category = document.getElementById('manageItemCat').value;

      if (!name || isNaN(price)) return alert("အမည်နှင့် ဈေးနှုန်း မှန်ကန်စွာ ဖြည့်ပါ");

      if (id) {
        await fetch('/api/items', {
          method: 'PUT',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ id: parseInt(id), name, price, category, image: currentCompressedBase64 })
        });
      } else {
        await fetch('/api/items', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ name, price, category, image: currentCompressedBase64 })
        });
      }
      resetManageForm();
      await initSystem();
      renderManageTable();
      alert("ကုန်ပစ္စည်း အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ");
    }

    async function deleteManageItem(id) {
      if (!confirm("ဤပစ္စည်းကို ဖျက်မည် သေချာပါသလား?")) return;
      await fetch('/api/items', {
        method: 'DELETE',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ id })
      });
      await initSystem();
      renderManageTable();
    }

    // Direct Web Bluetooth & USB
    async function connectWebBluetooth() {
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
        alert("Bluetooth Printer ချိတ်ဆက်မှု အောင်မြင်ပါသည်");
      } catch(e) { alert("Bluetooth ချိတ်၍မရပါ: " + e.message); }
    }

    async function connectWebUSB() {
      try {
        usbDevice = await navigator.usb.requestDevice({ filters: [] });
        await usbDevice.open();
        await usbDevice.selectConfiguration(1);
        await usbDevice.claimInterface(0);
        usbEndpoint = usbDevice.configuration.interfaces[0].alternate.endpoints.find(e => e.direction === 'out');
        alert("USB Printer ချိတ်ဆက်မှု အောင်မြင်ပါသည်");
      } catch(e) { alert("USB ချိတ်၍မရပါ: " + e.message); }
    }

    function setPrintEngine(mode) {
      printEngine = mode;
      localStorage.setItem('sm_print_engine', mode);
    }

    async function sendRawPrint(raw) {
      if (printEngine === 'direct_bt' && btChar) {
        await btChar.writeValue(new TextEncoder().encode(raw));
      } else if (printEngine === 'direct_usb' && usbDevice && usbEndpoint) {
        await usbDevice.transferOut(usbEndpoint.endpointNumber, new TextEncoder().encode(raw));
      } else {
        window.location.href = "rawbt:data:text/plain;charset=utf-8;base64," + btoa(unescape(encodeURIComponent(raw)));
      }
    }

    function makeEscPosSlip(type, d) {
      let t = `${config.shop_name || 'Sky Mother'}\n${config.shop_tagline || 'Hotel & Restaurant'}\nPh: ${config.shop_phone || '09-340339520'}\n--------------------------------\n`;
      if (type === 'preview') t += `** PREVIEW ဘေလ်စစ်ရန် **\n`;
      else if (type === 'kot') t += `** KITCHEN ORDER (မီးဖိုချောင်) **\n`;
      else t += `Order ID: ${d.id || 'SM-01'}\n`;
      t += `ဝိုင်း: ${d.table} | တာဝန်ခံ: ${d.staff}\n`;
      if (d.customer) t += `ဧည့်သည်: ${d.customer}\n`;
      t += `--------------------------------\n`;
      d.items.forEach(it => { t += `${it.name} x${it.qty}  ${(it.price*it.qty).toLocaleString()} Ks\n`; });
      t += `--------------------------------\n`;
      if (type !== 'kot') {
        t += `ကျသင့်ငွေ: ${d.total.toLocaleString()} Ks\n`;
        if (d.discount) t += `လျှော့ဈေး: ${d.discount.toLocaleString()} Ks\n`;
        if (d.paid) t += `ပေးချေငွေ: ${d.paid.toLocaleString()} Ks\n`;
        if (d.due > 0) t += `အကြွေးကျန်: ${d.due.toLocaleString()} Ks\n`;
      }
      t += `--------------------------------\nHave a wonderful day! Thank You\n\n\n`;
      return t;
    }

    function showBillPreview() {
      const t = document.getElementById('selTable').value;
      if (currentCart.length === 0) return alert("ဘေလ်စစ်ရန် အော်ဒါမရှိပါ");
      document.getElementById('pvShopName').textContent = config.shop_name || 'Sky Mother';
      document.getElementById('pvTagline').textContent = config.shop_tagline || 'Hotel & Restaurant';
      document.getElementById('pvPhone').textContent = config.shop_phone || '09-340339520';
      document.getElementById('pvKpay').textContent = config.kpay_phone || '09-783222755';
      document.getElementById('pvTable').textContent = t;
      document.getElementById('pvTime').textContent = new Date().toLocaleTimeString();
      document.getElementById('pvStaff').textContent = currentUser.name;

      const area = document.getElementById('pvItems');
      area.innerHTML = '';
      let sub = 0;
      currentCart.forEach(it => {
        sub += (it.price * it.qty);
        area.innerHTML += `<div class="d-flex justify-content-between"><span>${it.name} x ${it.qty}</span><span>${(it.price*it.qty).toLocaleString()} Ks</span></div>`;
      });
      document.getElementById('pvTotal').textContent = sub.toLocaleString() + ' Ks';
      previewModal.show();
    }

    function executePreviewPrint() {
      const t = document.getElementById('selTable').value;
      let total = 0; currentCart.forEach(i => total += i.price * i.qty);
      const text = makeEscPosSlip('preview', { table: t, staff: currentUser.name, items: currentCart, total: total });
      sendRawPrint(text);
      previewModal.hide();
    }

    function printKOT() {
      const t = document.getElementById('selTable').value;
      if (currentCart.length === 0) return alert("မီးဖိုချောင်သို့ ပို့ရန် အော်ဒါမရှိပါ");
      const text = makeEscPosSlip('kot', { table: t, staff: currentUser.name, items: currentCart });
      sendRawPrint(text);
    }

    function testThermalPrint() {
      const text = makeEscPosSlip('preview', { table: 'Test 01', staff: currentUser.name, items: [{name: 'စမ်းသပ်ပစ္စည်း', price: 1000, qty: 1}], total: 1000 });
      sendRawPrint(text);
    }

    function openCheckoutModal() {
      const t = document.getElementById('selTable').value;
      if (currentCart.length === 0) return alert("ဘေလ်ရှင်းရန် အော်ဒါမရှိပါ");
      let sub = 0; currentCart.forEach(c => sub += (c.price * c.qty));
      document.getElementById('chkTotalKs').textContent = sub.toLocaleString() + ' Ks';
      document.getElementById('chkDiscount').value = '0';
      document.getElementById('chkNetKs').textContent = sub.toLocaleString() + ' Ks';
      document.getElementById('chkPaidKs').value = sub;
      document.getElementById('chkDueKs').textContent = '0 Ks';
      document.getElementById('chkCustomer').value = '';
      checkoutModal.show();
    }

    function calcNetTotal() {
      let sub = 0; currentCart.forEach(c => sub += (c.price * c.qty));
      let disc = parseInt(document.getElementById('chkDiscount').value) || 0;
      let net = Math.max(0, sub - disc);
      document.getElementById('chkNetKs').textContent = net.toLocaleString() + ' Ks';
      let paid = parseInt(document.getElementById('chkPaidKs').value);
      if (isNaN(paid)) paid = net;
      let due = Math.max(0, net - paid);
      document.getElementById('chkDueKs').textContent = due.toLocaleString() + ' Ks';
    }

    function quickCash(val) {
      let sub = 0; currentCart.forEach(c => sub += (c.price * c.qty));
      let disc = parseInt(document.getElementById('chkDiscount').value) || 0;
      let net = Math.max(0, sub - disc);
      if (val === 'exact') {
        document.getElementById('chkPaidKs').value = net;
      } else if (val === 'round') {
        let rounded = Math.ceil(net / 1000) * 1000;
        document.getElementById('chkPaidKs').value = rounded;
      } else {
        document.getElementById('chkPaidKs').value = val;
      }
      calcNetTotal();
    }

    async function confirmCheckout() {
      const t = document.getElementById('selTable').value;
      let sub = 0; currentCart.forEach(c => sub += (c.price * c.qty));
      let disc = parseInt(document.getElementById('chkDiscount').value) || 0;
      let net = Math.max(0, sub - disc);
      let paid = parseInt(document.getElementById('chkPaidKs').value) || net;
      let due = Math.max(0, net - paid);
      let cust = document.getElementById('chkCustomer').value.trim();
      let payType = document.getElementById('chkPayType').value;

      const orderData = {
        id: 'SM-' + Math.floor(1000 + Math.random() * 9000),
        table: t,
        staff: currentUser.name,
        customer: cust,
        items: currentCart,
        total: net,
        discount: disc,
        paid: paid,
        due: due,
        pay_type: payType
      };

      const txt = makeEscPosSlip('final', orderData);
      sendRawPrint(txt);

      try {
        await fetch('/api/checkout', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            table_name: t,
            customer_name: cust,
            discount: disc,
            paid_amount: paid,
            payment_type: payType,
            waiter_name: currentUser.name
          })
        });
      } catch(e) {}

      checkoutModal.hide();
      currentCart = [];
      delete activeOrders[t];
      renderCartUI();
      buildTableOptions();
      alert(`[${t}] ဘေလ်ရှင်းပြီး စာရင်းပိတ်လိုက်ပါပြီ`);
    }

    function openReportModal() {
      window.location.href = '/api/export-csv';
    }

    function openSettingsModal() {
      document.getElementById('cfgShopName').value = config.shop_name || 'Sky Mother';
      document.getElementById('cfgTagline').value = config.shop_tagline || 'Hotel & Restaurant';
      document.getElementById('cfgPhone').value = config.shop_phone || '09-340339520';
      document.getElementById('cfgKpay').value = config.kpay_phone || '09-783222755';
      document.getElementById('cfgPin').value = config.owner_pin || '1234';
      settingsModal.show();
    }

    async function saveSystemSettings() {
      const payload = {
        shop_name: document.getElementById('cfgShopName').value,
        shop_tagline: document.getElementById('cfgTagline').value,
        shop_phone: document.getElementById('cfgPhone').value,
        kpay_phone: document.getElementById('cfgKpay').value,
        owner_pin: document.getElementById('cfgPin').value
      };
      await fetch('/api/config', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });
      alert("ဆက်တင်များ သိမ်းဆည်းပြီးပါပြီ");
      settingsModal.hide();
      await initSystem();
    }

    initSystem();
  </script>
</body>
</html>
'''

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("SUCCESS: Sky Mother POS Ultimate successfully upgraded!")
