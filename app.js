const { createBot, createFlow, addKeyword } = require('@bot-whatsapp/bot');
const BaileysProvider = require('@bot-whatsapp/provider/baileys');
const JsonFileAdapter = require('@bot-whatsapp/database/json');
const axios = require('axios');

// Flujo principal
const flujoIA = addKeyword(['hola', 'ia', 'inteligencia'])
  .addAction(async (ctx, { flowDynamic, fallBack }) => {
    try {
      const userMessage = ctx.body;

      const response = await axios.post('http://127.0.0.1:5000/ask', {
        message: userMessage
      }, {
        timeout: 18000
      });

      const aiResponse = response.data?.response || '🤖 Lo siento, no tengo una respuesta clara.';
      return await flowDynamic([{ body: aiResponse }]);
    } catch (err) {
      console.error('Error al consultar la IA:', err.message);
      return fallBack('⚠️ Hubo un problema al procesar tu solicitud, por favor pregunta de nuevo .');
    }
  });

// Inicialización del bot
const main = async () => {
  const adapterDB = new JsonFileAdapter();
  const adapterFlow = createFlow([flujoIA]);
  const adapterProvider = new BaileysProvider();

  await createBot({
    flow: adapterFlow,
    provider: adapterProvider,
    database: adapterDB
  });
};

main();


