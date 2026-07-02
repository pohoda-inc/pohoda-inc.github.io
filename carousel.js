// Screenshot carousels: swipe (native scroll-snap) + arrows + dots.
// No dependencies. Runs on any .carousel with a .carousel-track of .cslide items.
(function () {
  function centerOn(track, slide) {
    var left = slide.offsetLeft - (track.clientWidth - slide.offsetWidth) / 2;
    track.scrollTo({ left: left, behavior: 'smooth' });
  }

  document.querySelectorAll('.carousel').forEach(function (car) {
    var track = car.querySelector('.carousel-track');
    var slides = Array.prototype.slice.call(car.querySelectorAll('.cslide'));
    var dotsWrap = car.querySelector('.carousel-dots');
    var prev = car.querySelector('.carousel-prev');
    var next = car.querySelector('.carousel-next');
    if (!track || slides.length <= 1) {
      if (dotsWrap) dotsWrap.style.display = 'none';
      if (prev) prev.style.display = 'none';
      if (next) next.style.display = 'none';
      return;
    }

    if (dotsWrap) {
      slides.forEach(function (_, i) {
        var b = document.createElement('button');
        b.setAttribute('aria-label', (i + 1) + '枚目へ');
        b.addEventListener('click', function () { centerOn(track, slides[i]); });
        dotsWrap.appendChild(b);
      });
    }
    var dots = dotsWrap ? dotsWrap.querySelectorAll('button') : [];

    function currentIndex() {
      var center = track.scrollLeft + track.clientWidth / 2;
      var best = 0, bestDist = Infinity;
      slides.forEach(function (s, i) {
        var mid = s.offsetLeft + s.offsetWidth / 2;
        var d = Math.abs(mid - center);
        if (d < bestDist) { bestDist = d; best = i; }
      });
      return best;
    }
    function update() {
      var idx = currentIndex();
      for (var i = 0; i < dots.length; i++) dots[i].classList.toggle('on', i === idx);
    }

    var ticking = false;
    track.addEventListener('scroll', function () {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(function () { update(); ticking = false; });
      }
    });
    if (prev) prev.addEventListener('click', function () { centerOn(track, slides[Math.max(0, currentIndex() - 1)]); });
    if (next) next.addEventListener('click', function () { centerOn(track, slides[Math.min(slides.length - 1, currentIndex() + 1)]); });

    update();
  });
})();
