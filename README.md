# TooGoodToGo Discord Bot

A Discord bot that helps you monitor and order from TooGoodToGo stores automatically.

## Features

- Get notifications when items become available
- Automatically place orders
- Force order items when they become available
- Manage your TGTG account through Discord

## Commands

- `/register` - Create a new TGTG account connection
- `/login` - Connect to your existing TGTG account
- `/logout` - Disconnect from your TGTG account
- `/delete` - Remove your account data
- `/notify` - Set up notifications for stores
- `/forceorder` - Set up automatic ordering when items become available
- `/order` - Place an order for a specific item
- `/cancelorder` - Cancel a pending order
- `/getorders` - List your current orders

## Setup

1. Install dependencies:
   ```
   npm install
   pip install tgtg requests paramiko scp flask
   ```

2. Set up environment variables:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   DISCORD_APPLICATION_ID=your_discord_application_id
   DISCORD_PUBLIC_KEY=your_discord_public_key
   ```

3. Register Discord commands:
   ```
   node register.js
   ```

4. Start the Discord bot server

## Architecture

- JavaScript Discord bot for handling commands
- Python backend for interacting with the TGTG API
- Deployable to both AWS and Azure for redundancy

## How It Works

1. User sends a command in Discord
2. Discord bot processes the command
3. Command is forwarded to TGTG client
4. Client interacts with TGTG API
5. Results are sent back to Discord

## Notification System

The bot can monitor stores for availability and:
- Send Discord notifications when items become available
- Automatically place orders based on your preferences
- Monitor multiple stores simultaneously

## Server Deployment

Includes scripts for deploying to:
- AWS EC2
- Azure VMs

## Requirements

- Node.js
- Python 3.6+
- Discord bot token and application ID
- TGTG account