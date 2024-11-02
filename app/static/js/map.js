document.addEventListener("DOMContentLoaded", function() {
    // Initialize the map centered on the USA
    const map = L.map("map").setView([37.8, -96], 4);

    // Add OpenStreetMap tiles
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);

    // GeoJSON data for the USA (you'll need a GeoJSON source or a URL to fetch it)
    fetch("path/to/us-states.geojson") // Replace with the path to your GeoJSON file
        .then(response => response.json())
        .then(geojsonData => {
            // Define state styles and interactive behavior
            const stateStyle = {
                color: "#444",
                weight: 2,
                fillColor: "#88A4BC",
                fillOpacity: 0.6,
            };

            // Add state layer with hover and click interaction
            const statesLayer = L.geoJson(geojsonData, {
                style: stateStyle,
                onEachFeature: function(feature, layer) {
                    // Tooltip with state name
                    layer.bindTooltip(feature.properties.name, {
                        direction: "center",
                        className: "state-tooltip",
                        permanent: false,
                    });

                    // Hover effects
                    layer.on("mouseover", function(e) {
                        layer.setStyle({
                            fillColor: "#3B729F",
                        });
                    });

                    layer.on("mouseout", function(e) {
                        layer.setStyle(stateStyle);
                    });

                    // Click to navigate to the state's page
                    layer.on("click", function(e) {
                        const stateName = feature.properties.name.toLowerCase().replace(/\s+/g, "-");
                        window.location.href = `/state/${stateName}`; // Update with your actual URL structure
                    });
                },
            }).addTo(map);
        })
        .catch(error => console.error("Error loading GeoJSON data:", error));

    // Optional: Add a zoom control to the bottom-right corner
    L.control.zoom({
        position: "bottomright",
    }).addTo(map);
});
