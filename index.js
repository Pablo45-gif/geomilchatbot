const { createBot, createFlow, addKeyword } = require('@bot-whatsapp/bot');
const BaileysProvider = require('@bot-whatsapp/provider/baileys');
const JsonFileAdapter = require('@bot-whatsapp/database/json');
const axios = require('axios');

// 🔹 FLUJO SALUDO PRINCIPAL
const flow2 = addKeyword(['hola', 'buen día', 'buen dia', 'buenos días', 'buenas tardes', 'buenas noches', 'buenos dias'])
  .addAnswer('🙌 Hola, estás en contacto con el asistente virtual IA de Geomil Group.')
  .addAnswer(
    'Tienes preguntas de envíos o cotizaciones, solo escribe "*IA + (tu pregunta)*" y te contestaremos en segundos',
    'Ejemplo: IA cuanto sale el costo a Madrid agencia'
  )
  .addAnswer('Recuerda ser claro y detallar muy bien tu pregunta para darte una respuesta corta y concisa.');

// 🔹 FLUJO IA
const flujoIA = addKeyword(['ia', 'inteligencia'])
  .addAction(async (ctx, { flowDynamic, fallBack }) => {
    try {
      const userMessage = ctx.body;

      const response = await axios.post('http://127.0.0.1:5000/ask', {  // Cambia aquí si el backend está remoto
        message: userMessage
      }, { timeout: 22000 });

      const aiResponse = response.data?.response || '🤖 Lo siento, no tengo una respuesta clara.';
      return await flowDynamic([{ body: aiResponse }]);
    } catch (err) {
      console.error('Error al consultar la IA:', err.message);
      return fallBack('⚠️ Hubo un problema al procesar tu solicitud, por favor pregunta de nuevo.');
    }
  });

// 🔹 FLUJO AGRADECIMIENTOS
const flowGracias = addKeyword([
  'gracias', 'ok', 'grcs', 'grcs!', 'grx', 'grasias', 'grac', 'mil grcs',
  'ok gracias', 'ok grcs', 'oky gracias', 'grxs', 'okas gracias', 'muxas gracias',
  'muchas grcs', 'gracias x la ayuda', 'grcs x la info', 'grcs x responder', 'muy amable',
  'ma gracias', 'se agradece', 't lo agradesco', 't lo agradezco', 'se lo agradezco',
  'le agradezco', 'agradecido', 'quedo agradecido', 'grcs por todo', 'grcs x todo',
  'todo bien gracias', 'todo claro gracias', 'todo ok gracias', 'vale gracias',
  'valió gracias', 'grcs bro', 'grcs pana', 'listo gracias', 'listo grcs', 'ya gracias',
  'ya está gracias', 'perfecto gracias', 'ok perfecto', 'ya todo claro', 'ya está todo bien',
  'grcs estimado', 'grcs estimada', 'gracias estimado', 'gracias estimada', 'exelente gracias'
])
  .addAnswer([
    '🚀 Es un gusto ayudarte. Recuerda que Geomil hace envíos internacionales de forma rápida y segura.'
  ]);

// 🔹 Inicialización del bot
const main = async () => {
  const adapterDB = new JsonFileAdapter();
  const adapterFlow = createFlow([flujoIA, flow2, flowGracias]);
  const adapterProvider = new BaileysProvider();

  await createBot({
    flow: adapterFlow,
    provider: adapterProvider,
    database: adapterDB
  });
};

// Ejecutar y avisar al iniciar
main().then(() => {
  console.log('🤖 Bot iniciado y listo para recibir mensajes.');
}).catch(err => {
  console.error('Error iniciando el bot:', err);
});