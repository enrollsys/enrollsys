document.addEventListener("DOMContentLoaded", () => {
    const nav = document.querySelector("[data-nav]");
    const menuToggle = document.querySelector("[data-menu-toggle]");
    if (nav && menuToggle) {
        menuToggle.addEventListener("click", () => nav.classList.toggle("open"));
    }

    document.querySelectorAll("[data-accordion-button]").forEach((button) => {
        button.addEventListener("click", () => {
            const body = button.closest("[data-accordion-item]").querySelector("[data-accordion-body]");
            body.hidden = !body.hidden;
        });
    });

    document.querySelectorAll("[data-file-input]").forEach((input) => {
        input.addEventListener("change", () => {
            const preview = document.querySelector("[data-file-preview]");
            if (preview) {
                preview.textContent = input.files.length ? `Выбран файл: ${input.files[0].name}` : "Файл не выбран";
            }
        });
    });

    const revealItems = document.querySelectorAll("[data-reveal]");
    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });
        revealItems.forEach((item) => observer.observe(item));
    } else {
        revealItems.forEach((item) => item.classList.add("visible"));
    }
});
