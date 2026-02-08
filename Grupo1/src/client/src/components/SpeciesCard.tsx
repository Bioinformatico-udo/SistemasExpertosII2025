import { Trash2, Calendar, Ruler, MapPin, Microscope, CheckCircle2 } from 'lucide-react';
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

  /**
   * Lógica para interpretar el array de 16 posiciones:
   * Basado en tu JSON: [1,0, 1,0, ...] 
   * Índice 0: Caparazón (1: Liso, 0: Rugoso)
   * Índice 2: Antena (1: Lisa, 0: Aserrada)
   * Índice 4: Maxilipedos (1: Lisos, 0: Surcos)
   * Índice 10: Telsones (1: 7 Tels, 0: 5 Tels)
   */
  const getDatoTecnico = (index: number, opcionA: string, opcionB: string) => {
    const array = species.preguntas_identificacion;
    if (!array || array.length === 0) return 'N/A';
    return array[index] === 1 ? opcionA : opcionB;
  };

  return (
    <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden border-2 border-cyan-200 hover:border-teal-400 group">
      
      {/* SECCIÓN DE IMAGEN */}
      <div className="relative h-52 bg-gradient-to-br from-cyan-100 to-teal-100 overflow-hidden">
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
        

        {/* Botón Eliminar */}
        <Button
          variant="destructive"
          size="icon"
          onClick={handleDelete}
          className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300 shadow-lg border border-white/20"
        >
          <Trash2 className="w-4 h-4" />
        </Button>
      </div>

      {/* CUERPO DE LA CARD */}
      <div className="p-5">
        <div className="mb-4">
          <h3 className="text-lg font-bold text-teal-800 leading-tight line-clamp-1">
            {species.nombre}
          </h3>
          <p className="text-xs italic text-cyan-600 font-semibold">
            {species.nombreCientifico}
          </p>
        </div>

        {/* FICHA TÉCNICA (Basada en el array del JSON) */}
        <div className="mb-4 p-3 bg-cyan-50/30 rounded-lg border border-cyan-100 grid grid-cols-2 gap-2">
          <div className="flex items-center gap-1.5 text-[10px] text-slate-600">
            <CheckCircle2 className="w-3 h-3 text-teal-500 flex-shrink-0" />
            <span className="font-bold uppercase tracking-tighter">
              {getDatoTecnico(0, 'Liso', 'Rugoso')}
            </span>
          </div>
          <div className="flex items-center gap-1.5 text-[10px] text-slate-600">
            <CheckCircle2 className="w-3 h-3 text-teal-500 flex-shrink-0" />
            <span className="font-bold uppercase tracking-tighter">
              {getDatoTecnico(2, 'Ant. Lisa', 'Ant. Aserr.')}
            </span>
          </div>
          <div className="flex items-center gap-1.5 text-[10px] text-slate-600">
            <CheckCircle2 className="w-3 h-3 text-teal-500 flex-shrink-0" />
            <span className="font-bold uppercase tracking-tighter">
              {getDatoTecnico(10, '7 Tels.', '5 Tels.')}
            </span>
          </div>
          <div className="flex items-center gap-1.5 text-[10px] text-slate-600">
            <CheckCircle2 className="w-3 h-3 text-teal-500 flex-shrink-0" />
            <span className="font-bold uppercase tracking-tighter">
              {getDatoTecnico(14, 'Prot.', 'Duro')}
            </span>
          </div>
        </div>

        {/* DATOS DE UBICACIÓN Y TAMAÑO */}
        <div className="space-y-2 text-xs mb-4">
          <div className="flex items-start gap-2 text-slate-600">
            <MapPin className="w-3.5 h-3.5 text-cyan-500 mt-0.5" />
            <span className="line-clamp-1">{species.habitat}</span>
          </div>
          <div className="flex items-start gap-2 text-slate-600">
            <Ruler className="w-3.5 h-3.5 text-teal-500 mt-0.5" />
            <span>{species.tamano}</span>
          </div>
        </div>

        {/* FOOTER */}
        <div className="flex items-center justify-between pt-3 border-t border-slate-100">
          <div className="flex items-center gap-1 text-[9px] text-slate-400 font-bold">
            <Calendar className="w-3 h-3" />
            <span>{new Date(species.fechaAgregada).toLocaleDateString('es-ES')}</span>
          </div>
          <div className="px-2 py-0.5 rounded bg-slate-100 text-slate-500 text-[9px] font-mono">
            {species.nombreCientifico.split(' ')[0].toUpperCase()}
          </div>
        </div>
      </div>
    </div>
  );
}