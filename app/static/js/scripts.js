document.addEventListener("DOMContentLoaded", function() {
    // Smooth scrolling for internal links
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    smoothScrollLinks.forEach(link => {
        link.addEventListener("click", function(event) {
            event.preventDefault();
            const target = document.querySelector(this.getAttribute("href"));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop,
                    behavior: "smooth"
                });
            }
        });
    });

    // Dynamic active link highlighting for navigation
    const navLinks = document.querySelectorAll(".nav-link");
    const currentPath = window.location.pathname;
    navLinks.forEach(link => {
        const linkPath = link.getAttribute("href");
        if (currentPath.includes(linkPath)) {
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });

    // Fade-in effect for elements with the class 'fade-in'
    const fadeInElements = document.querySelectorAll(".fade-in");
    const fadeInOnScroll = () => {
        fadeInElements.forEach(element => {
            const rect = element.getBoundingClientRect();
            if (rect.top < window.innerHeight - 100) {
                element.classList.add("visible");
            }
        });
    };

    // Initial fade-in on load and scroll event listener
    fadeInOnScroll();
    window.addEventListener("scroll", fadeInOnScroll);

    // Close navbar on link click in mobile view
    const navbarToggler = document.querySelector(".navbar-toggler");
    const navbarCollapse = document.querySelector(".navbar-collapse");
    navLinks.forEach(link => {
        link.addEventListener("click", () => {
            if (navbarCollapse.classList.contains("show")) {
                navbarToggler.click();
            }
        });
    });
});
