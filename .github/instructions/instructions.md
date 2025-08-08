
### Stack Tecnológico
- **Frontend**: `/app/client` - React 19.1, TypeScript, Vite 7, TailwindCSS 4.1
- **Backend**: `/app/backend` - FastAPI (Python 3.12), Pydantic, WebSockets
- **IA/LLM**: Ollama + Llama3 (local)
- **Orquestación**: n8n (workflows automatizados)
- **Contenedores**: Docker + Docker Compose
- **Desarrollo**: VS Code, ESLint, Hot Reload


### Servicios Docker
1. **client** - Frontend React (Puerto 5173)
2. **backend** - API FastAPI (Puerto 3000)
3. **n8n** - Plataforma de automatización (Puerto 5678)
4. **ollama** - Servidor de IA local (Puerto 11434)


## Estructura del Proyecto

```
n8n-project/
├── app/
│   ├── client/          # Frontend React + TypeScript
│   │   ├── src/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── vite.config.ts
│   └── backend/         # API FastAPI + Python
│       ├── api/v1/      # Endpoints REST
│       ├── services/    # Lógica de negocio
│       ├── schemas/     # Modelos Pydantic
│       ├── Dockerfile
│       ├── main.py
│       └── requirements.txt
├── n8n-data/           # Datos persistentes de n8n
├── docker-compose.yml  # Configuración de servicios
└── setup.sh           # Script de inicialización
```


## Funcionalidades Principales

### 1. Corrección de Mensajes
- **Endpoint**: `POST /api/v1/chat`
- **WebSocket**: `/ws/chat` (action: "fix")
- **Función**: Corrige gramática y ortografía en inglés

### 2. Respuestas Inteligentes  
- **WebSocket**: `/ws/chat` (action: "response")
- **Función**: Genera respuestas contextualmente apropiadas

### 3. Comunicación en Tiempo Real
- **Tecnología**: WebSockets para chat instantáneo
- **Estado**: Conexión persistente cliente-servidor


## Flujo de Datos

1. **Usuario** envía mensaje desde el frontend
2. **Cliente React** se conecta via WebSocket al backend
3. **FastAPI** procesa la petición y llama al servicio correspondiente
4. **Servicio** formatea el prompt y hace petición HTTP a Ollama
5. **Ollama** ejecuta Llama3 y devuelve la respuesta
6. **Backend** envía respuesta via WebSocket al cliente
7. **Frontend** muestra la respuesta en tiempo real


## Configuración del Entorno

### Variables de Entorno
- `OLLAMA_API_URL`: http://localhost:11434/api/generate
- `TZ`: America/Bogota

### Puertos Utilizados
- **5173**: Frontend (React/Vite)
- **3000**: Backend (FastAPI)
- **5678**: n8n (Automatización)
- **11434**: Ollama (IA/LLM)


## Consideraciones Técnicas y Reglas para la IA

### Convenciones y Reglas Generales
- Mantener la estructura de carpetas y nombres de archivos según el esquema actual.
- Usar siempre rutas relativas o alias definidos en `tsconfig` y `vite.config.ts` para imports en frontend.
- Los archivos de solo tipos/interfaces deben tener extensión `.ts`, no `.tsx`.
- Los endpoints y rutas deben seguir el patrón REST y WebSocket documentado.
- No modificar la configuración de puertos ni rutas de servicios sin justificación.
- Toda nueva funcionalidad debe estar documentada en este archivo.
- No eliminar ni sobrescribir archivos de configuración esenciales (`docker-compose.yml`, `requirements.txt`, etc).
- Mantener la compatibilidad con Docker Compose para levantar todo el stack.
- Validar que los cambios no rompan la comunicación entre frontend, backend y Ollama.

### Seguridad
- Validación de longitud de mensajes (máx. 1000 caracteres)
- Manejo de errores en servicios de IA
- Sanitización de inputs

### Performance
- Timeouts configurados para peticiones a Ollama
- WebSockets para comunicación eficiente
- Caching de modelos en Ollama

### Escalabilidad
- Servicios containerizados
- Backend stateless (FastAPI)
- Frontend SPA optimizado

