// Mock data para o aplicativo de fitness
export const mockUser = {
  id: '1',
  name: 'Carlos',
  email: 'carlos@example.com',
  avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face',
  totalWorkouts: 45,
  streak: 7
};

export const mockWorkouts = [
  {
    id: '1',
    name: 'Peito e Tríceps',
    date: new Date().toISOString(),
    status: 'active',
    progress: 65,
    exercises: [
      {
        id: '1',
        name: 'Supino Reto',
        sets: 4,
        reps: 10,
        weight: 80,
        restTime: 90,
        completed: true,
        image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=80&h=80&fit=crop'
      },
      {
        id: '2',
        name: 'Supino Inclinado',
        sets: 4,
        reps: 8,
        weight: 70,
        restTime: 90,
        completed: true,
        image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=80&h=80&fit=crop'
      },
      {
        id: '3',
        name: 'Crucifixo',
        sets: 3,
        reps: 12,
        weight: 25,
        restTime: 60,
        completed: false,
        image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=80&h=80&fit=crop'
      },
      {
        id: '4',
        name: 'Tríceps Testa',
        sets: 4,
        reps: 12,
        weight: 30,
        restTime: 60,
        completed: false,
        image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=80&h=80&fit=crop'
      }
    ]
  },
  {
    id: '2',
    name: 'Costas e Bíceps',
    date: new Date(Date.now() - 86400000).toISOString(),
    status: 'completed',
    progress: 100,
    exercises: [
      {
        id: '5',
        name: 'Puxada Frontal',
        sets: 4,
        reps: 10,
        weight: 65,
        restTime: 90,
        completed: true
      }
    ]
  }
];

export const mockProgressData = [
  { week: 'Sem 1', volume: 2500, weight: 320 },
  { week: 'Sem 2', volume: 2800, weight: 335 },
  { week: 'Sem 3', volume: 3100, weight: 350 },
  { week: 'Sem 4', volume: 3400, weight: 365 },
  { week: 'Sem 5', volume: 3200, weight: 370 },
  { week: 'Sem 6', volume: 3600, weight: 385 },
  { week: 'Sem 7', volume: 3800, weight: 400 }
];

export const mockExerciseLibrary = [
  {
    id: '1',
    name: 'Supino Reto',
    muscle: 'Peito',
    category: 'Compound',
    image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=300&h=200&fit=crop'
  },
  {
    id: '2',
    name: 'Agachamento',
    muscle: 'Pernas',
    category: 'Compound',
    image: 'https://images.unsplash.com/photo-1566241440091-ec10de8db2e1?w=300&h=200&fit=crop'
  }
];