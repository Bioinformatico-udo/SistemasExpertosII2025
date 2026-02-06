import { useState } from 'react';
import { SpeciesList } from './SpeciesList';
import { AddSpeciesForm } from './AddSpeciesForm';
import { Button } from './ui/button';
import { ArrowLeft, Plus, List } from 'lucide-react';
import type { Species } from '../types/species';

interface SpeciesPageProps {
  species: Species[];
  onAddSpecies: (species: Omit<Species, 'id' | 'fechaAgregada'>) => void;
  onDeleteSpecies: (id: string) => void;
  onBack: () => void;
}

export function SpeciesPage({ species, onAddSpecies, onDeleteSpecies, onBack }: SpeciesPageProps) {
  const [showForm, setShowForm] = useState(false);

  const handleAddSpecies = (newSpecies: Omit<Species, 'id' | 'fechaAgregada'>) => {
    onAddSpecies(newSpecies);
    setShowForm(false);
  };

  return (
    <div className="space-y-6">
      {/* Header de navegación */}
      <div className="flex items-center justify-between gap-4 flex-wrap">
        <Button
          onClick={onBack}
          variant="outline"
          className="border-cyan-300 hover:bg-cyan-50 text-teal-700"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Volver a Inicio
        </Button>

        <Button
          onClick={() => setShowForm(!showForm)}
          className={`${
            showForm
              ? 'bg-gray-500 hover:bg-gray-600'
              : 'bg-gradient-to-r from-teal-500 to-cyan-500 hover:from-teal-600 hover:to-cyan-600'
          } text-white shadow-lg`}
        >
          {showForm ? (
            <>
              <List className="w-4 h-4 mr-2" />
              Ver Lista
            </>
          ) : (
            <>
              <Plus className="w-4 h-4 mr-2" />
              Agregar Especie
            </>
          )}
        </Button>
      </div>

      {/* Contenido principal */}
      {showForm ? (
        <AddSpeciesForm
          onAddSpecies={handleAddSpecies}
          onCancel={() => setShowForm(false)}
        />
      ) : (
        <SpeciesList
          species={species}
          onDeleteSpecies={onDeleteSpecies}
        />
      )}
    </div>
  );
}
