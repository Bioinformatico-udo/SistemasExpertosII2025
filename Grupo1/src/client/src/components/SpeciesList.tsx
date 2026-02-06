import { useState } from 'react';
import { SpeciesCard } from './SpeciesCard';
import { Search, Filter } from 'lucide-react';
import { Input } from './ui/input';
import type { Species } from '../types/species';

interface SpeciesListProps {
  species: Species[];
  onDeleteSpecies: (id: string) => void;
}

export function SpeciesList({ species, onDeleteSpecies }: SpeciesListProps) {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredSpecies = species.filter(s => 
    s.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
    s.nombreCientifico.toLowerCase().includes(searchTerm.toLowerCase()) ||
    s.habitat?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header con búsqueda */}
      <div className="bg-white/90 backdrop-blur-sm rounded-xl shadow-lg p-6 border-2 border-cyan-200">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-3xl font-bold text-teal-700">
              Catálogo de Especies
            </h2>
            <p className="text-gray-600 mt-1">
              {species.length} {species.length === 1 ? 'especie registrada' : 'especies registradas'}
            </p>
          </div>
          <div className="bg-gradient-to-br from-cyan-500 to-teal-500 text-white px-6 py-3 rounded-lg shadow-lg">
            <div className="text-3xl font-bold">{species.length}</div>
            <div className="text-xs opacity-90">Total</div>
          </div>
        </div>

        {/* Barra de búsqueda */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <Input
            type="text"
            placeholder="Buscar por nombre, nombre científico o hábitat..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10 border-cyan-300 focus:border-teal-500"
          />
        </div>
      </div>

      {/* Lista de especies */}
      {filteredSpecies.length === 0 ? (
        <div className="bg-white/90 backdrop-blur-sm rounded-xl shadow-lg p-12 text-center border-2 border-cyan-200">
          <div className="text-6xl mb-4">🔍</div>
          <h3 className="text-xl font-bold text-gray-700 mb-2">
            {searchTerm ? 'No se encontraron especies' : 'No hay especies registradas'}
          </h3>
          <p className="text-gray-500">
            {searchTerm 
              ? 'Intenta con otros términos de búsqueda'
              : 'Agrega tu primera especie de porcelánido usando el formulario'}
          </p>
        </div>
      ) : (
        <>
          {searchTerm && (
            <div className="flex items-center gap-2 text-sm text-gray-600 px-2">
              <Filter className="w-4 h-4" />
              <span>
                Mostrando {filteredSpecies.length} de {species.length} especies
              </span>
            </div>
          )}
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredSpecies.map((s) => (
              <SpeciesCard
                key={s.id}
                species={s}
                onDelete={onDeleteSpecies}
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
