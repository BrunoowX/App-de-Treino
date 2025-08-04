import React from 'react';
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
  ChevronRight
} from 'lucide-react';
import { mockWorkouts, mockProgressData } from '../../data/mockData';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  
  const todayWorkout = mockWorkouts.find(w => w.status === 'active');
  const completedExercises = todayWorkout?.exercises.filter(e => e.completed).length || 0;
  const totalExercises = todayWorkout?.exercises.length || 0;

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
        {todayWorkout && (
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
                    <span className="text-white">{todayWorkout.progress}%</span>
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
                  Continuar Treino
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Lista de Exercícios */}
        <Card className="bg-gray-900 border-gray-800">
          <CardHeader>
            <CardTitle className="text-white">Exercícios de Hoje</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {todayWorkout?.exercises.map((exercise, index) => (
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
                    </div>
                  </div>
                  <ChevronRight className="h-5 w-5 text-gray-400" />
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Mini Gráfico de Progresso */}
        <Card className="bg-gray-900 border-gray-800">
          <CardHeader>
            <CardTitle className="text-white">Progresso Semanal</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-end justify-between h-24 gap-2">
              {mockProgressData.slice(-7).map((data, index) => (
                <div key={index} className="flex flex-col items-center gap-2">
                  <div 
                    className="bg-red-500 w-6 rounded-t transition-all duration-300 hover:bg-red-400"
                    style={{ 
                      height: `${(data.volume / Math.max(...mockProgressData.map(d => d.volume))) * 100}%`,
                      minHeight: '8px'
                    }}
                  ></div>
                  <span className="text-xs text-gray-400 rotate-45 origin-center">
                    {data.week.replace('Sem ', '')}
                  </span>
                </div>
              ))}
            </div>
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