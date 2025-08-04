import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Progress } from '../ui/progress';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '../ui/avatar';
import { 
  Play, 
  Calendar, 
  Target, 
  Flame,
  Trophy,
  ChevronRight,
  Loader2
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { api } from '../../services/api';
import { useToast } from '../../hooks/use-toast';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();
  
  const [todayWorkout, setTodayWorkout] = useState(null);
  const [weeklyProgress, setWeeklyProgress] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Load today's workout and weekly progress in parallel
      const [workoutResponse, progressResponse] = await Promise.all([
        api.workouts.getToday().catch(() => ({ data: null })),
        api.progress.getWeekly().catch(() => ({ data: [] }))
      ]);

      setTodayWorkout(workoutResponse.data);
      setWeeklyProgress(progressResponse.data);
      
    } catch (error) {
      console.error('Erro ao carregar dados do dashboard:', error);
      toast({
        title: "Erro",
        description: "Não foi possível carregar os dados do dashboard",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin text-red-500 mx-auto mb-4" />
          <p className="text-gray-400">Carregando seu treino...</p>
        </div>
      </div>
    );
  }

  const completedExercises = todayWorkout?.exercises?.filter(e => e.completed).length || 0;
  const totalExercises = todayWorkout?.exercises?.length || 0;

  const stats = [
    { label: 'Sequência', value: user?.streak || 0, icon: Flame, color: 'text-orange-500' },
    { label: 'Treinos', value: user?.totalWorkouts || 0, icon: Trophy, color: 'text-yellow-500' },
    { label: 'Meta Semanal', value: '5/7', icon: Target, color: 'text-green-500' }
  ];

  return (
    <div className="min-h-screen bg-black text-white pb-20">
      {/* Header */}
      <div className="bg-gradient-to-r from-gray-900 to-black p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-white">
              Olá, {user?.name}! 👋
            </h1>
            <p className="text-gray-400 mt-1">Pronto para treinar hoje?</p>
          </div>
          <Avatar className="h-12 w-12 ring-2 ring-red-500">
            <AvatarImage src={user?.avatar} alt={user?.name} />
            <AvatarFallback className="bg-red-500 text-white">
              {user?.name?.charAt(0)}
            </AvatarFallback>
          </Avatar>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4">
          {stats.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <Card key={index} className="bg-gray-800/50 border-gray-700">
                <CardContent className="p-4 text-center">
                  <Icon className={`h-6 w-6 mx-auto mb-2 ${stat.color}`} />
                  <p className="text-2xl font-bold text-white">{stat.value}</p>
                  <p className="text-xs text-gray-400">{stat.label}</p>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Treino de Hoje */}
        {todayWorkout ? (
          <Card className="bg-gray-900 border-gray-800">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-white flex items-center gap-2">
                    <Calendar className="h-5 w-5 text-red-500" />
                    Treino de Hoje
                  </CardTitle>
                  <p className="text-gray-400 mt-1">{todayWorkout.name}</p>
                </div>
                <Badge variant="secondary" className="bg-red-500/20 text-red-400">
                  {completedExercises}/{totalExercises} concluídos
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-400">Progresso</span>
                    <span className="text-white">{Math.round(todayWorkout.progress)}%</span>
                  </div>
                  <Progress 
                    value={todayWorkout.progress} 
                    className="h-3 bg-gray-800"
                  />
                </div>
                
                <Button 
                  onClick={() => navigate('/workout-session', { state: { workout: todayWorkout } })}
                  className="w-full bg-red-500 hover:bg-red-600 text-white"
                >
                  <Play className="mr-2 h-4 w-4" />
                  {todayWorkout.progress > 0 ? 'Continuar Treino' : 'Iniciar Treino'}
                </Button>
              </div>
            </CardContent>
          </Card>
        ) : (
          <Card className="bg-gray-900 border-gray-800">
            <CardContent className="p-6 text-center">
              <Calendar className="h-12 w-12 mx-auto mb-4 text-gray-600" />
              <p className="text-gray-400 mb-4">Nenhum treino programado para hoje</p>
              <Button 
                onClick={() => navigate('/workouts')}
                variant="outline"
                className="border-red-500 text-red-400 hover:bg-red-500/10"
              >
                Ver Treinos Disponíveis
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Lista de Exercícios */}
        {todayWorkout && todayWorkout.exercises && (
          <Card className="bg-gray-900 border-gray-800">
            <CardHeader>
              <CardTitle className="text-white">Exercícios de Hoje</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {todayWorkout.exercises.map((exercise, index) => (
                  <div 
                    key={exercise.id}
                    className={`flex items-center justify-between p-3 rounded-lg border transition-all duration-200 ${
                      exercise.completed 
                        ? 'bg-green-500/10 border-green-500/30' 
                        : 'bg-gray-800/50 border-gray-700 hover:border-red-500/50'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div className="relative">
                        <img 
                          src={exercise.image} 
                          alt={exercise.name}
                          className="w-12 h-12 rounded-lg object-cover"
                        />
                        {exercise.completed && (
                          <div className="absolute -top-1 -right-1 bg-green-500 rounded-full p-1">
                            <div className="w-2 h-2 bg-white rounded-full"></div>
                          </div>
                        )}
                      </div>
                      <div>
                        <p className="font-medium text-white">{exercise.name}</p>
                        <p className="text-sm text-gray-400">
                          {exercise.sets}x{exercise.reps} • {exercise.weight}kg
                        </p>
                        {exercise.completedSets > 0 && (
                          <p className="text-xs text-green-400">
                            {exercise.completedSets}/{exercise.sets} séries concluídas
                          </p>
                        )}
                      </div>
                    </div>
                    <ChevronRight className="h-5 w-5 text-gray-400" />
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Mini Gráfico de Progresso */}
        <Card className="bg-gray-900 border-gray-800">
          <CardHeader>
            <CardTitle className="text-white">Progresso Semanal</CardTitle>
          </CardHeader>
          <CardContent>
            {weeklyProgress.length > 0 ? (
              <div className="flex items-end justify-between h-24 gap-2">
                {weeklyProgress.slice(-7).map((data, index) => (
                  <div key={index} className="flex flex-col items-center gap-2">
                    <div 
                      className="bg-red-500 w-6 rounded-t transition-all duration-300 hover:bg-red-400"
                      style={{ 
                        height: `${(data.volume / Math.max(...weeklyProgress.map(d => d.volume))) * 100}%`,
                        minHeight: '8px'
                      }}
                    ></div>
                    <span className="text-xs text-gray-400 rotate-45 origin-center">
                      {data.week.replace('Sem ', '')}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-gray-400">Dados de progresso não disponíveis</p>
                <p className="text-sm text-gray-500 mt-1">Complete alguns treinos para ver seu progresso</p>
              </div>
            )}
            <Button 
              variant="ghost" 
              className="w-full mt-4 text-red-400 hover:text-red-300 hover:bg-red-500/10"
              onClick={() => navigate('/progress')}
            >
              Ver detalhes completos
              <ChevronRight className="ml-2 h-4 w-4" />
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;