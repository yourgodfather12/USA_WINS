// script.js

document.addEventListener("DOMContentLoaded", () => {
    // Store the state data
    const stateData = {
        "Alabama": 67,
        "Alaska": 29,
        "Arizona": 15,
        "Arkansas": 75,
        "California": 58,
        "Colorado": 64,
        "Connecticut": 8,
        "Delaware": 3,
        "Florida": 67,
        "Georgia": 159,
        "Hawaii": 5,
        "Idaho": 44,
        "Illinois": 102,
        "Indiana": 92,
        "Iowa": 99,
        "Kansas": 105,
        "Kentucky": 120,
        "Louisiana": 64,
        "Maine": 16,
        "Maryland": 24,
        "Massachusetts": 14,
        "Michigan": 83,
        "Minnesota": 87,
        "Mississippi": 82,
        "Missouri": 114,
        "Montana": 56,
        "Nebraska": 93,
        "Nevada": 16,
        "New Hampshire": 10,
        "New Jersey": 21,
        "New Mexico": 33,
        "New York": 62,
        "North Carolina": 100,
        "North Dakota": 53,
        "Ohio": 88,
        "Oklahoma": 77,
        "Oregon": 36,
        "Pennsylvania": 67,
        "Rhode Island": 5,
        "South Carolina": 46,
        "South Dakota": 66,
        "Tennessee": 95,
        "Texas": 254,
        "Utah": 29,
        "Vermont": 14,
        "Virginia": 95,
        "Washington": 39,
        "West Virginia": 55,
        "Wisconsin": 72,
        "Wyoming": 23
    };

    // Initialize modal elements
    const modal = document.getElementById("modal");
    const overlay = document.getElementById("overlay");
    const modalClose = document.getElementById("modal-close");
    const stateNameModal = document.getElementById("state-name-modal");
    const numCounties = document.getElementById("num-counties");

    // State hover effect
    const statePaths = document.querySelectorAll("#us-map .state");
    statePaths.forEach((state) => {
        const stateName = state.getAttribute("data-name");
        state.addEventListener("mouseenter", () => {
            state.classList.add("state-active");
            showTooltip(state, stateName);
        });
        state.addEventListener("mouseleave", () => {
            state.classList.remove("state-active");
            hideTooltip();
        });
        state.addEventListener("click", () => showModal(stateName));
    });

    // Modal close functionality
    modalClose.addEventListener("click", hideModal);
    overlay.addEventListener("click", hideModal);
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && modal.classList.contains("show")) {
            hideModal();
        }
    });

    // Function to show tooltip
    function showTooltip(state, stateName) {
        const tooltip = document.getElementById("tooltip");
        tooltip.textContent = stateName;
        tooltip.style.opacity = 1;

        // Positioning the tooltip
        const rect = state.getBoundingClientRect();
        tooltip.style.left = `${rect.left + window.scrollX}px`;
        tooltip.style.top = `${rect.top + window.scrollY - tooltip.offsetHeight - 5}px`;
    }

    // Function to hide tooltip
    function hideTooltip() {
        const tooltip = document.getElementById("tooltip");
        tooltip.style.opacity = 0;
    }

    // Function to show modal with county information
    function showModal(stateName) {
        stateNameModal.textContent = stateName;
        numCounties.textContent = stateData[stateName];
        modal.classList.add("show");
        overlay.classList.add("show");
        modal.setAttribute('aria-hidden', 'false');
        modal.focus();
    }

    // Function to hide modal
    function hideModal() {
        modal.classList.remove("show");
        overlay.classList.remove("show");
        modal.setAttribute('aria-hidden', 'true');
    }

    // Zooming into states (optional)
    function zoomToState(state) {
        const bbox = state.getBBox();
        const scale = Math.min(1.5, Math.min(800 / bbox.width, 600 / bbox.height));
        const translateX = -bbox.x * scale + (800 - bbox.width * scale) / 2;
        const translateY = -bbox.y * scale + (600 - bbox.height * scale) / 2;
        const usMap = document.getElementById("us-map");
        usMap.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
    }

    // Fade out messages
    const messages = document.querySelectorAll(".message");
    messages.forEach((message) => {
        setTimeout(() => {
            message.style.opacity = "0";
        }, 3000);
    });
});
