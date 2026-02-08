import { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { Quiz } from './components/Quiz';
import { Results } from './components/Results';
import { InfoSection } from './components/InfoSection';
import { Footer } from './components/Footer';
import { SpeciesPage } from './components/SpeciesPage';
import type { Species } from './types/species';
// @ts-ignore: módulo de imagen de Figma sin declaraciones de tipo
import porcelainCrabBg from 'figma:asset/8e4e354dea92540e23d4ff457368ea3333d15dfe.png';
import { enviarDatosAxios } from './data/api/cangrejos/Apicangrejos';

export default function App() {
  // --- ESTADOS DEL QUIZ ---
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [score, setScore] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [answers, setAnswers] = useState<boolean[]>([]);
  const [quizStarted, setQuizStarted] = useState(false);
  const [answersHistory, setAnswersHistory] = useState<number[]>([]);
  const [apiResultString, setApiResultString] = useState<string | null>(null);

  // --- ESTADOS DE NAVEGACIÓN Y CATÁLOGO ---
  const [currentPage, setCurrentPage] = useState<'home' | 'species'>('home');
  const [species, setSpecies] = useState<Species[]>([]);
  const [loading, setLoading] = useState(false);

  // --- CONEXIÓN CON FLASK (127.0.0.1:5000) ---
  // FUNCIÓN ÚNICA DE CARGA 
  const loadSpeciesFromServer = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://127.0.0.1:5000/catalogo');
      if (!response.ok) throw new Error('Error al cargar catálogo');
      
      const data = await response.json();

      // Diccionario de imágenes basado en tu archivo cangrejos.py
      const imagenesReferencia: Record<string, string> = {
        'Neopisosoma_neglectum': 'src/assets/images/crab/caparazon_rugoso.jpg',
        'Neopisosoma_angustifrons': 'src/assets/images/crab/caparazon_rugoso.jpg',
        'Neopisosoma_orientale': 'src/assets/images/crab/caparazon_rugoso.jpg',
        'Clastotoechus_nodosus': 'src/assets/images/crab/caparazon_rugoso.jpg',
        'Pachycheles_serratus': 'src/assets/images/crab/caparazon_rugoso.jpg',
        'Pachycheles_monilifer': 'src/assets/images/crab/caparazon_rugoso.jpg',
        'Pachycheles_riseii': 'src/assets/images/crab/caparazon_rugoso.jpg',
        'Pachycheles_ackleianus': 'src/assets/images/crab/caparazon_rugoso.jpg',
        'Petrolisthes_tridentatus': 'src/assets/images/crab/caparazon_rugoso.jpg',
      };

      const speciesArray = Object.entries(data).map(([key, info]: [string, any]) => {
        const imagenFinal = imagenesReferencia[key] || info.imagen || 'src/assets/images/crab/default.jpg';

        return {
          id: key,
          nombre: info.nombre || key.replace(/_/g, ' '),
          nombreCientifico: info.nombreCientifico || key.replace(/_/g, ' '),
          habitat: info.habitat || 'No especificado',
          tamano: info.tamano || 'N/A',
          descripcion: info.descripcion || '',
          imagen: imagenFinal,
          fechaAgregada: info.fechaAgregada ? new Date(info.fechaAgregada) : new Date(),
          preguntas_identificacion: info.preguntas_identificacion || []
        };
      });
      
      setSpecies(speciesArray);
    } catch (error) {
      console.error("Error conectando con Flask:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSpeciesFromServer();
  }, []);

  const handleAddSpecies = async (newSpecies: Omit<Species, 'id' | 'fechaAgregada'>) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/guardar_especimen', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newSpecies),
      });
      
      if (response.ok) {
        await loadSpeciesFromServer(); 
      }
    } catch (error) {
      console.error("Error al guardar en Flask:", error);
    }
  };

  const handleDeleteSpecies = async (id: string) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/borrar_especimen/${id}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        setSpecies(prev => prev.filter(s => s.id !== id));
      }
    } catch (error) {
      console.error("Error al borrar en Flask:", error);
    }
  };

  // --- LÓGICA DEL QUIZ ---
  const questions = [
    {
      question: "¿Tiene el caparazon liso o rugoso??",
      correctAnswer: false,
      options: ['Liso/Casi liso', 'Rugoso'],
      imgOpcion1: 'src/assets/preguntas_imagenes/caparazon_liso.jpg',
      imgOpcion2: 'src/assets/preguntas_imagenes/caparazon_rugoso.jpg',
      explanation: "Los porcelánidos tienen 10 patas, pero el último par está oculto bajo el caparazón."
    },
    {
      question: "¿Su antena es desarmada(lisa) o tiene una parte aserrada/tuberculado?",
      correctAnswer: true,
      options: ['Desarmada/Lisa', 'Contiene surcos'],
      imgOpcion1: 'src/assets/preguntas_imagenes/antena_lisa.jpg',
      imgOpcion2: 'src/assets/preguntas_imagenes/aserrada.png',
      explanation: "Los porcelánidos tienen el abdomen reducido y plegado."
    },
    {
      question: "¿Sus maxilipedos son lisos/casi lisos o contienen surcos?",
      correctAnswer: true,
      options: ['Liso/Casi liso', 'Con surcos'],
      imgOpcion1: 'src/assets/preguntas_imagenes/maxilipedos_lisos.jpeg',
      imgOpcion2: 'src/assets/preguntas_imagenes/maxilipedos_tuberculados.jpeg',
      explanation: "Los porcelánidos tienen antenas largas."
    },
    {
      question: "¿Tiene quelipedos desiguales o iguales/subiguales??",
      correctAnswer: false,
      options: ['Desiguales', 'Iguales/Subiguales'],
      imgOpcion1: 'src/assets/preguntas_imagenes/pinzas_desiguales.jpg',
      imgOpcion2: 'src/assets/preguntas_imagenes/pinzas_iguales.png',
      explanation: "Los porcelánidos son anomuros."
    },
    {
      question: "¿Su caparazon es cuadrado/subcuadrado o rectangular?",
      correctAnswer: true,
      options: ['Cuadrado/Subcuadrado', 'Rectangular'],
      imgOpcion1: 'src/assets/preguntas_imagenes/caparazon_cuadrado.jpg',
      imgOpcion2: 'src/assets/preguntas_imagenes/caparazon_rectangular.jpg',
      explanation: "Tienen un caparazón característico de forma redondeada u ovalada."
    },
    {
      question: "'¿Cuantos telsones tiene?'",
      correctAnswer: true,
      options: ['7 Telsones', '5 Telsones'],
      imgOpcion1: 'src/assets/preguntas_imagenes/telson_7.jpeg',
      imgOpcion2: 'src/assets/preguntas_imagenes/telson_5.jpeg',
      explanation: "Importante para distinguir géneros."
    },
    {
      question: "¿Los machos presentan pleopodos?",
      correctAnswer: false,
      options: ['NO', 'SI'],
      imgOpcion1: 'src/assets/preguntas_imagenes/no_pleopodo.jpg',
      imgOpcion2: 'src/assets/preguntas_imagenes/si_pleopodos.png',
      explanation: "Característica dimórfica."
    },
    {
      question: "¿Como es su habitat?",
      correctAnswer: false,
      options: ['Habitats protegidos', 'Habitats Duros'],
      imgOpcion1: 'src/assets/preguntas_imagenes/habitat_protegido.jpg',
      imgOpcion2: 'src/assets/preguntas_imagenes/habitat_duro.jpg',
      explanation: "Viven bajo rocas o en arrecifes."
    }
  ];

  const handleAnswer = async (answer: boolean) => {
    const isCorrect = answer === questions[currentQuestion].correctAnswer;
    const binaryValue: number = answer ? 1 : 0;
    const binaryValue2: number = answer ? 0 : 1;

    if (isCorrect) setScore(score + 1);
    
    const historyToSend = [...answersHistory, binaryValue, binaryValue2];
    setAnswersHistory(historyToSend);
    setAnswers([...answers, answer]);

    if (currentQuestion + 1 < questions.length) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      const resultado: string = await enviarDatosAxios(historyToSend);
      setApiResultString(resultado);
      setShowResults(true);
    }
  };

  const resetQuiz = () => {
    setCurrentQuestion(0);
    setScore(0);
    setShowResults(false);
    setAnswers([]);
    setAnswersHistory([]);
    setQuizStarted(false);
  };

  const navigateToSpecies = () => setCurrentPage('species');
  const navigateToHome = () => setCurrentPage('home');

  return (
    <div className="min-h-screen bg-gradient-to-br from-cyan-100 via-teal-50 to-blue-100 relative overflow-hidden">
      <div className="absolute inset-0 opacity-5">
        <div
          className="absolute inset-0 bg-repeat"
          style={{
            backgroundImage: `url(${porcelainCrabBg})`,
            backgroundSize: '200px 200px'
          }}
        />
      </div>

      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute w-20 h-20 bg-cyan-300/20 rounded-full blur-xl animate-float" style={{ top: '10%', left: '10%', animationDelay: '0s' }} />
        <div className="absolute w-32 h-32 bg-teal-300/20 rounded-full blur-xl animate-float" style={{ top: '60%', right: '15%', animationDelay: '2s' }} />
        <div className="absolute w-24 h-24 bg-blue-300/20 rounded-full blur-xl animate-float" style={{ bottom: '20%', left: '20%', animationDelay: '4s' }} />
      </div>

      <Header />

      <main className="container mx-auto px-4 py-8 max-w-6xl relative z-10">
        {currentPage === 'home' ? (
          <>
            {!quizStarted ? (
              <InfoSection onStartQuiz={() => setQuizStarted(true)} onNavigateToSpecies={navigateToSpecies} />
            ) : !showResults ? (
              <Quiz
                question={questions[currentQuestion]}
                questionNumber={currentQuestion + 1}
                totalQuestions={questions.length}
                onAnswer={handleAnswer}
              />
            ) : (
              <Results
                resultado={apiResultString ?? ''}
                score={score}
                totalQuestions={questions.length}
                questions={questions}
                answers={answers}
                onRestart={resetQuiz}
              />
            )}
          </>
        ) : (
          <SpeciesPage
            species={species}
            onAddSpecies={handleAddSpecies}
            onDeleteSpecies={handleDeleteSpecies}
            onBack={navigateToHome}
          />
        )}
      </main>      
      <Footer />
    </div>
  );
}