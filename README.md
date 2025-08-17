# EnglisChat - Chat de Inglés con IA Local

Esto es básicamente una app de chat para practicar inglés que usa Ollama + Mistral corriendo local en Docker. Nada de APIs externas, nada de tokens, nada de límites. Solo tu CPU trabajando.

![English Chat Interface](./assets/banner.png)

## ¿Qué hace?

- **Chat en tiempo real** con IA para practicar inglés
- **Corrección automática** de gramática y palabras  
- **Respuestas conversacionales** para mantener la charla
- **Todo local** - sin internet, sin APIs, sin costos
- **WebSockets** para chat fluido
- **Docker** para no volverse loco con dependencias

## Stack Tecnológico

### Frontend
- **React 19.1** + TypeScript + Vite
- **TailwindCSS** para estilos sin llorar
- **WebSockets** para chat en tiempo real
- **React Router** para navegación

### Backend  
- **FastAPI** + Python 3.12
- **WebSockets** bidireccionales
- **httpx** para peticiones async
- **Pydantic** para validación

### IA y Modelos
- **Ollama** corriendo en Docker
- **Mistral** (optimizado para CPU sin GPU)
- **Prompts optimizados** para respuestas rápidas (15 palabras max)

### Infraestructura
- **Docker Compose** para orquestar todo
- **n8n** (porque estaba experimentando)
- **Nginx** reverse proxy (próximamente)

## Inicio Rápido

```bash
# Clona esto
git clone https://github.com/tu-usuario/n8n-ollama-local.git
cd n8n-ollama-local

# Levanta todo (incluye descargar Mistral automáticamente)
./setup.sh up mistral

# O si ya tienes modelos instalados
./setup.sh up

# Ver estado de los servicios
./setup.sh status

# Ver logs en tiempo real
./setup.sh logs ollama -f
```

**URLs después de levantar:**
- Chat: http://localhost:5173
- Backend API: http://localhost:3000
- n8n: http://localhost:5678
- Ollama: http://localhost:11434

## El Script setup.sh

Usa este script para manipular el proyecto de formas mas sencilla.

```bash
# Ver todos los comandos disponibles
./setup.sh

# Levantar servicios
./setup.sh up                    # Solo servicios
./setup.sh up llama3            # Servicios + instalar llama3

# Gestión de modelos
./setup.sh model install mistral
./setup.sh model list

# Control de servicios  
./setup.sh stop backend         # Parar solo backend
./setup.sh restart ollama       # Reiniciar ollama
./setup.sh status               # Ver estado general

# Limpieza
./setup.sh clean soft           # Bajar contenedores
./setup.sh clean hard           # Bajar + borrar volúmenes

# Logs y debugging
./setup.sh logs client -f       # Logs del frontend
./setup.sh logs backend         # Logs del backend
```

**Lo que hace internamente:**
1. Gestiona Docker Compose sin que tengas que recordar comandos
2. Espera a que Ollama esté listo antes de instalar modelos
3. Descarga modelos automáticamente si los especificas
4. Maneja errores de red y timeouts
5. Te da URLs para acceder a todo

## Optimizaciones para CPU

Este proyecto esta pensado para trabajar con un modelo pequeño, para dispositivos con pocos recursos, aun asi existe la posibilidad de usar modelos de mayor
capacidad, recuerda que esto se corre directamente en tu CPU/GPU, asi que ten en cuenta esto al momento de probarlo.

### Configuración Ollama
```yaml
# En docker-compose.yml
environment:
  - OLLAMA_CONTEXT_LENGTH=4096      # Contexto corto = más rápido
  - OLLAMA_NUM_PARALLEL=1          # Una request a la vez
  - OLLAMA_KEEP_ALIVE=30m          # Mantener modelo en memoria
```

### Prompts Optimizados
```python
# Para correcciones (máx 12 palabras)
prompt = f'Correct any grammar or word mistakes in "{message}". If perfect, reply "Looks great!". Max 12 words.'

# Para respuestas (máx 15 palabras) 
prompt = f'Reply to "{message}" with a fun, creative answer (max 15 words). Ask a playful question.'
```

### Recursos Docker
```yaml
# 6GB RAM, 4 CPUs para Ollama
deploy:
  resources:
    limits:
      memory: 6G
      cpus: '4.0'
```

**Resultado:** Respuestas en 3-8 segundos en lugar de 15+ segundos.

## Estructura del Proyecto

```
 n8n-project/
├──  docker-compose.yml       # Orquestación de servicios
├──  setup.sh                 # Script de gestión principal  
├──  app/
│   ├──  client/              # React + TypeScript
│   │   ├──  src/pages/chat/  # Componente principal de chat
│   │   ├──  src/components/  # Componentes reutilizables
│   │   └──  src/utils/       # WebSocket hooks
│   └──  backend/             # FastAPI + Python
│       ├──  api/v1/          # Endpoints REST y WebSocket
│       ├──  services/        # Lógica de Ollama
│       └──  test/            # Tests unitarios
└── 📁 n8n-data/               # Datos persistentes de n8n
```

## Funcionalidades

###  Chat Bidireccional
- **Envías:** "I are good today"
- **IA corrige:** "Grammar error: 'am' not 'are'. Corrected: I am good today"  
- **IA responde:** "That's great! What's making your day so good?"

###  Optimizaciones
- **Semáforo:** Solo 1 request a Ollama simultánea
- **Timeouts inteligentes:** 8s, 11s, 14s con reintentos
- **Prompts cortos:** Menos tokens = más velocidad
- **Context management:** 4096 tokens máximo

## Disclaimer

Esto no es para producción. Es un experimento para:
-  Aprender sobre modelos locales
-  Practicar WebSockets bidireccionales  
-  Optimizar prompts y performance
-  Entender Docker networking
-  Probar arquitecturas de microservicios

Si te sirve para aprender algo, perfecto. Si encuentras bugs o mejoras, los PRs son bienvenidos.

No soy experto en ML/AI, solo quería que funcionara rápido en mi laptop sin GPU. Si ves algo que se puede optimizar mejor, avísame.

## Próximas mejoras

- [ ] Nginx reverse proxy
- [ ] Autenticación básica
- [ ] Más modelos soportados
- [ ] Métricas de performance
- [ ] Deploy con Traefik
- [ ] Conversation history

---

**TL;DR:** Chat de inglés con IA local usando React + FastAPI + Ollama en Docker. Sin APIs externas, sin costos, sin límites. Solo para aprender y practicar.
