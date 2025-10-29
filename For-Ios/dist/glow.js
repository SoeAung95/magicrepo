// small subtle pulse for headers
(function(){
	const h1 = document.querySelector('.container h1');
	if(!h1) return;
	let on = false;
	setInterval(()=>{
		h1.style.textShadow = on ? '0 0 12px rgba(0,240,255,0.15)' : '0 0 24px rgba(0,240,255,0.25)';
		on = !on;
	}, 1800);
})();