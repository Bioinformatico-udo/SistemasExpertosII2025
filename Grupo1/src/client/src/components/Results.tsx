import { motion } from 'motion/react';
import { Trophy, RotateCcw, Award, Shell, BookOpen } from 'lucide-react';
import { CRAB_SPECIES } from '../data/api/cangrejos/Apicangrejos';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface ResultsProps {
  resultado: string;
  score: number;
  totalQuestions: number;
  questions: Array<{
    question: string;
    correctAnswer: boolean;
    explanation: string;
  }>;
  answers: boolean[];
  onRestart: () => void;
}


export function Results({ resultado, score, totalQuestions, questions, answers, onRestart }: ResultsProps) {
  const especieEncontrada = CRAB_SPECIES.find(
    (especie) => especie.nombre_cientifico === resultado
  );
  const percentage = (score / totalQuestions) * 100;

  const getResultMessage = () => {
    if (percentage === 100) {
      return {
        title: "¡Experto en Porcelánidos!",
        message: "¡Perfecto! Tienes todas las características de los porcelánidos. ¡Es un verdadero porcelánidos!",
        color: "from-yellow-400 to-amber-500"
      };
    } else if (percentage >= 80) {
      return {
        title: "¡Excelente tienes un Porcelánidos!",
        message: "Tiene la mayores caracteristicas de los Porcelánidos. ¡Muy bien!",
        color: "from-green-400 to-emerald-500"
      };
    } else if (percentage >= 60) {
      return {
        title: "¡Vuelve a intentaro!",
        message: "La especie que intentas identificar no parece ser un Porcelánidos, pero todavía hay espacio para volverlo identificar.",
        color: "from-blue-400 to-cyan-500"
      };
    } else {
      return {
        title: "¡Lo siento, No es un porcelánidos!",
        message: "Los porcelánidos son fascinantes. Pero la especie que intentas indentificar no es pertence a la familia porcellánidae.",
        color: "from-orange-400 to-red-500"
      };
    }
  };

  const result = getResultMessage();

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-white rounded-3xl shadow-2xl overflow-hidden max-w-4xl mx-auto"
    >
      <div className={`bg-gradient-to-r ${result.color} py-16`}>
        <div className="text-center text-white">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring" }}
            className="flex justify-center mb-6"
          >
            
          </motion.div>
          <h2 className="text-5xl mb-4 drop-shadow-lg">{resultado}</h2>
        </div>
      </div>

      <div className="p-10">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.4, type: "spring" }}
          className="text-center mb-10"
        >
          <div className="text-7xl mb-4 text-gray-800">
          </div>
          <p className="text-3xl text-gray-600 mb-3">
          </p>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          </p>
        </motion.div>

        {/* Resumen de respuestas */}
        <div className="mb-10">
          <h3 className="text-2xl text-gray-800 mb-6 text-center">
            Se determino esta especie por estas respuestas:
          </h3>
          <div className="space-y-4 max-h-96 overflow-y-auto pr-2">
            {questions.map((q, index) => {
              const userAnswer = answers[index];
              const isCorrect = userAnswer === q.correctAnswer;

              return (
                <div
                  key={index}
                  className={`
                    p-5 rounded-2xl border-2 bg-green-50 border-green-300
                    
                  `}
                >
                  <div className="flex items-start gap-3 mb-2">
                    <div className="flex-1">
                      <p className="text-gray-800 mb-2">
                        <strong>Pregunta {index + 1}:</strong> {q.question}
                      </p>
                      <p className="text-sm text-gray-600 mb-1">
                        Tu respuesta: <strong>{userAnswer ? 'SÍ' : 'NO'}</strong>
                      </p>
                      <p className="text-sm text-gray-700 italic">
                      </p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Información adicional */}
        <div className="bg-gradient-to-br from-cyan-50 to-teal-50 rounded-2xl p-8 mb-8 border-2 border-cyan-200">
          <h3 className="text-2xl text-teal-900 mb-4 flex items-center gap-3">
            <Shell className="w-8 h-8" />
            Datos curiosos sobre los Porcelánidos
          </h3>
          <ul className="space-y-3 text-gray-700">
            <li className="flex gap-3">
              <span className="text-cyan-600">•</span>
              <span>Existen más de 280 especies de porcelánidos distribuidas en todo el mundo.</span>
            </li>
            <li className="flex gap-3">
              <span className="text-cyan-600">•</span>
              <span>El nombre "cangrejo de porcelana" se debe a su fragilidad y facilidad para desprender sus extremidades.</span>
            </li>
            <li className="flex gap-3">
              <span className="text-cyan-600">•</span>
              <span>Son importantes indicadores de la salud de los ecosistemas de arrecifes de coral.</span>
            </li>
            <li className="flex gap-3">
              <span className="text-cyan-600">•</span>
              <span>Algunos porcelánidos viven en simbiosis con anémonas de mar, similar a los cangrejos ermitaños.</span>
            </li>
          </ul>
        </div>

        <div className="text-center">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onRestart}
            className="bg-gradient-to-r from-teal-500 via-cyan-400 to-blue-500 text-white py-5 px-10 rounded-2xl flex items-center gap-4 mx-auto hover:shadow-2xl transition-shadow text-xl"
          >
            <RotateCcw className="w-7 h-7" />
            <span>Volver al inicio</span>
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
}