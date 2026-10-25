(function () {
    "use strict";

    // Mobile navigation toggle
    var toggle = document.querySelector(".nav-toggle");
    var links = document.querySelector(".nav-links");
    if (toggle && links) {
        toggle.addEventListener("click", function () {
            var open = links.classList.toggle("open");
            toggle.setAttribute("aria-expanded", open ? "true" : "false");
        });
    }

    // Reveal-on-scroll animation
    var items = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window) {
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add("in");
                    io.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });
        items.forEach(function (el) { io.observe(el); });
    } else {
        items.forEach(function (el) { el.classList.add("in"); });
    }

    // Toast messages: close button + auto dismiss
    document.querySelectorAll(".toast").forEach(function (toast) {
        var close = toast.querySelector("button");
        var remove = function () { toast.remove(); };
        if (close) { close.addEventListener("click", remove); }
        setTimeout(remove, 6000);
    });

    // Appointment form: past dates disable karo
    var dt = document.querySelector("input[type=datetime-local]");
    if (dt) {
        var now = new Date();
        now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
        dt.min = now.toISOString().slice(0, 16);
    }

    // Cancel confirmation
    document.querySelectorAll("form[data-confirm]").forEach(function (form) {
        form.addEventListener("submit", function (event) {
            if (!window.confirm(form.getAttribute("data-confirm"))) {
                event.preventDefault();
            }
        });
    });
})();
