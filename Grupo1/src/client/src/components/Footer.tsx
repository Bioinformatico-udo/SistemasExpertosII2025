import { Github, Linkedin, Mail, ExternalLink } from 'lucide-react';

export function Footer() {
  const developers = [
    {
      name: "Andrés Alfonzo",
      role: "Desarrollador",
      portfolio: "https://vacaroja.github.io/",
      github: "https://github.com/Vacaroja",
      linkedin: "https://www.linkedin.com/in/andrés-alfonzo-4342351bb?utm_source=share_via&utm_content=profile&utm_medium=member_android",
      email: "vr.alfonzo1@gmail.com",
      avatar: "AA"
    },
    {
      name: "Alexandra Quijada",
      role: "Desarrollador",
      portfolio: "https://carlosramirez.dev",
      github: "https://github.com/carlosramirez",
      linkedin: "https://linkedin.com/in/carlosramirez",
      email: "alexandraquijada@gmail.com",
      avatar: "AQ"
    },
    {
      name: "Gilberto Velasquez",
      role: "Desarrolladores",
      portfolio: "https://gvelasquez03.github.io/",
      github: "https://gvelasquez03.github.io/",
      linkedin: "https://linkedin.com/in/anamartinez",
      email: "gilberto123rafael@gmail.com",
      avatar: "GV"
    }
  ];

  return (
    <footer className="relative mt-16 bg-gradient-to-br from-cyan-600 via-teal-600 to-blue-600 text-white overflow-hidden">
      {/* Patrón de ondas decorativo */}
      <div className="absolute top-0 left-0 w-full h-24 -translate-y-full">
        <svg 
          viewBox="0 0 1200 120" 
          preserveAspectRatio="none" 
          className="w-full h-full"
        >
          <path 
            d="M0,0 Q300,80 600,40 T1200,0 L1200,120 L0,120 Z" 
            fill="url(#gradient)" 
          />
          <defs>
            <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" style={{ stopColor: '#0891b2', stopOpacity: 1 }} />
              <stop offset="50%" style={{ stopColor: '#0d9488', stopOpacity: 1 }} />
              <stop offset="100%" style={{ stopColor: '#2563eb', stopOpacity: 1 }} />
            </linearGradient>
          </defs>
        </svg>
      </div>

      {/* Burbujas decorativas */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-20">
        <div className="absolute w-32 h-32 bg-white/30 rounded-full blur-2xl" style={{ top: '20%', left: '10%' }} />
        <div className="absolute w-24 h-24 bg-white/20 rounded-full blur-xl" style={{ bottom: '30%', right: '15%' }} />
        <div className="absolute w-40 h-40 bg-white/25 rounded-full blur-3xl" style={{ top: '50%', right: '30%' }} />
      </div>

      <div className="container mx-auto px-4 py-12 relative z-10">
        {/* Título */}
        <div className="text-center mb-12">
          <h3 className="text-3xl mb-2">Equipo de Desarrollo</h3>
          <p className="text-cyan-100 text-lg">
            Mejorando continuamente esta plataforma educativa
          </p>
        </div>

        {/* Tarjetas de desarrolladores */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          {developers.map((dev, index) => (
            <div 
              key={index}
              className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 hover:bg-white/20 transition-all duration-300 hover:scale-105 hover:shadow-2xl group"
            >
              {/* Avatar */}
              <div className="flex justify-center mb-4">
                <div className="w-20 h-20 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-full flex items-center justify-center shadow-lg group-hover:shadow-cyan-300/50 transition-shadow duration-300">
                  <span className="text-2xl text-white">{dev.avatar}</span>
                </div>
              </div>

              {/* Información */}
              <div className="text-center mb-4">
                <h4 className="text-xl mb-1">{dev.name}</h4>
                <p className="text-cyan-100 text-sm">{dev.role}</p>
              </div>

              {/* Enlace al portafolio */}
              <a 
                href={dev.portfolio}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-center gap-2 bg-white/20 hover:bg-white/30 rounded-lg px-4 py-2 mb-4 transition-colors duration-200 group/link"
              >
                <ExternalLink className="w-4 h-4 group-hover/link:scale-110 transition-transform" />
                <span className="text-sm">Ver Portafolio</span>
              </a>

              {/* Iconos sociales */}
              <div className="flex justify-center gap-3">
                <a 
                  href={dev.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-10 h-10 bg-white/20 hover:bg-white/30 rounded-full flex items-center justify-center transition-all duration-200 hover:scale-110"
                  aria-label="GitHub"
                >
                  <Github className="w-5 h-5" />
                </a>
                <a 
                  href={dev.linkedin}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-10 h-10 bg-white/20 hover:bg-white/30 rounded-full flex items-center justify-center transition-all duration-200 hover:scale-110"
                  aria-label="LinkedIn"
                >
                  <Linkedin className="w-5 h-5" />
                </a>
                <a 
                  href={`mailto:${dev.email}`}
                  className="w-10 h-10 bg-white/20 hover:bg-white/30 rounded-full flex items-center justify-center transition-all duration-200 hover:scale-110"
                  aria-label="Email"
                >
                  <Mail className="w-5 h-5" />
                </a>
              </div>
            </div>
          ))}
        </div>

        {/* Copyright */}
        <div className="text-center pt-8 border-t border-white/20">
          <p className="text-cyan-100 text-sm">
            © {new Date().getFullYear()} Porcelánidos Educación. Una página educativa sobre la familia Porcellanidae.
          </p>
          <p className="text-cyan-200 text-xs mt-2">
            Desarrollado con 💙 para promover el conocimiento de la vida marina
          </p>
        </div>
      </div>
    </footer>
  );
}
