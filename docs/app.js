// Countdown to IOAI 2026 opening — Aug 2, 2026, Astana (UTC+5)
(function () {
  var target = new Date("2026-08-02T09:00:00+05:00").getTime();
  var el = {
    d: document.getElementById("cd-d"),
    h: document.getElementById("cd-h"),
    m: document.getElementById("cd-m"),
    s: document.getElementById("cd-s"),
  };
  function pad(n) { return n < 10 ? "0" + n : "" + n; }
  function tick() {
    var diff = target - Date.now();
    if (diff <= 0) {
      el.d.textContent = "00"; el.h.textContent = "00"; el.m.textContent = "00"; el.s.textContent = "00";
      document.querySelector(".cd-label").textContent = "It's contest time. Go get it. \uD83C\uDFC1";
      return;
    }
    el.d.textContent = pad(Math.floor(diff / 864e5));
    el.h.textContent = pad(Math.floor(diff / 36e5) % 24);
    el.m.textContent = pad(Math.floor(diff / 6e4) % 60);
    el.s.textContent = pad(Math.floor(diff / 1e3) % 60);
    setTimeout(tick, 1000);
  }
  tick();
})();

// Copy-to-clipboard for prompt cards
document.querySelectorAll(".copy").forEach(function (btn) {
  btn.addEventListener("click", function () {
    var src = document.getElementById(btn.getAttribute("data-copy"));
    if (!src) return;
    navigator.clipboard.writeText(src.textContent.trim()).then(function () {
      var old = btn.textContent;
      btn.textContent = "copied ✓";
      btn.classList.add("copied");
      setTimeout(function () { btn.textContent = old; btn.classList.remove("copied"); }, 1600);
    });
  });
});
