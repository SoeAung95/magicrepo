// Modern Dashboard Functions
class Dashboard {
   constructor() {
       this.init();
   }
   async init() {
       await this.loadHealthStatus();
       await this.loadWalletBalance();
       await this.loadApiKeys();
       this.setupEventListeners();
   }
   async loadHealthStatus() {
       try {
           const response = await fetch('/api/health');
           const data = await response.json();
           document.getElementById('healthStatus').innerHTML =
               `<span class="text-success"><i class="fas fa-check-circle"></i> ${data.status}</span>`;
       } catch (error) {
           document.getElementById('healthStatus').innerHTML =
               `<span class="text-danger"><i class="fas fa-times-circle"></i> Error</span>`;
       }
   }
   async loadWalletBalance() {
       try {
           const response = await fetch('/api/wallet');
           const data = await response.json();
           document.getElementById('walletBalance').innerHTML =
               `<span class="text-success h4">$${data.balance}</span>`;
       } catch (error) {
           document.getElementById('walletBalance').innerHTML =
               `<span class="text-danger">Error loading</span>`;
       }
   }
   async loadApiKeys() {
       try {
           const response = await fetch('/api/keys');
           const data = await response.json();
           const keyCount = Object.keys(data.keys).length;
           document.getElementById('apiStatus').innerHTML =
               `<span class="text-info">${keyCount} Keys Active</span>`;
       } catch (error) {
           document.getElementById('apiStatus').innerHTML =
               `<span class="text-danger">Error</span>`;
       }
   }
   setupEventListeners() {
       // Wallet Connect
       document.getElementById('connectWallet').addEventListener('click', () => {
           this.connectWallet();
       });
       // Gmail Connect
       document.getElementById('gmailConnect').addEventListener('click', () => {
           this.connectGmail();
       });
   }
   connectWallet() {
       // Wallet connection logic
       alert('Wallet connection feature coming soon!');
   }
   connectGmail() {
       // Gmail OAuth integration
       alert('Gmail integration feature coming soon!');
   }
}
// Initialize Dashboard
document.addEventListener('DOMContentLoaded', () => {
   new Dashboard();
});
