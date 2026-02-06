import { Trash2, Calendar, Ruler, MapPin } from 'lucide-react';
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
      onDelete(species.id);
    }
  };

  return (
    <div className="bg-white/95 backdrop-blur-sm rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden border-2 border-cyan-200 hover:border-teal-400 group">
      {/* Imagen */}
      <div className="relative h-48 bg-gradient-to-br from-cyan-100 to-teal-100 overflow-hidden">
        {species.imagen ? (
          <ImageWithFallback
            src={species.imagen}
            alt={species.nombre}
            className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-teal-300">
            <div className="text-center">
              <div className="text-6xl mb-2">🦀</div>
              <p className="text-sm text-teal-500">Sin imagen</p>
            </div>
          </div>
        )}
        
        {/* Botón de eliminar */}
        <Button
          variant="destructive"
          size="icon"
          onClick={handleDelete}
          className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300 shadow-lg"
        >
          <Trash2 className="w-4 h-4" />
        </Button>
      </div>

      {/* Contenido */}
      <div className="p-5">
        <h3 className="text-xl font-bold text-teal-700 mb-1">
          {species.nombre}
        </h3>
        <p className="text-sm italic text-gray-600 mb-4">
          {species.nombreCientifico}
        </p>

        {species.descripcion && (
          <p className="text-gray-700 text-sm mb-4 line-clamp-3">
            {species.descripcion}
          </p>
        )}

        <div className="space-y-2 text-sm">
          {species.habitat && (
            <div className="flex items-start gap-2 text-gray-600">
              <MapPin className="w-4 h-4 mt-0.5 text-cyan-500 flex-shrink-0" />
              <span>{species.habitat}</span>
            </div>
          )}
          
          {species.tamano && (
            <div className="flex items-start gap-2 text-gray-600">
              <Ruler className="w-4 h-4 mt-0.5 text-teal-500 flex-shrink-0" />
              <span>{species.tamano}</span>
            </div>
          )}
          
          <div className="flex items-center gap-2 text-gray-400 text-xs pt-2 border-t border-gray-200">
            <Calendar className="w-3 h-3" />
            <span>
              Agregado: {new Date(species.fechaAgregada).toLocaleDateString('es-ES')}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
