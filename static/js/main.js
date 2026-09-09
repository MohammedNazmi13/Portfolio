document.addEventListener('DOMContentLoaded', () => {
    // 1. 3-Second Loading Screen with Dynamic Admin Name Typing & Animated Dots
    const loader = document.getElementById('loader');
    const loaderTextSpan = document.getElementById('loader-status-text');
    const loaderDotsSpan = document.getElementById('loader-dots');
    
    const adminName = (loaderTextSpan && loaderTextSpan.getAttribute('data-name')) || 'Mohammed Nazmi';
    const targetLoaderPhrase = `Initializing ${adminName}’s portfolio`;
    
    let dotCount = 0;
    let dotInterval = null;
    let typingStarted = false;

    // Type character-by-character for loader phrase
    if (loaderTextSpan) {
        loaderTextSpan.innerText = '';
        if (loaderDotsSpan) loaderDotsSpan.innerText = '';
        let i = 0;
        const loaderTypingTimer = setInterval(() => {
            if (i < targetLoaderPhrase.length) {
                loaderTextSpan.innerText += targetLoaderPhrase.charAt(i);
                i++;
            } else {
                clearInterval(loaderTypingTimer);
                // Cycle 0 -> 1 -> 2 -> 3 -> 0 dots
                dotInterval = setInterval(() => {
                    if (!loaderDotsSpan) return;
                    dotCount = (dotCount + 1) % 4;
                    if (dotCount === 0) loaderDotsSpan.innerText = '';
                    else if (dotCount === 1) loaderDotsSpan.innerText = '.';
                    else if (dotCount === 2) loaderDotsSpan.innerText = '..';
                    else if (dotCount === 3) loaderDotsSpan.innerText = '...';
                }, 220);
            }
        }, 18);
    }

    const dismissLoader = () => {
        if (dotInterval) clearInterval(dotInterval);
        if (loader && !loader.classList.contains('warp-exit')) {
            loader.classList.add('warp-exit');
            setTimeout(() => {
                loader.style.display = 'none';
                if (!typingStarted) {
                    typingStarted = true;
                    initSequentialHeroTyping();
                }
            }, 600);
        } else if (!typingStarted) {
            typingStarted = true;
            initSequentialHeroTyping();
        }
    };

    // Show loader for exactly 3 seconds (3000ms)
    setTimeout(dismissLoader, 3000);

    // 2. Background Particle System
    const canvas = document.getElementById('bg-canvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let particles = [];
        let w, h;

        const resize = () => {
            w = canvas.width = window.innerWidth;
            h = canvas.height = window.innerHeight;
        };

        window.addEventListener('resize', resize);
        resize();

        class Particle {
            constructor() {
                this.x = Math.random() * w;
                this.y = Math.random() * h;
                this.size = Math.random() * 2 + 0.5;
                this.speedX = Math.random() * 1 - 0.5;
                this.speedY = Math.random() * 1 - 0.5;
                this.color = Math.random() > 0.5 ? '#10b981' : '#3b82f6';
                this.opacity = Math.random() * 0.5 + 0.1;
            }

            update() {
                this.x += this.speedX;
                this.y += this.speedY;

                if (this.x > w) this.x = 0;
                if (this.x < 0) this.x = w;
                if (this.y > h) this.y = 0;
                if (this.y < 0) this.y = h;
            }

            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.globalAlpha = this.opacity;
                ctx.fill();
            }
        }

        const initParticles = () => {
            particles = [];
            for (let i = 0; i < 80; i++) {
                particles.push(new Particle());
            }
        };

        const animate = () => {
            ctx.clearRect(0, 0, w, h);
            particles.forEach(p => {
                p.update();
                p.draw();
            });
            requestAnimationFrame(animate);
        };

        initParticles();
        animate();
    }

    // 3. Ultra-Fast Magnetic Hover Effect Helper
    function bindMagneticEffect(elements) {
        elements.forEach(el => {
            let magFrame = null;
            el.addEventListener('mousemove', (e) => {
                if (magFrame) cancelAnimationFrame(magFrame);
                magFrame = requestAnimationFrame(() => {
                    const rect = el.getBoundingClientRect();
                    const x = e.clientX - rect.left - rect.width / 2;
                    const y = e.clientY - rect.top - rect.height / 2;
                    el.style.transform = `translate3d(${x * 0.25}px, ${y * 0.25}px, 0) scale(1.04)`;
                });
            }, { passive: true });

            el.addEventListener('mouseleave', () => {
                if (magFrame) cancelAnimationFrame(magFrame);
                el.style.transform = '';
            });
        });
    }

    const magneticElements = document.querySelectorAll('.nav-link-mag, .btn, .skill-card, .info-block-premium, .about-profile-card');
    bindMagneticEffect(magneticElements);

    // 4. Back to Top & Scroll Progress with Scroll Hover Pointer Detection
    if (history.scrollRestoration) {
        history.scrollRestoration = 'manual';
    }
    window.scrollTo(0, 0);

    const progressBar = document.querySelector('.scroll-progress');
    const backToTop = document.getElementById('back-to-top');
    let scrollTicking = false;

    window.addEventListener('scroll', () => {
        if (!scrollTicking) {
            requestAnimationFrame(() => {
                const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
                const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                const scrolled = (winScroll / height) * 100;
                if (progressBar) progressBar.style.width = scrolled + "%";
                
                if (winScroll > 400) {
                    backToTop?.classList.add('visible');
                } else {
                    backToTop?.classList.remove('visible');
                }

                // Update element mouse coordinates on scroll for stationary pointer hover reaction
                if (mouseX && mouseY) {
                    const elemUnderPointer = document.elementFromPoint(mouseX, mouseY);
                    if (elemUnderPointer) {
                        const card = elemUnderPointer.closest('.info-block-premium, .skill-card-futuristic, .about-profile-card, .education-item, .experience-card-premium, .certificate-card, .project-card-cert');
                        if (card) {
                            const rect = card.getBoundingClientRect();
                            card.style.setProperty('--mouse-x', `${mouseX - rect.left}px`);
                            card.style.setProperty('--mouse-y', `${mouseY - rect.top}px`);
                        }
                    }
                }

                scrollTicking = false;
            });
            scrollTicking = true;
        }
    }, { passive: true });

    backToTop?.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // 4b. Ultra-Responsive Hardware-Accelerated Custom Cursor
    const cursor = document.getElementById('custom-cursor');
    let mouseX = 0, mouseY = 0;
    let cursorX = 0, cursorY = 0;
    let isMoving = false;

    const hoverTargetSelector = 'a, button, .btn, .skill-card, .project-card, .certificate-card, .education-item, .timeline-item, .project-card-cert, .nav-link-mag, .view-project-details, .view-cert-details, .close-modal, .skill-card-futuristic, .copy-click, textarea';

    window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        
        if (cursor && cursor.style.display !== 'block') {
            cursor.style.display = 'block';
            cursor.style.opacity = '1';
        }

        if (!isMoving) {
            isMoving = true;
            requestAnimationFrame(updateCursor);
        }
    }, { passive: true });

    function updateCursor() {
        cursorX += (mouseX - cursorX) * 0.75;
        cursorY += (mouseY - cursorY) * 0.75;
        
        if (cursor) {
            cursor.style.transform = `translate3d(${cursorX}px, ${cursorY}px, 0)`;
        }
        
        if (Math.abs(mouseX - cursorX) > 0.05 || Math.abs(mouseY - cursorY) > 0.05) {
            requestAnimationFrame(updateCursor);
        } else {
            isMoving = false;
        }
    }

    document.addEventListener('mouseleave', () => {
        if (cursor) cursor.style.opacity = '0';
    });

    // Smooth hover effect delegation without layout thrashing
    document.addEventListener('mouseover', (e) => {
        const target = e.target.closest(hoverTargetSelector);
        if (target) {
            document.body.classList.add('cursor-hover');
        }
    }, { passive: true });

    document.addEventListener('mouseout', (e) => {
        const target = e.target.closest(hoverTargetSelector);
        if (target) {
            document.body.classList.remove('cursor-hover');
        }
    }, { passive: true });

    // Click to Copy Logic
    const copyElements = document.querySelectorAll('.copy-click');
    copyElements.forEach(el => {
        el.addEventListener('click', () => {
            const textToCopy = el.getAttribute('data-copy');
            const tooltip = el.querySelector('.copy-tooltip');
            
            navigator.clipboard.writeText(textToCopy).then(() => {
                if (tooltip) {
                    const originalText = tooltip.innerText;
                    tooltip.innerText = 'Copied!';
                    tooltip.classList.add('copied');
                    
                    setTimeout(() => {
                        tooltip.innerText = originalText;
                        tooltip.classList.remove('copied');
                    }, 2000);
                }
            }).catch(err => {
                console.error('Failed to copy: ', err);
            });
        });
    });

    // 5. Intersection Observer for Smooth Reveal Animations
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.05, rootMargin: "0px 0px -20px 0px" });

    const initReveals = () => {
        const reveals = document.querySelectorAll('.reveal');
        reveals.forEach(el => revealObserver.observe(el));
    };
    initReveals();

    // 6. Navbar Effect
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }, { passive: true });

    // 7. Sequential Hero Typing Effect (Initial State Empty -> 1st -> 2nd -> 3rd)
    async function typeCharacterByCharacter(elementId, text, charDelay = 35) {
        const el = document.getElementById(elementId);
        if (!el) return;
        el.innerText = '';
        for (let i = 0; i < text.length; i++) {
            el.innerText += text.charAt(i);
            await new Promise(resolve => setTimeout(resolve, charDelay));
        }
        el.classList.add('typing-done');
    }

    async function initSequentialHeroTyping() {
        try {
            const nameEl = document.getElementById('hero-name');
            const titleEl = document.getElementById('hero-title');
            const taglineEl = document.getElementById('hero-tagline');

            const nameText = nameEl ? (nameEl.getAttribute('data-text') || 'Mohammed Nazmi A') : '';
            const titleText = titleEl ? (titleEl.getAttribute('data-text') || 'Full Stack Developer (Backend & Frontend) | SEO | Python | MySQL | Data Analytics with NumPy & Pandas | Security & Deployment') : '';
            const taglineText = taglineEl ? (taglineEl.getAttribute('data-text') || 'Building scalable full-stack applications with optimized SEO, robust backend systems, and data-driven insights using MySQL, NumPy, and Pandas.') : '';

            // Ensure elements are empty before typing starts
            if (nameEl) nameEl.innerText = '';
            if (titleEl) titleEl.innerText = '';
            if (taglineEl) taglineEl.innerText = '';

            // 1st: Hi, I'm Mohammed Nazmi A
            if (nameEl) {
                await typeCharacterByCharacter('hero-name', nameText, 45);
                await new Promise(r => setTimeout(r, 200));
            }

            // 2nd: Full Stack Developer (Backend & Frontend)...
            if (titleEl) {
                await typeCharacterByCharacter('hero-title', titleText, 20);
                await new Promise(r => setTimeout(r, 200));
            }

            // 3rd: Building scalable full-stack applications...
            if (taglineEl) {
                await typeCharacterByCharacter('hero-tagline', taglineText, 12);
            }
        } catch (e) {
            console.error('Sequential hero typing error:', e);
        }
    }

    // 8. Throttled Premium Card Interactions (Zero Lag during scroll)
    const aboutSection = document.querySelector('.about-section-premium');
    if (aboutSection) {
        aboutSection.addEventListener('mousemove', (e) => {
            const rect = aboutSection.getBoundingClientRect();
            aboutSection.style.setProperty('--mouse-x', `${e.clientX - rect.left}px`);
            aboutSection.style.setProperty('--mouse-y', `${e.clientY - rect.top}px`);
        }, { passive: true });
    }

    const premiumCards = document.querySelectorAll('.skill-card-futuristic, .about-profile-card, .info-block-premium, .looking-card, .education-item, .experience-card-premium');
    
    premiumCards.forEach(card => {
        let cardFrame = null;
        card.addEventListener('mousemove', (e) => {
            if (cardFrame) cancelAnimationFrame(cardFrame);
            cardFrame = requestAnimationFrame(() => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                card.style.setProperty('--mouse-x', `${x}px`);
                card.style.setProperty('--mouse-y', `${y}px`);
                
                if (card.classList.contains('skill-card-futuristic') || card.classList.contains('about-profile-card') || card.classList.contains('info-block-premium') || card.classList.contains('education-item')) {
                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;
                    const rotateX = (centerY - y) / 25; 
                    const rotateY = (x - centerX) / 25;
                    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
                }
            });
        }, { passive: true });

        card.addEventListener('mouseleave', () => {
            if (cardFrame) cancelAnimationFrame(cardFrame);
            card.style.transform = '';
        });
    });

    // 6b. Stats Count-Up Animation
    const countUpElements = document.querySelectorAll('.count-up');
    const countUpObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const targetValue = el.getAttribute('data-value');
                const numericPart = parseFloat(targetValue);
                const suffix = targetValue.replace(/[0-9.]/g, '');
                
                if (!isNaN(numericPart)) {
                    let start = 0;
                    const duration = 2000;
                    const startTime = performance.now();
                    
                    function updateCount(currentTime) {
                        const elapsed = currentTime - startTime;
                        const progress = Math.min(elapsed / duration, 1);
                        const easeOutQuad = t => t * (2 - t);
                        const current = Math.floor(easeOutQuad(progress) * numericPart);
                        
                        el.innerText = current + suffix;
                        
                        if (progress < 1) {
                            requestAnimationFrame(updateCount);
                        } else {
                            el.innerText = targetValue;
                        }
                    }
                    requestAnimationFrame(updateCount);
                }
                countUpObserver.unobserve(el);
            }
        });
    }, { threshold: 0.5 });

    countUpElements.forEach(el => countUpObserver.observe(el));

    // 11. Infinite Scroll experience cards are handled by CSS animations
    
    // 11b. Certificate Filtering (Fixing potential conflict with new content)
    const filterBtns = document.querySelectorAll('.filter-btn');
    const certCards = document.querySelectorAll('.certificate-card');
    
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const filter = btn.getAttribute('data-filter');
            certCards.forEach(card => {
                const category = card.getAttribute('data-category');
                if (filter === 'all' || category === filter) {
                    card.style.display = 'flex';
                    card.classList.add('active'); // Trigger reveal if needed
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // 8. Mobile Navigation Toggle
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    if (hamburger) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const icon = hamburger.querySelector('i');
            icon.classList.toggle('fa-bars');
            icon.classList.toggle('fa-times');
        });

        // Close mobile menu when a link is clicked
        const navItems = navLinks.querySelectorAll('a');
        navItems.forEach(item => {
            item.addEventListener('click', () => {
                navLinks.classList.remove('active');
                const icon = hamburger.querySelector('i');
                icon.classList.add('fa-bars');
                icon.classList.remove('fa-times');
            });
        });
    }

    // 9. Dynamic Projects Fetch
    const projectsContainer = document.getElementById('projects-container');
    if (projectsContainer) {
        fetchProjects();
    }

    async function fetchProjects() {
        try {
            const response = await fetch('/api/projects');
            const projects = await response.json();
            const spinner = document.getElementById('loading-spinner');
            if (spinner) spinner.style.display = 'none';

            projects.forEach((project, index) => {
                const staggerClass = `stagger-${(index % 5) + 1}`;
                
                // GitHub and Demo links for top-right
                let topLinksHtml = '<div class="project-top-links">';
                if (project.github_link) {
                    topLinksHtml += `<a href="${project.github_link}" target="_blank" title="GitHub" class="top-link-icon github-icon"><i class="fab fa-github"></i></a>`;
                }
                if (project.demo_link) {
                    topLinksHtml += `<a href="${project.demo_link}" target="_blank" title="Live Demo" class="top-link-icon demo-icon"><i class="fas fa-external-link-alt"></i></a>`;
                }
                topLinksHtml += '</div>';

                const isPdf = project.image_url && project.image_url.toLowerCase().endsWith('.pdf');
                const imageHtml = project.image_url
                    ? (isPdf 
                        ? `<img src="${project.image_url}.png" alt="${project.title}" class="project-card-img" onerror="this.outerHTML='<div class=\'project-img-placeholder pdf-bg\'><i class=\'fas fa-file-pdf\'></i><span>PDF Preview Unavailable</span></div>'">`
                        : `<img src="${project.image_url}" alt="${project.title}" class="project-card-img">`)
                    : `<div class="project-img-placeholder"><i class="far fa-folder-open"></i></div>`;

                const projectHtml = `
                    <div class="project-card-cert reveal reveal-zoom ${staggerClass}">
                        ${topLinksHtml}
                        <div class="project-card-image">
                            ${imageHtml}
                        </div>
                        <div class="project-card-body">
                            <h3 class="project-card-title">${project.title}</h3>
                            <p class="project-card-desc">${project.description}</p>
                            <button class="btn btn-primary btn-full view-project-details"
                                    data-title="${project.title}"
                                    data-tech="${project.tech_stack}"
                                    data-full-desc="${(project.full_description || project.description).replace(/"/g, '&quot;')}"
                                    data-github="${project.github_link || ''}"
                                    data-demo="${project.demo_link || ''}"
                                    data-image="${project.image_url || ''}">
                                View Details
                            </button>
                        </div>
                    </div>
                `;
                projectsContainer.insertAdjacentHTML('beforeend', projectHtml);
            });
            // Re-observe new cards for reveal animation and bind magnetic effects
            setTimeout(() => {
                const newCards = projectsContainer.querySelectorAll('.reveal:not(.active)');
                newCards.forEach(el => revealObserver.observe(el));

                const projectButtons = projectsContainer.querySelectorAll('.view-project-details, .top-link-icon');
                bindMagneticEffect(projectButtons);
            }, 100);
        } catch (e) { console.error(e); }
    }

    // Modal Logic
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('view-project-details')) {
            const d = e.target.dataset;
            // Removed image display from modal as per request
            const modalImg = document.getElementById('modal-project-image');
            const modalGrid = document.querySelector('#project-modal .modal-grid');
            if (modalImg && modalImg.parentElement) {
                modalImg.parentElement.style.display = 'none';
            }
            if (modalGrid) {
                modalGrid.classList.add('no-image');
            }
            
            document.getElementById('modal-project-title').innerText = d.title;
            // Full description from left to right with small space
            document.getElementById('modal-project-desc').innerHTML = `<div class="full-description-container">${d.fullDesc.replace(/\n/g, '<br>')}</div>`;
            document.getElementById('modal-project-tech').innerHTML = d.tech.split(',').map(t => `<span class="tech-tag">${t.trim()}</span>`).join('');
            
            const links = document.getElementById('modal-project-links');
            if (links) {
                links.innerHTML = '';
                if (d.github || d.demo) {
                    if (links.parentElement) links.parentElement.style.display = 'block';
                    if (d.github) {
                        links.innerHTML += `<a href="${d.github}" target="_blank" class="btn btn-primary btn-small"><i class="fab fa-github"></i> Github</a>`;
                    }
                    if (d.demo) {
                        links.innerHTML += `<a href="${d.demo}" target="_blank" class="btn btn-outline btn-small"><i class="fas fa-external-link-alt"></i> Demo</a>`;
                    }
                } else {
                    if (links.parentElement) links.parentElement.style.display = 'none';
                }
            }
            
            document.getElementById('project-modal').style.display = 'block';
            document.body.style.overflow = 'hidden';
        }
        if (e.target.classList.contains('view-cert-details')) {
            const d = e.target.dataset;
            const modal = document.getElementById('cert-modal');
            const img = document.getElementById('modal-cert-image');
            const modalGrid = modal.querySelector('.modal-grid');
            
            const isPdf = d.image.toLowerCase().endsWith('.pdf');
            if (isPdf) {
                img.style.display = 'none';
                if (img.parentElement) img.parentElement.style.display = 'none';
                if (modalGrid) modalGrid.classList.add('no-image');
            } else {
                img.style.display = 'block';
                img.src = d.image;
                if (img.parentElement) img.parentElement.style.display = 'flex';
                if (modalGrid) modalGrid.classList.remove('no-image');
            }

            document.getElementById('modal-cert-title').innerText = d.title;
            // Show only year in the issuer field as requested
            document.getElementById('modal-cert-issuer').innerText = d.year;
            document.getElementById('modal-cert-desc').innerText = d.fullDesc;
            document.getElementById('modal-cert-skills').innerHTML = d.skills ? d.skills.split(',').map(s => `<span>${s.trim()}</span>`).join('') : '';
            
            const fullViewBtn = document.getElementById('modal-cert-full-view');
            if (fullViewBtn) {
                // Generate a pretty slug from the title
                const slug = d.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
                fullViewBtn.href = `/certificate/MohammedNazmi-Portfolio/${slug}/${d.dbId}`;
            }

            const footer = document.getElementById('modal-cert-footer');
            if (footer) footer.style.display = 'none';

            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        }
        if (e.target.classList.contains('close-modal') || e.target.classList.contains('modal')) {
            document.querySelectorAll('.modal').forEach(m => m.style.display = 'none');
            document.body.style.overflow = 'auto';
        }
    });

    // 10. Contact Form
    const form = document.getElementById('contact-form');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = document.getElementById('submit-btn');
            const status = document.getElementById('form-status');
            const data = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                message: document.getElementById('message').value
            };
            btn.innerHTML = 'Sending...';
            btn.disabled = true;
            try {
                const res = await fetch('/contact', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (res.ok) {
                    status.innerHTML = 'Message Sent!';
                    form.reset();
                }
            } catch (e) { status.innerHTML = 'Error sending message.'; }
            btn.innerHTML = 'Send Message';
            btn.disabled = false;
        });
    }
});
