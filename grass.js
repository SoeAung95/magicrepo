function startSale() {
  alert("Sale started! 🎉");
}

window.onload = function() {
  try {
    // Fake connection logic
    console.log("Connecting to Grass Lite Node...");
    // Simulate connection fail
    setTimeout(() => {
      console.error("❌ Grass Lite Node disconnected.");
      alert("Grass Lite Node disconnected. Please check network!");
    }, 2000);
  } catch (e) {
    console.error("Error: ", e);
  }
};
