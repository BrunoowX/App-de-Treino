import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { 
  TrendingUp, 
  Calendar, 
  Target,
  Award,
  BarChart3,
  Activity
} from 'lucide-react';
import { mockProgressData, mockWorkouts } from '../data/mockData';

const ProgressPage = () => {
  const [selectedPeriod, setSelectedPeriod] = useState('week');

  const totalVolume = mockProgressData.reduce((acc, data) => acc + data.volume, 0);
  const avgWeight = Math.round(mockProgressData.reduce((acc, data) => acc + data.weight, 0) / mockProgressData.length);
  const completedWorkouts = mockWorkouts.filter(w => w.status === 'completed').length;

  const achievements = [
    { title: '7 dias seguidos', description: 'Sequência perfeita!', icon: Award, color: 'text-yellow-500' },
    { title: 'Primeira meta', description: '50 treinos concluídos', icon: Target, color: 'text-green-500' },
    { title: 'Força crescente', description: '+20kg no supino', icon: TrendingUp, color: 'text-blue-500' }
  ];

  return (
    <div className="min-h-screen bg-black text-white pb-20">
      {/* Header */}
      <div className="bg-gradient-to-r from-gray-900 to-black p-6">
        <h1 className="text-2xl font-bold text-white mb-2">Seu Progresso</h1>
        <p className="text-gray-400">Acompanhe sua evolução</p>
      </div>

      <div className="p-6 space-y-6">
        {/* Stats Cards */}
        <div className="grid grid-cols-2 gap-4">
          <Card className="bg-gray-900 border-gray-800">
            <CardContent className="p-4 text-center">
              <BarChart3 className="h-8 w-8 mx-auto mb-2 text-red-500" />
              <p className="text-2xl font-bold text-white">{totalVolume.toLocaleString()}</p>
              <p className="text-sm text-gray-400">Volume Total</p>
            </CardContent>
          </Card>
          
          <Card className="bg-gray-900 border-gray-800">
            <CardContent className="p-4 text-center">
              <Activity className="h-8 w-8 mx-auto mb-2 text-green-500" />
              <p className="text-2xl font-bold text-white">{avgWeight}kg</p>
              <p className="text-sm text-gray-400">Peso Médio</p>
            </CardContent>
          </Card>
        </div>

        {/* Gráfico Principal */}
        <Card className="bg-gray-900 border-gray-800">
          <CardHeader>
            <CardTitle className="text-white">Volume Semanal</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {/* Gráfico de Barras */}
              <div className="flex items-end justify-between h-48 gap-2">
                {mockProgressData.map((data, index) => (
                  <div key={index} className="flex flex-col items-center gap-2 flex-1">
                    <div className="relative w-full">
                      <div 
                        className="bg-gradient-to-t from-red-600 to-red-400 w-full rounded-t transition-all duration-500 hover:from-red-500 hover:to-red-300"
                        style={{ 
                          height: `${(data.volume / Math.max(...mockProgressData.map(d => d.volume))) * 100}%`,
                          minHeight: '12px'
                        }}
                      />
                      <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 text-xs text-white font-medium">
                        {data.volume}
                      </div>
                    </div>
                    <span className="text-xs text-gray-400 text-center">
                      {data.week}
                    </span>
                  </div>
                ))}
              </div>
              
              {/* Legenda */}
              <div className="flex justify-center gap-6 text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-red-500 rounded"></div>
                  <span className="text-gray-400">Volume (kg)</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Tabs para diferentes métricas */}
        <Tabs defaultValue="volume" className="w-full">
          <TabsList className="grid w-full grid-cols-2 bg-gray-800">
            <TabsTrigger value="volume" className="text-white">Volume</TabsTrigger>
            <TabsTrigger value="strength" className="text-white">Força</TabsTrigger>
          </TabsList>
          
          <TabsContent value="volume" className="space-y-4">
            <Card className="bg-gray-900 border-gray-800">
              <CardHeader>
                <CardTitle className="text-white">Análise de Volume</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center p-3 bg-gray-800 rounded-lg">
                    <span className="text-gray-400">Volume desta semana</span>
                    <span className="text-white font-bold">3,800 kg</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-gray-800 rounded-lg">
                    <span className="text-gray-400">Média semanal</span>
                    <span className="text-white font-bold">3,200 kg</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-green-500/10 border border-green-500/30 rounded-lg">
                    <span className="text-gray-400">Crescimento</span>
                    <Badge className="bg-green-500 text-white">+18.7%</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          
          <TabsContent value="strength" className="space-y-4">
            <Card className="bg-gray-900 border-gray-800">
              <CardHeader>
                <CardTitle className="text-white">Evolução de Força</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    { exercise: 'Supino Reto', current: '85kg', previous: '80kg', change: '+5kg' },
                    { exercise: 'Agachamento', current: '120kg', previous: '115kg', change: '+5kg' },
                    { exercise: 'Levantamento Terra', current: '140kg', previous: '135kg', change: '+5kg' }
                  ].map((item, index) => (
                    <div key={index} className="flex justify-between items-center p-3 bg-gray-800 rounded-lg">
                      <div>
                        <p className="text-white font-medium">{item.exercise}</p>
                        <p className="text-gray-400 text-sm">{item.previous} → {item.current}</p>
                      </div>
                      <Badge className="bg-green-500 text-white">{item.change}</Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Conquistas */}
        <Card className="bg-gray-900 border-gray-800">
          <CardHeader>
            <CardTitle className="text-white">Conquistas Recentes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {achievements.map((achievement, index) => {
                const Icon = achievement.icon;
                return (
                  <div 
                    key={index}
                    className="flex items-center gap-4 p-3 bg-gray-800/50 rounded-lg border border-gray-700 hover:border-red-500/30 transition-colors"
                  >
                    <div className="bg-gray-800 p-2 rounded-lg">
                      <Icon className={`h-6 w-6 ${achievement.color}`} />
                    </div>
                    <div>
                      <p className="font-medium text-white">{achievement.title}</p>
                      <p className="text-sm text-gray-400">{achievement.description}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>

        {/* Calendário de Treinos */}
        <Card className="bg-gray-900 border-gray-800">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <Calendar className="h-5 w-5" />
              Últimos 30 Dias
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-7 gap-2">
              {Array.from({ length: 30 }, (_, i) => {
                const hasWorkout = Math.random() > 0.3; // 70% chance de ter treino
                return (
                  <div
                    key={i}
                    className={`aspect-square rounded-lg flex items-center justify-center text-xs font-medium transition-colors ${
                      hasWorkout 
                        ? 'bg-red-500 text-white' 
                        : 'bg-gray-800 text-gray-500'
                    }`}
                  >
                    {30 - i}
                  </div>
                );
              })}
            </div>
            <div className="flex justify-between items-center mt-4 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-red-500 rounded"></div>
                <span className="text-gray-400">Dia de treino</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-gray-800 rounded"></div>
                <span className="text-gray-400">Descanso</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ProgressPage;