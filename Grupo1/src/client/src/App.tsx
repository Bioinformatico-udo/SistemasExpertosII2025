import { useState } from 'react';
import { Header } from './components/Header';
import { Quiz } from './components/Quiz';
import { Results } from './components/Results';
import { InfoSection } from './components/InfoSection';
import { Footer } from './components/Footer';
// @ts-ignore: módulo de imagen de Figma sin declaraciones de tipo
import porcelainCrabBg from 'figma:asset/8e4e354dea92540e23d4ff457368ea3333d15dfe.png';
import { enviarDatosAxios } from './data/api/cangrejos/Apicangrejos';

export default function App() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [score, setScore] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [answers, setAnswers] = useState<boolean[]>([]);
  const [quizStarted, setQuizStarted] = useState(false);
  const [answersHistory, setAnswersHistory] = useState<number[]>([]);
  const [apiResultString, setApiResultString] = useState<string | null>(null);

  const questions = [
    {
      question: "¿Tiene el caparazon liso o rugoso??",
      correctAnswer: false,
      options: ['Liso/Casi liso', 'Rugoso'],
      imgOpcion1: 'src/assets/preguntas_imagenes/caparazon_liso.jpg',
      imgOpcion2: 'src/assets/preguntas_imagenes/caparazon_rugoso.jpg',
      explanation: "Los porcelánidos tienen 10 patas, pero el último par está oculto bajo el caparazón, así que solo se ven 8 patas."
    },
    {
      question: "¿Su antena es desarmada(lisa) o tiene una parte aserrada/tuberculado?",
      correctAnswer: true,
      options: ['Desarmada/Lisa', 'Contiene surcos'],
      imgOpcion1: 'src/assets/preguntas_imagenes/antena_lisa.jpg',
      imgOpcion2: 'src/assets/preguntas_imagenes/aserrada.png',
      explanation: "Sí, como los cangrejos verdaderos, los porcelánidos tienen el abdomen reducido y plegado."
    },
    {
      question: "¿Sus maxilipedos son lisos/casi lisos o contienen surcos?",
      correctAnswer: true,
      options: ['Liso/Casi liso', 'Con surcos'],
      imgOpcion1: 'src/assets/preguntas_imagenes/maxilipedos_lisos.jpeg',
      imgOpcion2: 'src/assets/preguntas_imagenes/maxilipedos_tuberculados.jpeg',
      explanation: "Los porcelánidos tienen antenas largas, a diferencia de los cangrejos verdaderos."
    },
    {
      question: "¿Tiene quelipedos desiguales o iguales/subiguales??",
      correctAnswer: false,
      options: ['Desiguales', 'Iguales/Subiguales'],
      imgOpcion1: 'src/assets/preguntas_imagenes/pinzas_desiguales.jpg',
      imgOpcion2: 'src/assets/preguntas_imagenes/pinzas_iguales.png',
      explanation: "No, los porcelánidos son anomuros, no braquiuros. Solo se parecen superficialmente a los cangrejos."
    },
    {
      question: "¿Su caparazon es cuadrado/subcuadrado o rectangular?",
      correctAnswer: true,
      options: ['Cuadrado/Subcuadrado', 'Rectangular'],
      imgOpcion1: 'src/assets/preguntas_imagenes/caparazon_cuadrado.jpg',
      imgOpcion2: 'src/assets/preguntas_imagenes/caparazon_rectangular.jpg',
      explanation: "Sí, los porcelánidos tienen un caparazón característico de forma redondeada u ovalada."
    },
    {
      question: "'¿Cuantos telsones tiene?'",
      correctAnswer: true,
      options: ['7 Telsones', '5 Telsones'],
      imgOpcion1: 'src/assets/preguntas_imagenes/telson_7.jpeg',
      imgOpcion2: 'src/assets/preguntas_imagenes/telson_5.jpeg',
      explanation: "Los porcelánidos pueden nadar usando movimientos rápidos del abdomen, especialmente cuando son larvas o juveniles."
    },
    {
      question: "¿Los machos presentan pleopodos?",
      correctAnswer: false,
      options: ['NO', 'SI'],
      imgOpcion1: 'src/assets/preguntas_imagenes/no_pleopodo.jpg',
      imgOpcion2: 'src/assets/preguntas_imagenes/si_pleopodos.png',
      explanation: "La mayoría de porcelánidos viven en aguas poco profundas, bajo rocas o en arrecifes de coral."
    },
    {
      question: "¿Como es su habitat?",
      correctAnswer: false,
      options: ['Habitats protegidos(Galerias,colonias y bajo rocas)', 'Habitats Duros(Rocas,corales,grietas de rocas y esponjas)'],
      imgOpcion1: 'src/assets/preguntas_imagenes/habitat_protegido.jpg',
      imgOpcion2: 'src/assets/preguntas_imagenes/habitat_duro.jpg',
      explanation: "La mayoría de porcelánidos viven en aguas poco profundas, bajo rocas o en arrecifes de coral."
    }
  ];

  const handleAnswer = async (answer: boolean) => {
    const isCorrect = answer === questions[currentQuestion].correctAnswer;
    const binaryValue: number = answer ? 1 : 0;
    const binaryValue2: number = answer ? 0 : 1;

    if (isCorrect) {
      setScore(score + 1);
    }
    const historyToSend = [...answersHistory, binaryValue, binaryValue2];
    setAnswersHistory(historyToSend);

    setAnswers([...answers, answer]);
    console.log('Quiz terminado. Puntuación final:', historyToSend);

    if (currentQuestion + 1 < questions.length) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      console.log('Quiz terminado. Puntuación final:', historyToSend);
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
    setQuizStarted(false);
  };

  const startQuiz = () => {
    setQuizStarted(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-cyan-100 via-teal-50 to-blue-100 relative overflow-hidden">
      {/* Patrón de fondo decorativo con imagen del porcelánido */}
      <div className="absolute inset-0 opacity-5">
        <div
          className="absolute inset-0 bg-repeat"
          style={{
            backgroundImage: `url(${porcelainCrabBg})`,
            backgroundSize: '200px 200px'
          }}
        />
      </div>

      {/* Burbujas decorativas flotantes */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute w-20 h-20 bg-cyan-300/20 rounded-full blur-xl animate-float" style={{ top: '10%', left: '10%', animationDelay: '0s' }} />
        <div className="absolute w-32 h-32 bg-teal-300/20 rounded-full blur-xl animate-float" style={{ top: '60%', right: '15%', animationDelay: '2s' }} />
        <div className="absolute w-24 h-24 bg-blue-300/20 rounded-full blur-xl animate-float" style={{ bottom: '20%', left: '20%', animationDelay: '4s' }} />
        <div className="absolute w-16 h-16 bg-cyan-400/20 rounded-full blur-xl animate-float" style={{ top: '40%', right: '30%', animationDelay: '1s' }} />
      </div>

      <Header />

      <main className="container mx-auto px-4 py-8 max-w-6xl relative z-10">
        {!quizStarted ? (
          <InfoSection onStartQuiz={startQuiz} />
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
      </main>
      <Footer />
    </div>
  );
}