import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Progress } from '../ui/progress';
import { Badge } from '../ui/badge';
import { 
  Play, 
  Pause, 
  RotateCcw, 
  Check, 
  X,
  ArrowLeft,
  Timer,
  SkipForward
} from 'lucide-react';
import { useToast } from '../../hooks/use-toast';

const WorkoutSession = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { toast } = useToast();
  
  const workout = location.state?.workout;
  
  const [currentExerciseIndex, setCurrentExerciseIndex] = useState(0);
  const [isResting, setIsResting] = useState(false);
  const [restTime, setRestTime] = useState(0);
  const [isTimerRunning, setIsTimerRunning] = useState(false);
  const [completedSets, setCompletedSets] = useState({});
  
  if (!workout) {
    navigate('/dashboard');
    return null;
  }

  const currentExercise = workout.exercises[currentExerciseIndex];
  const exerciseKey = `${currentExerciseIndex}`;
  const currentSetCount = completedSets[exerciseKey] || 0;
  
  // Timer effect
  useEffect(() => {
    let interval;
    if (isTimerRunning && restTime > 0) {
      interval = setInterval(() => {
        setRestTime(prev => {
          if (prev <= 1) {
            setIsTimerRunning(false);
            setIsResting(false);
            toast({
              title: "Descanso concluído!",
              description: "Hora da próxima série",
            });
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isTimerRunning, restTime, toast]);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const startRest = () => {
    setRestTime(currentExercise.restTime);
    setIsResting(true);
    setIsTimerRunning(true);
  };

  const pauseTimer = () => {
    setIsTimerRunning(!isTimerRunning);
  };

  const resetTimer = () => {
    setRestTime(currentExercise.restTime);
    setIsTimerRunning(false);
  };

  const skipRest = () => {
    setRestTime(0);
    setIsTimerRunning(false);
    setIsResting(false);
  };

  const completeSet = () => {
    const newCount = currentSetCount + 1;
    setCompletedSets(prev => ({
      ...prev,
      [exerciseKey]: newCount
    }));

    if (newCount >= currentExercise.sets) {
      // Exercício completo
      toast({
        title: "Exercício concluído! 🎉",
        description: `${currentExercise.name} finalizado com sucesso`,
      });
      
      if (currentExerciseIndex < workout.exercises.length - 1) {
        setTimeout(() => {
          setCurrentExerciseIndex(prev => prev + 1);
        }, 1000);
      } else {
        // Treino completo
        toast({
          title: "Treino concluído! 🏆",
          description: "Parabéns! Você finalizou o treino de hoje",
        });
        setTimeout(() => {
          navigate('/dashboard');
        }, 2000);
      }
    } else {
      // Próxima série
      startRest();
    }
  };

  const goBack = () => {
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-black text-white pb-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-gray-900 to-black p-6">
        <div className="flex items-center gap-4 mb-4">
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={goBack}
            className="text-gray-400 hover:text-white"
          >
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <div>
            <h1 className="text-xl font-bold text-white">{workout.name}</h1>
            <p className="text-gray-400">
              Exercício {currentExerciseIndex + 1} de {workout.exercises.length}
            </p>
          </div>
        </div>
        
        <Progress 
          value={(currentExerciseIndex / workout.exercises.length) * 100} 
          className="h-2 bg-gray-800"
        />
      </div>

      <div className="p-6 space-y-6">
        {/* Exercício Atual */}
        <Card className="bg-gray-900 border-gray-800">
          <CardHeader>
            <CardTitle className="text-white text-center">
              {currentExercise.name}
            </CardTitle>
          </CardHeader>
          <CardContent className="text-center">
            <img 
              src={currentExercise.image} 
              alt={currentExercise.name}
              className="w-32 h-32 mx-auto rounded-lg object-cover mb-4"
            />
            <div className="grid grid-cols-3 gap-4 mb-6">
              <div className="text-center">
                <p className="text-2xl font-bold text-red-500">{currentExercise.sets}</p>
                <p className="text-sm text-gray-400">Séries</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-red-500">{currentExercise.reps}</p>
                <p className="text-sm text-gray-400">Repetições</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-red-500">{currentExercise.weight}kg</p>
                <p className="text-sm text-gray-400">Peso</p>
              </div>
            </div>
            
            <div className="mb-4">
              <Badge variant="secondary" className="bg-gray-800 text-white">
                Série {currentSetCount + 1} de {currentExercise.sets}
              </Badge>
            </div>
          </CardContent>
        </Card>

        {/* Cronômetro de Descanso */}
        {isResting && (
          <Card className="bg-red-500/10 border-red-500/30">
            <CardHeader>
              <CardTitle className="text-red-400 text-center flex items-center justify-center gap-2">
                <Timer className="h-5 w-5" />
                Tempo de Descanso
              </CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <div className="text-6xl font-bold text-red-500 mb-4">
                {formatTime(restTime)}
              </div>
              <div className="flex justify-center gap-4">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={pauseTimer}
                  className="border-red-500 text-red-400 hover:bg-red-500/10"
                >
                  {isTimerRunning ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={resetTimer}
                  className="border-red-500 text-red-400 hover:bg-red-500/10"
                >
                  <RotateCcw className="h-4 w-4" />
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={skipRest}
                  className="border-red-500 text-red-400 hover:bg-red-500/10"
                >
                  <SkipForward className="h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Controles */}
        {!isResting && (
          <div className="space-y-4">
            <Button 
              onClick={completeSet}
              className="w-full bg-red-500 hover:bg-red-600 text-white h-14 text-lg"
            >
              <Check className="mr-2 h-6 w-6" />
              Finalizar Série
            </Button>
            
            <Button 
              variant="outline"
              onClick={goBack}
              className="w-full border-gray-600 text-gray-400 hover:bg-gray-800"
            >
              <X className="mr-2 h-4 w-4" />
              Finalizar Treino
            </Button>
          </div>
        )}

        {/* Próximos Exercícios */}
        {currentExerciseIndex < workout.exercises.length - 1 && (
          <Card className="bg-gray-900 border-gray-800">
            <CardHeader>
              <CardTitle className="text-white text-lg">Próximos Exercícios</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {workout.exercises.slice(currentExerciseIndex + 1, currentExerciseIndex + 3).map((exercise, index) => (
                  <div key={exercise.id} className="flex items-center gap-3 p-2 rounded bg-gray-800/50">
                    <img 
                      src={exercise.image} 
                      alt={exercise.name}
                      className="w-8 h-8 rounded object-cover"
                    />
                    <div>
                      <p className="text-white text-sm font-medium">{exercise.name}</p>
                      <p className="text-gray-400 text-xs">
                        {exercise.sets}x{exercise.reps} • {exercise.weight}kg
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default WorkoutSession;