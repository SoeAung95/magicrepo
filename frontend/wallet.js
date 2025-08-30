document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 For-iOS Dashboard Loaded');
    
    const connectBtn = document.getElementById('connect-btn');
    const walletInfo = document.getElementById('wallet-info');
    const addressEl = document.getElementById('address');
    const balanceEl = document.getElementById('balance');
    const testApiBtn = document.getElementById('test-api');
    const apiResult = document.getElementById('api-result');
    
    // Wallet Connection
    connectBtn.addEventListener('click', async function() {
        try {
            connectBtn.textContent = 'Connecting...';
            connectBtn.disabled = true;
            
            // Simulate connection delay
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            // Mock wallet data
            const mockAddress = '0x742d35Cc6634C0532925a3b8D4C9db96590e4CAF';
            const mockBalance = '2.547 ETH';
            
            // Update UI
            addressEl.textContent = `Address: ${mockAddress}`;
            balanceEl.textContent = `Balance: ${mockBalance}`;
            
            connectBtn.style.display = 'none';
            walletInfo.classList.remove('hidden');
            
            console.log('✅ Wallet connected:', mockAddress);
            
            // Test wallet API
            testWalletAPI();
            
        } catch (error) {
            console.error('❌ Wallet connection failed:', error);
            connectBtn.textContent = 'Connection Failed';
            setTimeout(() => {
                connectBtn.textContent = 'Connect Wallet';
                connectBtn.disabled = false;
            }, 2000);
        }
    });
    
    // API Test
    testApiBtn.addEventListener('click', async function() {
        try {
            testApiBtn.textContent = 'Testing...';
            testApiBtn.disabled = true;
            
            const response = await fetch('/api/health');
            const data = await response.json();
            
            apiResult.textContent = JSON.stringify(data, null, 2);
            apiResult.style.color = '#00ff88';
            
            console.log('✅ Health API test successful:', data);
            
        } catch (error) {
            console.error('❌ API test failed:', error);
            apiResult.textContent = `Error: ${error.message}`;
            apiResult.style.color = '#ff6b6b';
        } finally {
            testApiBtn.textContent = 'Test Health API';
            testApiBtn.disabled = false;
        }
    });
    
    // Test Wallet API
    async function testWalletAPI() {
        try {
            const response = await fetch('/api/wallet');
            const data = await response.json();
            console.log('✅ Wallet API response:', data);
        } catch (error) {
            console.error('❌ Wallet API failed:', error);
        }
    }
});
