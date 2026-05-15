/* =========================================================
   Управление организацией приема — Main JavaScript
   ========================================================= */

(function () {
    'use strict';

    /* ── Helpers ── */
    const $ = (sel, ctx = document) => ctx.querySelector(sel);
    const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

    /* ── Header scroll shadow ── */
    function initHeaderScroll() {
        const header = $('.site-header');
        if (!header) return;
        const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 8);
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    /* ── Mobile navigation ── */
    function initMobileNav() {
        const toggle = $('[data-menu-toggle]');
        const nav = $('[data-nav]');
        if (!toggle || !nav) return;

        toggle.addEventListener('click', () => {
            const open = nav.classList.toggle('nav-open');
            toggle.classList.toggle('open', open);
            toggle.setAttribute('aria-expanded', open);
            document.body.style.overflow = open ? 'hidden' : '';
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!nav.contains(e.target) && !toggle.contains(e.target)) {
                nav.classList.remove('nav-open');
                toggle.classList.remove('open');
                toggle.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            }
        });

        // Mobile dropdown toggles
        $$('[data-dropdown]').forEach(item => {
            const link = item.querySelector('.nav-link');
            if (!link) return;
            link.addEventListener('click', (e) => {
                if (window.innerWidth <= 960) {
                    e.preventDefault();
                    item.classList.toggle('dd-open');
                }
            });
        });
    }

    /* ── Active nav link ── */
    function initActiveNav() {
        const path = window.location.pathname;
        $$('.nav-link, .sidebar-nav-item, .tabs a').forEach(link => {
            const href = link.getAttribute('href');
            if (!href) return;
            if (href === path || (href !== '/' && path.startsWith(href))) {
                link.classList.add('active');
            }
        });
    }

    /* ── Scroll reveal ── */
    function initReveal() {
        const items = $$('[data-reveal]');
        if (!items.length) return;

        if ('IntersectionObserver' in window) {
            const io = new IntersectionObserver((entries) => {
                entries.forEach((entry, i) => {
                    if (entry.isIntersecting) {
                        const delay = entry.target.dataset.revealDelay || 0;
                        setTimeout(() => {
                            entry.target.classList.add('visible');
                        }, delay * 80);
                        io.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

            items.forEach(el => io.observe(el));
        } else {
            items.forEach(el => el.classList.add('visible'));
        }
    }

    /* ── Animated number counters ── */
    function animateCounter(el) {
        const target = parseFloat(el.dataset.counter);
        if (isNaN(target)) return;
        const duration = 1400;
        const startTime = performance.now();
        const isDecimal = String(target).includes('.');

        const tick = (now) => {
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const ease = 1 - Math.pow(1 - progress, 3);
            const value = target * ease;
            el.textContent = isDecimal
                ? value.toFixed(1)
                : Math.round(value).toLocaleString('ru-RU');
            if (progress < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
    }

    function initCounters() {
        const counters = $$('[data-counter]');
        if (!counters.length) return;

        const io = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    io.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(el => io.observe(el));
    }

    /* ── Accordion / FAQ ── */
    function initAccordion() {
        $$('[data-accordion-btn], .accordion-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const item = btn.closest('[data-accordion-item], .accordion-item');
                if (!item) return;
                const body = item.querySelector('[data-accordion-body], .accordion-body');
                if (!body) return;

                const isOpen = item.classList.contains('open');

                // Close siblings
                if (item.closest('.accordion')) {
                    $$('.accordion-item', item.closest('.accordion')).forEach(sibling => {
                        sibling.classList.remove('open');
                        const sibBody = sibling.querySelector('.accordion-body');
                        if (sibBody) {
                            sibBody.style.maxHeight = null;
                            sibBody.hidden = true;
                        }
                    });
                }

                // Toggle current
                if (!isOpen) {
                    item.classList.add('open');
                    body.hidden = false;
                    body.style.maxHeight = body.scrollHeight + 'px';
                } else {
                    item.classList.remove('open');
                    body.style.maxHeight = null;
                    setTimeout(() => { body.hidden = true; }, 220);
                }
            });
        });

        // Initialize hidden state
        $$('.accordion-body').forEach(body => {
            if (!body.closest('.accordion-item').classList.contains('open')) {
                body.hidden = true;
            }
        });
    }

    /* ── File upload drag-and-drop ── */
    function initFileUpload() {
        $$('[data-file-drop]').forEach(zone => {
            const input = zone.querySelector('input[type="file"]') || $('[data-file-input]');
            const preview = zone.querySelector('[data-file-preview]') || $('[data-file-preview]');

            if (input) {
                input.addEventListener('change', () => {
                    if (input.files.length && preview) {
                        preview.textContent = '📎 ' + input.files[0].name;
                        preview.style.display = 'block';
                        zone.classList.add('has-file');
                    }
                });
            }

            ['dragenter', 'dragover'].forEach(ev => {
                zone.addEventListener(ev, (e) => {
                    e.preventDefault();
                    zone.classList.add('dragover');
                });
            });

            ['dragleave', 'drop'].forEach(ev => {
                zone.addEventListener(ev, (e) => {
                    e.preventDefault();
                    zone.classList.remove('dragover');
                    if (ev === 'drop' && e.dataTransfer.files.length) {
                        if (input) {
                            // Note: can't programmatically set files, just show name
                            if (preview) {
                                preview.textContent = '📎 ' + e.dataTransfer.files[0].name;
                                preview.style.display = 'block';
                            }
                        }
                    }
                });
            });

            zone.addEventListener('click', () => { if (input) input.click(); });
        });

        // Legacy single file input
        $$('[data-file-input]').forEach(input => {
            input.addEventListener('change', () => {
                const preview = $('[data-file-preview]');
                if (preview) {
                    preview.textContent = input.files.length
                        ? '📎 ' + input.files[0].name
                        : 'Файл не выбран';
                }
            });
        });
    }

    /* ── Toast notifications ── */
    window.showToast = function (message, type = 'info', duration = 4000) {
        let container = $('#toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.style.cssText = `
                position: fixed; bottom: 24px; right: 24px; z-index: 9999;
                display: flex; flex-direction: column; gap: 10px;
                pointer-events: none;
            `;
            document.body.appendChild(container);
        }

        const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
        const colors = {
            success: '#1E7E53',
            error: '#C0392B',
            warning: '#D97706',
            info: '#0f6d7a'
        };

        const toast = document.createElement('div');
        toast.style.cssText = `
            display: flex; align-items: center; gap: 12px;
            padding: 14px 18px; border-radius: 12px;
            background: #0C1E35; color: #fff;
            font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 500;
            box-shadow: 0 8px 32px rgba(12,30,53,.3);
            pointer-events: auto; cursor: pointer;
            transform: translateX(120%); transition: transform .3s cubic-bezier(.4,0,.2,1);
            max-width: 360px; border-left: 4px solid ${colors[type] || colors.info};
        `;
        toast.innerHTML = `<span style="font-size:18px">${icons[type] || icons.info}</span><span>${message}</span>`;
        container.appendChild(toast);

        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                toast.style.transform = 'translateX(0)';
            });
        });

        const dismiss = () => {
            toast.style.transform = 'translateX(120%)';
            setTimeout(() => toast.remove(), 300);
        };

        toast.addEventListener('click', dismiss);
        setTimeout(dismiss, duration);
    };

    /* ── Auto-dismiss alerts ── */
    function initAlerts() {
        $$('.alert[data-auto-dismiss]').forEach(alert => {
            const delay = parseInt(alert.dataset.autoDismiss) || 5000;
            setTimeout(() => {
                alert.style.transition = 'opacity .4s ease';
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 400);
            }, delay);
        });

        // Dismiss button
        $$('[data-dismiss-alert]').forEach(btn => {
            btn.addEventListener('click', () => {
                const alert = btn.closest('.alert');
                if (alert) {
                    alert.style.opacity = '0';
                    setTimeout(() => alert.remove(), 300);
                }
            });
        });
    }

    /* ── Progress bars animate on scroll ── */
    function initProgressBars() {
        $$('.progress-fill[data-width]').forEach(bar => {
            const io = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        bar.style.width = bar.dataset.width + '%';
                        io.unobserve(bar);
                    }
                });
            }, { threshold: 0.5 });
            io.observe(bar);
        });
    }

    /* ── Table search filter ── */
    function initTableFilter() {
        $$('[data-table-filter]').forEach(input => {
            const tableId = input.dataset.tableFilter;
            const table = tableId ? $(`#${tableId}`) : input.closest('.table-wrap, .table-card')?.querySelector('table');
            if (!table) return;

            input.addEventListener('input', () => {
                const q = input.value.toLowerCase().trim();
                $$('tbody tr', table).forEach(row => {
                    const text = row.textContent.toLowerCase();
                    row.style.display = (!q || text.includes(q)) ? '' : 'none';
                });
            });
        });
    }

    /* ── Smooth anchor scroll ── */
    function initSmoothScroll() {
        $$('a[href^="#"]').forEach(link => {
            link.addEventListener('click', (e) => {
                const id = link.getAttribute('href').slice(1);
                const target = id ? document.getElementById(id) : null;
                if (target) {
                    e.preventDefault();
                    const top = target.getBoundingClientRect().top + window.scrollY - 88;
                    window.scrollTo({ top, behavior: 'smooth' });
                }
            });
        });
    }

    /* ── Confirm dialogs ── */
    function initConfirm() {
        $$('[data-confirm]').forEach(el => {
            el.addEventListener('click', (e) => {
                const msg = el.dataset.confirm || 'Вы уверены?';
                if (!confirm(msg)) e.preventDefault();
            });
        });
    }

    /* ── Copy to clipboard ── */
    function initCopy() {
        $$('[data-copy]').forEach(btn => {
            btn.addEventListener('click', () => {
                const text = btn.dataset.copy;
                if (!text) return;
                navigator.clipboard.writeText(text).then(() => {
                    const orig = btn.textContent;
                    btn.textContent = '✓ Скопировано';
                    setTimeout(() => { btn.textContent = orig; }, 2000);
                });
            });
        });
    }

    /* ── Sidebar active state ── */
    function initSidebar() {
        const path = window.location.pathname;
        $$('.sidebar-nav-item').forEach(item => {
            const href = item.getAttribute('href');
            if (href && (href === path || (href !== '/' && path.startsWith(href)))) {
                item.classList.add('active');
            }
        });
    }

    /* ── Stats counters from DOM text ── */
    function initStatCounters() {
        $$('.stat strong, .stat-value').forEach(el => {
            const raw = el.textContent.trim();
            const num = parseFloat(raw.replace(/\s/g, ''));
            if (!isNaN(num) && num > 0) {
                el.dataset.counter = num;
                el.textContent = '0';
                const io = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            animateCounter(el);
                            io.unobserve(el);
                        }
                    });
                }, { threshold: 0.5 });
                io.observe(el);
            }
        });
    }

    /* ── Hero typing animation ── */
    function initTyping() {
        const el = $('[data-typing]');
        if (!el) return;
        const words = (el.dataset.typing || '').split('|').map(w => w.trim()).filter(Boolean);
        if (!words.length) return;

        let wi = 0, ci = 0, deleting = false;
        const cursor = document.createElement('span');
        cursor.style.cssText = 'border-right: 2px solid currentColor; animation: blink 1s step-end infinite;';
        const style = document.createElement('style');
        style.textContent = '@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }';
        document.head.appendChild(style);
        el.appendChild(cursor);

        function tick() {
            const word = words[wi];
            if (deleting) {
                el.childNodes[0] && (el.childNodes[0].textContent = word.slice(0, --ci));
                if (ci === 0) { deleting = false; wi = (wi + 1) % words.length; }
                setTimeout(tick, 60);
            } else {
                if (!el.childNodes[0] || el.childNodes[0].nodeType !== 3) {
                    el.insertBefore(document.createTextNode(''), cursor);
                }
                el.childNodes[0].textContent = word.slice(0, ++ci);
                if (ci === word.length) { deleting = true; setTimeout(tick, 2000); }
                else { setTimeout(tick, 80); }
            }
        }
        setTimeout(tick, 600);
    }

    /* ── Status filter buttons ── */
    function initStatusFilter() {
        $$('[data-status-filter]').forEach(btn => {
            btn.addEventListener('click', () => {
                $$('[data-status-filter]').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const filter = btn.dataset.statusFilter;
                $$('[data-status-row]').forEach(row => {
                    if (filter === 'all' || row.dataset.statusRow === filter) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            });
        });
    }

    /* ── Back to top ── */
    function initBackToTop() {
        const btn = document.createElement('button');
        btn.innerHTML = '↑';
        btn.title = 'Наверх';
        btn.style.cssText = `
            position: fixed; bottom: 24px; left: 24px; z-index: 999;
            width: 44px; height: 44px; border-radius: 12px;
            background: var(--navy); color: #fff; border: none;
            font-size: 18px; cursor: pointer;
            box-shadow: 0 4px 20px rgba(12,30,53,.25);
            opacity: 0; transition: opacity .3s ease, transform .3s ease;
            transform: translateY(8px);
        `;
        document.body.appendChild(btn);

        window.addEventListener('scroll', () => {
            const show = window.scrollY > 400;
            btn.style.opacity = show ? '1' : '0';
            btn.style.transform = show ? 'translateY(0)' : 'translateY(8px)';
        }, { passive: true });

        btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    }

    /* ── Form validation feedback ── */
    function initFormFeedback() {
        $$('form').forEach(form => {
            form.addEventListener('submit', (e) => {
                const btn = form.querySelector('[type="submit"]');
                if (btn && !btn.disabled) {
                    btn.disabled = true;
                    const orig = btn.innerHTML;
                    btn.innerHTML = '⏳ Отправка...';
                    setTimeout(() => {
                        btn.disabled = false;
                        btn.innerHTML = orig;
                    }, 6000);
                }
            });
        });
    }

    /* ── Init all ── */
    document.addEventListener('DOMContentLoaded', () => {
        initHeaderScroll();
        initMobileNav();
        initActiveNav();
        initReveal();
        initCounters();
        initAccordion();
        initFileUpload();
        initAlerts();
        initProgressBars();
        initTableFilter();
        initSmoothScroll();
        initConfirm();
        initCopy();
        initSidebar();
        initStatCounters();
        initTyping();
        initStatusFilter();
        initBackToTop();
        initFormFeedback();
    });

})();
