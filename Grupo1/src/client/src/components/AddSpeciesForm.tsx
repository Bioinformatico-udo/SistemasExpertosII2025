import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Label } from './ui/label';
import { Plus, X, Image as ImageIcon } from 'lucide-react';
import type { Species } from '../types/species';

interface AddSpeciesFormProps {
  onAddSpecies: (species: Omit<Species, 'id' | 'fechaAgregada'>) => void;
  onCancel?: () => void;
}

export function AddSpeciesForm({ onAddSpecies, onCancel }: AddSpeciesFormProps) {
  const [formData, setFormData] = useState({
    nombre: '',
    nombreCientifico: '',
    tamano: '',
    descripcion: '',
    imagen: '',
    caparazon: '0',
    antena: '0',
    maxilipedos: '0',
    quelipedos: '0',
    formaCaparazon: '0',
    telsones: '0',
    pleopodos: '0',
    habitatTipo: '0' 
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setFormData({ ...formData, imagen: reader.result as string });
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const crearPar = (val: string) => (val === '1' ? [0, 1] : [1, 0]);

    // Generamos el array de 16 posiciones que requiere el servidor/TS
    const preguntas_identificacion = [
      ...crearPar(formData.caparazon),
      ...crearPar(formData.antena),
      ...crearPar(formData.maxilipedos),
      ...crearPar(formData.quelipedos),
      ...crearPar(formData.formaCaparazon),
      ...crearPar(formData.telsones),
      ...crearPar(formData.pleopodos),
      ...crearPar(formData.habitatTipo),
    ];

    const finalData = {
      nombre: formData.nombre,
      nombreCientifico: formData.nombreCientifico,
      habitat: formData.habitatTipo === '0' ? 'Habitats protegidos (Galerias/Rocas)' : 'Habitats Duros (Arrecifes/Corales)',
      tamano: formData.tamano,
      descripcion: formData.descripcion,
      imagen: formData.imagen,
      preguntas_identificacion: preguntas_identificacion 
    };

    onAddSpecies(finalData);
    onCancel?.();
  };

  return (
    <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-xl p-6 border-2 border-cyan-200">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-2xl font-bold text-teal-700 flex items-center gap-2">
          <Plus className="w-6 h-6" />
          Agregar Nueva Especie
        </h3>
        {onCancel && (
          <Button variant="ghost" size="icon" onClick={onCancel} className="text-gray-500">
            <X className="w-5 h-5" />
          </Button>
        )}
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Nombres */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Label className="text-teal-700 font-bold">Nombre Común *</Label>
            <Input name="nombre" value={formData.nombre} onChange={handleChange} required className="border-cyan-300" />
          </div>
          <div>
            <Label className="text-teal-700 font-bold">Nombre Científico *</Label>
            <Input name="nombreCientifico" value={formData.nombreCientifico} onChange={handleChange} required className="border-cyan-300 italic" />
          </div>
        </div>

        {/* Imagen */}
        <div className="p-4 bg-cyan-50/50 rounded-xl border border-cyan-100 space-y-3">
          <Label className="text-teal-700 flex items-center gap-2 font-bold">
            <ImageIcon className="w-4 h-4" /> Imagen de la Especie
          </Label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input 
              type="text" 
              name="imagen" 
              placeholder="URL de imagen..." 
              value={formData.imagen.startsWith('data:') ? '' : formData.imagen} 
              onChange={handleChange}
              className="border-cyan-300"
            />
            <Input 
              type="file" 
              accept="image/*" 
              onChange={handleFileChange}
              className="border-cyan-300 bg-white shadow-sm"
            />
          </div>
          {formData.imagen && (
            <div className="mt-2 flex justify-center animate-in fade-in zoom-in duration-300">
              <img src={formData.imagen} alt="Preview" className="h-32 w-48 object-cover rounded-lg border-2 border-cyan-200 shadow-md" />
            </div>
          )}
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 bg-slate-50 p-4 rounded-xl border border-slate-200">
          {[
            { label: 'Caparazón', name: 'caparazon', opts: ['Liso', 'Rugoso'] },
            { label: 'Antena', name: 'antena', opts: ['Lisa', 'Aserrada'] },
            { label: 'Maxilipedos', name: 'maxilipedos', opts: ['Lisos', 'Surcos'] },
            { label: 'Quelipedos', name: 'quelipedos', opts: ['Desiguales', 'Iguales'] },
            { label: 'Forma', name: 'formaCaparazon', opts: ['Cuadrado', 'Rectangular'] },
            { label: 'Telsones', name: 'telsones', opts: ['7 Tels.', '5 Tels.'] },
            { label: 'Pleópodos', name: 'pleopodos', opts: ['No', 'Si'] },
            { label: 'Hábitat', name: 'habitatTipo', opts: ['Protegido', 'Duro'] },
          ].map((item) => (
            <div key={item.name} className="flex flex-col gap-1">
              <Label className="text-[10px] uppercase font-bold text-teal-600 tracking-wider" htmlFor={item.name}>{item.label}</Label>
              <select 
                name={item.name} 
                id={item.name}
                aria-label={item.label}
                value={(formData as any)[item.name]}
                onChange={handleChange}
                className="w-full h-9 rounded-md border border-cyan-300 bg-white px-2 py-1 text-xs shadow-sm focus:ring-2 focus:ring-teal-500 outline-none transition-all"
              >
                {item.opts.map((opt, i) => <option key={opt} value={i}>{opt}</option>)}
              </select>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
                <Label className="text-teal-700 font-bold">Tamaño</Label>
                <Input name="tamano" value={formData.tamano} onChange={handleChange} className="border-cyan-300" placeholder="Ej: 1.5 cm" />
            </div>

        </div>

        <div>
          <Label className="text-teal-700 font-bold">Descripción</Label>
          <Textarea name="descripcion" value={formData.descripcion} onChange={handleChange} className="border-cyan-300 resize-none" rows={3} placeholder="Breve descripción taxonómica..." />
        </div>

        <div className="flex gap-3 pt-2">
          <Button type="submit" className="flex-1 bg-gradient-to-r from-teal-500 to-cyan-500 text-white font-bold h-11 hover:from-teal-600 hover:to-cyan-600 shadow-md transition-all">
            <Plus className="w-4 h-4 mr-2" /> Registrar en Sistema
          </Button>
          {onCancel && (
            <Button type="button" variant="outline" onClick={onCancel} className="h-11 border-cyan-200 text-slate-500">
              Cancelar
            </Button>
          )}
        </div>
      </form>
    </div>
  );
}