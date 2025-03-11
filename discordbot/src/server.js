import { AutoRouter } from 'itty-router';
import {
  InteractionResponseType,
  InteractionType,
  verifyKey,
} from 'discord-interactions';
import { InteractionResponseFlags } from 'discord-interactions';
import { REGISTER, LOGIN, LOGOUT, DELETE, NOTIFY, FORCEORDER, ORDER, CANCELORDER, GETORDERS } from './commands.js';

class JsonResponse extends Response {
  constructor(body, init) {
    const jsonBody = JSON.stringify(body);
    init = init || {
      headers: {
        'content-type': 'application/json;charset=UTF-8',
      },
    };
    super(jsonBody, init);
  }
}

async function sendDiscordMessage(channelForDisc, message, botToken) {
  if (!channelForDisc || !message || !botToken) {    
    throw new Error('Missing required parameters for sending Discord message');
  }

  const url = `https://discord.com/api/v10/channels/${channelForDisc}/messages`;

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bot ${botToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ content: message })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(`Discord API error: ${response.status} ${response.statusText} ${errorData ? JSON.stringify(errorData) : ''}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error sending Discord message:', error);
    throw error;
  }
}

const router = AutoRouter();

router.post('/notification', async (request, env) => {
  try {
    const data = await request.json();


    if (!data.channelToSend || !data.message) {
      return new JsonResponse({
        success: false,
        message: 'Missing required fields: channelId and type are required'
      }, { status: 400 });
    }


    const channelForDisc = data.channelToSend;
    await sendDiscordMessage(
        channelForDisc,
        data.message,
        env.DISCORD_TOKEN
    );

  } catch (error) {
    console.error('Error processing notification:', error);
    return new JsonResponse({
      success: false,
      message: error.message
    }, { status: 500 });
  }
});

router.get('/', (request, env) => {
  return new Response(`👋 ${env.DISCORD_APPLICATION_ID}`);
});

router.post('/', async (request, env) => {

  const { isValid, interaction } = await server.verifyDiscordRequest(
    request,
    env,
  );
  if (!isValid || !interaction) {
    return new Response('Bad request signature.', { status: 401 });
  }

  if (interaction.type === InteractionType.PING) {
    return new JsonResponse({
      type: InteractionResponseType.PONG,
    });
  }

  if (interaction.type === InteractionType.APPLICATION_COMMAND) {
    switch (interaction.data.name.toLowerCase()) {
        case REGISTER.name.toLowerCase():
            return new JsonResponse({
            type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            data: {
                content: REGISTER.description,
                flags: InteractionResponseFlags.EPHEMERAL,
            },
            });
        case LOGIN.name.toLowerCase():
            return new JsonResponse({
            type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            data: {
                content: LOGIN.description,
                flags: InteractionResponseFlags.EPHEMERAL,
            },
            });
        case LOGOUT.name.toLowerCase():
            return new JsonResponse({
            type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            data: {
                content: LOGOUT.description,
                flags: InteractionResponseFlags.EPHEMERAL,
            },
            });
        case DELETE.name.toLowerCase():
            return new JsonResponse({
            type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            data: {
                content: DELETE.description,
                flags: InteractionResponseFlags.EPHEMERAL,
            },
            });
        case NOTIFY.name.toLowerCase():
            return new JsonResponse({
            type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            data: {
                content: NOTIFY.description,
                flags: InteractionResponseFlags.EPHEMERAL,
            },
            });
        case FORCEORDER.name.toLowerCase():
            return new JsonResponse({
            type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            data: {
                content: FORCEORDER.description,
                flags: InteractionResponseFlags.EPHEMERAL,
            },
            });
        case ORDER.name.toLowerCase():
            return new JsonResponse({
            type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            data: {
                content: ORDER.description,
                flags: InteractionResponseFlags.EPHEMERAL,
            },
            });
        case CANCELORDER.name.toLowerCase():
            return new JsonResponse({
            type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            data: {
                content: CANCELORDER.description,
                flags: InteractionResponseFlags.EPHEMERAL,
            },
            });
        case GETORDERS.name.toLowerCase():
            return new JsonResponse({
            type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            data: {
                content: GETORDERS.description,
                flags: InteractionResponseFlags.EPHEMERAL,
            },
            });
        default:
            return new JsonResponse({
            type: InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            data: {
                content: 'not implemeneted',
                flags: InteractionResponseFlags.EPHEMERAL,
            },
            });
    }
  }

  console.error('Unknown Type');
  return new JsonResponse({ error: 'Unknown Type' }, { status: 400 });
});

// Catch-all route (should be defined LAST)
router.all('*', () => new Response('Not Found.', { status: 404 }));

async function verifyDiscordRequest(request, env) {
  const signature = request.headers.get('x-signature-ed25519');
  const timestamp = request.headers.get('x-signature-timestamp');
  const body = await request.text();
  const isValidRequest =
    signature &&
    timestamp &&
    (await verifyKey(body, signature, timestamp, env.DISCORD_PUBLIC_KEY));
  if (!isValidRequest) {
    return { isValid: false };
  }

  return { interaction: JSON.parse(body), isValid: true };
}

const server = {
  verifyDiscordRequest,
  fetch: router.fetch,
};

export default server;