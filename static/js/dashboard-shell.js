(function () {
  var shell = document.getElementById('dashboard-shell');
  var toggle = document.getElementById('sidebar-toggle');
  if (!shell || !toggle) return;

  var key = 'anpress_sidebar_collapsed';
  if (localStorage.getItem(key) === '1') {
    shell.classList.add('sidebar-collapsed');
  }

  toggle.addEventListener('click', function () {
    shell.classList.toggle('sidebar-collapsed');
    localStorage.setItem(key, shell.classList.contains('sidebar-collapsed') ? '1' : '0');
  });
})();
