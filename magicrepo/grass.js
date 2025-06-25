function startSale() {
  alert("Sale started by MagicStone POS! 🚀");
}

window.onload = function() {
  console.log("🌿 Connecting to Grass Lite Node...");
  setTimeout(() => {
    console.error("❌ Grass Lite Node disconnected.");
    alert("Grass Lite Node disconnected. Check your network connection!");
  }, 2000);
};

