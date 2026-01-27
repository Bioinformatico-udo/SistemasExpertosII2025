import { ReactNode } from 'react';

interface FlipCardProps {
  icon: ReactNode;
  title: string;
  items: string[];
  color: string;
  imageUrl: string;
}

export function FlipCard({ icon, title, items, color, imageUrl }: FlipCardProps) {
  return (
    <div className="flip-card h-80">
      <div className="flip-card-inner">
        {/* Frente de la tarjeta */}
        <div className={`flip-card-front bg-gradient-to-br ${color} p-6 rounded-2xl border-2 border-opacity-30 relative overflow-hidden`}>
          {/* Imagen de fondo */}
          <div 
            className="absolute inset-0 bg-cover bg-center opacity-30"
            style={{ backgroundImage: `url(${imageUrl})` }}
          />
          
          {/* Overlay de color */}
          <div className="absolute inset-0 bg-gradient-to-br from-white/40 to-transparent" />
          
          {/* Contenido */}
          <div className="relative z-10 h-full flex flex-col items-center justify-center text-center">
            <div className="mb-4 drop-shadow-lg">
              {icon}
            </div>
            <h4 className="text-2xl drop-shadow-md">
              {title}
            </h4>
            <p className="text-sm mt-4 opacity-70">Pasa el cursor para ver más</p>
          </div>
        </div>

        {/* Reverso de la tarjeta */}
        <div className={`flip-card-back bg-gradient-to-br ${color} p-6 rounded-2xl border-2 border-opacity-30`}>
          <h4 className="text-xl mb-4 text-center">
            {title}
          </h4>
          <ul className="space-y-2 text-gray-700">
            {items.map((item, index) => (
              <li key={index} className="flex items-start gap-2">
                <span className="text-current flex-shrink-0">•</span>
                <span className="text-sm">{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
