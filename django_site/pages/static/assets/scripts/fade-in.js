(function() {
  document.addEventListener('DOMContentLoaded', function() {
    var targets = document.querySelectorAll('article h1, article h2, article h3, article img');
    if (!('IntersectionObserver' in window)) {
      targets.forEach(function(el) { el.classList.add('in-view'); });
      return;
    }
    var observer = new IntersectionObserver(function(entries, obs) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    targets.forEach(function(el) {
      el.classList.add('fade-element');
      observer.observe(el);
    });
  });
})();
