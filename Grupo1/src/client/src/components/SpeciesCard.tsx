import { Trash2, Calendar, Ruler, MapPin, CheckCircle2 } from 'lucide-react';
import { Button } from './ui/button';
import type { Species } from '../types/species';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface SpeciesCardProps {
  species: Species;
  onDelete: (id: string) => void;
}

export function SpeciesCard({ species, onDelete }: SpeciesCardProps) {
  const handleDelete = () => {
    if (window.confirm(`¿Estás seguro de eliminar "${species.nombre}"?`)) {
      onDelete(species.id || '');
    }
  };

  const getDatoTecnico = (index: number, opcionA: string, opcionB: string) => {
    const array = species.preguntas_identificacion;
    if (!array || array.length === 0) return 'N/A';
    return array[index] === 1 ? opcionA : opcionB;
  };

  return (
    <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden border-2 border-cyan-200 hover:border-teal-400 group flex flex-col h-[550px]">
      
      {/* 1. SECCIÓN DE IMAGEN: Altura fija y estricta */}
      <div className="relative h-48 w-full bg-gradient-to-br from-cyan-100 to-teal-100 flex-shrink-0 overflow-hidden">
        {species.imagen ? (
          <ImageWithFallback
            src={species.imagen}
            alt={species.nombre}
            className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-teal-300">
            <div className="text-center">
              <div className="text-5xl mb-2">🦀</div>
              <p className="text-[10px] font-bold uppercase tracking-widest text-teal-500">Sin Imagen</p>
            </div>
          </div>
        )}
        
        <Button
          variant="destructive"
          size="icon"
          onClick={handleDelete}
          className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300 shadow-lg z-10"
        >
          <Trash2 className="w-4 h-4" />
        </Button>
      </div>

      {/* 2. CUERPO DE LA CARD: Espaciado interno controlado */}
      <div className="p-5 flex flex-col flex-grow">
        
        {/* Nombres: Altura mínima para que siempre ocupen el mismo espacio */}
        <div className="min-h-[60px] mb-2">
          <h3 className="text-lg font-bold text-teal-800 leading-tight line-clamp-2">
            {species.nombre}
          </h3>
          <p className="text-xs italic text-cyan-600 font-semibold truncate">
            {species.nombreCientifico}
          </p>
        </div>

        {/* FICHA TÉCNICA: Cuadrícula fija para que no se mueva el diseño */}
        <div className="mb-4 p-3 bg-cyan-50/30 rounded-lg border border-cyan-100 grid grid-cols-2 gap-y-2 gap-x-1 min-h-[85px] items-center">
          {[
            { idx: 0, a: 'Liso', b: 'Rugoso' },
            { idx: 2, a: 'Ant. Lisa', b: 'Ant. Aserr.' },
            { idx: 10, a: '7 Tels.', b: '5 Tels.' },
            { idx: 14, a: 'Prot.', b: 'Duro' }
          ].map((item, i) => (
            <div key={i} className="flex items-center gap-1.5 text-[10px] text-slate-600 overflow-hidden">
              <CheckCircle2 className="w-3 h-3 text-teal-500 flex-shrink-0" />
              <span className="font-bold uppercase tracking-tighter truncate">
                {getDatoTecnico(item.idx, item.a, item.b)}
              </span>
            </div>
          ))}
        </div>

        {/* UBICACIÓN Y TAMAÑO: Espacio flexible pero con límite */}
        <div className="space-y-2 text-xs mb-4 flex-grow">
          <div className="flex items-start gap-2 text-slate-600">
            <MapPin className="w-3.5 h-3.5 text-cyan-500 mt-0.5 flex-shrink-0" />
            <span className="line-clamp-2 leading-relaxed h-[32px] overflow-hidden">
                {species.habitat}
            </span>
          </div>
          <div className="flex items-center gap-2 text-slate-600">
            <Ruler className="w-3.5 h-3.5 text-teal-500 flex-shrink-0" />
            <span className="truncate font-medium">{species.tamano}</span>
          </div>
        </div>

        {/* FOOTER: Pegado abajo */}
        <div className="flex items-center justify-between pt-3 border-t border-slate-100 flex-shrink-0">
          <div className="flex items-center gap-1 text-[9px] text-slate-400 font-bold">
            <Calendar className="w-3 h-3" />
            <span>{new Date(species.fechaAgregada).toLocaleDateString('es-ES')}</span>
          </div>
          <div className="px-2 py-0.5 rounded bg-slate-100 text-slate-500 text-[9px] font-mono font-bold">
            {species.nombreCientifico?.split(' ')[0]?.toUpperCase() || 'GENUS'}
          </div>
        </div>
      </div>
    </div>
  );
}