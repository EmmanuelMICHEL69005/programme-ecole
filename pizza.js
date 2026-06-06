// Shared pizza SVG utility
const PZ = {
  cx: 50, cy: 50, r: 44,
  bg: '#fef9e7',
  border: '#d97706',
  fillOrange: '#f97316',
  fillGreen: '#22c55e',
  fillStatic: '#fb923c'
};

function _rad(deg) { return deg * Math.PI / 180; }

function _slicePath(n, i) {
  const a1 = _rad(i * 360 / n - 90);
  const a2 = _rad((i + 1) * 360 / n - 90);
  const x1 = (PZ.cx + PZ.r * Math.cos(a1)).toFixed(2);
  const y1 = (PZ.cy + PZ.r * Math.sin(a1)).toFixed(2);
  const x2 = (PZ.cx + PZ.r * Math.cos(a2)).toFixed(2);
  const y2 = (PZ.cy + PZ.r * Math.sin(a2)).toFixed(2);
  const large = 360 / n > 180 ? 1 : 0;
  return `M ${PZ.cx} ${PZ.cy} L ${x1} ${y1} A ${PZ.r} ${PZ.r} 0 ${large} 1 ${x2} ${y2} Z`;
}

function _buildSVG(n, colorFn, width) {
  const ns = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(ns, 'svg');
  svg.setAttribute('viewBox', '0 0 100 100');
  svg.setAttribute('width', width || '100');
  svg.setAttribute('height', width || '100');

  const bg = document.createElementNS(ns, 'circle');
  bg.setAttribute('cx', PZ.cx); bg.setAttribute('cy', PZ.cy);
  bg.setAttribute('r', PZ.r);
  bg.setAttribute('fill', PZ.bg);
  bg.setAttribute('stroke', PZ.border);
  bg.setAttribute('stroke-width', '2.5');
  svg.appendChild(bg);

  const slices = [];
  for (let i = 0; i < n; i++) {
    const path = document.createElementNS(ns, 'path');
    path.setAttribute('d', _slicePath(n, i));
    path.setAttribute('fill', colorFn ? colorFn(i) : 'transparent');
    path.setAttribute('fill-opacity', '0.85');
    path.setAttribute('stroke', PZ.border);
    path.setAttribute('stroke-width', '1.5');
    svg.appendChild(path);
    slices.push(path);
  }
  return { svg, slices };
}

// Returns an SVG element (static) — reusable
function pizzaStaticEl(n, filled, size) {
  const { svg } = _buildSVG(n, i => i < filled ? PZ.fillStatic : 'transparent', size || '80');
  return svg;
}

// Static pizza for "Je retiens" — already shows colored slices
function pizzaStatic(containerId, n, filled) {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.appendChild(pizzaStaticEl(n, filled, '80'));
}

// Interactive pizza — user clicks slices, gets feedback
function pizzaInteractive(containerId, n, correct) {
  const el = document.getElementById(containerId);
  if (!el) return;
  const fb = el.querySelector('.pizza-feedback');

  const { svg, slices } = _buildSVG(n, () => 'transparent', '120');
  svg.style.display = 'block';
  svg.style.margin = '6px auto';

  slices.forEach(path => {
    path.style.cursor = 'pointer';
    path.style.transition = 'fill 0.15s';
    path.dataset.on = '0';

    path.addEventListener('click', () => {
      path.dataset.on = path.dataset.on === '1' ? '0' : '1';
      const count = slices.filter(p => p.dataset.on === '1').length;

      slices.forEach(p => {
        p.setAttribute('fill', p.dataset.on === '1' ? PZ.fillOrange : 'transparent');
      });

      if (count === correct) {
        slices.forEach(p => {
          if (p.dataset.on === '1') p.setAttribute('fill', PZ.fillGreen);
        });
        if (fb) { fb.textContent = '✅ Bravo !'; fb.style.color = '#166534'; }
      } else if (count > correct) {
        if (fb) { fb.textContent = `❌ Trop ! (${count} parts sur ${n})`; fb.style.color = '#991b1b'; }
      } else {
        if (fb) { fb.textContent = ''; }
      }
    });
  });

  el.insertBefore(svg, fb);
}
