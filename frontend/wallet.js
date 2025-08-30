// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    updateTime();
    setInterval(updateTime, 1000);
});

function initializeApp() {
    loadWallets();
    setupEventListeners();
    showLoading(false);
}

function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: false
    });
    const timeElement = document.getElementById('current-time');
    if (timeElement) {
        timeElement.textContent = timeString;
    }
}

function showLoading(show = true) {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.toggle('show', show);
    }
}

function setupEventListeners() {
    // Navigation buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const section = btn.dataset.section;
            handleNavigation(section);
        });
    });

    // Action buttons
    document.getElementById('connect-wallet')?.addEventListener('click', connectWallet);
    document.getElementById('view-portfolio')?.addEventListener('click', viewPortfolio);
    document.getElementById('send-crypto')?.addEventListener('click', sendCrypto);
    document.getElementById('receive-crypto')?.addEventListener('click', receiveCrypto);
    
    // Refresh button
    document.getElementById('refresh-wallets')?.addEventListener('click', () => {
        loadWallets(true);
    });
}

function handleNavigation(section) {
    console.log(`Navigating to: ${section}`);
    // Add navigation logic here
    
    switch(section) {
        case 'wallet':
            loadWallets();
            break;
        case 'portfolio':
            showPortfolio();
            break;
        case 'trade':
            showTrading();
            break;
        case 'settings':
            showSettings();
            break;
    }
}

function connectWallet() {
    showNotification('🔗 Connecting to wallet...', 'info');
    // Add WalletConnect integration here
    setTimeout(() => {
        showNotification('✅ Wallet connected successfully!', 'success');
    }, 2000);
}

function viewPortfolio() {
    showNotification('📊 Loading portfolio...', 'info');
}

function sendCrypto() {
    showNotification('💸 Send feature coming soon!', 'info');
}

function receiveCrypto() {
    showNotification('📥 Receive feature coming soon!', 'info');
}

function showPortfolio() {
    console.log('Showing portfolio view');
}

function showTrading() {
    console.log('Showing trading view');
}

function showSettings() {
    console.log('Showing settings view');
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.9);
        color: white;
        padding: 15px 20px;
        border-radius: 12px;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 1001;
        font-size: 14px;
        font-weight: 500;
        max-width: 90%;
        text-align: center;
        animation: slideDown 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideUp 0.3s ease forwards';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

async function loadWallets(refresh = false) {
    if (refresh) {
        showLoading(true);
    }
    
    try {
        const container = document.getElementById('wallet-container');
        if (!container) return;
        
        // Show demo wallets from env.js
        const wallets = [
            {
                name: 'ETH Main Wallet',
                network: 'ETH',
                address: window.APP_CONFIG?.BINANCE_WALLETS?.ETH_BNB || '0x1234...5678',
                balance: '2.45 ETH',
                usdValue: '$4,200.00',
                color: 'var(--ios-blue)'
            },
            {
                name: 'Solana Wallet',
                network: 'SOL',
                address: window.APP_CONFIG?.BITGET_WALLETS?.SOL || '9knB...sTiX',
                balance: '145.32 SOL',
                usdValue: '$3,850.00',
                color: 'var(--ios-purple)'
            },
            {
                name: 'TON Wallet',
                network: 'TON',
                address: window.APP_CONFIG?.BINANCE_WALLETS?.TON || 'UQAK...w9Ut',
                balance: '1,250 TON',
                usdValue: '$2,100.00',
                color: 'var(--ios-teal)'
            }
        ];
        
        container.innerHTML = '';
        
        wallets.forEach((wallet, index) => {
            const walletCard = createWalletCard(wallet);
            walletCard.style.animationDelay = `${index * 0.1}s`;
            container.appendChild(walletCard);
        });
        
        // Try to fetch real balance for first wallet
        try {
            const response = await fetch(`/api/wallet?address=${wallets[0].address}`);
            if (response.ok) {
                const data = await response.json();
                updateWalletBalance(0, data.balance);
            }
        } catch (error) {
            console.log('API not available, using demo data');
        }
        
    } catch (error) {
        console.error('Error loading wallets:', error);
        showNotification('❌ Error loading wallets', 'error');
    } finally {
        showLoading(false);
    }
}

function createWalletCard(wallet) {
    const card = document.createElement('div');
    card.className = 'wallet-card';
    card.innerHTML = `
        <div class="wallet-header">
            <div class="wallet-name">${wallet.name}</div>
            <div class="wallet-network" style="background: ${wallet.color}">${wallet.network}</div>
        </div>
        <div class="wallet-address">${formatAddress(wallet.address)}</div>
        <div class="wallet-balance">
            <div class="balance-amount">${wallet.balance}</div>
            <div class="balance-usd">${wallet.usdValue}</div>
        </div>
    `;
    
    // Add click handler
    card.addEventListener('click', () => {
        showNotification(`📱 ${wallet.name} selected`, 'info');
    });
    
    return card;
}

function formatAddress(address) {
    if (address.length > 20) {
        return `${address.slice(0, 8)}...${address.slice(-8)}`;
    }
    return address;
}

function updateWalletBalance(index, balance) {
    const walletCards = document.querySelectorAll('.wallet-card');
    if (walletCards[index]) {
        const balanceElement = walletCards[index].querySelector('.balance-amount');
        if (balanceElement && balance) {
            // Convert wei to ETH (simple conversion)
            const ethBalance = (parseInt(balance) / 1e18).toFixed(4);
            balanceElement.textContent = `${ethBalance} ETH`;
        }
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translate(-50%, -20px);
        }
        to {
            opacity: 1;
            transform: translate(-50%, 0);
        }
    }
    
    @keyframes slideUp {
        from {
            opacity: 1;
            transform: translate(-50%, 0);
        }
        to {
            opacity: 0;
            transform: translate(-50%, -20px);
        }
    }
`;
document.head.appendChild(style);