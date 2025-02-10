export default {
    async fetch(request, env) {
      if (request.method !== "POST") {
        return new Response("Use a POST request to register commands.", {
          status: 405,
        });
      }
  
      // Retrieve secrets from Cloudflare Worker environment
      const token = env.DISCORD_TOKEN;
      const applicationId = env.DISCORD_APPLICATION_ID;
  
      if (!token || !applicationId) {
        return new Response("Missing DISCORD_TOKEN or DISCORD_APPLICATION_ID", {
          status: 500,
        });
      }
  
      // Define the 'hi' command
      const commands = [
        {
          name: "hi",
          description: "The bot says 'Hi' in the chat",
        },
      ];
  
      const url = `https://discord.com/api/v10/applications/${applicationId}/commands`;
      const response = await fetch(url, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bot ${token}`,
        },
        method: "PUT",
        body: JSON.stringify(commands),
      });
  
      if (response.ok) {
        return new Response("Registered 'hi' command successfully!", { status: 200 });
      } else {
        const errorText = await response.text();
        return new Response(`Error registering command: ${errorText}`, {
          status: 500,
        });
      }
    },
  };
  