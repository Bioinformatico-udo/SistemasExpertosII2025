import { Shell } from 'lucide-react';
const porcelainCrabBg = '/images/porcelainCrabBg.png'; // place the image in your public/images folder (or adjust path)

export function Header() {
  return (
    <header className="relative bg-gradient-to-r from-teal-500 via-cyan-400 to-blue-400 text-white py-12 shadow-xl overflow-hidden">
      {/* Imagen de fondo con opacidad */}
      <div
        className="absolute inset-0 bg-cover bg-center opacity-15"
        style={{
          backgroundImage: `url(${porcelainCrabBg})`,
        }}
      />

      {/* Overlay con gradiente caribeño */}
      <div className="absolute inset-0 bg-gradient-to-b from-teal-600/40 via-cyan-500/40 to-blue-500/40" />

      {/* Contenido del header */}
      <div className="container mx-auto px-4 text-center relative z-10">
        <div className="flex items-center justify-center gap-4 mb-4">
          <Shell className="w-16 h-16 drop-shadow-lg animate-bounce" style={{ animationDuration: '3s' }} />
          <h1 className="text-6xl drop-shadow-lg">Porcelánidos</h1>
          <Shell className="w-16 h-16 drop-shadow-lg animate-bounce" style={{ animationDuration: '3s', animationDelay: '1.5s' }} />
        </div>
        <p className="text-2xl text-cyan-50 mb-2 drop-shadow-md">
          Familia Porcellanidae
        </p>
        <p className="text-xl text-cyan-100 drop-shadow-md">
          Crustáceos decápodos que se asemejan a los cangrejos verdaderos
        </p>
      </div>
    </header>
  );
}