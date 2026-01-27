import { motion } from 'motion/react';
import { Info, Search, Waves, Shell, ArrowRight } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { FlipCard } from './FlipCard';

interface InfoSectionProps {
  onStartQuiz: () => void;
}

export function InfoSection({ onStartQuiz }: InfoSectionProps) {
  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-3xl shadow-2xl overflow-hidden"
      >
        <div className="grid md:grid-cols-2 gap-8 p-8">
          <div className="space-y-6">
            <h2 className="text-4xl text-blue-900">
              ¿Qué son los Porcelánidos?
            </h2>
            <p className="text-gray-700 text-lg leading-relaxed">
              Los porcelánidos son crustáceos decápodos que pertenecen a la familia <strong>Porcellanidae</strong>. 
              Aunque se asemejan superficialmente a los cangrejos verdaderos (Brachyura), en realidad son 
              más cercanos a las langostas y cangrejos ermitaños.
            </p>
            <p className="text-gray-700 text-lg leading-relaxed">
              Son conocidos como <strong>"cangrejos de porcelana"</strong> debido a su caparazón liso y brillante, 
              y a su tendencia a desprender sus apéndices cuando se sienten amenazados, como la porcelana que se rompe.
            </p>
          </div>
          <div className="rounded-2xl overflow-hidden shadow-lg">
            <ImageWithFallback
              src="https://inaturalist-open-data.s3.amazonaws.com/photos/277928534/medium.jpg"
              alt="Vida marina submarina"
              className="w-full h-full object-cover"
            />
          </div>
        </div>
      </motion.div>

      {/* Características principales con flip cards */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-3xl shadow-2xl p-8"
      >
        <h3 className="text-3xl text-blue-900 mb-8 flex items-center gap-3 justify-center">
          <Info className="w-8 h-8 text-cyan-600" />
          Características principales
        </h3>
        <div className="grid md:grid-cols-3 gap-6">
          <FlipCard
            icon={<Shell className="w-12 h-12 text-blue-600" />}
            title="Apariencia"
            color="from-blue-50 to-cyan-50 border-blue-200"
            imageUrl="https://images.unsplash.com/photo-1642702022200-98bc1289e380?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjcmFiJTIwb2NlYW4lMjB1bmRlcndhdGVyfGVufDF8fHx8MTc2MzkwMDkwMnww&ixlib=rb-4.1.0&q=80&w=1080"
            items={[
              'Caparazón circular u ovalado',
              'Solo 8 patas visibles',
              'Abdomen plegado bajo el cuerpo',
              'Pinzas generalmente simétricas'
            ]}
          />

          <FlipCard
            icon={<Waves className="w-12 h-12 text-teal-600" />}
            title="Hábitat"
            color="from-teal-50 to-green-50 border-teal-200"
            imageUrl="https://images.unsplash.com/photo-1613779584796-99179ac65955?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb3JhbCUyMHJlZWYlMjBjcnVzdGFjZWFufGVufDF8fHx8MTc2MzkwMDkwM3ww&ixlib=rb-4.1.0&q=80&w=1080"
            items={[
              'Aguas poco profundas',
              'Bajo rocas y corales',
              'Zonas intermareales',
              'Ambientes marinos tropicales'
            ]}
          />

          <FlipCard
            icon={<Search className="w-12 h-12 text-cyan-600" />}
            title="Comportamiento"
            color="from-cyan-50 to-blue-50 border-cyan-200"
            imageUrl="https://images.unsplash.com/photo-1611794501034-13369f948303?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxvY2VhbiUyMHdhdmVzJTIwYmx1ZXxlbnwxfHx8fDE3NjM4MzA1NzV8MA&ixlib=rb-4.1.0&q=80&w=1080"
            items={[
              'Filtradores de alimento',
              'Pueden nadar activamente',
              'Regeneran extremidades',
              'Autotomía defensiva'
            ]}
          />
        </div>
      </motion.div>

      {/* Diferencias con cangrejos verdaderos */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-3xl shadow-2xl p-8 border-2 border-amber-200"
      >
        <h3 className="text-3xl text-amber-900 mb-6">
          Diferencias clave con los cangrejos verdaderos
        </h3>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="text-xl text-amber-800 mb-3">
              Porcelánidos (Anomura)
            </h4>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-start gap-2">
                <span className="text-green-600">✓</span>
                <span>Solo 3 pares de patas caminadoras visibles</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-600">✓</span>
                <span>Último par de patas reducido y oculto</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-600">✓</span>
                <span>Antenas largas y prominentes</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-600">✓</span>
                <span>Puede usar el abdomen para nadar.</span>
              </li>
            </ul>
          </div>
          <div>
            <h4 className="text-xl text-amber-800 mb-3">
              Cangrejos verdaderos (Brachyura)
            </h4>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-start gap-2">
                <span className="text-blue-600">✓</span>
                <span>4 pares de patas caminadoras visibles</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600">✓</span>
                <span>Todas las patas bien desarrolladas</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600">✓</span>
                <span>Antenas cortas</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600">✓</span>
                <span>Abdomen completamente inmóvil</span>
              </li>
            </ul>
          </div>
        </div>
      </motion.div>

      {/* CTA para el quiz */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.4 }}
        className="text-center"
      >
        <div className="bg-gradient-to-r from-teal-500 via-cyan-400 to-blue-500 rounded-3xl shadow-2xl p-12">
          <h3 className="text-4xl text-white mb-4">
            ¿Quires identificar un Porcelánido?
          </h3>
          <p className="text-xl text-cyan-50 mb-8 max-w-2xl mx-auto">
            Con tan solo una serie de preguntas podras indetificar a los porcelanidos.
            Respondé SÍ o NO a cada pregunta para poder diferenciar 
            los porcelánidos de otros crustáceos.
          </p>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onStartQuiz}
            className="bg-white text-teal-700 py-4 px-12 rounded-2xl text-2xl flex items-center gap-4 mx-auto hover:shadow-2xl transition-shadow"
          >
            Comenzar
            <ArrowRight className="w-8 h-8" />
          </motion.button>
        </div>
      </motion.div>
    </div>
  );
}