document.addEventListener('DOMContentLoaded', () => {
    // Seleções que serão usadas em várias partes
    const body = document.body;
    const themeToggle = document.getElementById('theme-toggle');
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('[data-section]');
    const skillBars = document.querySelectorAll('.skill-bar');
    const timelineItems = document.querySelectorAll('.timeline-item');

    // --- Gerenciamento do tema (dark/light) ---
    const prefersDarkTheme = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const savedTheme = localStorage.getItem('theme');

    // Aplica o tema salvo ou o padrão do sistema
    if (savedTheme === 'light') {
        body.classList.add('light-mode');
    } else if (savedTheme === 'dark') {
        body.classList.remove('light-mode');
    } else if (!prefersDarkTheme) {
        body.classList.add('light-mode');
    }

    // Alterna tema ao clicar no botão
    themeToggle?.addEventListener('click', e => {
        e.preventDefault();
        if (body.classList.contains('light-mode')) {
            body.classList.remove('light-mode');
            localStorage.setItem('theme', 'dark');
        } else {
            body.classList.add('light-mode');
            localStorage.setItem('theme', 'light');
        }
    });

    // --- Animação de carregamento ---
    body.classList.add('loaded');

    // --- Intersection Observer para animações de scroll ---
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('in-view');
            }
        });
    }, { threshold: 0.1 });

    // Observa as seções e barras de skill para animações
    sections.forEach(section => observer.observe(section));
    document.querySelectorAll('.skill-bar-fill').forEach(skillBarFill => {
        observer.observe(skillBarFill.parentElement);
    });

    // --- Destacar link da nav conforme scroll ---
    function highlightNavLink() {
        const scrollY = window.scrollY;

        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.id;

            if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.toggle('active', link.getAttribute('data-section') === sectionId);
                });
            }
        });
    }

    window.addEventListener('scroll', highlightNavLink);
    highlightNavLink(); // chama uma vez na carga para ajustar nav

    // --- Inicializa as skill bars com texto e barra preenchida ---
    skillBars.forEach(bar => {
        const skill = bar.getAttribute('data-skill') || '';
        const level = bar.getAttribute('data-level') || '0';

        bar.innerHTML = `
            <div class="flex justify-between mb-1 skill-bar-text">
                <span>${skill}</span>
                <span>${level}%</span>
            </div>
            <div class="h-2 bg-zinc-800 rounded-sm overflow-hidden">
                <div class="h-full bg-white skill-bar-fill" style="--percentage: ${level}%"></div>
            </div>
        `;
    });

    // --- Inicializa índices dos itens da timeline para animação ---
    timelineItems.forEach((item, index) => {
        item.style.setProperty('--item-index', index + 1);
    });
});
