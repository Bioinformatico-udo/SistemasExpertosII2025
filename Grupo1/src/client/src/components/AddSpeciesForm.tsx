import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Label } from './ui/label';
import { Plus, X } from 'lucide-react';
import type { Species } from '../types/species';

interface AddSpeciesFormProps {
  onAddSpecies: (species: Omit<Species, 'id' | 'fechaAgregada'>) => void;
  onCancel?: () => void;
}

export function AddSpeciesForm({ onAddSpecies, onCancel }: AddSpeciesFormProps) {
  const [formData, setFormData] = useState({
    nombre: '',
    nombreCientifico: '',
    habitat: '',
    tamano: '',
    descripcion: '',
    imagen: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.nombre || !formData.nombreCientifico) {
      alert('Por favor completa al menos el nombre común y científico');
      return;
    }

    onAddSpecies(formData);
    
    // Reset form
    setFormData({
      nombre: '',
      nombreCientifico: '',
      habitat: '',
      tamano: '',
      descripcion: '',
      imagen: ''
    });
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl p-6 border-2 border-cyan-200">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-2xl font-bold text-teal-700 flex items-center gap-2">
          <Plus className="w-6 h-6" />
          Agregar Nueva Especie
        </h3>
        {onCancel && (
          <Button
            variant="ghost"
            size="icon"
            onClick={onCancel}
            className="text-gray-500 hover:text-gray-700"
          >
            <X className="w-5 h-5" />
          </Button>
        )}
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="nombre" className="text-teal-700">
              Nombre Común <span className="text-red-500">*</span>
            </Label>
            <Input
              id="nombre"
              name="nombre"
              value={formData.nombre}
              onChange={handleChange}
              placeholder="ej. Cangrejo porcelana manchado"
              className="border-cyan-300 focus:border-teal-500"
              required
            />
          </div>

          <div>
            <Label htmlFor="nombreCientifico" className="text-teal-700">
              Nombre Científico <span className="text-red-500">*</span>
            </Label>
            <Input
              id="nombreCientifico"
              name="nombreCientifico"
              value={formData.nombreCientifico}
              onChange={handleChange}
              placeholder="ej. Petrolisthes galathinus"
              className="border-cyan-300 focus:border-teal-500 italic"
              required
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="habitat" className="text-teal-700">
              Hábitat
            </Label>
            <Input
              id="habitat"
              name="habitat"
              value={formData.habitat}
              onChange={handleChange}
              placeholder="ej. Arrecifes de coral, bajo rocas"
              className="border-cyan-300 focus:border-teal-500"
            />
          </div>

          <div>
            <Label htmlFor="tamano" className="text-teal-700">
              Tamaño
            </Label>
            <Input
              id="tamano"
              name="tamano"
              value={formData.tamano}
              onChange={handleChange}
              placeholder="ej. 1-2 cm de caparazón"
              className="border-cyan-300 focus:border-teal-500"
            />
          </div>
        </div>

        <div>
          <Label htmlFor="imagen" className="text-teal-700">
            URL de Imagen
          </Label>
          <Input
            id="imagen"
            name="imagen"
            value={formData.imagen}
            onChange={handleChange}
            placeholder="ej. https://ejemplo.com/imagen.jpg"
            className="border-cyan-300 focus:border-teal-500"
          />
        </div>

        <div>
          <Label htmlFor="descripcion" className="text-teal-700">
            Descripción
          </Label>
          <Textarea
            id="descripcion"
            name="descripcion"
            value={formData.descripcion}
            onChange={handleChange}
            placeholder="Describe las características principales de esta especie..."
            className="border-cyan-300 focus:border-teal-500 min-h-[100px]"
          />
        </div>

        <div className="flex gap-3 pt-4">
          <Button
            type="submit"
            className="flex-1 bg-gradient-to-r from-teal-500 to-cyan-500 hover:from-teal-600 hover:to-cyan-600 text-white shadow-lg"
          >
            <Plus className="w-4 h-4 mr-2" />
            Agregar Especie
          </Button>
          {onCancel && (
            <Button
              type="button"
              variant="outline"
              onClick={onCancel}
              className="border-gray-300 hover:bg-gray-100"
            >
              Cancelar
            </Button>
          )}
        </div>
      </form>
    </div>
  );
}
