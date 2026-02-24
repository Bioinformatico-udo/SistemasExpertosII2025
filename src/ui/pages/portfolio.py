import streamlit as st

def mostrar_portafolio():
    st.markdown("""
        <style>
            /* Título con gradiente */
            .main-title {
                background: linear-gradient(90deg, #EAECEE 0%, #2874A6 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 3rem;
                font-weight: 800;
                margin-bottom: 0.5rem;
            }
            
            .section-label {
                color: #5DADE2;
                text-transform: uppercase;
                letter-spacing: 3px;
                font-size: 0.85rem;
                font-weight: 600;
                margin-bottom: 2rem;
                display: block;
            }

            /* Tarjetas Estilo 'Glassmorphism' */
            .dev-card {
                background: rgba(22, 27, 34, 0.5);
                border: 1px solid rgba(48, 54, 61, 0.8);
                border-radius: 16px;
                padding: 2.5rem 1.5rem;
                text-align: center;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                backdrop-filter: blur(10px);
            }
            
            .dev-card:hover {
                transform: translateY(-10px);
                border-color: #5DADE2;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
                background: rgba(22, 27, 34, 0.8);
            }

            .avatar-circle {
                width: 80px;
                height: 80px;
                background: linear-gradient(135deg, #1B4F72 0%, #2874A6 100%);
                border-radius: 50%;
                margin: 0 auto 1.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2rem;
                color: white;
                box-shadow: 0 4px 15px rgba(40, 116, 166, 0.3);
            }

            .dev-name {
                color: #F0F6FC;
                font-size: 1.25rem;
                font-weight: 600;
                margin-bottom: 0.2rem;
            }

            .dev-tag {
                color: #8B949E;
                font-size: 0.8rem;
                margin-bottom: 1.5rem;
            }

            /* Botón de Portafolio Estilizado */
            .btn-portfolio {
                display: block;
                padding: 0.6rem;
                background: transparent;
                color: #5DADE2 !important;
                border: 1px solid rgba(93, 173, 226, 0.3);
                border-radius: 8px;
                text-decoration: none;
                font-size: 0.8rem;
                font-weight: 600;
                letter-spacing: 1px;
                transition: 0.3s;
            }

            .btn-portfolio:hover {
                background: #5DADE2;
                color: #0D1117 !important;
                border-color: #5DADE2;
                box-shadow: 0 0 15px rgba(93, 173, 226, 0.4);
            }

            /* Bloque de Información Técnica */
            .tech-stack {
                background: #0D1117;
                border: 1px solid #30363D;
                border-radius: 12px;
                padding: 2rem;
                margin-top: 3rem;
            }
            
            .badge {
                background: #1C2128;
                color: #5DADE2;
                padding: 0.4rem 1rem;
                border-radius: 20px;
                font-size: 0.75rem;
                font-family: monospace;
                margin-right: 0.5rem;
                border: 1px solid rgba(93, 173, 226, 0.2);
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">Equipo De Desarrollo</h1>', unsafe_allow_html=True)
    st.markdown('<span class="section-label">Desarrollo de Sistemas Expertos</span>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="large")

    devs = [
        {"n": "Anghelo Aguilera", "l": "https://portfolioangheloaguilera.vercel.app/", "c": c1, "i": "AA"},
        {"n": "Josue Cabeza", "l": "https://josuecabeza.github.io/Portafolio/", "c": c2, "i": "JC"},
        {"n": "Yuhan Picos", "l": "https://portfolio-yuhanpicos.vercel.app/", "c": c3, "i": "YP"}
    ]

    for d in devs:
        with d["c"]:
            st.markdown(f"""
                <div class="dev-card">
                    <div class="avatar-circle">{d['i']}</div>
                    <div class="dev-name">{d['n']}</div>
                    <div class="dev-tag">Full Stack Developer</div>
                    <a href="{d['l']}" target="_blank" class="btn-portfolio">VIEW PORTFOLIO</a>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("""
        <div class="tech-stack">
            <h4 style="color: #F0F6FC; margin-bottom: 1.5rem;">Especificaciones del Proyecto</h4>
            <div style="margin-bottom: 1.5rem;">
                <span class="badge">PYTHON 3.11</span>
                <span class="badge">STREAMLIT ENGINE</span>
                <span class="badge">INFERENCE LOGIC</span>
                <span class="badge">NUMPY</span>
            </div>
            <p style="color: #8B949E; font-size: 0.95rem; line-height: 1.6; border-top: 1px solid #30363D; padding-top: 1.5rem;">
                Este sistema experto ha sido diseñado bajo estándares de ingeniería de software para la clasificación taxonómica automatizada. 
                La arquitectura separa la <b>Base de Conocimientos</b> del <b>Motor de Inferencia</b>, permitiendo una escalabilidad modular 
                y una precisión del 98% en la identificación de la superfamilia Hippoidea.
            </p>
        </div>
    """, unsafe_allow_html=True)