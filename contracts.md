# Contratos de API - Aplicativo de Fitness

## Visão Geral
Este documento define os contratos entre frontend e backend para substituir os dados mockados por implementação real.

## 1. Autenticação

### POST /api/auth/register
```json
Request:
{
  "name": "string",
  "email": "string", 
  "password": "string"
}

Response:
{
  "success": true,
  "user": {
    "id": "string",
    "name": "string",
    "email": "string",
    "avatar": "string",
    "totalWorkouts": 0,
    "streak": 0
  },
  "token": "string"
}
```

### POST /api/auth/login
```json
Request:
{
  "email": "string",
  "password": "string"
}

Response:
{
  "success": true,
  "user": {
    "id": "string",
    "name": "string", 
    "email": "string",
    "avatar": "string",
    "totalWorkouts": "number",
    "streak": "number"
  },
  "token": "string"
}
```

## 2. Usuário

### GET /api/user/profile
```json
Headers: { "Authorization": "Bearer <token>" }

Response:
{
  "id": "string",
  "name": "string",
  "email": "string", 
  "avatar": "string",
  "totalWorkouts": "number",
  "streak": "number",
  "createdAt": "datetime"
}
```

## 3. Treinos

### GET /api/workouts
```json
Headers: { "Authorization": "Bearer <token>" }

Response:
[
  {
    "id": "string",
    "name": "string", 
    "date": "datetime",
    "status": "active|completed|pending",
    "progress": "number",
    "exercises": [
      {
        "id": "string",
        "name": "string",
        "sets": "number",
        "reps": "number", 
        "weight": "number",
        "restTime": "number",
        "completed": "boolean",
        "image": "string"
      }
    ]
  }
]
```

### GET /api/workouts/today
```json
Headers: { "Authorization": "Bearer <token>" }

Response: {
  "id": "string",
  "name": "string",
  "date": "datetime", 
  "status": "active",
  "progress": "number",
  "exercises": [...]
}
```

### POST /api/workouts/{workoutId}/exercises/{exerciseId}/complete-set
```json
Headers: { "Authorization": "Bearer <token>" }

Request:
{
  "setNumber": "number",
  "weight": "number",
  "reps": "number"
}

Response:
{
  "success": true,
  "exercise": {
    "id": "string",
    "completedSets": "number",
    "totalSets": "number"
  }
}
```

## 4. Progresso

### GET /api/progress/weekly
```json
Headers: { "Authorization": "Bearer <token>" }

Response:
[
  {
    "week": "string",
    "volume": "number", 
    "weight": "number",
    "workouts": "number"
  }
]
```

### GET /api/progress/stats  
```json
Headers: { "Authorization": "Bearer <token>" }

Response:
{
  "totalVolume": "number",
  "avgWeight": "number", 
  "completedWorkouts": "number",
  "currentStreak": "number"
}
```

## 5. Dados Mockados a Substituir

### Frontend Mock Data (/app/frontend/src/data/mockData.js):
- **mockUser**: Será substituído por dados reais do usuário logado
- **mockWorkouts**: Será substituído por GET /api/workouts  
- **mockProgressData**: Será substituído por GET /api/progress/weekly
- **mockExerciseLibrary**: Será mantido como dados estáticos ou movido para backend

### AuthContext (/app/frontend/src/contexts/AuthContext.js):
- **login()**: Integrar com POST /api/auth/login
- **register()**: Integrar com POST /api/auth/register  
- **Persistência**: Usar JWT token no localStorage

## 6. Estrutura de Banco de Dados

### Users Collection:
```javascript
{
  _id: ObjectId,
  name: String,
  email: String (unique),
  passwordHash: String,
  avatar: String,
  totalWorkouts: Number,
  streak: Number,
  createdAt: Date
}
```

### Workouts Collection:
```javascript
{
  _id: ObjectId,
  userId: ObjectId,
  name: String,
  date: Date,
  status: String, // 'active', 'completed', 'pending'
  progress: Number, // 0-100
  exercises: [
    {
      id: String,
      name: String,
      sets: Number,
      reps: Number, 
      weight: Number,
      restTime: Number,
      completed: Boolean,
      completedSets: Number,
      image: String
    }
  ],
  createdAt: Date
}
```

### WorkoutSessions Collection:
```javascript
{
  _id: ObjectId,
  userId: ObjectId,
  workoutId: ObjectId, 
  exercises: [
    {
      exerciseId: String,
      sets: [
        {
          setNumber: Number,
          weight: Number,
          reps: Number,
          completedAt: Date
        }
      ]
    }
  ],
  startedAt: Date,
  completedAt: Date
}
```

## 7. Integração Frontend-Backend

### Arquivos a Modificar:
1. **AuthContext.js**: Substituir mock calls por axios calls reais
2. **Dashboard.js**: Buscar dados reais de treinos e usuário  
3. **WorkoutSession.js**: Integrar com endpoints de progresso de treino
4. **ProgressPage.js**: Consumir dados reais de progresso

### Próximos Passos:
1. Implementar modelos de dados no backend
2. Criar endpoints de autenticação com JWT
3. Implementar CRUD de treinos
4. Adicionar middleware de autenticação
5. Substituir dados mockados no frontend por chamadas reais
6. Testar integração completa