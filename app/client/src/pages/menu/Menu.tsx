import Chat from '@pages/chat/Chat';
import { Card } from  "../../components/sidemenu/Card"

export default function Menu() {
  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-slate-50 via-white to-blue-50 flex">
      <aside className="w-52 border-r bg-white/60 backdrop-blur flex flex-col">
        <div className="px-4 py-4 border-b">
          <div className='flex'>
            <img src="/icon_english.webp" alt="EnglishChat" className="w-10 mb-4"/>
            <h1 className="text-base font-semibold tracking-tight mt-2.5 me-1.5">EnglishChat</h1>
          </div>
          <p className="text-[10px] text-slate-500 mt-1">Tu rincón para practicar</p>
        </div>
        <div className="p-3 border-t text-[10px] text-slate-500 leading-snug">
          <p>CPU Mode • Local</p>
          <p>Ligero y privado</p>
        </div>
      </aside>
      <main className="flex-1 flex flex-col">
        <div className="flex-1 grid grid-cols-1 lg:grid-cols-[minmax(0,1fr)_260px] gap-4 p-4 md:p-6">
          <section className="flex flex-col min-h-0">
            <Chat/>
          </section>
          <aside className="hidden lg:flex flex-col gap-4">
            <Card
              title="Tip"
              text="Usa prompts cortos y precisos, prompts muy largos o complicados pueden tardar mucho o fallar."
              color="blue"
            />
            <Card
              title="Modelo Mistral"
              text="Mistral es un modelo de IA rápido y eficiente, ideal para correcciones y respuestas en inglés. Funciona localmente, sin enviar tus datos a la nube."
              color="green"
            />
            <Card
              title="¿Cómo usar el chat?"
              text="Escribe tu frase en inglés y recibirás corrección y respuesta divertida."
              color="gray"
            />
            <Card
              title="Privacidad"
              text="Tus mensajes no salen de tu equipo. Todo el procesamiento es local."
              color="yellow"
            />
            <Card
              title="Próximamente"
              text="- Estadísticas de progreso\n- Modo conversación larga\n- Personalización de nivel"
              color="pink"
            />
          </aside>
        </div>
      </main>
    </div>
  );
}

