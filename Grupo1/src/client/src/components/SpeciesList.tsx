import { useState } from 'react';
import { SpeciesCard } from './SpeciesCard';
import { Search, Filter, RotateCcw } from 'lucide-react'; // Importamos RotateCcw para el icono de reset
import { Input } from './ui/input';
import type { Species } from '../types/species';

interface SpeciesListProps {
  species: Species[];
  onDeleteSpecies: (id: string) => void;
}

export function SpeciesList({ species, onDeleteSpecies }: SpeciesListProps) {
  const [searchTerm, setSearchTerm] = useState('');

  // 1. Definimos la lista de IDs fijos (según tu archivo cangrejos.py)
  const IDS_FIJOS = [
    'Neopisosoma_neglectum', 'Neopisosoma_angustifrons', 'Neopisosoma_orientale',
    'Clastotoechus_nodosus', 'Pachycheles_serratus', 'Pachycheles_monilifer',
    'Pachycheles_riseii', 'Pachycheles_ackleianus', 'Petrolisthes_tridentatus'
  ];

  // 2. Función para resetear el catálogo
  const handleResetCatalog = () => {
    const confirmacion = window.confirm(
      "¿Estás seguro de que deseas eliminar todas las especies agregadas manualmente? Las 9 especies originales se conservarán."
    );
    
    if (confirmacion) {
      // 1. Filtramos asegurando que el ID exista (s.id ??) y no esté en los fijos
      const especiesNuevas = species.filter(s => !IDS_FIJOS.includes(s.id ?? ''));
      
      // 2. Al iterar, solo llamamos a onDeleteSpecies si el ID realmente existe
      especiesNuevas.forEach(e => {
        if (e.id) {
          onDeleteSpecies(e.id);
        }
      });
    }
  };

  const filteredSpecies = species.filter(s => 
    s.nombre?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    s.nombreCientifico?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    s.habitat?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="bg-white/90 backdrop-blur-sm rounded-xl shadow-lg p-6 border-2 border-cyan-200">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-3xl font-bold text-teal-700">
              Catálogo de Especies
            </h2>
            <div className="flex items-center gap-4 mt-1">
              <p className="text-gray-600">
                {species.length} {species.length === 1 ? 'especie registrada' : 'especies registradas'}
              </p>
              
              {/* BOTÓN DE RESET */}
              {species.length > 9 && (
                <button 
                  onClick={handleResetCatalog}
                  className="flex items-center gap-1 text-xs font-bold text-red-500 hover:text-red-700 transition-colors uppercase tracking-tighter"
                  title="Eliminar especies agregadas manualmente"
                >
                  <RotateCcw className="w-3 h-3" />
                  Resetear Catálogo
                </button>
              )}
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-cyan-500 to-teal-500 text-white px-6 py-3 rounded-lg shadow-lg text-center min-w-[100px]">
            <div className="text-3xl font-bold leading-none">{species.length}</div>
            <div className="text-[10px] uppercase font-bold tracking-widest mt-1 opacity-90">Total</div>
          </div>
        </div>

        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-cyan-400 w-5 h-5" />
          <Input
            type="text"
            placeholder="Buscar por nombre, nombre científico o hábitat..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10 border-cyan-200 focus:border-teal-500 bg-white/50 backdrop-blur-none"
          />
        </div>
      </div>

      {/* Grid de Resultados */}
      {filteredSpecies.length === 0 ? (
        <div className="bg-white/90 backdrop-blur-sm rounded-xl shadow-lg p-12 text-center border-2 border-cyan-200">
          <div className="text-6xl mb-4">🔍</div>
          <h3 className="text-xl font-bold text-gray-700 mb-2">
            {searchTerm ? 'No se encontraron coincidencias' : 'El catálogo está vacío'}
          </h3>
          <p className="text-gray-500">
            {searchTerm 
              ? `No hay resultados para "${searchTerm}"`
              : 'Empieza registrando una especie en el botón superior'}
          </p>
        </div>
      ) : (
        <>
          {searchTerm && (
            <div className="flex items-center gap-2 text-sm text-teal-600 px-2 font-medium">
              <Filter className="w-4 h-4" />
              <span>
                Mostrando {filteredSpecies.length} de {species.length} registros encontrados
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