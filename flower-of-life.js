// Flower of Life SVG Generator
// Creates a compact sacred geometry symbol for resume decoration

function generateFlowerOfLifeSVG(size = 200, circles = 19) {
    const radius = 50;
    const centerX = 150;
    const centerY = 150;

    // Calculate circle positions for 19-circle pattern
    let circlePositions = [];

    // Center circle
    circlePositions.push({ x: centerX, y: centerY, phase: 'vesica' });

    // First ring (6 circles)
    for (let i = 0; i < 6; i++) {
        const angle = i * (Math.PI * 2 / 6);
        const x = centerX + radius * Math.cos(angle);
        const y = centerY + radius * Math.sin(angle);
        circlePositions.push({ x, y, phase: 'seed' });
    }

    // Second ring (6 circles at intersections)
    for (let i = 0; i < 6; i++) {
        const angle = (i * (Math.PI * 2 / 6)) + (Math.PI / 6);
        const x = centerX + radius * Math.sqrt(3) * Math.cos(angle);
        const y = centerY + radius * Math.sqrt(3) * Math.sin(angle);
        circlePositions.push({ x, y, phase: 'egg' });
    }

    // Third ring (6 circles)
    for (let i = 0; i < 6; i++) {
        const angle = i * (Math.PI * 2 / 6);
        const x = centerX + radius * 2 * Math.cos(angle);
        const y = centerY + radius * 2 * Math.sin(angle);
        circlePositions.push({ x, y, phase: 'flower' });
    }

    const colors = {
        vesica: '#FFB3B3',
        seed: '#4ECDC4',
        egg: '#45B7D1',
        flower: '#FFD700'
    };

    const circleRadius = radius / 2.5;
    let svg = `<svg width="${size}" height="${size}" viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <style>
                .fol-circle { fill: none; stroke-width: 1.5; opacity: 0.8; }
            </style>
        </defs>
        <rect width="300" height="300" fill="transparent"/>`;

    // Group circles by phase for layered effect
    ['vesica', 'seed', 'egg', 'flower'].forEach(phase => {
        const phaseCircles = circlePositions.filter(c => c.phase === phase);
        phaseCircles.forEach(circle => {
            svg += `<circle cx="${circle.x}" cy="${circle.y}" r="${circleRadius}" class="fol-circle" stroke="${colors[phase]}"/>`;
        });
    });

    // Center dot
    svg += `<circle cx="${centerX}" cy="${centerY}" r="2" fill="#FFD700"/>`;
    svg += `</svg>`;

    return svg;
}

// Replace profile image with flower of life on print
function replaceProfileImageWithFlower() {
    const profileImages = document.querySelectorAll('.profile-image');
    profileImages.forEach(img => {
        img.innerHTML = generateFlowerOfLifeSVG(150);
        img.style.backgroundImage = 'none';
        img.style.display = 'flex';
        img.style.alignItems = 'center';
        img.style.justifyContent = 'center';
    });
}
