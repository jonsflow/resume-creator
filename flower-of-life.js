// Flower of Life SVG Generator
// Adapted from the FlowerOfLife project - creates authentic sacred geometry with overlapping circles

function generateFlowerOfLifeSVG(size = 200, inverted = false) {
    const centerX = 300;
    const centerY = 300;
    const radius = 45;
    const canvasSize = 600;
    const outerBoundaryRadius = 80; // Outer circle boundary
    const maxCircularRadius = 120; // Allow circles to grow beyond boundary for intersection

    // Choose color based on inverted state
    const strokeColor = inverted ? '#333333' : '#FFD700';

    // Helper function to find intersection points between two circles
    function findCircleIntersections(x1, y1, r1, x2, y2, r2) {
        const d = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));

        // Check if circles intersect
        if (d > r1 + r2 || d < Math.abs(r1 - r2) || d === 0) {
            return [];
        }

        const a = (Math.pow(r1, 2) - Math.pow(r2, 2) + Math.pow(d, 2)) / (2 * d);
        const h = Math.sqrt(Math.pow(r1, 2) - Math.pow(a, 2));

        const px = x1 + a * (x2 - x1) / d;
        const py = y1 + a * (y2 - y1) / d;

        const intersection1 = {
            x: px + h * (y2 - y1) / d,
            y: py - h * (x2 - x1) / d
        };

        const intersection2 = {
            x: px - h * (y2 - y1) / d,
            y: py + h * (x2 - x1) / d
        };

        return [intersection1, intersection2];
    }

    // Check if a circle already exists at this position
    function circleExists(x, y, circles, tolerance = 4) {
        return circles.some(circle =>
            Math.abs(circle.x - x) < tolerance && Math.abs(circle.y - y) < tolerance
        );
    }

    // Add circle if it doesn't exist and is within circular bounds
    function addCircle(x, y, circles) {
        // Check if circle center is within the maximum circular radius
        const distanceFromCenter = Math.sqrt(Math.pow(x - centerX, 2) + Math.pow(y - centerY, 2));
        // Allow circles slightly beyond boundary to generate intersections, but they'll be clipped
        if (distanceFromCenter > maxCircularRadius) {
            return false;
        }

        if (!circleExists(x, y, circles)) {
            circles.push({ x, y });
            return true;
        }
        return false;
    }

    // Generate the pattern using pure intersection discovery
    let circles = [];

    // Start with center circle
    circles.push({ x: centerX, y: centerY });

    // Generate pattern through iterations
    for (let iteration = 0; iteration < 5; iteration++) {
        const startingCount = circles.length;

        // Base case: only 1 circle, place 6 circles around it
        if (circles.length === 1) {
            for (let i = 0; i < 6; i++) {
                const angle = i * (Math.PI * 2 / 6);
                const x = centerX + radius * Math.cos(angle);
                const y = centerY + radius * Math.sin(angle);
                addCircle(x, y, circles);
            }
        } else {
            // Find ALL intersections between ALL existing circles
            for (let i = 0; i < circles.length; i++) {
                for (let j = i + 1; j < circles.length; j++) {
                    const intersections = findCircleIntersections(
                        circles[i].x, circles[i].y, radius,
                        circles[j].x, circles[j].y, radius
                    );

                    intersections.forEach(point => {
                        addCircle(point.x, point.y, circles);
                    });
                }
            }
        }

        // Stop if no new circles were added (natural termination)
        if (circles.length === startingCount) break;
    }

    // Calculate the bounds of the flower pattern
    const patternRadius = outerBoundaryRadius + radius;
    const minX = centerX - patternRadius;
    const minY = centerY - patternRadius;
    const patternSize = patternRadius * 2;

    // Build SVG with transparent background, sized to fit pattern exactly
    let svg = `<svg width="${size}" height="${size}" viewBox="${minX} ${minY} ${patternSize} ${patternSize}" xmlns="http://www.w3.org/2000/svg" style="background: transparent;">
        <defs>
            <style>
                .fol-circle { fill: none; stroke-width: 2.5; opacity: 1; stroke: ${strokeColor}; }
            </style>
            <clipPath id="circleClip">
                <circle cx="${centerX}" cy="${centerY}" r="${outerBoundaryRadius + radius}"/>
            </clipPath>
        </defs>

        <g clip-path="url(#circleClip)">`;

    // Draw all circles in the appropriate color (clipped by outer circle)
    circles.forEach(circle => {
        svg += `<circle cx="${circle.x}" cy="${circle.y}" r="${radius}" class="fol-circle"/>`;
    });

    svg += `</g>`;

    // Draw outer boundary circle
    svg += `<circle cx="${centerX}" cy="${centerY}" r="${outerBoundaryRadius + radius}" fill="none" stroke="${strokeColor}" stroke-width="2.5" opacity="1"/>`;

    // Center dot
    svg += `<circle cx="${centerX}" cy="${centerY}" r="3" fill="${strokeColor}"/>`;
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

/*
FLOWER OF LIFE - Sacred Geometry Circle Intersection Algorithm

RECURSIVE SEQUENCE PATTERN:
  f(0) = 1              (center circle)
  f(n) = f(n-1) + 6n    (for n ≥ 1)

CIRCLE COUNTS BY LEVEL:
  Level 0: 1 circle
  Level 1: 1 + 6 = 7 circles
  Level 2: 1 + 6 + 12 = 19 circles
  Level 3: 1 + 6 + 12 + 18 = 37 circles

CLOSED FORM: f(n) = 3n² + 3n + 1

CIRCLE INTERSECTION FORMULA:
  Given two circles with centers (x₁,y₁), (x₂,y₂) and radius r:
  d = √[(x₂-x₁)² + (y₂-y₁)²]
  a = (r² - r² + d²) / (2d)
  h = √(r² - a²)

  Intersection points are perpendicular to the line between centers:
  point₁ = (x₁ + a(x₂-x₁)/d + h(y₂-y₁)/d, y₁ + a(y₂-y₁)/d - h(x₂-x₁)/d)
  point₂ = (x₁ + a(x₂-x₁)/d - h(y₂-y₁)/d, y₁ + a(y₂-y₁)/d + h(x₂-x₁)/d)

ALGORITHM: Starting with a center circle, place 6 circles around it.
Then iteratively find all intersection points between existing circle pairs
and place new circles at those intersections until reaching the boundary.
*/
